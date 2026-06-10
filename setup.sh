#!/bin/bash
set -e

echo "── Перевірка Homebrew ─────────────────────────────"
if ! command -v brew &>/dev/null; then
    echo "▶ Встановлення Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✓ Homebrew вже встановлено"
fi

echo ""
echo "── Встановлення yt-dlp ────────────────────────────"
if command -v yt-dlp &>/dev/null; then
    echo "✓ yt-dlp вже встановлено: $(yt-dlp --version)"
else
    echo "▶ Встановлення через pipx..."
    brew install pipx
    pipx install yt-dlp
    pipx ensurepath
    echo "✓ yt-dlp встановлено"
fi

echo ""
echo "── Налаштування скрипта ───────────────────────────"
chmod +x downloader.py
echo "✓ downloader.py — виконуваний"

echo ""
echo "✅ Готово! Запускай:"
echo ""
echo "   python3 downloader.py"
echo ""
