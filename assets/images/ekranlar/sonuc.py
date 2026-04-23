# ekranlar/sonuc.py — Suçlama Popup, Karar Ekranı, Oyun Sonu Ekranı

import tkinter as tk
import random
from renkler import *
from veri import BOLUMLER


class SuclamaPopup:
    def __init__(self, oyun, supheli_isim):
        self.oyun = oyun
        bolum = BOLUMLER[oyun.bolum_idx]
        self.supheli = next(
            (s for s in bolum["supheliler"] if s["isim"] == supheli_isim), None
        )
        if not self.supheli:
            return
        self._olustur()

    def _olustur(self):
        bolum = BOLUMLER[self.oyun.bolum_idx]
        n_delil = len(self.oyun.envanter)

        if n_delil < bolum["min_delil"]:
            from tkinter import messagebox
            messagebox.showwarning(
                "Yeterli Delil Yok!",
                f"Suçlama için en az {bolum['min_delil']} delil gerekli!\n"
                f"Şu anda {n_delil} delilin var."
            )
            return

        pencere = tk.Toplevel(self.oyun.kok)
        pencere.title("⚖️  Suçlama")
        pencere.geometry("500x390")
        pencere.configure(bg=PANEL)
        pencere.grab_set()
        pencere.resizable(False, False)

        s = self.supheli

        tk.Label(pencere, text="⚖️  SUÇLAMA",
                 font=("Impact", 22), bg=PANEL, fg=GOLD).pack(pady=15)
        tk.Label(pencere, text=f"{s['emoji']}  {s['isim']}  ({s['rol']})",
                 font=("Impact", 16), bg=PANEL, fg=s["renk"]).pack(pady=5)
        tk.Label(pencere,
                 text=(
                     f"Toplanan delil:    {n_delil}\n"
                     f"Analiz edilen:     {len(self.oyun.analiz_edilenler)}"
                 ),
                 font=("Consolas", 12), bg=PANEL, fg=GRAY).pack(pady=8)
        tk.Label(pencere,
                 text=f"'{s['isim']}' kişisini bu suçtan\nsorumlu tuttuğunu onaylıyor musun?",
                 font=("Segoe UI", 12), bg=PANEL, fg=WHITE,
                 justify="center").pack(pady=10)

        def onayla():
            pencere.destroy()
            self.oyun.karar_ver(s)

        satirlar = tk.Frame(pencere, bg=PANEL)
        satirlar.pack(pady=15)

        tk.Button(satirlar, text="⚖️  EVET, SUÇLUYORUM!",
                  font=("Impact", 14), bg=RED, fg=WHITE,
                  relief="flat", padx=18, pady=10, cursor="hand2",
                  command=onayla).pack(side="left", padx=8)

        tk.Button(satirlar, text="🔙  Vazgeç",
                  font=("Segoe UI", 12), bg=CARD2, fg=GRAY,
                  relief="flat", padx=14, pady=10, cursor="hand2",
                  command=pencere.destroy).pack(side="left", padx=4)


class KararEkrani:
    def __init__(self, oyun, supheli, dogru, yildizlar):
        self.oyun     = oyun
        self.supheli  = supheli
        self.dogru    = dogru
        self.yildizlar = yildizlar
        self._olustur()

    def _olustur(self):
        f = self.oyun.ana_cerceve
        bolum = BOLUMLER[self.oyun.bolum_idx]
        s = self.supheli

        arka = BG if self.dogru else "#1a0505"
        canvas = tk.Canvas(f, bg=arka, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        if self.dogru:
            canvas.create_text(640, 80,  text="🎉  TEBRİKLER!",
                               font=("Impact", 42), fill=GREEN)
            canvas.create_text(640, 150, text="DOĞRU KİŞİYİ BULDUN!",
                               font=("Consolas", 20, "bold"), fill=YELLOW)
            canvas.create_text(640, 200,
                               text=f"{s['emoji']}  {s['isim']}  ({s['rol']})",
                               font=("Impact", 22), fill=s["renk"])
            canvas.create_text(640, 255,
                               text=f"Bölüm {bolum['num']}:  {bolum['title']}  çözüldü!",
                               font=("Segoe UI", 14), fill=WHITE)
            yildiz_str = "⭐" * self.yildizlar + "☆" * (3 - self.yildizlar)
            canvas.create_text(640, 310, text=yildiz_str,
                               font=("Segoe UI Emoji", 38), fill=YELLOW)
            canvas.create_text(640, 375,
                               text=f"Bu bölüm skoru:  {self.oyun.skor} puan",
                               font=("Consolas", 16, "bold"), fill=GOLD)
            canvas.create_text(640, 415,
                               text=f"Toplam skor:  {self.oyun.toplam_skor} puan",
                               font=("Consolas", 14), fill=GRAY)
        else:
            suclu = next(s2 for s2 in bolum["supheliler"] if s2["suclu"])
            canvas.create_text(640, 80,  text="💀  YANLIŞ KİŞİYİ SUÇLADIN!",
                               font=("Impact", 36), fill=RED)
            canvas.create_text(640, 150,
                               text=f"'{s['isim']}' masum biri!",
                               font=("Consolas", 18), fill=WHITE)
            canvas.create_text(640, 210,
                               text=f"Gerçek suçlu:  {suclu['emoji']}  {suclu['isim']}",
                               font=("Impact", 20), fill=YELLOW)
            canvas.create_text(640, 270,
                               text="Daha fazla delil toplayarak tekrar dene.",
                               font=("Segoe UI", 13), fill=GRAY)

        btn_f = tk.Frame(canvas, bg=arka)
        canvas.create_window(640, 505, window=btn_f)

        if self.dogru and self.oyun.bolum_idx < len(BOLUMLER) - 1:
            tk.Button(
                btn_f,
                text=f"▶  Bölüm {self.oyun.bolum_idx + 2}'ye Geç",
                font=("Impact", 17), bg=GREEN, fg=BG,
                relief="flat", padx=25, pady=12, cursor="hand2",
                command=self.oyun.sonraki_bolum
            ).pack(side="left", padx=8)
        elif self.dogru and self.oyun.bolum_idx == len(BOLUMLER) - 1:
            tk.Button(
                btn_f, text="🏆  Oyun Sonu",
                font=("Impact", 17), bg=GOLD, fg=BG,
                relief="flat", padx=25, pady=12, cursor="hand2",
                command=self.oyun.goster_oyun_sonu
            ).pack(side="left", padx=8)
        else:
            tk.Button(
                btn_f, text="🔄  Bu Bölümü Tekrar Oyna",
                font=("Impact", 15), bg=BLUE, fg=WHITE,
                relief="flat", padx=20, pady=12, cursor="hand2",
                command=self.oyun.goster_bolum_giris
            ).pack(side="left", padx=8)

        tk.Button(
            btn_f, text="🏠  Ana Menü",
            font=("Impact", 15), bg=CARD2, fg=GRAY,
            relief="flat", padx=20, pady=12, cursor="hand2",
            command=self.oyun.goster_baslik
        ).pack(side="left", padx=8)


class OyunSonuEkrani:
    def __init__(self, oyun):
        self.oyun = oyun
        self._olustur()

    def _olustur(self):
        f = self.oyun.ana_cerceve
        canvas = tk.Canvas(f, bg=BG, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Dekoratif parıltılar
        for _ in range(25):
            x = random.randint(0, 1280)
            y = random.randint(0, 780)
            col = random.choice([GOLD, GREEN, CYAN, PURPLE, ORANGE])
            canvas.create_text(x, y, text="✨", font=("Segoe UI Emoji", 14), fill=col)

        canvas.create_text(640, 90,  text="🏆  TÜM BÖLÜMLER TAMAMLANDI!",
                           font=("Impact", 40), fill=GOLD)
        canvas.create_text(640, 155, text="İstanbul'un sırları çözüldü!",
                           font=("Segoe UI", 16, "italic"), fill=CYAN)

        # Bölüm kartları
        for i, bolum in enumerate(BOLUMLER):
            bx = 180 + i * 300
            yildiz = self.oyun.bolum_yildizlari[i]
            canvas.create_rectangle(bx - 130, 238, bx + 130, 418,
                                    fill=CARD, outline=GOLD, width=2)
            canvas.create_text(bx, 262, text=f"Bölüm {i + 1}",
                               font=("Consolas", 12, "bold"), fill=GRAY)
            canvas.create_text(bx, 292, text=bolum["title"],
                               font=("Impact", 13), fill=WHITE, width=240)
            canvas.create_text(bx, 348, text="⭐" * yildiz + "☆" * (3 - yildiz),
                               font=("Segoe UI Emoji", 28), fill=YELLOW)
            canvas.create_text(bx, 398, text=f"{yildiz}/3 yıldız",
                               font=("Consolas", 11), fill=GRAY)

        toplam_yildiz = sum(self.oyun.bolum_yildizlari)
        canvas.create_text(640, 462,
                           text=f"Toplam Yıldız:  {'⭐' * toplam_yildiz}{'☆' * (9 - toplam_yildiz)}",
                           font=("Segoe UI Emoji", 28), fill=YELLOW)
        canvas.create_text(640, 528,
                           text=f"TOPLAM SKOR:  {self.oyun.toplam_skor} PUAN",
                           font=("Impact", 30, "bold"), fill=GREEN)

        if toplam_yildiz >= 8:
            unvan, renk = "🥇 EFSANEVİ DEDEKTİF", GOLD
        elif toplam_yildiz >= 5:
            unvan, renk = "🥈 UZMAN DEDEKTİF", LBLUE
        else:
            unvan, renk = "🥉 ÇAYLAK DEDEKTİF", GRAY

        canvas.create_text(640, 588, text=unvan, font=("Impact", 26), fill=renk)

        btn_f = tk.Frame(canvas, bg=BG)
        canvas.create_window(640, 658, window=btn_f)

        tk.Button(btn_f, text="🔄  Yeniden Oyna",
                  font=("Impact", 16), bg=GREEN, fg=BG,
                  relief="flat", padx=22, pady=12, cursor="hand2",
                  command=self.oyun.yeniden_baslat).pack(side="left", padx=8)

        tk.Button(btn_f, text="🏠  Ana Menü",
                  font=("Impact", 16), bg=CARD2, fg=GRAY,
                  relief="flat", padx=22, pady=12, cursor="hand2",
                  command=self.oyun.goster_baslik).pack(side="left", padx=8)
