# ekranlar/sorusturma.py — Soruşturma Ekranı

import tkinter as tk
from renkler import *
from veri import BOLUMLER
from sahneler import ciz_sahne


class SorusturmaEkrani:
    def __init__(self, oyun):
        self.oyun = oyun
        self.bolum = BOLUMLER[oyun.bolum_idx]
        self._olustur()

    def _olustur(self):
        f = self.oyun.ana_cerceve
        b = self.bolum

        # ── Üst bar
        ustbar = tk.Frame(f, bg=CARD, height=55)
        ustbar.pack(fill="x", side="top")
        ustbar.pack_propagate(False)

        tk.Label(ustbar, text=f"🔍  {b['title']}",
                 font=("Impact", 17), bg=CARD, fg=GOLD).pack(side="left", padx=15, pady=10)
        tk.Label(ustbar, text=b["location"],
                 font=("Segoe UI", 10, "italic"), bg=CARD, fg=CYAN).pack(side="left", padx=5)

        self.oyun.skor_etiketi = tk.Label(
            ustbar, text=f"⭐ Skor: {self.oyun.skor}",
            font=("Consolas", 13, "bold"), bg=CARD, fg=YELLOW
        )
        self.oyun.skor_etiketi.pack(side="right", padx=15)

        self.oyun.delil_sayisi_etiketi = tk.Label(
            ustbar,
            text=f"🗂 Delil: 0 / {b['min_delil']} gerekli",
            font=("Consolas", 12), bg=CARD, fg=GRAY
        )
        self.oyun.delil_sayisi_etiketi.pack(side="right", padx=10)

        # ── Ana içerik
        icerik = tk.Frame(f, bg=BG)
        icerik.pack(fill="both", expand=True)

        # ── SOL: Şüpheliler
        sol = tk.Frame(icerik, bg=PANEL, width=230)
        sol.pack(side="left", fill="y", padx=(8, 4), pady=8)
        sol.pack_propagate(False)

        tk.Label(sol, text="👥  ŞÜPHELİLER",
                 font=("Impact", 14), bg=PANEL, fg=GOLD).pack(pady=(12, 6))

        for s in b["supheliler"]:
            kart = tk.Frame(sol, bg=CARD, cursor="hand2")
            kart.pack(fill="x", padx=8, pady=5)
            kart.bind("<Enter>", lambda e, fr=kart, col=s["renk"]: fr.configure(bg=col))
            kart.bind("<Leave>", lambda e, fr=kart: fr.configure(bg=CARD))

            tk.Label(kart, text=f"{s['emoji']}  {s['isim']}",
                     font=("Impact", 13), bg=CARD, fg=s["renk"],
                     cursor="hand2").pack(anchor="w", padx=10, pady=(8, 2))
            tk.Label(kart, text=s["rol"],
                     font=("Segoe UI", 9), bg=CARD, fg=GRAY).pack(anchor="w", padx=12)
            tk.Label(kart, text=s["biyografi"],
                     font=("Segoe UI", 9), bg=CARD, fg=DARK,
                     justify="left", wraplength=190).pack(anchor="w", padx=12, pady=(2, 6))

            tk.Button(
                kart, text="⚖️  Suçla",
                font=("Segoe UI", 9, "bold"), bg=RED, fg=WHITE,
                relief="flat", padx=8, pady=3, cursor="hand2",
                command=lambda isim=s["isim"]: self.oyun.sucla(isim)
            ).pack(anchor="e", padx=8, pady=(0, 8))

        # ── ORTA: Olay yeri + butonlar
        orta = tk.Frame(icerik, bg=BG)
        orta.pack(side="left", fill="both", expand=True, padx=4, pady=8)

        self.oyun.sahne_canvas = tk.Canvas(
            orta, bg=CARD, highlightthickness=2,
            highlightbackground=BORDER, height=375, width=800
        )
        self.oyun.sahne_canvas.pack(fill="x", pady=(0, 6))
        ciz_sahne(self.oyun.sahne_canvas, b["sahne_turu"])

        # Aksiyon butonları
        aksiyon = tk.Frame(orta, bg=BG)
        aksiyon.pack(fill="x", pady=4)

        tk.Button(
            aksiyon, text="🔎  Olay Yerini İncele  (+Delil)",
            font=("Impact", 14), bg=BLUE, fg=WHITE,
            relief="flat", padx=18, pady=10, cursor="hand2",
            command=self.oyun.olay_yeri_incele
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            aksiyon, text="🔬  Delili Laboratuvara Gönder",
            font=("Impact", 14), bg=PURPLE, fg=WHITE,
            relief="flat", padx=18, pady=10, cursor="hand2",
            command=self.oyun.lab_ac
        ).pack(side="left", padx=4)

        tk.Button(
            aksiyon, text="💾  Dosyayı Kaydet",
            font=("Impact", 14), bg="#065f46", fg=WHITE,
            relief="flat", padx=18, pady=10, cursor="hand2",
            command=self.oyun.notlari_kaydet
        ).pack(side="left", padx=4)

        # Bilgi / durum satırı
        self.oyun.bilgi_etiketi = tk.Label(
            orta,
            text="💡  'Olay Yerini İncele' butonuna basarak delil toplayabilirsin!",
            font=("Segoe UI", 10, "italic"), bg=BG, fg=GRAY,
            wraplength=680, justify="left"
        )
        self.oyun.bilgi_etiketi.pack(fill="x", pady=(4, 0))

        # ── SAĞ: Envanter
        sag = tk.Frame(icerik, bg=PANEL, width=260)
        sag.pack(side="right", fill="y", padx=(4, 8), pady=8)
        sag.pack_propagate(False)

        tk.Label(sag, text="🗂️  DELİL ENVANTERİ",
                 font=("Impact", 14), bg=PANEL, fg=GOLD).pack(pady=(12, 4))
        tk.Label(sag, text="Bir delil seçip lab'a gönder:",
                 font=("Segoe UI", 9, "italic"), bg=PANEL, fg=GRAY).pack()

        # Listbox + scrollbar
        liste_cerceve = tk.Frame(sag, bg=PANEL)
        liste_cerceve.pack(fill="both", expand=True, padx=8, pady=6)

        kaydirici = tk.Scrollbar(liste_cerceve, bg=CARD2)
        kaydirici.pack(side="right", fill="y")

        self.oyun.envanter_listesi = tk.Listbox(
            liste_cerceve,
            font=("Consolas", 11),
            bg=CARD, fg=WHITE,
            selectbackground=BLUE, selectforeground=WHITE,
            relief="flat", bd=0,
            yscrollcommand=kaydirici.set,
            activestyle="none", cursor="hand2",
            height=14
        )
        self.oyun.envanter_listesi.pack(fill="both", expand=True)
        kaydirici.config(command=self.oyun.envanter_listesi.yview)

        # Analiz edilenler
        tk.Label(sag, text="✅  ANALİZ EDİLENLER",
                 font=("Impact", 12), bg=PANEL, fg=GREEN).pack(pady=(8, 2))

        self.oyun.analiz_etiketi = tk.Label(
            sag,
            text="Henüz analiz yok.",
            font=("Segoe UI", 9, "italic"), bg=PANEL, fg=DARK,
            wraplength=220, justify="left"
        )
        self.oyun.analiz_etiketi.pack(anchor="w", padx=8)
