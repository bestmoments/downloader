1#!/usr/bin/env python3
"""
🎬 MediaGrab — завантажувач відео з YouTube та музики з SoundCloud
Використовує yt-dlp як CLI-команду (встанови: brew install pipx && pipx install yt-dlp)
"""

import os
import sys
import shutil
import subprocess

# ─── Кольори ────────────────────────────────────────────────────────────────
R = "\033[0m";  B = "\033[1m";  C = "\033[96m"
G = "\033[92m"; Y = "\033[93m"; M = "\033[95m"; E = "\033[91m"

BANNER = f"""
{C}{B}╔══════════════════════════════════════════════════════╗
║        🎬  MediaGrab  —  YouTube & SoundCloud        ║
╚══════════════════════════════════════════════════════╝{R}
"""

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

def run(args: list, output_dir: str):
    """Запускає yt-dlp з аргументами"""
    template = os.path.join(output_dir, "%(title)s.%(ext)s")
    cmd = [YTDLP] + args + ["--progress", "--no-check-certificate", "-o", template]
    print(f"\n  {C}📁 Збереження до: {output_dir}{R}\n")
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print(f"\n  {Y}⛔ Скасовано{R}")

def show_formats(url: str):
    print(f"\n  {Y}⏳ Отримання форматів...{R}\n")
    subprocess.run([YTDLP, "-F", "--no-check-certificate", url], check=False)

# ─── Меню YouTube ────────────────────────────────────────────────────────────
YT_MENU = [
    ("Найкраща якість (mp4)",        ["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", "--merge-output-format", "mp4"]),
    ("1080p (mp4)",                  ["-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]", "--merge-output-format", "mp4"]),
    ("720p (mp4)",                   ["-f", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]", "--merge-output-format", "mp4"]),
    ("480p (mp4)",                   ["-f", "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]", "--merge-output-format", "mp4"]),
    ("360p (mp4)",                   ["-f", "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]", "--merge-output-format", "mp4"]),
    ("Лише аудіо — MP3 320kbps",     ["-f", "bestaudio/best", "-x", "--audio-format", "mp3", "--audio-quality", "0"]),
    ("Лише аудіо — MP3 192kbps",     ["-f", "bestaudio/best", "-x", "--audio-format", "mp3", "--audio-quality", "5"]),
    ("Лише аудіо — AAC",             ["-f", "bestaudio/best", "-x", "--audio-format", "aac"]),
    ("Лише аудіо — FLAC",            ["-f", "bestaudio/best", "-x", "--audio-format", "flac"]),
    ("Лише аудіо — WAV",             ["-f", "bestaudio/best", "-x", "--audio-format", "wav"]),
    ("Найкраща якість (webm)",       ["-f", "bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]", "--merge-output-format", "webm"]),
    ("Показати всі доступні формати", None),
]

# ─── Меню SoundCloud ─────────────────────────────────────────────────────────
SC_MENU = [
    ("MP3 найкраща якість",          ["-f", "bestaudio/best", "-x", "--audio-format", "mp3", "--audio-quality", "0"]),
    ("Оригінальний формат",          ["-f", "bestaudio/best"]),
    ("FLAC",                         ["-f", "bestaudio/best", "-x", "--audio-format", "flac"]),
    ("Показати всі доступні формати", None),
]

def show_menu(title: str, items: list, output_dir: str):
    print(f"\n{B}{C}  ── {title} {'─'*(46-len(title))}{R}")
    for i, (label, _) in enumerate(items, 1):
        print(f"  {Y}{i:>2}.{R} {label}")
    print(f"  {Y} 0.{R} ← Назад")

    choice = input(f"\n  {B}Оберіть формат: {R}").strip()
    if choice == "0":
        return
    try:
        idx = int(choice) - 1
        assert 0 <= idx < len(items)
    except (ValueError, AssertionError):
        print(f"  {E}Невірний вибір{R}")
        return

    label, args = items[idx]
    url = input(f"  {B}Вставте посилання: {R}").strip()
    if not url:
        print(f"  {E}Порожнє посилання{R}")
        return

    if args is None:
        show_formats(url)
        return

    print(f"\n  {G}▶ {label}{R}")
    run(args + [url], output_dir)

def main():
    global YTDLP
    YTDLP = check_ytdlp()

    print(BANNER)
    output_dir = get_output_dir()
    print(f"  {C}📁 Файли зберігатимуться до: {B}{output_dir}{R}")
    print(f"  {C}🔧 yt-dlp: {YTDLP}{R}")

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
            show_menu("Формати YouTube", YT_MENU, output_dir)
        elif choice == "2":
            show_menu("Формати SoundCloud", SC_MENU, output_dir)
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
