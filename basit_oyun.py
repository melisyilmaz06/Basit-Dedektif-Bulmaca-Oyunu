# basit_oyun.py - Basit Grafik Arayüz

"""
Criminal Case: İstanbul Dosyaları - Basit Grafik Arayüz

Bu script, oyunu basit bir Tkinter arayüzü ile çalıştırır.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Proje yolunu ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.karakter import Supheli, KarakterYoneticisi
from services.delil_analiz_servisi import DelilAnalizServisi
from data.veri import BOLUMLER


class BasitDedektifOyunu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔍 Criminal Case: İstanbul Dosyaları")
        self.root.geometry("900x700")
        self.root.configure(bg="#2c3e50")
        
        # Oyun durumu
        self.bolum_idx = 0
        self.envanter = []
        self.analiz_edilenler = []
        self.skor = 0
        self.karakter_yoneticisi = None
        self.analiz_servisi = None
        
        # Arayüz oluştur
        self.arayuzu_olustur()
        self.oyunu_baslat()
    
    def arayuzu_olustur(self):
        """Ana arayüzü oluşturur."""
        # Başlık
        baslik = tk.Label(
            self.root, 
            text="🔍 CRIMINAL CASE: İSTANBUL DOSYALARI",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        baslik.pack(pady=10)
        
        # Ana çerçeve
        self.ana_cerceve = tk.Frame(self.root, bg="#34495e")
        self.ana_cerceve.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Sol panel - Oyun bilgileri
        self.sol_panel = tk.Frame(self.ana_cerceve, bg="#34495e")
        self.sol_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Sağ panel - Karakterler
        self.sag_panel = tk.Frame(self.ana_cerceve, bg="#34495e")
        self.sag_panel.pack(side="right", fill="both", expand=True)
        
        # Bölüm bilgileri
        self.bolum_text = tk.Text(
            self.sol_panel,
            height=8,
            bg="#2c3e50",
            fg="white",
            font=("Arial", 10),
            wrap=tk.WORD
        )
        self.bolum_text.pack(fill="both", expand=True, pady=(0, 10))
        
        # Butonlar
        buton_cerceve = tk.Frame(self.sol_panel, bg="#34495e")
        buton_cerceve.pack(fill="x")
        
        tk.Button(
            buton_cerceve,
            text="🔍 Delil Topla",
            command=self.delil_topla,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            buton_cerceve,
            text="🔬 Analiz Et",
            command=self.delil_analiz_et,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            buton_cerceve,
            text="🚨 Suçla",
            command=self.sucla,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(side="left", padx=5)
        
        # Durum bilgisi
        self.durum_label = tk.Label(
            self.sol_panel,
            text="Oyun başlatılıyor...",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Arial", 10)
        )
        self.durum_label.pack(pady=10)
        
        # Skor
        self.skor_label = tk.Label(
            self.sol_panel,
            text="⭐ Skor: 0",
            bg="#34495e",
            fg="#f39c12",
            font=("Arial", 12, "bold")
        )
        self.skor_label.pack()
        
        # Karakter listesi
        tk.Label(
            self.sag_panel,
            text="👥 ŞÜPHELİLER",
            bg="#34495e",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))
        
        self.karakter_listbox = tk.Listbox(
            self.sag_panel,
            bg="#2c3e50",
            fg="white",
            font=("Arial", 10),
            height=8
        )
        self.karakter_listbox.pack(fill="both", expand=True, pady=(0, 10))
        
        # Karakter detayları
        self.karakter_detay = tk.Text(
            self.sag_panel,
            height=8,
            bg="#2c3e50",
            fg="white",
            font=("Arial", 9),
            wrap=tk.WORD
        )
        self.karakter_detay.pack(fill="both", expand=True)
        
        # Listbox seçim olayı
        self.karakter_listbox.bind('<<ListboxSelect>>', self.karakter_secildi)
    
    def oyunu_baslat(self):
        """Oyunu başlatır."""
        try:
            # Karakter yöneticisi oluştur
            self.karakter_yoneticisi = KarakterYoneticisi()
            
            # Bölüm verilerini yükle
            bolum = BOLUMLER[self.bolum_idx]
            
            # Şüphelileri ekle
            for supheli_veri in bolum["supheliler"]:
                supheli = Supheli(
                    supheli_veri["isim"],
                    supheli_veri["rol"],
                    supheli_veri["suclu"],
                    supheli_veri["emoji"],
                    supheli_veri["renk"]
                )
                supheli.deliller = supheli_veri["deliller"]
                supheli.biyografi = supheli_veri["biyografi"]
                self.karakter_yoneticisi.karakter_ekle(supheli)
            
            # Analiz servisi oluştur
            self.analiz_servisi = DelilAnalizServisi()
            
            # Bölüm bilgilerini göster
            self.bolum_bilgilerini_goster()
            
            # Karakterleri listele
            self.karakterleri_listele()
            
            self.durum_label.config(text="🎮 Oyun başladı! Delil toplayın.")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Oyun başlatılamadı: {e}")
    
    def bolum_bilgilerini_goster(self):
        """Bölüm bilgilerini gösterir."""
        bolum = BOLUMLER[self.bolum_idx]
        
        metin = f"📖 {bolum['title']}\n"
        metin += f"📍 {bolum['location']}\n\n"
        metin += f"📜 HİKAYE:\n{bolum['hikaye']}\n\n"
        metin += f"🎯 Gerekli delil: {bolum['min_delil']}\n"
        metin += f"🔍 Toplanan delil: {len(self.envanter)}"
        
        self.bolum_text.delete(1.0, tk.END)
        self.bolum_text.insert(1.0, metin)
    
    def karakterleri_listele(self):
        """Karakterleri listeler."""
        self.karakter_listbox.delete(0, tk.END)
        
        supheliler = self.karakter_yoneticisi.suphelileri_getir()
        for supheli in supheliler:
            durum = "🔴" if supheli.suclu else "🟢"
            self.karakter_listbox.insert(tk.END, f"{durum} {supheli.isim} ({supheli.rol})")
    
    def karakter_secildi(self, event):
        """Karakter seçildiğinde detayları gösterir."""
        secim = self.karakter_listbox.curselection()
        if secim:
            index = secim[0]
            supheliler = self.karakter_yoneticisi.suphelileri_getir()
            if index < len(supheliler):
                supheli = supheliler[index]
                
                detay = f"👤 {supheli.isim}\n"
                detay += f"🏢 {supheli.rol}\n\n"
                detay += f"📝 BİYOGRAFİ:\n{supheli.biyografi}\n\n"
                detay += f"🔍 DELİLLER:\n"
                for delil in supheli.deliller:
                    detay += f"  • {delil}\n"
                
                self.karakter_detay.delete(1.0, tk.END)
                self.karakter_detay.insert(1.0, detay)
    
    def delil_topla(self):
        """Delil toplar."""
        import random
        
        bolum = BOLUMLER[self.bolum_idx]
        kalan_deliller = [d for d in bolum["tum_deliller"] if d not in self.envanter]
        
        if not kalan_deliller:
            self.durum_label.config(text="🔍 Tüm deliller toplandı!")
            return
        
        adet = random.randint(1, min(3, len(kalan_deliller)))
        bulunanlar = random.sample(kalan_deliller, adet)
        
        for delil in bulunanlar:
            self.envanter.append(delil)
        
        self.skor += adet * 10
        self.skor_label.config(text=f"⭐ Skor: {self.skor}")
        self.durum_label.config(text=f"🔎 {adet} delil bulundu: {', '.join(bulunanlar)}")
        
        self.bolum_bilgilerini_goster()
    
    def delil_analiz_et(self):
        """Seçili delili analiz eder."""
        if not self.envanter:
            self.durum_label.config(text="⚠️ Önce delil toplamalısınız!")
            return
        
        # Son delili analiz et
        delil = self.envanter[-1]
        
        if self.analiz_servisi.delil_analiz_et(delil):
            sonuc = self.analiz_servisi.analiz_sonucu_getir()
            self.analiz_edilenler.append(delil)
            
            self.skor += 20
            self.skor_label.config(text=f"⭐ Skor: {self.skor}")
            
            messagebox.showinfo(
                "🔬 Analiz Sonucu",
                f"Delil: {delil}\n\n"
                f"Yöntem: {sonuc['yontem']}\n\n"
                f"Sonuç: {sonuc['sonuc']['sonuc']}\n\n"
                f"Detay: {sonuc['sonuc']['detay']}"
            )
            
            self.durum_label.config(text=f"✅ {delil} analiz edildi!")
        else:
            messagebox.showerror("❌ Hata", "Analiz başarısız oldu!")
    
    def sucla(self):
        """Suçlama yapar."""
        if len(self.analiz_edilenler) < 2:
            messagebox.showwarning("⚠️ Uyarı", "Önce en az 2 delil analiz etmelisiniz!")
            return
        
        secim = self.karakter_listbox.curselection()
        if not secim:
            messagebox.showwarning("⚠️ Uyarı", "Önce bir şüpheli seçin!")
            return
        
        index = secim[0]
        supheliler = self.karakter_yoneticisi.suphelileri_getir()
        supheli = supheliler[index]
        
        if supheli.suclu:
            self.skor += 200
            messagebox.showinfo(
                "🎉 TEBRİKLER!",
                f"✅ DOĞRU TAHMİN!\n\n"
                f"{supheli.isim} gerçekten suçluydu!\n\n"
                f"🏆 Bonus: 200 puan\n"
                f"⭐ Toplam Skor: {self.skor}"
            )
        else:
            self.skor = max(0, self.skor - 50)
            messagebox.showinfo(
                "😔 YANLIŞ TAHMİN!",
                f"❌ YANLIŞ!\n\n"
                f"{supheli.isim} masumdu!\n\n"
                f"💔 Ceza: -50 puan\n"
                f"⭐ Skor: {self.skor}"
            )
        
        self.skor_label.config(text=f"⭐ Skor: {self.skor}")
        self.durum_label.config(text="🏁 Oyun bitti! Tebrikler!")
    
    def calistir(self):
        """Oyunu başlatır."""
        self.root.mainloop()


if __name__ == "__main__":
    try:
        oyun = BasitDedektifOyunu()
        oyun.calistir()
    except Exception as e:
        print(f"Oyun başlatılamadı: {e}")
        import traceback
        traceback.print_exc()
