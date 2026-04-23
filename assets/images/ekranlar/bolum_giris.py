# ekranlar/bolum_giris.py — Bölüm Giriş Ekranı

import tkinter as tk
from renkler import *
from veri import BOLUMLER


class BolumGirisEkrani:
    def __init__(self, oyun):
        self.oyun = oyun
        self.bolum = BOLUMLER[oyun.bolum_idx]
        self._olustur()

    def _olustur(self):
        f = self.oyun.ana_cerceve
        canvas = tk.Canvas(f, bg=PANEL, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        b = self.bolum

        # Üst başlık şeridi
        canvas.create_rectangle(0, 0, 1280, 80, fill=CARD, outline="")
        canvas.create_text(640, 24, text=f"BÖLÜM  {b['num']}  /  3",
                           font=("Consolas", 13), fill=GRAY)
        canvas.create_text(640, 54, text=b["title"],
                           font=("Impact", 30, "bold"), fill=GOLD)

        # Konum
        canvas.create_text(640, 105, text=b["location"],
                           font=("Segoe UI", 13, "italic"), fill=CYAN)

        # Hikaye kutusu
        canvas.create_rectangle(240, 122, 1040, 308,
                                 fill=CARD, outline=BORDER, width=2)
        canvas.create_text(640, 215, text=b["hikaye"],
                           font=("Segoe UI", 13), fill=WHITE,
                           width=750, justify="center")

        # Şüpheliler önizleme
        canvas.create_text(640, 342, text="─── ŞÜPHELİLER ───",
                           font=("Impact", 16), fill=GRAY)

        for i, s in enumerate(b["supheliler"]):
            bx = 280 + i * 240
            canvas.create_rectangle(bx - 100, 368, bx + 100, 488,
                                    fill=CARD, outline=s["renk"], width=2)
            canvas.create_text(bx, 400, text=s["emoji"],
                               font=("Segoe UI Emoji", 28), fill=s["renk"])
            canvas.create_text(bx, 440, text=s["isim"],
                               font=("Impact", 14), fill=s["renk"])
            canvas.create_text(bx, 460, text=s["rol"],
                               font=("Segoe UI", 10), fill=GRAY)
            canvas.create_text(bx, 480, text="❓",
                               font=("Segoe UI Emoji", 13), fill=DARK)

        # Gereksinim bilgisi
        canvas.create_text(640, 528,
                           text=f"Bu bölümü çözmek için en az  {b['min_delil']}  delil toplamalısın!",
                           font=("Segoe UI", 12), fill=YELLOW)

        # Butonlar
        btn_f = tk.Frame(canvas, bg=PANEL)
        canvas.create_window(640, 590, window=btn_f)

        tk.Button(
            btn_f, text="🔍  SORUŞTURMAYA BAŞLA",
            font=("Impact", 19), bg=RED, fg=WHITE,
            relief="flat", padx=30, pady=12, cursor="hand2",
            command=self.oyun.goster_sorusturma
        ).pack(side="left", padx=10)

        tk.Button(
            btn_f, text="◀  Ana Menü",
            font=("Segoe UI", 12), bg=CARD2, fg=GRAY,
            relief="flat", padx=16, pady=12, cursor="hand2",
            command=self.oyun.goster_baslik
        ).pack(side="left", padx=5)
