# run_tests.py — Test Çalıştırıcı

"""
Criminal Case: İstanbul Dosyaları - Test Çalıştırıcı

Bu script, tüm testleri çalıştırır ve sonuçları raporlar.
Kullanım: python run_tests.py
"""

import unittest
import sys
import os
from io import StringIO

# Proje yolunu ekle
proje_yolu = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, proje_yolu)

# Test modüllerini import et
from test_karakter import *
from test_delil_analiz import *


class TestSonucRaporlayici:
    """Test sonuçlarını raporlayan sınıf."""
    
    def __init__(self):
        self.toplam_test = 0
        self.basarili_test = 0
        self.basarisiz_test = 0
        self.hatalar = []
    
    def test_sonuclari_raporla(self, test_sonucu):
        """Test sonuçlarını raporlar."""
        self.toplam_test = test_sonucu.testsRun
        self.basarili_test = test_sonucu.testsRun - len(test_sonucu.failures) - len(test_sonucu.errors)
        self.basarisiz_test = len(test_sonucu.failures) + len(test_sonucu.errors)
        
        # Hataları kaydet
        for test, hata in test_sonucu.failures + test_sonucu.errors:
            self.hatalar.append(f"{test}: {hata}")
    
    def ozet_raporu_yazdir(self):
        """Özet rapor yazdırır."""
        print("\n" + "="*60)
        print("🧪 TEST SONUÇLARI ÖZETİ")
        print("="*60)
        print(f"📊 Toplam Test: {self.toplam_test}")
        print(f"✅ Başarılı: {self.basarili_test}")
        print(f"❌ Başarısız: {self.basarisiz_test}")
        
        if self.basarili_test > 0:
            yuzde = (self.basarili_test / self.toplam_test) * 100
            print(f"📈 Başarı Oranı: %{yuzde:.1f}")
        
        if self.hatalar:
            print(f"\n❌ HATALAR ({len(self.hatalar)}):")
            for i, hata in enumerate(self.hatalar[:5], 1):  # İlk 5 hata
                print(f"{i}. {hata.split(':')[0]}")
            
            if len(self.hatalar) > 5:
                print(f"... ve {len(self.hatalar) - 5} hata daha")
        
        print("="*60)


def tum_testleri_calistir():
    """Tüm testleri çalıştırır."""
    print("🚀 Criminal Case: İstanbul Dosyaları - Testler Başlıyor...")
    print("="*60)
    
    # Test suite oluştur
    test_suite = unittest.TestSuite()
    
    # Test modüllerini ekle
    test_modules = [
        'test_karakter',
        'test_delil_analiz'
    ]
    
    for module_name in test_modules:
        try:
            print(f"📂 {module_name} modülü yükleniyor...")
            module = __import__(module_name)
            test_suite.addTest(unittest.TestLoader().loadTestsFromModule(module))
            print(f"✅ {module_name} yüklendi")
        except Exception as e:
            print(f"❌ {module_name} yüklenemedi: {e}")
    
    # Testleri çalıştır
    print("\n🧪 Testler çalıştırılıyor...")
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    sonuc = runner.run(test_suite)
    
    # Sonuçları raporla
    raporlayici = TestSonucRaporlayici()
    raporlayici.test_sonuclari_raporla(sonuc)
    raporlayici.ozet_raporu_yazdir()
    
    # Başarı durumunu döndür
    return sonuc.wasSuccessful()


def ozel_test_calistir(test_adi):
    """Belirli bir testi çalıştırır."""
    print(f"🎯 {test_adi} testi çalıştırılıyor...")
    
    try:
        suite = unittest.TestLoader().loadTestsFromName(test_adi)
        runner = unittest.TextTestRunner(verbosity=2)
        sonuc = runner.run(suite)
        
        if sonuc.wasSuccessful():
            print(f"✅ {test_adi} başarılı!")
        else:
            print(f"❌ {test_adi} başarısız!")
        
        return sonuc.wasSuccessful()
    
    except Exception as e:
        print(f"❌ Test çalıştırma hatası: {e}")
        return False


def main():
    """Ana fonksiyon."""
    if len(sys.argv) > 1:
        # Belirli bir test çalıştır
        test_adi = sys.argv[1]
        ozel_test_calistir(test_adi)
    else:
        # Tüm testleri çalıştır
        basarili = tum_testleri_calistir()
        
        if basarili:
            print("\n🎉 TÜM TESTLER BAŞARILI!")
            print("Proje BGT 132 gereksinimlerini karşılıyor! ✅")
        else:
            print("\n⚠️ BAZI TESTLER BAŞARISIZ!")
            print("Lütfen hataları düzeltin ve tekrar deneyin.")
        
        return 0 if basarili else 1


if __name__ == '__main__':
    sys.exit(main())
