import os
import multiprocessing as mp
import ollama

FMZQUANT_REPO = "https://github.com/fmzquant/strategies.git"
SOURCE_DIR = os.path.join(os.path.expanduser("~"), "qwen-dev", "Trading-Strategies", "fmz-source")
OUT_DIR = os.path.join(os.path.expanduser("~"), "qwen-dev", "Future-Trading", "2_translated")

os.makedirs(OUT_DIR, exist_ok=True)

N_WORKERS = 24  # <-- THIS is your N (try 4, then 6, 8)

def translate_one(filepath):
    rel_path = os.path.relpath(filepath, SOURCE_DIR)
    out_path = os.path.join(OUT_DIR, rel_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    if os.path.exists(out_path):
        print(f"[SKIP] {rel_path}")
        return

    print(f"[TRANSLATING] {rel_path}")
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if len(content.strip()) == 0:
            print(f"[EMPTY] {rel_path}")
            return

        response = ollama.chat(
            model="qwen2.5:7b",
            messages=[{
                "role": "user",
                "content": (
                    "Translate the following trading strategy document from Chinese to English. "
                    "Keep all code blocks, numbers, and formatting exactly as-is. "
                    "Only translate the human-readable text.\n\n" + content[:6000]
                )
            }]
        )
        translated = response["message"]["content"]

        with open(out_path, "w", encoding="utf-8") as f_out:
            f_out.write(translated)

    except Exception as e:
        print(f"[ERROR] {rel_path}: {e}")


if __name__ == "__main__":
    # Build file list once
    all_files = []
    for root, dirs, files in os.walk(SOURCE_DIR):
        for f in files:
            if f.endswith(".md"):
                all_files.append(os.path.join(root, f))

    total = len(all_files)
    print(f"[INFO] Found {total} .md files to translate.")

    with mp.Pool(N_WORKERS) as pool:
        pool.map(translate_one, all_files)

    print("[DONE] All files processed (multi-worker).")
