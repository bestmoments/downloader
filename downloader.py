#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess

R = "\033[0m";  B = "\033[1m";  C = "\033[96m"
G = "\033[92m"; Y = "\033[93m"; E = "\033[91m"

def find_ytdlp():
    """Знаходить виконуваний файл yt-dlp"""
    # Стандартні шляхи pipx/brew/pip
    candidates = [
        shutil.which("yt-dlp"),
        os.path.expanduser("~/.local/bin/yt-dlp"),
        "/opt/homebrew/bin/yt-dlp",
        "/usr/local/bin/yt-dlp",
        os.path.expanduser("~/.pipx/venvs/yt-dlp/bin/yt-dlp"),
    ]
    for p in candidates:
        if p and os.path.isfile(p):
            return p
    return None

def check_ytdlp():
    path = find_ytdlp()
    if path:
        return path
    print(f"""
{E}❌  yt-dlp не знайдено!{R}

Встанови його однією з команд:

  {Y}brew install pipx && pipx install yt-dlp && pipx ensurepath{R}

  або просто:

  {Y}pip3 install --user yt-dlp{R}

Після встановлення {B}перезапусти термінал{R} і запусти скрипт знову.
""")
    sys.exit(1)

def get_output_dir():
    home = os.path.expanduser("~")
    for name in ["Downloads", "Завантаження"]:
        p = os.path.join(home, name)
        if os.path.isdir(p):
            return p
    return os.getcwd()

def run(ytdlp: str, args: list, output_dir: str):
    """Запускає yt-dlp з аргументами"""
    tmp_dir = "/tmp/yt-dlp-tmp"
    os.makedirs(tmp_dir, exist_ok=True)
    cmd = [ytdlp] + args + [
        "--progress", "--no-check-certificate",
        "--paths", f"home:{output_dir}",
        "--paths", f"temp:{tmp_dir}",
        "-o", "%(title)s.%(ext)s",
    ]
    print(f"\n  {C}📁 Збереження до: {output_dir}{R}\n")
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n  {Y}⛔ Скасовано{R}")


SEPARATOR = None

# ─── Меню YouTube ────────────────────────────────────────────────────────────
YT_MENU = [
    ("Відео — 1080p",                 ["-f", "bestvideo[height<=1080][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]", "--merge-output-format", "mp4"]),
    ("Відео — 720p",                  ["-f", "bestvideo[height<=720][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]", "--merge-output-format", "mp4"]),
    ("Відео — 360p",                  ["-f", "bestvideo[height<=360][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]", "--merge-output-format", "mp4"]),
    ("Найкраща якість відео",         ["-f", "bestvideo+bestaudio/best", "--merge-output-format", "mp4"]),
    SEPARATOR,
    ("Аудіо — AAC (для Apple)",      ["-f", "bestaudio/best", "-x", "--audio-format", "aac"]),
    ("Аудіо — MP3",                  ["-f", "bestaudio/best", "-x", "--audio-format", "mp3", "--audio-quality", "0"]),
]

# ─── Меню SoundCloud ─────────────────────────────────────────────────────────
SC_MENU = [
    ("Найкраща якість в MP3",               ["-f", "bestaudio/best", "-x", "--audio-format", "mp3", "--audio-quality", "0"]),
    ("AAC (Оригінальний формат для Apple)", ["-f", "bestaudio/best"]),
    ("FLAC (максимальна якість, але великі файли)", ["-f", "bestaudio/best", "-x", "--audio-format", "flac"]),
]

def show_menu(ytdlp: str, title: str, items: list, output_dir: str):
    selectable = [item for item in items if item is not SEPARATOR]
    print(f"\n{B}{C}  ── {title} {'─'*(46-len(title))}{R}")
    num = 1
    for item in items:
        if item is SEPARATOR:
            print()
        else:
            label, _ = item
            print(f"  {Y}{num:>2}.{R} {label}")
            num += 1
    print(f"\n  {Y} 0.{R} ← Назад")

    choice = input(f"\n  {B}Оберіть формат: {R}").strip()
    if choice == "0":
        return
    try:
        idx = int(choice) - 1
    except ValueError:
        print(f"  {E}Невірний вибір{R}")
        return
    if not (0 <= idx < len(selectable)):
        print(f"  {E}Невірний вибір{R}")
        return

    label, args = selectable[idx]

    url = input(f"  {B}Вставте посилання: {R}").strip()
    if not url:
        print(f"  {E}Порожнє посилання{R}")
        return

    print(f"\n  {G}▶ {label}{R}")
    run(ytdlp, args + [url], output_dir)

def main():
    ytdlp = check_ytdlp()

    output_dir = get_output_dir()
    print(f"  {C}📁 Файли зберігатимуться до: {B}{output_dir}{R}")
    print(f"  {C}🔧 yt-dlp: {ytdlp}{R}")

    while True:
        print(f"""
{B}{C}  ── Головне меню ─────────────────────────────────────{R}
  {Y}1.{R} 🎬  YouTube
  {Y}2.{R} 🎵  SoundCloud
  {Y}3.{R} 📁  Змінити теку  ({output_dir})
  {Y}0.{R} 🚪  Вийти
""")
        choice = input(f"  {B}Ваш вибір: {R}").strip()

        if choice == "1":
            show_menu(ytdlp, "Формати YouTube", YT_MENU, output_dir)
        elif choice == "2":
            show_menu(ytdlp, "Формати SoundCloud", SC_MENU, output_dir)
        elif choice == "3":
            new = input(f"  {B}Нова тека (Enter — без змін): {R}").strip()
            if new:
                os.makedirs(new, exist_ok=True)
                output_dir = new
                print(f"  {G}✅ Теку змінено: {output_dir}{R}")
        elif choice == "0":
            print(f"\n  {G}👋 До побачення!{R}\n")
            break
        else:
            print(f"  {E}Невірний вибір{R}")

if __name__ == "__main__":
    main()
