# ekranlar/baslik.py — Başlık Ekranı

import tkinter as tk
import random
from renkler import *
from veri import BOLUMLER


class BaslikEkrani:
    def __init__(self, oyun):
        self.oyun = oyun
        self._olustur()

    def _olustur(self):
        f = self.oyun.ana_cerceve
        canvas = tk.Canvas(f, bg=BG, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Dekoratif arka plan daireleri
        for _ in range(8):
            x = random.randint(50, 1230)
            y = random.randint(50, 730)
            r = random.randint(20, 80)
            col = random.choice(["#0d2045", "#0a1a35", "#122040", "#0e1c38"])
            canvas.create_oval(x - r, y - r, x + r, y + r, fill=col, outline="")

        # Başlık / Logo
        canvas.create_text(640, 155, text="🔍", font=("Segoe UI Emoji", 60), fill=GOLD)
        canvas.create_text(640, 255, text="CRIMINAL CASE",
                           font=("Impact", 52, "bold"), fill=GOLD)
        canvas.create_text(640, 315, text="İSTANBUL DOSYALARI",
                           font=("Consolas", 22, "bold"), fill=CYAN)
        canvas.create_text(640, 365, text="─── ✦ Üç Bölümlü Dedektiflik Macerası ✦ ───",
                           font=("Segoe UI", 13), fill=GRAY)

        # Bölüm önizlemeleri
        onizleme = [
            ("1", "Müzedeki Cinayet", "#dc2626"),
            ("2", "Limandaki Şifre",  "#059669"),
            ("3", "Karanlık Orman",   "#6d28d9"),
        ]
        for i, (num, isim, renk) in enumerate(onizleme):
            bx = 340 + i * 200
            canvas.create_rectangle(bx - 80, 415, bx + 80, 488,
                                    fill=CARD, outline=renk, width=2)
            canvas.create_text(bx, 438, text=f"Bölüm {num}",
                               font=("Consolas", 11, "bold"), fill=renk)
            canvas.create_text(bx, 462, text=isim,
                               font=("Segoe UI", 10), fill=WHITE)

        # Toplam yıldız gösterimi
        toplam = sum(self.oyun.bolum_yildizlari)
        yildiz_str = "⭐" * toplam + "☆" * (9 - toplam)
        canvas.create_text(640, 522, text=f"Toplam Yıldız:  {yildiz_str}",
                           font=("Segoe UI", 12), fill=YELLOW)

        # Butonlar
        btn_cerceve = tk.Frame(canvas, bg=BG)
        canvas.create_window(640, 588, window=btn_cerceve)

        tk.Button(
            btn_cerceve, text="▶  OYUNA BAŞLA",
            font=("Impact", 18), bg=GOLD, fg=BG,
            relief="flat", padx=30, pady=12, cursor="hand2",
            command=self.oyun.goster_bolum_giris
        ).pack(side="left", padx=10)

        tk.Button(
            btn_cerceve, text="🏆  SKORLAR",
            font=("Impact", 18), bg=CARD2, fg=YELLOW,
            relief="flat", padx=20, pady=12, cursor="hand2",
            command=self._goster_skorlar
        ).pack(side="left", padx=10)

        canvas.create_text(640, 655, text="Delil topla  •  Analiz et  •  Suçluyu yakala!",
                           font=("Segoe UI", 11, "italic"), fill=DARK)
        canvas.create_text(640, 685, text="v1.0  |  © 2025 Criminal Case: İstanbul",
                           font=("Segoe UI", 9), fill=DARK)

    def _goster_skorlar(self):
        import tkinter as tk
        pencere = tk.Toplevel(self.oyun.kok)
        pencere.title("🏆 Skor Tablosu")
        pencere.geometry("400x360")
        pencere.configure(bg=PANEL)
        pencere.grab_set()

        tk.Label(pencere, text="🏆  SKOR TABLOSU",
                 font=("Impact", 20), bg=PANEL, fg=GOLD).pack(pady=20)

        for i, bolum in enumerate(BOLUMLER):
            yildiz = self.oyun.bolum_yildizlari[i]
            satir = tk.Frame(pencere, bg=CARD, pady=8, padx=15)
            satir.pack(fill="x", padx=20, pady=4)
            tk.Label(satir, text=f"Bölüm {i + 1}: {bolum['title']}",
                     font=("Segoe UI", 11, "bold"), bg=CARD, fg=WHITE).pack(side="left")
            tk.Label(satir, text="⭐" * yildiz + "☆" * (3 - yildiz),
                     font=("Segoe UI", 14), bg=CARD, fg=YELLOW).pack(side="right")

        tk.Label(pencere, text=f"Toplam Skor:  {self.oyun.toplam_skor} puan",
                 font=("Consolas", 14, "bold"), bg=PANEL, fg=GREEN).pack(pady=15)

        tk.Button(pencere, text="Kapat", bg=CARD2, fg=WHITE,
                  font=("Segoe UI", 11), relief="flat", padx=20, pady=6,
                  command=pencere.destroy).pack()
