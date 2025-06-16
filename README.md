🌎 languages: English and Russian(below)

# 🇺🇸 TwoClapLaunch

TwoClapLaunch is a lightweight Python tool that listens for exactly **two hand claps** and launches a **Steam game** by its Game ID. It's designed to use minimal system resources and respond quickly.

> **Note:** This project was created by a novice Python programmer with a little help from ChatGPT. If you find any inaccuracies or errors in the code, please let me know on GitHub or, better yet, on Telegram at t.me/neosury

---

## 🎯 Features

- Detects exactly two claps within a time window  
- Ignores accidental or extra claps  
- Low CPU usage (callback-based audio processing)  
- Launches a Steam game via `steam://rungameid/<GAME_ID>`  
- Customizable detection and timing parameters  

## 🛠 Requirements

- Python 3.8+  
- `pyaudio`  
- `numpy`  

Install dependencies:

```bash
pip install -r requirements.txt
````

> If `pyaudio` fails to install, use precompiled wheels or your OS package manager.

## 🚀 How to Use

1. Open `main.py`

2. Set your desired `GAME_ID` (e.g. Dota 2 is `570`)

3. (Optional) Enable logging with `LOGGING_ENABLED = 1`

4. Run the program:

   ```bash
   python main.py
   ```

5. After a short silence, clap **twice**. If recognized correctly, the program will launch the Steam game via:

   ```
   steam://rungameid/<GAME_ID>
   ```

## ⚙️ Configuration

In `main.py` adjust:

```python
GAME_ID         = 570     # Steam Game ID to launch (e.g. 570 for Dota 2)
SAMPLING_RATE   = 22050   # Audio sampling rate, Hz
CLAP_WINDOW     = 1.5     # Time window for second clap, seconds
PRE_SILENCE     = 2.0     # Required silence before first clap, seconds
LOGGING_ENABLED = 1       # 1 = enable console logs, 0 = disable
```

## 📦 Project Structure

```
TwoClapLaunch/
├── main.py            # Main detection script
├── requirements.txt   # Python dependencies
└── ...
```
---
ㅤ
---
ㅤ
---
ㅤ
---
ㅤ
---
# 🇷🇺 TwoClapLaunch

**TwoClapLaunch** — это лёгкий инструмент на Python, который слушает микрофон и запускает **игру в Steam по её ID**, если пользователь хлопает **ровно два раза**. Оптимизирован для минимальной нагрузки на систему.

> **Примечание:** Этот проект был создан начинающим программистом Python с небольшой помощью ChatGPT. Если вы обнаружите какие-либо неточности или ошибки в коде, сообщите мне об этом на GitHub или, лучше всего, в Telegram по адресу t.me/neosury.

---

## 🎯 Возможности

* Распознаёт ровно два хлопка в заданное окно времени
* Игнорирует случайные или лишние хлопки
* Минимальная нагрузка на процессор (callback‑обработка аудио)
* Запускает игру через Steam по URL: `steam://rungameid/<GAME_ID>`
* Настраиваемые параметры чувствительности и времени

## 🛠 Требования

* Python 3.8+
* `pyaudio`
* `numpy`

Установка зависимостей:

```bash
pip install -r requirements.txt
```

> Если `pyaudio` не устанавливается, используйте готовые wheels или менеджер пакетов вашей ОС.

## 🚀 Как использовать

1. Откройте `main.py`

2. Укажите нужный `GAME_ID` (например, для Dota 2 — `570`)

3. (Необязательно) Включите логирование: `LOGGING_ENABLED = 1`

4. Запустите программу:

   ```bash
   python main.py
   ```

5. После короткой паузы хлопните **дважды**. При корректном распознавании игра запустится через Steam:

   ```
   steam://rungameid/<GAME_ID>
   ```

## ⚙️ Настройки

В `main.py` отредактируйте:

```python
GAME_ID         = 570     # ID игры в Steam (например, 570 для Dota 2)
SAMPLING_RATE   = 22050   # Частота дискретизации, Гц
CLAP_WINDOW     = 1.5     # Временное окно для второго хлопка, с
PRE_SILENCE     = 2.0     # Необходимая тишина перед первым хлопком, с
LOGGING_ENABLED = 1       # 1 = включить логи, 0 = отключить
```

## 📦 Структура проекта

```
TwoClapLaunch/
├── main.py            # Основной скрипт
├── requirements.txt   # Зависимости Python
└── ...
```
