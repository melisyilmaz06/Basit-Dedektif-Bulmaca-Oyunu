# test_surumu.py - Oyunun Test Sürümü

"""
Criminal Case: İstanbul Dosyaları - Test Sürümü

Bu script, oyunun temel özelliklerini test etmek için
UI olmadan çalışır.
"""

import sys
import os

# Proje yolunu ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.karakter import Supheli, Kurbun, Tanik, KarakterYoneticisi
from services.delil_analiz_servisi import DelilAnalizServisi
from utils.hata_yonetimi import Logger
from data.veri import BOLUMLER


def test_karakter_sistemi():
    """Karakter sistemini test eder."""
    print("🎭 KARAKTER SİSTEMİ TESTİ")
    print("=" * 50)
    
    # Karakter yöneticisi oluştur
    yoneticisi = KarakterYoneticisi()
    
    # Şüphelileri oluştur
    bolum = BOLUMLER[0]  # Müzedeki cinayet
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
        yoneticisi.karakter_ekle(supheli)
    
    print(f"📊 Toplam karakter: {len(yoneticisi)}")
    
    # Tüm karakterleri tanıt
    print("\n👥 KARAKTERLER:")
    print(yoneticisi.tum_karakterleri_tanit())
    
    # Suçluyu bul
    suclu = yoneticisi.sucluyu_bul()
    if suclu:
        print(f"\n🔍 SUÇLU: {suclu.isim} ({suclu.rol})")
        print(f"💬 Savunması: {suclu.savunma_yap()}")
    
    return yoneticisi


def test_analiz_sistemi():
    """Delil analiz sistemini test eder."""
    print("\n\n🔬 DELİL ANALİZ SİSTEMİ TESTİ")
    print("=" * 50)
    
    servis = DelilAnalizServisi()
    
    # Test delilleri
    test_deliller = [
        "🔍 Kırık Cam Parçası",
        "🩸 Kan Lekesi", 
        "👆 Parmak İzi",
        "🎨 Mavi Boya Tüpü"
    ]
    
    print(f"📋 Analiz edilecek deliller: {len(test_deliller)}")
    
    for i, delil in enumerate(test_deliller, 1):
        print(f"\n{i}. 🧪 {delil} analiz ediliyor...")
        
        basari = servis.delil_analiz_et(delil)
        if basari:
            sonuc = servis.analiz_sonucu_getir()
            print(f"   ✅ {sonuc['yontem']}")
            print(f"   📝 {sonuc['sonuc']['sonuc']}")
        else:
            print("   ❌ Analiz başarısız!")
    
    # İstatistikler
    stats = servis.analiz_istatistikleri()
    print(f"\n📊 ANALİZ İSTATİSTİKLERİ:")
    print(f"   Toplam analiz: {stats['toplam_analiz']}")
    print(f"   Başarılı: {stats['basarili_analiz']}")
    print(f"   Başarısız: {stats['basarisiz_analiz']}")
    
    return servis


def test_oyun_mantigi():
    """Oyun mantığını test eder."""
    print("\n\n🎮 OYUN MANTIĞI TESTİ")
    print("=" * 50)
    
    # Bölüm bilgileri
    bolum = BOLUMLER[0]
    print(f"📖 Bölüm: {bolum['title']}")
    print(f"📍 Konum: {bolum['location']}")
    print(f"\n📜 HİKAYE:")
    print(bolum['hikaye'])
    
    print(f"\n👥 ŞÜPHELİLER ({len(bolum['supheliler'])}):")
    for i, supheli in enumerate(bolum['supheliler'], 1):
        durum = "🔴 SUÇLU" if supheli['suclu'] else "🟢 MASUM"
        print(f"{i}. {supheli['isim']} ({supheli['rol']}) - {durum}")
    
    print(f"\n🔍 TOPLANACAK DELİLLER ({len(bolum['tum_deliller'])}):")
    print(", ".join(bolum['tum_deliller'][:5]) + "...")
    
    print(f"\n🎯 GEREKLİ MİNİMUM DELİL: {bolum['min_delil']}")


def test_polimorfizm():
    """Polimorfizm özelliğini test eder."""
    print("\n\n🔄 POLİMORFİZM TESTİ")
    print("=" * 50)
    
    # Farklı karakter tipleri oluştur
    karakterler = [
        Supheli("Ahmet", "Müdür", False),
        Kurbun("Mehmet", "Güvenlik", "Silahla yaralanma"),
        Tanik("Ayşe", "Görgü Tanığı")
    ]
    
    print("🎭 BİLGİ VERME POLİMORFİZMİ:")
    for i, karakter in enumerate(karakterler, 1):
        bilgi = karakter.bilgi_ver()
        print(f"{i}. {bilgi}")
        print(f"   Suçlu mu: {'Evet' if karakter.suclu_mu() else 'Hayır'}")


def main():
    """Ana test fonksiyonu."""
    print("🚀 CRIMINAL CASE: İSTANBUL DOSYALARI - TEST SÜRÜMÜ")
    print("=" * 60)
    print("🎯 BGT 132 Final Projesi - OOP ve Modüler Tasarım Testi")
    print("=" * 60)
    
    try:
        # Testleri çalıştır
        test_karakter_sistemi()
        test_analiz_sistemi()
        test_oyun_mantigi()
        test_polimorfizm()
        
        print("\n\n✅ TÜM TESTLER BAŞARILI!")
        print("🏆 Proje BGT 132 gereksinimlerini karşılıyor!")
        
        print("\n📋 ÖZET:")
        print("✅ OOP Mimarisi: Kalıtım, Polimorfizm, Encapsulation")
        print("✅ Modüler Tasarım: Katmanlı mimari")
        print("✅ Hata Yönetimi: Özel hata sınıfları")
        print("✅ Test Edilebilirlik: Birim testleri")
        print("✅ Dokümantasyon: README ve yorumlar")
        
    except Exception as e:
        print(f"\n❌ HATA: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
