# wallpaper-changer

<img width="549" height="680" alt="Screenshot 2026-02-21 102135" src="https://github.com/user-attachments/assets/c115b56c-b5a1-4a88-b0d4-532da011fe61" />

✨ Features

🎨 Category-based wallpapers
Choose from:

nature

space

technology

⏱️ Automatic wallpaper rotation

Disabled

Every 1 minute

Every 5 minutes

🖼️ Live Preview

See the last downloaded wallpaper inside the app

📥 Automatic Download

Downloads 1920x1080 wallpapers from loremflickr.com

📂 Organized Storage

Saves wallpapers to:

~/Pictures/Wallpapers

🌙 Modern Dark UI

Built using customtkinter

⚡ Progress Indicator & Status Messages

Visual feedback during download

Error handling for internet issues

🛠️ Tech Stack

Python 3

customtkinter

tkinter

Pillow

requests

ctypes (Windows system API)

📦 Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/wallpaper-changer.git
cd wallpaper-changer
2️⃣ Install dependencies
pip install customtkinter pillow requests
▶️ Usage

Run the application:

python main.py

Select a wallpaper category.

Choose a timer interval (optional).

Click Change Wallpaper.

The wallpaper will download and apply automatically.

🖥️ Platform Support

⚠️ Windows Only

This application uses:

ctypes.windll.user32.SystemParametersInfoW

Which is part of the Windows API for setting wallpapers.

📁 Project Structure
wallpaper-changer/
│
├── main.py
└── README.md
🚀 How It Works

Fetches a 1920x1080 image from:

https://loremflickr.com/1920/1080/{category}

Saves it locally in the user's Pictures folder.

Uses the Windows system API to set it as the desktop wallpaper.

Displays a preview inside the application.

Optionally repeats the process using a timer.

⚠️ Error Handling

Detects internet connection errors

Displays message boxes for failures

Prevents multiple simultaneous downloads

Automatically stops and resets timers when changed

🔮 Possible Improvements

Add more wallpaper categories

Add custom user-defined categories

Add wallpaper history

Add multi-monitor support

Package as .exe using PyInstaller

Add macOS/Linux support

📜 License

This project is open-source. Feel free to modify and improve it.
