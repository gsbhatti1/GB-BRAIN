import os
import re
import subprocess

OUT_DIR = os.path.join(os.path.expanduser("~"), "qwen-dev", "Future-Trading", "2_translated")
REPO_DIR = os.path.join(os.path.expanduser("~"), "qwen-dev", "Future-Trading")

def is_chinese(char):
    return '\u4e00' <= char <= '\u9fff'

def has_chinese(text):
    return any(is_chinese(c) for c in text)

def clean_filename(filename):
    # Remove .md extension to work with the name
    name = filename[:-3] if filename.endswith('.md') else filename

    # If no Chinese at all, already clean
    if not has_chinese(name):
        return filename

    # Strategy: find the last continuous English block after Chinese chars
    # Many files are like: ChineseName-English-Name or ChineseNameEnglish-Name
    # Split on Chinese characters and get all non-Chinese segments
    parts = re.split(r'[\u4e00-\u9fff]+', name)
    english_parts = [p.strip('-').strip() for p in parts if p.strip('-').strip()]

    if english_parts:
        # Join parts with dash, clean up multiple dashes
        new_name = '-'.join(english_parts)
        new_name = re.sub(r'-+', '-', new_name).strip('-')
        if new_name:
            return new_name + '.md'

    # Fallback: remove all Chinese chars
    cleaned = re.sub(r'[\u4e00-\u9fff]+', '', name)
    cleaned = re.sub(r'-+', '-', cleaned).strip('-')
    if cleaned:
        return cleaned + '.md'

    return filename  # give up, keep original

renamed = 0
skipped = 0
errors = 0

print(f"[INFO] Scanning: {OUT_DIR}")

for root, dirs, files in os.walk(OUT_DIR):
    for fname in files:
        if not fname.endswith('.md'):
            continue
        if not has_chinese(fname):
            skipped += 1
            continue

        new_fname = clean_filename(fname)

        if new_fname == fname:
            skipped += 1
            continue

        old_path = os.path.join(root, fname)
        new_path = os.path.join(root, new_fname)

        # Avoid overwriting existing files
        if os.path.exists(new_path):
            print(f"[SKIP - EXISTS] {fname} -> {new_fname}")
            skipped += 1
            continue

        try:
            os.rename(old_path, new_path)
            print(f"[RENAMED] {fname}")
            print(f"       -> {new_fname}")
            renamed += 1
        except Exception as e:
            print(f"[ERROR] {fname}: {e}")
            errors += 1

print(f"\n[DONE] Renamed: {renamed} | Skipped: {skipped} | Errors: {errors}")

# Auto push to GitHub
if renamed > 0:
    print("[GIT] Pushing renamed files to GitHub...")
    try:
        subprocess.run(["git", "-C", REPO_DIR, "pull", "--rebase"], check=True)
        subprocess.run(["git", "-C", REPO_DIR, "add", "2_translated/"], check=True)
        subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", f"Rename {renamed} files to English-only filenames"], check=True)
        subprocess.run(["git", "-C", REPO_DIR, "push"], check=True)
        print("[GIT] Pushed successfully!")
    except Exception as e:
        print(f"[GIT ERROR] {e}")
