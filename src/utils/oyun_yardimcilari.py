# oyun_yardimcilari.py — Oyun Yardımcı Fonksiyonları

import json
import os
import random
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib

from .hata_yonetimi import hata_yakala, VeriYuklemeHatasi, logger


class VeriYoneticisi:
    """
    Veri yönetimi için yardımcı sınıf.
    JSON dosyalarını okur, yazar ve doğrular.
    """
    
    def __init__(self, veri_dizini: str = "data"):
        self.veri_dizini = veri_dizini
        self._veri_oznbellek: Dict[str, Any] = {}
    
    def json_oku(self, dosya_adi: str, oznbellek_kullan: bool = True) -> Dict[str, Any]:
        """
        JSON dosyasını okur.
        
        Args:
            dosya_adi: Okunacak dosya adı
            oznbellek_kullan: Önbellek kullanılsın mı
            
        Returns:
            Dict: JSON verisi
            
        Raises:
            VeriYuklemeHatasi: Dosya okunamazsa
        """
        try:
            dosya_yolu = os.path.join(self.veri_dizini, dosya_adi)
            
            # Önbellek kontrolü
            if oznbellek_kullan and dosya_adi in self._veri_oznbellek:
                logger.debug(f"Veri önbellekten alındı: {dosya_adi}")
                return self._veri_oznbellek[dosya_adi]
            
            if not os.path.exists(dosya_yolu):
                raise VeriYuklemeHatasi(f"Dosya bulunamadı: {dosya_yolu}", dosya_yolu)
            
            with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
                veri = json.load(dosya)
            
            # Önbelleğe ekle
            if oznbellek_kullan:
                self._veri_oznbellek[dosya_adi] = veri
            
            logger.info(f"Veri yüklendi: {dosya_adi}")
            return veri
            
        except json.JSONDecodeError as e:
            raise VeriYuklemeHatasi(f"JSON format hatası: {str(e)}", dosya_yolu)
        except Exception as e:
            raise VeriYuklemeHatasi(f"Dosya okuma hatası: {str(e)}", dosya_yolu)
    
    def json_yaz(self, dosya_adi: str, veri: Dict[str, Any], girinti: int = 2) -> bool:
        """
        JSON dosyasına yazar.
        
        Args:
            dosya_adi: Yazılacak dosya adı
            veri: Yazılacak veri
            girinti: JSON girinti seviyesi
            
        Returns:
            bool: Başarılı mı?
        """
        try:
            dosya_yolu = os.path.join(self.veri_dizini, dosya_adi)
            
            # Dizin yoksa oluştur
            os.makedirs(os.path.dirname(dosya_yolu), exist_ok=True)
            
            with open(dosya_yolu, 'w', encoding='utf-8') as dosya:
                json.dump(veri, dosya, ensure_ascii=False, indent=girinti)
            
            # Önbelleği güncelle
            self._veri_oznbellek[dosya_adi] = veri
            
            logger.info(f"Veri kaydedildi: {dosya_adi}")
            return True
            
        except Exception as e:
            logger.error(f"Veri yazma hatası: {str(e)}")
            return False
    
    def oznbellek_temizle(self):
        """Veri önbelleğini temizler."""
        self._veri_oznbellek.clear()
        logger.debug("Veri önbelleği temizlendi")


class OyunYardimcisi:
    """
    Oyun için genel yardımcı fonksiyonlar.
    """
    
    @staticmethod
    def rastgele_secim(secenekler: List[Any], adet: int = 1) -> List[Any]:
        """
        Listeden rastgele seçim yapar.
        
        Args:
            secenekler: Seçenek listesi
            adet: Seçilecek eleman sayısı
            
        Returns:
            List: Seçilen elemanlar
        """
        if not secenekler:
            return []
        
        adet = min(adet, len(secenekler))
        return random.sample(secenekler, adet)
    
    @staticmethod
    def yuzde_hesapla(bolen: int, bolunen: int) -> float:
        """
        Yüzde hesaplar.
        
        Args:
            bolen: Bölünen
            bolunen: Bölen
            
        Returns:
            float: Yüzde
        """
        if bolunen == 0:
            return 0.0
        return (bolen / bolunen) * 100
    
    @staticmethod
    def zaman_farki_hesapla(baslangic_zamani: float) -> str:
        """
        Zaman farkını hesaplar ve formatlar.
        
        Args:
            baslangic_zamani: Başlangıç zamanı (timestamp)
            
        Returns:
            str: Formatlanmış zaman farkı
        """
        fark = time.time() - baslangic_zamani
        
        if fark < 60:
            return f"{fark:.1f} saniye"
        elif fark < 3600:
            return f"{fark/60:.1f} dakika"
        else:
            return f"{fark/3600:.1f} saat"
    
    @staticmethod
    def metin_kisalt(metin: str, max_uzunluk: int = 50, son_ek: str = "...") -> str:
        """
        Metni kısaltır.
        
        Args:
            metin: Kısaltılacak metin
            max_uzunluk: Maksimum uzunluk
            son_ek: Son ek
            
        Returns:
            str: Kısaltılmış metin
        """
        if len(metin) <= max_uzunluk:
            return metin
        
        return metin[:max_uzunluk - len(son_ek)] + son_ek
    
    @staticmethod
    def skor_hesapla(bulunan_deliller: int, toplam_delil: int, 
                    analiz_edilenler: int, zaman_bonus: float = 0) -> int:
        """
        Oyun skorunu hesaplar.
        
        Args:
            bulunan_deliller: Bulunan delil sayısı
            toplam_delil: Toplam delil sayısı
            analiz_edilenler: Analiz edilen delil sayısı
            zaman_bonus: Zaman bonusu
            
        Returns:
            int: Hesaplanan skor
        """
        # Delil bulma skoru
        delil_skoru = (bulunan_deliller / max(toplam_delil, 1)) * 100
        
        # Analiz skoru
        analiz_skoru = analiz_edilenler * 20
        
        # Zaman bonusu
        zaman_skoru = int(zaman_bonus)
        
        # Toplam skor
        toplam_skor = int(delil_skoru + analiz_skoru + zaman_skoru)
        
        return max(0, toplam_skor)
    
    @staticmethod
    def yildiz_hesapla(skor: int, max_skor: int = 300) -> int:
        """
        Skora göre yıldız sayısını hesaplar.
        
        Args:
            skor: Oyuncu skoru
            max_skor: Maksimum skor
            
        Returns:
            int: Yıldız sayısı (1-3)
        """
        yuzde = OyunYardimcisi.yuzde_hesapla(skor, max_skor)
        
        if yuzde >= 80:
            return 3
        elif yuzde >= 50:
            return 2
        else:
            return 1


class DosyaYoneticisi:
    """
    Dosya işlemleri için yardımcı sınıf.
    """
    
    @staticmethod
    def dosya_var_mi(dosya_yolu: str) -> bool:
        """Dosyanın var olup olmadığını kontrol eder."""
        return os.path.exists(dosya_yolu)
    
    @staticmethod
    def dizin_olustur(dizin_yolu: str) -> bool:
        """Dizin oluşturur."""
        try:
            os.makedirs(dizin_yolu, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Dizin oluşturma hatası: {str(e)}")
            return False
    
    @staticmethod
    def dosya_hash_hesapla(dosya_yolu: str) -> Optional[str]:
        """
        Dosyanın MD5 hash'ini hesaplar.
        
        Args:
            dosya_yolu: Dosya yolu
            
        Returns:
            str: MD5 hash
        """
        try:
            hash_md5 = hashlib.md5()
            with open(dosya_yolu, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Hash hesaplama hatası: {str(e)}")
            return None
    
    @staticmethod
    def kayit_dosyasi_olustur(oyuncu_adi: str, skor: int, 
                            bolum: int, yildiz: int) -> str:
        """
        Kayıt dosyası adı oluşturur.
        
        Args:
            oyuncu_adi: Oyuncu adı
            skor: Skor
            bolum: Bölüm
            yildiz: Yıldız
            
        Returns:
            str: Dosya adı
        """
        zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
        temiz_oyuncu_adi = "".join(c for c in oyuncu_adi if c.isalnum() or c in (' ', '-')).rstrip()
        
        return f"kayit_{temiz_oyuncu_adi}_{zaman_damgasi}_B{bolum}_S{skor}_Y{yildiz}.json"


class ValidasyonYardimcisi:
    """
    Veri doğrulama yardımcı sınıfı.
    """
    
    @staticmethod
    def metin_dogrula(metin: str, min_uzunluk: int = 1, 
                     max_uzunluk: int = 100) -> Tuple[bool, str]:
        """
        Metin doğrular.
        
        Args:
            metin: Doğrulanacak metin
            min_uzunluk: Minimum uzunluk
            max_uzunluk: Maksimum uzunluk
            
        Returns:
            Tuple: (Geçerli mi?, Hata mesajı)
        """
        if not isinstance(metin, str):
            return False, "Metin olmalıdır"
        
        if len(metin) < min_uzunluk:
            return False, f"En az {min_uzunluk} karakter olmalıdır"
        
        if len(metin) > max_uzunluk:
            return False, f"En fazla {max_uzunluk} karakter olabilir"
        
        return True, ""
    
    @staticmethod
    def sayi_dogrula(sayi: Any, min_deger: int = 0, 
                    max_deger: int = 1000) -> Tuple[bool, str]:
        """
        Sayı doğrular.
        
        Args:
            sayi: Doğrulanacak sayı
            min_deger: Minimum değer
            max_deger: Maksimum değer
            
        Returns:
            Tuple: (Geçerli mi?, Hata mesajı)
        """
        try:
            sayi = int(sayi)
        except (ValueError, TypeError):
            return False, "Sayı olmalıdır"
        
        if sayi < min_deger:
            return False, f"En az {min_deger} olmalıdır"
        
        if sayi > max_deger:
            return False, f"En fazla {max_deger} olabilir"
        
        return True, ""
    
    @staticmethod
    def liste_dogrula(liste: Any, min_uzunluk: int = 0, 
                     max_uzunluk: int = 100) -> Tuple[bool, str]:
        """
        Liste doğrular.
        
        Args:
            liste: Doğrulanacak liste
            min_uzunluk: Minimum uzunluk
            max_uzunluk: Maksimum uzunluk
            
        Returns:
            Tuple: (Geçerli mi?, Hata mesajı)
        """
        if not isinstance(liste, list):
            return False, "Liste olmalıdır"
        
        if len(liste) < min_uzunluk:
            return False, f"En az {min_uzunluk} eleman olmalıdır"
        
        if len(liste) > max_uzunluk:
            return False, f"En fazla {max_uzunluk} eleman olabilir"
        
        return True, ""


# Global yardımcı nesneler
veri_yoneticisi = VeriYoneticisi()
oyun_yardimcisi = OyunYardimcisi()
dosya_yoneticisi = DosyaYoneticisi()
validasyon_yardimcisi = ValidasyonYardimcisi()
