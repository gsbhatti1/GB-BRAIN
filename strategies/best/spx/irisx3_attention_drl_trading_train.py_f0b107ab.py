# SOURCE: https://github.com/irisx3/attention_drl_trading
# FILE  : train.py

# train.py
import argparse
import numpy as np
import torch
from typing import List
from env import PortfolioEnv
from policy import StochasticHierarchicalDualAttentionPolicy
from agents import PPOConfig, PPOTrainer, RolloutBuffer, A2CTrainer, REINFORCETrainer
from utils import set_seeds, cs_zscore
from data import load_panel_from_csv
from metrics import compute_metrics_from_returns
def run_training(csv_path: str,
                 window: int = 30,
                 tc_cost: float = 5e-4,
                 d_model: int = 64,
                 heads_time: int = 2,
                 layers_time: int = 1,
                 heads_cross: int = 2,
                 layers_cross: int = 1,
                 buffer_steps: int = 128,
                 num_updates: int = 5,
                 lr: float = 3e-4,
                 minibatch_size: int = 256,
                 update_epochs: int = 3,
                 device: str = "auto",
                 temporal_asset_chunk: int = 64,
                 temporal_use_ckpt: bool = True,
                 minibatch_micro: int = 32,
                 out_dir: str = "./runs",
                 seed: int = 42):
    set_seeds(seed)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"

    panel = load_panel_from_csv(csv_path, window)
    prices_rel = panel["prices_rel"]; features = panel["features"]; tradable_mask = panel["tradable_mask"]
    sector_ids = panel["sector_ids"]; num_sectors = panel["num_sectors"]
    N, Fdim = panel["N"], panel["Fdim"]; market_factors = panel["market_factors"]
    dates = panel["dates"]

    # Build env
    env = PortfolioEnv(prices_rel=prices_rel,
                       features=features,
                       sector_ids=sector_ids,
                       tradable_mask=tradable_mask,
                       market_factors=market_factors,
                       tc_cost=tc_cost,
                       window=window,
                       sector_caps=None,
                       include_cash=True)

    # Policy (flat single-Dirichlet in the provided module)
    policy = StochasticHierarchicalDualAttentionPolicy(
        d_model=d_model,
        n_heads_time=heads_time, n_layers_time=layers_time,
        n_heads_cross=heads_cross, n_layers_cross=layers_cross,
        num_sectors=num_sectors,               # ignored by flat policy (kept for signature)
        include_cash=True,
        dropout=0.1,
        temporal_asset_chunk=temporal_asset_chunk,
        temporal_use_ckpt=temporal_use_ckpt
    ).to(device)

    cfg = PPOConfig(gamma=0.99, gae_lambda=0.95, clip_coef=0.2, vf_coef=0.5,
                    ent_coef=0.0, max_grad_norm=0.5, learning_rate=lr,
                    update_epochs=update_epochs, minibatch_size=minibatch_size,
                    minibatch_micro=minibatch_micro)
    trainer = PPOTrainer(policy, cfg, device=device)

    sector_ids_torch = torch.from_numpy(sector_ids).long().to(device)
    obs_shape = (window, N, Fdim)

    # Logging containers
    loss_hist = []
    mean_reward_hist = []
    eval_cum_wealth_hist = []
    eval_metrics_hist = []

    for update in range(num_updates):
        # keep rollout buffer on CPU → avoids GPU OOM
        buffer = RolloutBuffer(T=buffer_steps, B=1, obs_shape=obs_shape,
                               n_assets=N, sector_ids=sector_ids_torch,
                               device="cpu",
                               has_mkt=(env.mkt is not None),
                               k_mkt=(0 if env.mkt is None else env.mkt.shape[-1]))
        buffer._step = 0
        obs, _ = env.reset()

        for t in range(buffer_steps):
            x_t   = torch.from_numpy(env._get_state()).unsqueeze(0).to(device)    # (1,W,N,F)
            trad_t= torch.from_numpy(env.mask[env.t]).unsqueeze(0).to(device)     # (1,N) bool
            mkt_t = None if env.mkt is None else torch.from_numpy(env.mkt[env.t]).unsqueeze(0).to(device)
            with torch.no_grad():
                weights, logp, value, action, _ = policy.get_action_and_value(
                    x=x_t,
                    sector_ids=sector_ids_torch.unsqueeze(0),
                    tradable_mask=trad_t,
                    market_factors=mkt_t,
                    sample=True
                )
            # Env expects logits; map weights→logits stably
            logits = torch.log(weights.clamp_min(1e-8))[0].cpu().numpy()
            next_obs, reward, done, truncated, info = env.step(logits)

            buffer.add(
                obs_t=x_t[0].cpu(),
                tradable_t=trad_t[0].cpu(),
                mkt_t=None if mkt_t is None else mkt_t[0].cpu(),
                action=action,
                weight_t=weights[0].cpu(),
                reward_t=torch.tensor(reward, dtype=torch.float32),
                done_t=torch.tensor(done, dtype=torch.bool),
                value_t=value[0].detach().cpu(),
                logp_t=logp[0].detach().cpu()
            )
            obs = next_obs
            if done:
                obs, _ = env.reset()

        # Bootstrap advantages
        x_last   = torch.from_numpy(env._get_state()).unsqueeze(0).to(device)
        trad_last= torch.from_numpy(env.mask[env.t]).unsqueeze(0).to(device)
        mkt_last = None if env.mkt is None else torch.from_numpy(env.mkt[env.t]).unsqueeze(0).to(device)
        with torch.no_grad():
            _, _, last_value, _, _ = policy.get_action_and_value(x_last, sector_ids_torch.unsqueeze(0), trad_last, mkt_last, sample=False)
        buffer.compute_gae(last_value.squeeze(-1).detach().cpu(), gamma=cfg.gamma, lam=cfg.gae_lambda)

        # PPO update
        loss = trainer.update(buffer)
        loss_hist.append(loss)
        mean_reward_hist.append(float(buffer.rewards.mean().cpu().numpy()))

        # Deterministic evaluation over full dataset
        eval_out = eval_policy_full_dataset(policy,
                                            prices_rel, features, tradable_mask,
                                            sector_ids, market_factors,
                                            window, device)
        eval_cum_wealth_hist.append(eval_out["cum_wealth"])
        eval_metrics_hist.append(eval_out["metrics"])

        m = eval_out["metrics"]
        print(f"[{update+1}/{num_updates}] loss={loss:.4f} | meanR={mean_reward_hist[-1]:.6f} | "
              f"Eval: Sharpe={m['sharpe']:.3f}  CAGR={m['cagr']:.3%}  MDD={m['mdd']:.2%}")

    # Save CSV log
    rows = []
    for i, (loss_i, mr_i, em_i) in enumerate(zip(loss_hist, mean_reward_hist, eval_metrics_hist), start=1):
        rows.append({
            "update": i,
            "ppo_loss": loss_i,
            "mean_buffer_reward": mr_i,
            "eval_sharpe": em_i["sharpe"],
            "eval_cagr": em_i["cagr"],
            "eval_mdd": em_i["mdd"],
        })
    df_log = pd.DataFrame(rows)
    out_dir.mkdir(parents=True, exist_ok=True)
    df_log.to_csv(out_dir / "training_log.csv", index=False)

    # Save plots (training curves + last equity curve)
    save_training_plots(out_dir, loss_hist, mean_reward_hist, eval_cum_wealth_hist, dates, window)

    print(f"\nSaved: {out_dir/'training_log.csv'}, {out_dir/'training_curves.png'}, "
          f"{out_dir/'eval_equity_curve.png'}")


def train_and_save(csv_path: str,
                   save_path: str = "./checkpoints/policy.pt",
                   window: int = 30,
                   tc_cost: float = 5e-4,
                   d_model: int = 64,
                   heads_time: int = 2,
                   layers_time: int = 1,
                   heads_cross: int = 2,
                   layers_cross: int = 1,
                   buffer_steps: int = 128,
                   num_updates: int = 5,
                   lr: float = 3e-4,
                   minibatch_size: int = 256,
                   update_epochs: int = 3,
                   device: str = "auto",
                   temporal_asset_chunk: int = 64,
                   temporal_use_ckpt: bool = True,
                   minibatch_micro: int = 32,
                   seed: int = 42):

    set_seeds(seed)
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"

    panel = load_panel_from_csv(csv_path, window)
    prices_rel = panel["prices_rel"]; features = panel["features"]; tradable_mask = panel["tradable_mask"]
    sector_ids = panel["sector_ids"]; num_sectors = panel["num_sectors"]
    N, Fdim = panel["N"], panel["Fdim"]

    env = PortfolioEnv(prices_rel=prices_rel,
                       features=features,
                       sector_ids=sector_ids,
                       tradable_mask=tradable_mask,
                       market_factors=None,
                       tc_cost=tc_cost,
                       window=window,
                       include_cash=True)

    # Flat single-Dirichlet policy (class name kept for compatibility)
    policy = StochasticHierarchicalDualAttentionPolicy(
        d_model=d_model,
        n_heads_time=heads_time, n_layers_time=layers_time,
        n_heads_cross=heads_cross, n_layers_cross=layers_cross,
        num_sectors=num_sectors,   # ignored by flat actor
        include_cash=True,
        dropout=0.1,
        temporal_asset_chunk=temporal_asset_chunk,
        temporal_use_ckpt=temporal_use_ckpt
    ).to(device)

    cfg = PPOConfig(gamma=0.99, gae_lambda=0.95, clip_coef=0.2, vf_coef=0.5,
                    ent_coef=0.0, max_grad_norm=0.5, learning_rate=lr,
                    update_epochs=update_epochs, minibatch_size=minibatch_size,
                    minibatch_micro=minibatch_micro)
    trainer = PPOTrainer(policy, cfg, device=device)

    obs_shape = (window, N, Fdim)
    sector_ids_torch = torch.from_numpy(sector_ids).long().to(device)

    for update in range(num_updates):
        buffer = RolloutBuffer(T=buffer_steps, B=1, obs_shape=obs_shape,
                               n_assets=N, sector_ids=sector_ids_torch,
                               device="cpu", has_mkt=False, k_mkt=0)
        buffer._step = 0
        env.reset()

        # collect rollout
        for t in range(buffer_steps):
            x_t   = torch.from_numpy(env._get_state()).unsqueeze(0).to(device)    # (1,W,N,F)
            trad_t= torch.from_numpy(env.mask[env.t]).unsqueeze(0).to(device)     # (1,N) bool
            with torch.no_grad():
                weights, logp, value, action, _ = policy.get_action_and_value(
                    x=x_t,
                    sector_ids=sector_ids_torch.unsqueeze(0),
                    tradable_mask=trad_t,
                    market_factors=None,
                    sample=True
                )
            # Env expects logits; map weights→logits stably
            logits = torch.log(weights.clamp_min(1e-8))[0].cpu().numpy()
            _, reward, done, _, _ = env.step(logits)

            buffer.add(
                obs_t=x_t[0].cpu(),
                tradable_t=trad_t[0].cpu(),
                mkt_t=None,
                action=action,
                weight_t=weights[0].cpu(),
                reward_t=torch.tensor(reward, dtype=torch.float32),
                done_t=torch.tensor(done, dtype=torch.bool),
                value_t=value[0].detach().cpu(),
                logp_t=logp[0].detach().cpu()
            )
            if done:
                env.reset()

        # bootstrap
        x_last   = torch.from_numpy(env._get_state()).unsqueeze(0).to(device)
        trad_last= torch.from_numpy(env.mask[env.t]).unsqueeze(0).to(device)
        with torch.no_grad():
            _, _, last_value, _, _ = policy.get_action_and_value(
                x_last, sector_ids_torch.unsqueeze(0), trad_last, None, sample=False
            )
        buffer.compute_gae(last_value.squeeze(-1).detach().cpu(), gamma=cfg.gamma, lam=cfg.gae_lambda)

        # update
        loss = trainer.update(buffer)
        print(f"[{update+1}/{num_updates}] PPO loss = {loss:.4f}")

    # -------- save checkpoint --------
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    ckpt = {
        "state_dict": policy.state_dict(),
        "config": {
            "window": window,
            "tc_cost": tc_cost,
            "d_model": d_model,
            "heads_time": heads_time,
            "layers_time": layers_time,
            "heads_cross": heads_cross,
            "layers_cross": layers_cross,
            "temporal_asset_chunk": temporal_asset_chunk,
            "temporal_use_ckpt": temporal_use_ckpt,
            "include_cash": True,
        }
    }
    torch.save(ckpt, save_path)
    print(f"Saved model to: {str(save_path.resolve())}")


def parse_args():
    p = argparse.ArgumentParser(description="Train PPO/A2C/REINFORCE/DDPG on portfolio policy.")
    p.add_argument("--csv", type=str, required=True)
    p.add_argument("--algo", type=str, default="ppo", choices=["ppo","a2c","reinforce","ddpg"])
    p.add_argument("--window", type=int, default=30)
    p.add_argument("--tc", type=float, default=5e-4)
    p.add_argument("--d_model", type=int, default=64)
    p.add_argument("--heads_time", type=int, default=2)
    p.add_argument("--layers_time", type=int, default=1)
    p.add_argument("--heads_cross", type=int, default=2)
    p.add_argument("--layers_cross", type=int, default=1)
    p.add_argument("--buffer_steps", type=int, default=128)
    p.add_argument("--updates", type=int, default=5)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--mb", type=int, default=256)
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--device", type=str, default="auto")
    p.add_argument("--asset_chunk", type=int, default=64)
    p.add_argument("--no_ckpt", action="store_true")
    p.add_argument("--mb_micro", type=int, default=32)
    p.add_argument("--out_dir", type=str, default="./runs_multi")
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def run(args):
    set_seeds(args.seed)
    device = "cuda" if args.device=="auto" and torch.cuda.is_available() else args.device

    # load & split
    df = pd.read_csv(args.csv, low_memory=False)
    assert {"Date","ticker","Close"}.issubset(df.columns)
    df_train, df_test, split_date = date_split_20y(df, years=20)
    print(f"Train {df_train['Date'].min().date()} → {df_train['Date'].max().date()} | "
          f"Test {df_test['Date'].min().date()} → {df_test['Date'].max().date()} | split={split_date.date()}")

    # features
    default_feats = [
        "Open","High","Low","Close","Volume",
        "macd","macd_signal","macd_hist",
        "macdboll","ubboll","lb","rsi","30cci",
        "plus_di_14","minus_di_14","dx_14","dx30",
        "close30_sma","close60_sma"
    ]
    feature_cols = [c for c in default_feats if c in df.columns]
    if not feature_cols: raise ValueError("No numeric feature columns found.")

    # panels
    panel_tr = build_panel(df_train, feature_cols)
    panel_te = build_panel(df_test,  feature_cols)

    # env for training
    env = PortfolioEnv(prices_rel=panel_tr["prices_rel"], features=panel_tr["features"],
                       sector_ids=panel_tr["sector_ids"], tradable_mask=panel_tr["mask"],
                       market_factors=None, tc_cost=args.tc, window=args.window, include_cash=True)

    N = panel_tr["features"].shape[1]; Fdim = panel_tr["features"].shape[2]
    obs_shape = (args.window, N, Fdim)

    # actor (shared)
    policy = StochasticHierarchicalDualAttentionPolicy(
        d_model=args.d_model, n_heads_time=args.heads_time, n_layers_time=args.layers_time,
        n_heads_cross=args.heads_cross, n_layers_cross=args.layers_cross,
        include_cash=True, temporal_asset_chunk=args.asset_chunk, temporal_use_ckpt=(not args.no_ckpt)
    ).to(device)

    out_dir = Path(args.out_dir) / args.algo
    out_dir.mkdir(parents=True, exist_ok=True)

    # ----- select algo -----
    loss_hist, mean_reward_hist = [], []
    if args.algo == "ppo":
        cfg = PPOConfig(gamma=0.99, gae_lambda=0.95, clip_coef=0.2, vf_coef=0.5,
                        ent_coef=0.0, max_grad_norm=0.5, learning_rate=args.lr,
                        update_epochs=args.epochs, minibatch_size=args.mb, minibatch_micro=args.mb_micro)
        trainer = PPOTrainer(policy, cfg, device=device)
        sid_t = torch.from_numpy(panel_tr["sector_ids"]).long().to(device)
        for upd in range(args.updates):
            buffer = RolloutBuffer(T=args.buffer_steps, B=1, obs_shape=obs_shape,
                                   n_assets=N, sector_ids=sid_t, device="cpu",
                                   has_mkt=False, k_mkt=0)
            buffer._step = 0; env.reset()
            for t in range(args.buffer_steps):
                x = torch.from_numpy(env._get_state()).unsqueeze(0).to(device)
                trad = torch.from_numpy(env.mask[env.t]).unsqueeze(0).to(device)
                with torch.no_grad():
                    w, logp, v, a, _ = policy.get_action_and_value(x, sid_t.unsqueeze(0), trad, None, sample=True)
                logits = torch.log(w.clamp_min(1e-8))[0].cpu().numpy()
                _, r, done, _, _ = env.step(logits)
                buffer.add(x[0].cpu(), trad[0].cpu(), None, a, w[0].cpu(),
                           torch.tensor(r, dtype=torch.float32), torch.tensor(done, dtype=torch.bool),
                           v[0].detach().cpu(), logp[0].detach().cpu())
                if done: env.reset()
            with torch.no_grad():
                xl = torch.from_numpy(env._get_state()).unsqueeze(0).to(device)
                tradl = torch.from_numpy(env.mask[env.t]).unsqueeze(0).to(device)
                _, _, lv, _, _ = policy.get_action_and_value(xl, sid_t.unsqueeze(0), tradl, None, sample=False)
            buffer.compute_gae(lv.squeeze(-1).detach().cpu(), cfg.gamma, cfg.gae_lambda)
            loss = trainer.update(buffer); loss_hist.append(loss)
            mean_reward_hist.append(float(buffer.rewards.mean().cpu().numpy()))
            print(f"[PPO {upd+1}/{args.updates}] loss={loss:.4f} | meanR={mean_reward_hist[-1]:.6f}")

    elif args.algo == "a2c":
        cfg = A2CConfig(lr=args.lr, update_epochs=args.epochs, minibatch_size=args.mb,
                        minibatch_micro=args.mb_micro, vf_coef=0.5, ent_coef=0.0)
        trainer = A2CTrainer(policy, cfg, device=device)
        sid_t = torch.from_numpy(panel_tr["sector_ids"]).long().to(device)
        for upd in range(args.updates):
            buffer = RolloutBuffer(T=args.buffer_steps, B=1, obs_shape=obs_shape,
                                   n_assets=N, sector_ids=sid_t, device="cpu", has_mkt=False, k_mkt=0)
            buffer._step = 0; env.reset()
            for t in range(args.buffer_steps):
                x = torch.from_numpy(env._get_state()).unsqueeze(0).to(device)
                trad = torch.from_numpy(env.mask[env.t]).unsqueeze(0).to(device)
                with torch.no_grad():
                    w, logp, v, a, _ = policy.get_action_and_value(x, sid_t.unsqueeze(0), trad, None, sample=True)
                logits = torch.log(w.clamp_min(1e-8))[0].cpu().numpy()
                _, r, done, _, _ = env.step(logits)
                buffer.add(x[0].cpu(), trad[0].cpu(), None, a, w[0].cpu(),
                           torch.tensor(r, dtype=torch.float32), torch.tensor(done, dtype=torch.bool),
                           v[0].detach().cpu(), logp[0].detach().cpu())
                if done: env.reset()
            with torch.no_grad():
                xl = torch.from_numpy(env._get_state()).unsqueeze(0).to(device)
                tradl = torch.from_numpy(env.mask[env.t]).unsqueeze(0).to(device)
                _, _, lv, _, _ = policy.get_action_and_value(xl, sid_t.unsqueeze(0), tradl, None, sample=False)
            buffer.compute_gae(lv.squeeze(-1).detach().cpu(), cfg.gamma, cfg.gae_lambda)
            loss = trainer.update(buffer); loss_hist.append(loss)
            mean_reward_hist.append(float(buffer.rewards.mean().cpu().numpy()))
            print(f"[A2C {upd+1}/{args.updates}] loss={loss:.4f} | meanR={mean_reward_hist[-1]:.6f}")

    elif args.algo == "reinforce":
        trainer = REINFORCETrainer(policy, lr=args.lr, vf_coef=0.5, device=device, max_grad_norm=0.5)
        sid_t = torch.from_numpy(panel_tr["sector_ids"]).long().to(device)
        for upd in range(args.updates):
            buffer = RolloutBuffer(T=args.buffer_steps, B=1, obs_shape=obs_shape,
                                   n_assets=N, sector_ids=sid_t, device="cpu", has_mkt=False, k_mkt=0)
            buffer._step = 0; env.reset()
            for t in range(args.buffer_steps):
                x = torch.from_numpy(env._get_state()).unsqueeze(0).to(device)
                trad = torch.from_numpy(env.mask[env.t]).unsqueeze(0).to(device)
                with torch.no_grad():
                    w, logp, v, a, _ = policy.get_action_and_value(x, sid_t.unsqueeze(0), trad, None, sample=True)
                logits = torch.log(w.clamp_min(1e-8))[0].cpu().numpy()
                _, r, done, _, _ = env.step(logits)
                buffer.add(x[0].cpu(), trad[0].cpu(), None, a, w[0].cpu(),
                           torch.tensor(r, dtype=torch.float32), torch.tensor(done, dtype=torch.bool),
                           v[0].detach().cpu(), logp[0].detach().cpu())
                if done: env.reset()
            # Monte Carlo returns (no bootstrap): use buffer.rewards cumulative with gamma
            # We can reuse compute_gae with lam=1 and next_value=0:
            buffer.compute_gae(torch.zeros(1), gamma=0.99, lam=1.0)
            loss = trainer.update(buffer); loss_hist.append(loss)
            mean_reward_hist.append(float(buffer.rewards.mean().cpu().numpy()))
            print(f"[REINFORCE {upd+1}/{args.updates}] loss={loss:.4f} | meanR={mean_reward_hist[-1]:.6f}")

    elif args.algo == "ddpg":
        # short off-policy run on a rolling window of the training panel
        cfg = DDPGConfig(gamma=0.99, tau=0.005, lr_actor=1e-4, lr_critic=1e-3,
                         batch_size=64, explore_alpha=0.3, updates_per_step=1)
        trainer = DDPGSoftmaxTrainer(policy, d_model=args.d_model, action_dim=N+1, cfg=cfg, device=device)
        replay = Replay(capacity=5000)
        env.reset()
        sid_t = torch.from_numpy(panel_tr["sector_ids"]).long().to(device)  # unused
        for step in range(args.buffer_steps * args.updates):
            x = torch.from_numpy(env._get_state()).unsqueeze(0).to(device)
            trad = torch.from_numpy(env.mask[env.t]).unsqueeze(0).to(device)
            # exploration action
            with torch.no_grad():
                w = trainer._actor_weights(x, trad, deterministic=True, explore_alpha=cfg.explore_alpha)
            logits = torch.log(w.clamp_min(1e-8))[0].cpu().numpy()
            prev_state = env._get_state().copy(); prev_trad = env.mask[env.t].copy()
            _, r, done, _, _ = env.step(logits)
            next_state = env._get_state().copy(); next_trad = env.mask[env.t].copy()
            replay.push(prev_state, prev_trad, w[0].detach().cpu().numpy(), r, next_state, next_trad, float(done))
            loss = trainer.update(replay)
            if done: env.reset()
        # DDPG doesn't have per-update loss history; store last total loss
        loss_hist = [loss] if isinstance(loss, float) else []

    else:
        raise ValueError(f"Unknown algo: {args.algo}")

    # ----- save model -----
    out_dir.mkdir(parents=True, exist_ok=True)
    ckpt_path = out_dir / f"{args.algo}_policy.pth"
    torch.save({"state_dict": policy.state_dict(),
                "config": {"d_model": args.d_model, "window": args.window, "tc_cost": args.tc}},
               ckpt_path)
    print(f"Saved model → {ckpt_path}")

    # ----- evaluation & plots -----
    train_daily, train_cw, train_metrics = eval_on_panel(policy, panel_tr, args.window, args.tc, device, deterministic=True)
    test_daily,  test_cw,  test_metrics  = eval_on_panel(policy, panel_te, args.window, args.tc, device, deterministic=True)
    print(f"Train: Sharpe={train_metrics['sharpe']:.3f}  CAGR={train_metrics['cagr']:.2%}  MDD={train_metrics['mdd']:.2%}")
    print(f"Test : Sharpe={test_metrics['sharpe']:.3f}  CAGR={test_metrics['cagr']:.2%}  MDD={test_metrics['mdd']:.2%}")

    # save CSV log and plots
    pd.DataFrame({"update": np.arange(1, len(loss_hist)+1),
                  "loss": loss_hist,
                  "mean_reward": mean_reward_hist[:len(loss_hist)] if len(mean_reward_hist)>=len(loss_hist) else None}
                 ).to_csv(out_dir/"training_log.csv", index=False)
    save_plots(out_dir, loss_hist, mean_reward_hist, train_cw, test_cw, panel_tr["dates"], panel_te["dates"], args.window)
    print(f"Saved plots & logs → {out_dir}")
