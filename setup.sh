#!/bin/bash

# Запросите у пользователя путь к временной директории
read -p "Введите путь к временной директории: " TEMP_DIR

# Убедитесь, что путь существует, или создайте его
if [ ! -d "$TEMP_DIR" ]; then
    echo "Директория '$TEMP_DIR' не существует. Создаем ее..."
    mkdir -p "$TEMP_DIR"
fi

# Установите Python и pip, если они не установлены
if ! command -v python3 &> /dev/null; then
    echo "Python3 не установлен. Устанавливаем..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Установите необходимые Python-библиотеки
pip3 install yt-dlp

# Установите ffmpeg, если он не установлен
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg не установлен. Устанавливаем..."
    sudo apt update
    sudo apt install -y ffmpeg
fi

# Создайте файл с пользовательским путем TEMP_DIR
echo "TEMP_DIR = '$TEMP_DIR'" > main.py

echo "Установка завершена."
echo "Временная директория установлена в '$TEMP_DIR'"
echo "Файл main.py отредактирован"
