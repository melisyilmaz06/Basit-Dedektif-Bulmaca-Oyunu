# ekranlar/lab.py — Laboratuvar Penceresi

import tkinter as tk
from tkinter import ttk
import threading
import time
from renkler import *
from veri import BOLUMLER


class LaboratuvarPenceresi:
    def __init__(self, oyun, delil):
        self.oyun  = oyun
        self.delil = delil
        self._olustur()

    def _olustur(self):
        self.pencere = tk.Toplevel(self.oyun.kok)
        self.pencere.title("🔬 Dedektif Laboratuvarı")
        self.pencere.geometry("520x430")
        self.pencere.configure(bg=PANEL)
        self.pencere.grab_set()
        self.pencere.resizable(False, False)

        tk.Label(self.pencere, text="🔬  DEDEKTİF LABORATUVARI",
                 font=("Impact", 18), bg=PANEL, fg=CYAN).pack(pady=15)
        tk.Label(self.pencere, text=f"Analiz ediliyor:  {self.delil}",
                 font=("Consolas", 13), bg=PANEL, fg=WHITE).pack(pady=5)

        self.durum_etiketi = tk.Label(
            self.pencere, text="⚗️  Analiz başlatılıyor...",
            font=("Segoe UI", 11, "italic"), bg=PANEL, fg=GRAY
        )
        self.durum_etiketi.pack(pady=8)

        # İlerleme çubuğu stili
        stil = ttk.Style()
        stil.theme_use("clam")
        stil.configure(
            "Lab.Horizontal.TProgressbar",
            troughcolor=CARD2, background=GREEN,
            bordercolor=PANEL, lightcolor=GREEN, darkcolor=GREEN, thickness=28
        )

        cerceve = tk.Frame(self.pencere, bg=CARD2, pady=5)
        cerceve.pack(fill="x", padx=30)

        self.ilerleme = ttk.Progressbar(
            cerceve, style="Lab.Horizontal.TProgressbar",
            orient="horizontal", length=460,
            mode="determinate", maximum=100
        )
        self.ilerleme.pack(pady=8)

        self.yuzde_etiketi = tk.Label(
            self.pencere, text="0%",
            font=("Consolas", 14, "bold"), bg=PANEL, fg=GREEN
        )
        self.yuzde_etiketi.pack(pady=4)

        self.sonuc_etiketi = tk.Label(
            self.pencere, text="",
            font=("Consolas", 13, "bold"), bg=PANEL, fg=WHITE,
            wraplength=460, justify="center"
        )
        self.sonuc_etiketi.pack(pady=12)

        self.kapat_btn = tk.Button(
            self.pencere, text="Kapat", state="disabled",
            font=("Segoe UI", 12), bg=CARD2, fg=GRAY,
            relief="flat", padx=20, pady=8,
            command=self.pencere.destroy
        )
        self.kapat_btn.pack(pady=5)

        threading.Thread(target=self._analiz_yap, daemon=True).start()

    def _analiz_yap(self):
        adimlar = [
            "🔬  Örnek hazırlanıyor...",
            "⚗️   Kimyasal bileşenler analiz ediliyor...",
            "🧬  DNA / parmak izi taranıyor...",
            "💾  Veritabanıyla eşleştiriliyor...",
            "✅  Analiz tamamlandı!",
        ]

        for i, adim in enumerate(adimlar):
            if not self.pencere.winfo_exists():
                break
            self.durum_etiketi.configure(text=adim)
            hedef = (i + 1) * 20
            current = self.ilerleme["value"]
            while current < hedef:
                current += 2
                self.ilerleme["value"] = current
                self.yuzde_etiketi.configure(text=f"{int(current)}%")
                time.sleep(0.04)

        if not self.pencere.winfo_exists():
            self.oyun.lab_mesgul = False
            return

        sonuc_metni, sonuc_rengi = self._sonuc_belirle()

        self.sonuc_etiketi.configure(text=sonuc_metni, fg=sonuc_rengi)
        self.ilerleme["value"] = 100
        self.yuzde_etiketi.configure(text="100%", fg=GREEN)

        # Analiz edilenler listesine ekle
        self.oyun.analiz_edilenler.append(self.delil)
        self.oyun.analiz_guncelle()
        self.oyun.skor_guncelle(15 if sonuc_rengi == CYAN else 30)

        self.kapat_btn.configure(state="normal", bg=GREEN, fg=BG)
        self.oyun.lab_mesgul = False

    def _sonuc_belirle(self):
        bolum = BOLUMLER[self.oyun.bolum_idx]
        sahip = None

        # Şüphelilerin delilleriyle eşleştir
        for s in bolum["supheliler"]:
            for sd in s["deliller"]:
                if sd.lower() in self.delil.lower() or self.delil.lower() in sd.lower():
                    sahip = s
                    break
            if sahip:
                break

        # Suclu delilleriyle eşleştir
        if not sahip:
            for gc in bolum["suclu_deliller"]:
                if gc.lower() in self.delil.lower() or self.delil.lower() in gc.lower():
                    sahip = next((s for s in bolum["supheliler"] if s["suclu"]), None)
                    break

        if sahip:
            if sahip["suclu"]:
                metin = (
                    f"🎯  SONUÇ BULUNDU!\n\n"
                    f"Bu delil  '{sahip['isim']}'  ile eşleşti!\n"
                    f"({sahip['rol']})\n\n"
                    f"⚠️  Şüpheli işaretlendi!"
                )
                return metin, RED
            else:
                metin = (
                    f"ℹ️  Delil analiz edildi.\n\n"
                    f"Bu delil  '{sahip['isim']}'  ile bağlantılı.\n"
                    f"({sahip['rol']})\n\n"
                    f"✅  Bu kişi temize çıktı."
                )
                return metin, GREEN
        else:
            metin = (
                f"🔍  Delil analiz edildi.\n\n"
                f"Bilinen şüphelilerle doğrudan\n"
                f"bağlantı kurulamadı.\n"
                f"Daha fazla delil gerekebilir."
            )
            return metin, CYAN
