"""
MASA 01_Weather App Using Tkinter in Python with Source Code
Developer: MASA
"""

import tkinter as tk
from tkinter import messagebox
import requests

BG_COLOR = "#eef2f5"
CARD_COLOR = "#ffffff"
ACCENT = "#2b7cff"
TEXT_COLOR = "#333333"


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("520x540")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        self.build_ui()

    # ---------------- UI ----------------
    def build_ui(self):
        tk.Label(
            self.root,
            text="Weather Forecast",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=20)

        search_frame = tk.Frame(self.root, bg=BG_COLOR)
        search_frame.pack(pady=5)

        self.city_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 13),
            width=24,
            justify="center"
        )
        self.city_entry.pack(side="left", padx=10)

        self.add_placeholder()
        self.city_entry.bind("<FocusIn>", self.remove_placeholder)
        self.city_entry.bind("<FocusOut>", self.restore_placeholder)

        tk.Button(
            search_frame,
            text="Search",
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT,
            fg="white",
            relief="flat",
            width=10,
            command=self.get_weather
        ).pack(side="left")

        self.current_card = tk.Frame(
            self.root,
            bg=CARD_COLOR,
            bd=1,
            relief="solid"
        )
        self.current_card.pack(padx=20, pady=20, fill="x")

        self.current_label = tk.Label(
            self.current_card,
            font=("Segoe UI", 12),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            justify="left"
        )
        self.current_label.pack(padx=15, pady=15)

        tk.Label(
            self.root,
            text="3-Day Forecast",
            font=("Segoe UI", 14, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        self.forecast_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.forecast_frame.pack()

        self.forecast_labels = []
        for _ in range(3):
            card = tk.Frame(
                self.forecast_frame,
                bg=CARD_COLOR,
                bd=1,
                relief="solid",
                width=140,
                height=140
            )
            card.pack(side="left", padx=10)
            card.pack_propagate(False)

            lbl = tk.Label(
                card,
                font=("Segoe UI", 11),
                bg=CARD_COLOR,
                fg=TEXT_COLOR,
                justify="center"
            )
            lbl.pack(expand=True)

            self.forecast_labels.append(lbl)

    # ---------------- PLACEHOLDER ----------------
    def add_placeholder(self):
        self.city_entry.insert(0, "Enter city")
        self.city_entry.config(fg="gray")

    def remove_placeholder(self, event):
        if self.city_entry.get() == "Enter city":
            self.city_entry.delete(0, tk.END)
            self.city_entry.config(fg="black")

    def restore_placeholder(self, event):
        if not self.city_entry.get():
            self.add_placeholder()

    # ---------------- WEATHER ----------------
    def get_weather(self):
        city = self.city_entry.get().strip()

        if city == "" or city == "Enter city":
            messagebox.showwarning("Input Error", "Please enter a city")
            return

        try:
            url = f"https://wttr.in/{city}?format=j1"
            headers = {"User-Agent": "Mozilla/5.0"}

            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()

            self.display_weather(data)

            self.city_entry.delete(0, tk.END)
            self.add_placeholder()

        except requests.exceptions.RequestException:
            messagebox.showerror(
                "Error",
                "Unable to fetch weather data.\nCheck your internet connection."
            )

    def display_weather(self, data):
        current = data["current_condition"][0]
        forecast = data["weather"][:3]

        self.current_label.config(
            text=(
                f"{self.icon(current['weatherDesc'][0]['value'])}  "
                f"{current['weatherDesc'][0]['value']}\n\n"
                f"Temperature: {current['temp_C']} °C\n"
                f"Humidity: {current['humidity']}%\n"
                f"Wind: {current['windspeedKmph']} km/h"
            )
        )

        for i, day in enumerate(forecast):
            desc = day["hourly"][4]["weatherDesc"][0]["value"]
            self.forecast_labels[i].config(
                text=(
                    f"{self.icon(desc)}\n"
                    f"{day['date']}\n\n"
                    f"{desc}\n"
                    f"{day['maxtempC']}° / {day['mintempC']}°"
                )
            )

    # ---------------- ICON ----------------
    def icon(self, desc):
        d = desc.lower()
        if "sun" in d or "clear" in d:
            return "☀️"
        if "cloud" in d:
            return "☁️"
        if "rain" in d:
            return "🌧"
        if "storm" in d or "thunder" in d:
            return "⛈"
        if "snow" in d:
            return "❄️"
        if "fog" in d or "mist" in d:
            return "🌫"
        return "🌡"


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    WeatherApp(root)
    root.mainloop()