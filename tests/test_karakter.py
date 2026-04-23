# test_karakter.py — Karakter Sınıfları Testleri

import unittest
import sys
import os

# Proje yolunu ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.karakter import Karakter, Supheli, Kurbun, Tanik, KarakterYoneticisi
from utils.hata_yonetimi import DedektifOyunuHatasi


class TestKarakter(unittest.TestCase):
    """Karakter temel sınıfı testleri."""
    
    def setUp(self):
        """Test öncesi hazırlık."""
        self.karakter = Supheli("Test Kullanıcı", "Test Rolü", False)
    
    def test_karakter_olusturma(self):
        """Karakter oluşturma testi."""
        self.assertEqual(self.karakter.isim, "Test Kullanıcı")
        self.assertEqual(self.karakter.rol, "Test Rolü")
        self.assertFalse(self.karakter.suclu)
    
    def test_encapsulation(self):
        """Encapsulation testi."""
        # Private attribute'a doğrudan erişim olmamalı
        with self.assertRaises(AttributeError):
            _ = self.karakter._isim
        
        # Getter metotları çalışmalı
        self.assertEqual(self.karakter.isim, "Test Kullanıcı")
    
    def test_deliller_ekleme(self):
        """Deliller ekleme testi."""
        yeni_deliller = ["Test Delil 1", "Test Delil 2"]
        self.karakter.deliller = yeni_deliller
        
        self.assertEqual(len(self.karakter.deliller), 2)
        self.assertIn("Test Delil 1", self.karakter.deliller)
    
    def test_gecersiz_deliller(self):
        """Geçersiz deliller testi."""
        with self.assertRaises(ValueError):
            self.karakter.deliller = "Bu bir liste değil"


class TestSupheli(unittest.TestCase):
    """Şüpheli sınıfı testleri."""
    
    def setUp(self):
        """Test öncesi hazırlık."""
        self.supheli = Supheli("Ahmet Yılmaz", "Müdür", True, "👤", "#FF0000")
    
    def test_supheli_olusturma(self):
        """Şüpheli oluşturma testi."""
        self.assertEqual(self.supheli.isim, "Ahmet Yılmaz")
        self.assertEqual(self.supheli.rol, "Müdür")
        self.assertTrue(self.supheli.suclu)
        self.assertEqual(self.supheli.emoji, "👤")
        self.assertEqual(self.supheli.renk, "#FF0000")
    
    def test_bilgi_ver(self):
        """Bilgi ver metodu testi."""
        bilgi = self.supheli.bilgi_ver()
        self.assertIn("Ahmet Yılmaz", bilgi)
        self.assertIn("Müdür", bilgi)
    
    def test_savunma_yap(self):
        """Savunma yap metodu testi."""
        savunma = self.supheli.savunma_yap()
        self.assertIsInstance(savunma, str)
        self.assertGreater(len(savunma), 0)


class TestKurbun(unittest.TestCase):
    """Kurban sınıfı testleri."""
    
    def setUp(self):
        """Test öncesi hazırlık."""
        self.kurban = Kurbun("Mehmet Kaya", "Güvenlik", "Silahla yaralanma")
    
    def test_kurban_olusturma(self):
        """Kurban oluşturma testi."""
        self.assertEqual(self.kurban.isim, "Mehmet Kaya")
        self.assertEqual(self.kurban.olum_sebebi, "Silahla yaralanma")
        self.assertFalse(self.kurban.suclu)  # Kurbanlar suçlu olamaz
    
    def test_bilgi_ver(self):
        """Bilgi ver metodu testi."""
        bilgi = self.kurban.bilgi_ver()
        self.assertIn("Mehmet Kaya", bilgi)
        self.assertIn("Silahla yaralanma", bilgi)


class TestTanik(unittest.TestCase):
    """Tanık sınıfı testleri."""
    
    def setUp(self):
        """Test öncesi hazırlık."""
        self.tanik = Tanik("Ayşe Demir", "Görgü Tanığı")
    
    def test_tanik_olusturma(self):
        """Tanık oluşturma testi."""
        self.assertEqual(self.tanik.isim, "Ayşe Demir")
        self.assertEqual(self.tanik.rol, "Görgü Tanığı")
        self.assertFalse(self.tanik.suclu)
    
    def test_ifade_ekle(self):
        """İfade ekleme testi."""
        self.tanik.ifade_ekle("Ses duydum")
        self.tanik.ifade_ekle("Gölge gördüm")
        
        ifadeler = self.tanik.ifadeler
        self.assertEqual(len(ifadeler), 2)
        self.assertIn("Ses duydum", ifadeler)
    
    def test_tum_ifadeler(self):
        """Tüm ifadeler metodu testi."""
        self.tanik.ifade_ekle("Test ifadesi")
        tum_ifadeler = self.tanik.tum_ifadeler()
        
        self.assertIn("Test ifadesi", tum_ifadeler)


class TestKarakterYoneticisi(unittest.TestCase):
    """Karakter yöneticisi testleri."""
    
    def setUp(self):
        """Test öncesi hazırlık."""
        self.yoneticisi = KarakterYoneticisi()
    
    def test_karakter_ekleme(self):
        """Karakter ekleme testi."""
        supheli = Supheli("Test Şüpheli", "Test Rolü")
        self.yoneticisi.karakter_ekle(supheli)
        
        self.assertEqual(self.yoneticisi.karakter_sayisi(), 1)
    
    def test_gecersiz_karakter_ekleme(self):
        """Geçersiz karakter ekleme testi."""
        with self.assertRaises(ValueError):
            self.yoneticisi.karakter_ekle("Bu bir karakter değil")
    
    def test_suphelileri_getir(self):
        """Şüphelileri getir testi."""
        supheli1 = Supheli("Şüpheli 1", "Rol 1")
        supheli2 = Supheli("Şüpheli 2", "Rol 2")
        kurban = Kurbun("Kurban", "Rol 3")
        
        self.yoneticisi.karakter_ekle(supheli1)
        self.yoneticisi.karakter_ekle(supheli2)
        self.yoneticisi.karakter_ekle(kurban)
        
        supheliler = self.yoneticisi.suphelileri_getir()
        self.assertEqual(len(supheliler), 2)
    
    def test_sucluyu_bul(self):
        """Suçluyu bul testi."""
        supheli1 = Supheli("Masum", "Rol 1", False)
        supheli2 = Supheli("Suçlu", "Rol 2", True)
        
        self.yoneticisi.karakter_ekle(supheli1)
        self.yoneticisi.karakter_ekle(supheli2)
        
        suclu = self.yoneticisi.sucluyu_bul()
        self.assertEqual(suclu.isim, "Suçlu")
        self.assertTrue(suclu.suclu)
    
    def test_tum_karakterleri_tanit(self):
        """Tüm karakterleri tanıt testi."""
        supheli = Supheli("Test Şüpheli", "Test Rolü")
        self.yoneticisi.karakter_ekle(supheli)
        
        tanitim = self.yoneticisi.tum_karakterleri_tanit()
        self.assertIn("Test Şüpheli", tanitim)
    
    def test_len_operator(self):
        """Len operator testi."""
        supheli = Supheli("Test", "Rol")
        self.yoneticisi.karakter_ekle(supheli)
        
        self.assertEqual(len(self.yoneticisi), 1)


if __name__ == '__main__':
    unittest.main()
