# main.py — Oyunu Başlatan Giriş Noktası

import tkinter as tk
from src.core.oyun import CriminalCaseOyunu

if __name__ == "__main__":
    kok = tk.Tk()
    CriminalCaseOyunu(kok)
    kok.mainloop()
