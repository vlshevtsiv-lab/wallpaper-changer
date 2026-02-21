import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import ctypes
from pathlib import Path

class WallpaperChanger:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Wallpaper Changer")
        self.app.geometry("550x650")
        ctk.set_appearance_mode("dark")

        self.window = self.app
        self.timer_id = None
        self.wallpaper_dir = Path.home() / "Pictures" / "Wallpapers"
        self.wallpaper_dir.mkdir(exist_ok=True)

        self.categories = {"nature", "space", "technology"}
        self.intervals = {"Disabled": 0, "1 Minute": 60000, "5 Minutes": 300000}

        self.create_ui()

    def create_ui(self):
        ctk.CTkLabel(self.window, text="  Wallpaper Changer",
                     font=("Arial", 24, "bold")).pack(pady=20)
        
        frame = ctk.CTkFrame(self.window)
        frame.pack(pady=10,  padx=20, fill="x")

        ctk.CTkLabel(frame, text="Category:", font=("ARIAL", 12, "bold")).pack(pady=(10, 5))
        self.category_combo = ctk.CTkComboBox(frame, values=list(self.categories),
                                              width=250, state="readonly")
        self.category_combo.set("nature")
        self.category_combo.pack(pady=(0, 10))

        ctk.CTkLabel(frame, text="Interval:", font=("ARIAL", 12, "bold")).pack(pady=(5, 5))
        self.timer_combo = ctk.CTkComboBox(frame, values=list(self.intervals.keys()),
                                            width=250, state="readonly", command=self.on_timer_change)
        self.timer_combo.set("Disabled")
        self.timer_combo.pack(pady=(0, 10))

        self.btn = ctk.CTkButton(self.window, text="Change Wallpaper",
                                 font=("Arial", 14, "bold"), height=40, command=self.change_wallpaper)
        self.btn.pack(pady=15, padx=20, fill="x")

        self.progress = ctk.CTkProgressBar(self.window, width=500, mode="indeterminate")

        self.status = ctk.CTkLabel(self.window, text="Done", text_color="gray")
        self.status.pack(pady=5)

        self.preview_frame = ctk.CTkFrame(self.window, width=510, height=285)
        self.preview_frame.pack(pady=15, padx=20)
        self.preview_frame.pack_propagate(False)

        self.preview_label = ctk.CTkLabel(self.preview_frame,
                                           text="Last preview will appear here",
                                           text_color="gray")
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

    def download_image(self, category):
        try:
            self.status.configure(text="Downloading..... ", text_color="yellow")
            self.progress.pack(pady=5)
            self.progress.start()
            self.window.update()

            url = f"https://loremflickr.com/1920/1080/{category}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            image_path = self.wallpaper_dir / f"wallpaper_{category}.jpg"
            with open(image_path, 'wb') as f:
                f.write(response.content)

            self.progress.stop()
            self.progress.pack_forget()
            self.status.configure(text="Download complete", text_color="green")

            return str(image_path)
        
        except requests.exceptions.ConnectionError:
            self.progress.stop()
            self.progress.pack_forget()
            self.status.configure(text="No internet connection", text_color="red")
            messagebox.showerror("Error", "No internet connection. Please check your connection and try again.")
            return None
        except Exception as e:
            self.progress.stop()
            self.progress.pack_forget()
            self.status.configure(text="Error", text_color="red")
            messagebox.showerror("Error", str(e))
            return None
        
    def set_wallpaper(self, image_path):
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            self.status.configure(text="Wallpaper set successfully", text_color="green")
            return True
        except Exception as e:
            self.status.configure(text="Error setting wallpaper", text_color="red")
            messagebox.showerror("error", f"Error setting wallpaper: {e}")
            return False
    def show_preview(self, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((510, 285), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            if hasattr(self, 'preview_img'):
                self.preview_img.configure(image=photo)
                self.preview_img.image = photo
            else:
                self.preview_label.destroy()
                self.preview_img = ctk.CTkLabel(self.preview_frame, image=photo, text="")
                self.preview_img.image = photo
                self.preview_img.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Error showing preview: {e}")

    def change_wallpaper(self):
        self.btn.configure(state="disabled")

        category = self.category_combo.get()
        image_path = self.download_image(category)

        if image_path:
            if self.set_wallpaper(image_path):
                self.show_preview(image_path)

        self.btn.configure(state="normal")

    def on_timer_change(self, choice):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

        interval = self.intervals[choice]
        if interval > 0:
            self.status.configure(text=f"Wallpaper will change every {choice}", text_color="blue")
            self.start_timer(interval)
        else:
            self.status.configure(text="Ready", text_color="gray")

    def start_timer(self, interval):
        def callback():
            self.change_wallpaper()
            self.timer_id = self.window.after(interval, callback)
        self.timer_id = self.window.after(interval, callback)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = WallpaperChanger()
    app.run()