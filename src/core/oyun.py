# oyun.py — Ana Oyun Sınıfı (Durum Yönetimi + Navigasyon + Mantık)

# Kalıtım kuralı için Base Class
class OyunVarligi:
    def __init__(self, isim):
        self.isim = isim

# Kalıtım uygulanan sınıf
class Delil(OyunVarligi): 
    def __init__(self, isim, detay):
        super().__init__(isim) # Kalıtım burada gerçekleşiyor
        self.detay = detay

import tkinter as tk
import random
from src.ui.renkler import *
from src.data.veri import BOLUMLER


class CriminalCaseOyunu:
    def __init__(self, kok):
        self.kok = kok
        self.kok.title("🔍 Criminal Case: İstanbul Dosyaları")
        self.kok.geometry("1280x780")
        self.kok.configure(bg=BG)
        self.kok.resizable(True, True)
        self.kok.minsize(1100, 700)

        # ── Oyun Durumu
        self.bolum_idx          = 0
        self.envanter           = []
        self.analiz_edilenler   = []
        self.skor               = 0
        self.toplam_skor        = 0
        self.bolum_yildizlari   = [0, 0, 0]
        self.lab_mesgul         = False

        # ── UI Referansları (ekranlar tarafından doldurulur)
        self.skor_etiketi       = None
        self.delil_sayisi_etiketi = None
        self.bilgi_etiketi      = None
        self.envanter_listesi   = None
        self.analiz_etiketi     = None
        self.sahne_canvas       = None

        # ── Ana çerçeve
        self.ana_cerceve = None
        self.goster_baslik()

    # ══════════════════════════════════════
    #  EKRAN TEMİZLEME
    # ══════════════════════════════════════
    def _temizle(self):
        if self.ana_cerceve:
            self.ana_cerceve.destroy()
        self.ana_cerceve = tk.Frame(self.kok, bg=BG)
        self.ana_cerceve.pack(fill="both", expand=True)

    # ══════════════════════════════════════
    #  NAVİGASYON METOTLARİ
    # ══════════════════════════════════════
    def goster_baslik(self):
        self._temizle()
        from ekranlar.baslik import BaslikEkrani
        BaslikEkrani(self)

    def goster_bolum_giris(self):
        self._temizle()
        # Bölüm durumunu sıfırla
        self.envanter.clear()
        self.analiz_edilenler.clear()
        self.skor = 0
        self.lab_mesgul = False
        from ekranlar.bolum_giris import BolumGirisEkrani
        BolumGirisEkrani(self)

    def goster_sorusturma(self):
        self._temizle()
        from ekranlar.sorusturma import SorusturmaEkrani
        SorusturmaEkrani(self)

    def goster_oyun_sonu(self):
        self._temizle()
        from ekranlar.sonuc import OyunSonuEkrani
        OyunSonuEkrani(self)

    def sonraki_bolum(self):
        self.bolum_idx += 1
        self.goster_bolum_giris()

    def yeniden_baslat(self):
        self.bolum_idx          = 0
        self.envanter           = []
        self.analiz_edilenler   = []
        self.skor               = 0
        self.toplam_skor        = 0
        self.bolum_yildizlari   = [0, 0, 0]
        self.goster_baslik()

    # ══════════════════════════════════════
    #  OLAY YERİ İNCELEME
    # ══════════════════════════════════════
    def olay_yeri_incele(self):
        bolum = BOLUMLER[self.bolum_idx]
        kalanlar = [d for d in bolum["tum_deliller"] if d not in self.envanter]

        if not kalanlar:
            self._bilgi_guncelle("🔍 Olay yerinde toplanacak başka delil kalmadı!", YELLOW)
            return

        adet = random.randint(1, min(3, len(kalanlar)))
        bulunanlar = random.sample(kalanlar, adet)

        for delil in bulunanlar:
            self.envanter.append(delil)
            self.envanter_listesi.insert(tk.END, f"  {delil}")

        self._delil_sayisi_guncelle()
        self.skor_guncelle(adet * 10)
        self._bilgi_guncelle(
            f"🔎  Bulunan: {', '.join(bulunanlar)}", GREEN
        )
        self._sahne_flas()

    def _sahne_flas(self):
        if self.sahne_canvas:
            self.sahne_canvas.configure(
                highlightbackground=GREEN, highlightthickness=3
            )
            self.kok.after(300, lambda: self.sahne_canvas.configure(
                highlightbackground=BORDER, highlightthickness=2
            ))

    # ══════════════════════════════════════
    #  LAB AÇMA
    # ══════════════════════════════════════
    def lab_ac(self):
        secim = self.envanter_listesi.curselection()
        if not secim:
            self._bilgi_guncelle("⚠️  Önce listeden bir delil seç!", RED)
            return
        if self.lab_mesgul:
            self._bilgi_guncelle("⚗️  Laboratuvar meşgul, lütfen bekle...", YELLOW)
            return

        delil = self.envanter_listesi.get(secim[0]).strip()
        if delil in self.analiz_edilenler:
            self._bilgi_guncelle(f"✅  '{delil}' zaten analiz edildi!", CYAN)
            return

        self.lab_mesgul = True
        from ekranlar.lab import LaboratuvarPenceresi
        LaboratuvarPenceresi(self, delil)

    # ══════════════════════════════════════
    #  SUÇLAMA
    # ══════════════════════════════════════
    def sucla(self, supheli_isim):
        from ekranlar.sonuc import SuclamaPopup
        SuclamaPopup(self, supheli_isim)

    # ══════════════════════════════════════
    #  KARAR VERME (DOĞRU / YANLIŞ)
    # ══════════════════════════════════════
    def karar_ver(self, supheli):
        dogru = supheli["suclu"]

        if dogru:
            bonus    = len(self.analiz_edilenler) * 20
            self.skor += 200 + bonus
            self.toplam_skor += self.skor
            yildiz = min(
                3,
                1
                + (len(self.analiz_edilenler) >= 3)
                + (len(self.envanter) >= BOLUMLER[self.bolum_idx]["min_delil"] + 2)
            )
            self.bolum_yildizlari[self.bolum_idx] = yildiz
        else:
            self.skor = max(0, self.skor - 50)
            self.toplam_skor += self.skor
            yildiz = 0

        self._temizle()
        from ekranlar.sonuc import KararEkrani
        KararEkrani(self, supheli, dogru, yildiz)

    # ══════════════════════════════════════
    #  NOTLARI KAYDET
    # ══════════════════════════════════════
    def notlari_kaydet(self):
        from araclar.kaydet import dosya_kaydet
        yol = dosya_kaydet(self)
        self._bilgi_guncelle(f"💾  Kaydedildi: {yol}", GREEN)

    # ══════════════════════════════════════
    #  UI GÜNCELLEME YARDIMCILARI
    # ══════════════════════════════════════
    def skor_guncelle(self, artis=0):
        self.skor += artis
        if self.skor_etiketi:
            self.skor_etiketi.configure(text=f"⭐ Skor: {self.skor}")

    def _delil_sayisi_guncelle(self):
        bolum = BOLUMLER[self.bolum_idx]
        n   = len(self.envanter)
        req = bolum["min_delil"]
        renk = GREEN if n >= req else YELLOW
        if self.delil_sayisi_etiketi:
            self.delil_sayisi_etiketi.configure(
                text=f"🗂 Delil: {n} / {req} gerekli", fg=renk
            )

    def _bilgi_guncelle(self, mesaj, renk=GRAY):
        if self.bilgi_etiketi:
            self.bilgi_etiketi.configure(text=mesaj, fg=renk)

    def analiz_guncelle(self):
        if self.analiz_etiketi:
            metin = (
                "\n".join(f"✅ {a}" for a in self.analiz_edilenler[-6:])
                or "Henüz analiz yok."
            )
            self.analiz_etiketi.configure(
                text=metin,
                fg=GREEN if self.analiz_edilenler else DARK
            )
