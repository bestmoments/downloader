# downloader — контекст проекту

## Що це

CLI-скрипт на Python для завантаження відео/аудіо з YouTube та SoundCloud через `yt-dlp`.

## Структура

```
downloader/
├── downloader.py       — весь код
├── setup.sh            — встановлення залежностей на новому Mac (одноразово)
├── README.md           — інструкція для GitHub
└── .claude/
    └── CONTEXT.md      — цей файл, контекст для Claude
```

## Залежності

- `yt-dlp` — зовнішній CLI-інструмент. Встановлюється через `setup.sh` або вручну:
  - `brew install pipx && pipx install yt-dlp && pipx ensurepath`

## Як запустити

```bash
python3 downloader.py
```

## Архітектура

- `find_ytdlp()` — шукає yt-dlp у стандартних шляхах
- `check_ytdlp()` — викликає `find_ytdlp`, виходить з помилкою якщо не знайдено
- `get_output_dir()` — повертає ~/Downloads або ~/Завантаження або поточну теку
- `run(ytdlp, args, output_dir)` — запускає yt-dlp з аргументами
- `show_menu(ytdlp, title, items, output_dir)` — інтерактивне меню вибору формату
- `main()` — головний цикл: YouTube / SoundCloud / змінити теку / вийти

## Меню YouTube

- Відео — 1080p (H.264, сумісний з QuickTime)
- Відео — 720p (H.264, сумісний з QuickTime)
- Відео — 360p (H.264, сумісний з QuickTime)
- Найкраща якість відео (без обмежень — може бути 4K/AV1, потрібен VLC або IINA)
- Аудіо — AAC (для Apple)
- Аудіо — MP3

## Меню SoundCloud

- Найкраща якість в MP3
- AAC Оригінальний формат (для Apple) — завантажує як є, без конвертації
- FLAC (максимальна якість, але великі файли)

## Важливо

- mp4 формати використовують `[vcodec^=avc1]` для H.264 — відкриваються в QuickTime
- "Найкраща якість відео" без обмежень по кодеку — для 4K потрібен IINA або VLC
- `SEPARATOR = None` — використовується для порожнього рядка між пунктами меню
