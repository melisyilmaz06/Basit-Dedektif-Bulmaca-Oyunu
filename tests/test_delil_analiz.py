# test_delil_analiz.py — Delil Analiz Servisi Testleri

import unittest
import sys
import os
import time

# Proje yolunu ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.delil_analiz_servisi import (
    DelilAnalizServisi, ParmakIziAnalizi, DNAAnalizi, 
    KimyasalAnaliz, AnalizYontemi
)


class TestAnalizYontemleri(unittest.TestCase):
    """Analiz yöntemleri testleri."""
    
    def test_parmak_izi_analizi(self):
        """Parmak izi analizi testi."""
        analiz = ParmakIziAnalizi()
        
        self.assertEqual(analiz.isim, "Parmak İzi Analizi")
        self.assertEqual(analiz.sure, 4)
        self.assertGreater(analiz.basari_orani(), 0)
        
        sonuc = analiz.analiz_et("Test Delili")
        self.assertIn("sonuc", sonuc)
        self.assertIn("detay", sonuc)
        self.assertIn("yontem", sonuc)
        self.assertIn("basari", sonuc)
    
    def test_dna_analizi(self):
        """DNA analizi testi."""
        analiz = DNAAnalizi()
        
        self.assertEqual(analiz.isim, "DNA Analizi")
        self.assertEqual(analiz.sure, 6)
        self.assertGreater(analiz.basari_orani(), 0)
        
        sonuc = analiz.analiz_et("Test DNA Örneği")
        self.assertIn("DNA", sonuc["detay"])
    
    def test_kimyasal_analiz(self):
        """Kimyasal analiz testi."""
        analiz = KimyasalAnaliz()
        
        self.assertEqual(analiz.isim, "Kimyasal Analiz")
        self.assertEqual(analiz.sure, 3)
        self.assertGreater(analiz.basari_orani(), 0)
        
        sonuc = analiz.analiz_et("Test Kimyasal")
        self.assertIn("⚗️", sonuc["detay"])


class TestDelilAnalizServisi(unittest.TestCase):
    """Delil analiz servisi testleri."""
    
    def setUp(self):
        """Test öncesi hazırlık."""
        self.servis = DelilAnalizServisi()
    
    def test_servis_olusturma(self):
        """Servis oluşturma testi."""
        self.assertIsNotNone(self.servis)
        self.assertGreater(len(self.servis.analiz_yontemlerini_getir()), 0)
    
    def test_analiz_yontemi_ekleme(self):
        """Analiz yöntemi ekleme testi."""
        # Özel analiz yöntemi oluştur
        class TestAnaliz(AnalizYontemi):
            def analiz_et(self, delil):
                return {"sonuc": "Test sonucu", "detay": "Test detayı"}
            
            def basari_orani(self):
                return 1.0
        
        test_analiz = TestAnaliz("Test Analizi", 2)
        self.servis.analiz_yontemi_ekle(test_analiz)
        
        yontemler = self.servis.analiz_yontemlerini_getir()
        self.assertIn("Test Analizi", yontemler)
    
    def test_gecersiz_yontem_ekleme(self):
        """Geçersiz yöntem ekleme testi."""
        with self.assertRaises(ValueError):
            self.servis.analiz_yontemi_ekle("Bu bir yöntem değil")
    
    def test_delil_analiz_et(self):
        """Delil analiz etme testi."""
        basari = self.servis.delil_analiz_et("Test Delili")
        self.assertTrue(basari)
        
        sonuc = self.servis.analiz_sonucu_getir()
        self.assertIsNotNone(sonuc)
        self.assertEqual(sonuc["delil"], "Test Delili")
    
    def test_belirli_yontemle_analiz(self):
        """Belirli yöntemle analiz testi."""
        # İlk yöntemle analiz yap
        basari = self.servis.delil_analiz_et("Test Delili", 0)
        self.assertTrue(basari)
        
        sonuc = self.servis.analiz_sonucu_getir()
        self.assertIsNotNone(sonuc)
    
    def test_gecersiz_yontem_indeksi(self):
        """Geçersiz yöntem indeksi testi."""
        basari = self.servis.delil_analiz_et("Test Delili", 999)
        self.assertFalse(basari)
    
    def test_gecersiz_delil(self):
        """Geçersiz delil testi."""
        basari = self.servis.delil_analiz_et("")
        self.assertFalse(basari)
        
        basari = self.servis.delil_analiz_et(None)
        self.assertFalse(basari)
    
    def test_analiz_gecmisi(self):
        """Analiz geçmişi testi."""
        # Birkaç analiz yap
        self.servis.delil_analiz_et("Delil 1")
        self.servis.delil_analiz_et("Delil 2")
        
        gecmis = self.servis.analiz_gecmisini_getir()
        self.assertEqual(len(gecmis), 2)
        
        # Son analiz sonucunu kontrol et
        son_analiz = self.servis.analiz_sonucu_getir()
        self.assertEqual(son_analiz["delil"], "Delil 2")
    
    def test_mevcut_analiz_durumu(self):
        """Mevcut analiz durumu testi."""
        # Analiz başlamadan önce
        durum = self.servis.mevcut_analiz_durumu()
        self.assertIsNone(durum)
        
        # Analiz sırasında (simüle edilmiş)
        # Not: Gerçek uygulamada bu async olurdu
        # Burada sadece sonucu kontrol ediyoruz
    
    def test_analiz_istatistikleri(self):
        """Analiz istatistikleri testi."""
        # Başarılı analiz
        self.servis.delil_analiz_et("Başarılı Delil")
        
        # Başarısız analiz
        basari = self.servis.delil_analiz_et("", 0)
        self.assertFalse(basari)
        
        stats = self.servis.analiz_istatistikleri()
        self.assertGreater(stats["toplam_analiz"], 0)
        self.assertIn("basarili_analiz", stats)
        self.assertIn("basarisiz_analiz", stats)
    
    def test_temizle(self):
        """Temizleme testi."""
        # Analiz yap
        self.servis.delil_analiz_et("Test Delil")
        self.assertGreater(len(self.servis.analiz_gecmisini_getir()), 0)
        
        # Temizle
        self.servis.temizle()
        self.assertEqual(len(self.servis.analiz_gecmisini_getir()), 0)
        self.assertEqual(len(self.servis), 0)
    
    def test_len_operator(self):
        """Len operator testi."""
        # Başlangıçta boş olmalı
        self.assertEqual(len(self.servis), 0)
        
        # Analiz yap
        self.servis.delil_analiz_et("Test Delil")
        self.assertEqual(len(self.servis), 1)
        
        # Temizle
        self.servis.temizle()
        self.assertEqual(len(self.servis), 0)


class TestAnalizSonuclari(unittest.TestCase):
    """Analiz sonuçları testleri."""
    
    def setUp(self):
        """Test öncesi hazırlık."""
        self.servis = DelilAnalizServisi()
    
    def test_sonuc_yapisi(self):
        """Analiz sonucu yapısı testi."""
        self.servis.delil_analiz_et("Test Delili")
        sonuc = self.servis.analiz_sonucu_getir()
        
        # Gerekli alanları kontrol et
        gerekli_alanlar = ["delil", "yontem", "sonuc", "detay", "basari"]
        for alan in gerekli_alanlar:
            self.assertIn(alan, sonuc)
    
    def test_farkli_deliller(self):
        """Farklı delillerle analiz testi."""
        deliller = [
            "🔍 Kırık Cam Parçası",
            "🩸 Kan Lekesi", 
            "👆 Parmak İzi",
            "🎨 Mavi Boya Tüpü"
        ]
        
        for delil in deliller:
            basari = self.servis.delil_analiz_et(delil)
            self.assertTrue(basari)
            
            sonuc = self.servis.analiz_sonucu_getir()
            self.assertEqual(sonuc["delil"], delil)
            self.assertIsNotNone(sonuc["sonuc"])


if __name__ == '__main__':
    unittest.main()
