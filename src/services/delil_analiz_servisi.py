# delil_analiz_servisi.py — Delil Analiz Servisi Sınıfı

import random
import time
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod

# Base Class - Soyut Analiz Sınıfı
class AnalizYontemi(ABC):
    """
    Tüm analiz yöntemleri için temel arayüz.
    Polimorfizm örneği: Her analiz yöntemi aynı arayüzü farklı şekilde uygular.
    """
    
    def __init__(self, isim: str, sure: int = 3):
        self._isim = isim
        self._sure = sure  # Analiz süresi (saniye)
    
    @property
    def isim(self) -> str:
        return self._isim
    
    @property
    def sure(self) -> int:
        return self._sure
    
    @abstractmethod
    def analiz_et(self, delil: str) -> Dict[str, str]:
        """Delili analiz eder ve sonuç döndürür."""
        pass
    
    @abstractmethod
    def basari_orani(self) -> float:
        """Analiz başarısını döndürür (0.0 - 1.0)."""
        pass


# Somut Analiz Sınıfları
class ParmakIziAnalizi(AnalizYontemi):
    """Parmak izi analiz sınıfı."""
    
    def __init__(self):
        super().__init__("Parmak İzi Analizi", 4)
    
    def analiz_et(self, delil: str) -> Dict[str, str]:
        """Parmak izi analizini simüle eder."""
        sonuclar = [
            "Parmak izi Mert Demir'e ait!",
            "Parmak izi Selma Koç'a ait!",
            "Parmak izi Dr. Şahin'e ait!",
            "Parmak izi veritabanında bulunamadı."
        ]
        
        sonuc = random.choice(sonuclar)
        detay = f"🔬 {self._isim} tamamlandı.\n📋 Sonuç: {sonuc}\n⏱️ Analiz süresi: {self._sure} saniye"
        
        return {
            "sonuc": sonuc,
            "detay": detay,
            "yontem": self._isim,
            "basari": "Başarılı" if "ait" in sonuc else "Kısmi Başarılı"
        }
    
    def basari_orani(self) -> float:
        return 0.85


class DNAAnalizi(AnalizYontemi):
    """DNA analiz sınıfı."""
    
    def __init__(self):
        super().__init__("DNA Analizi", 6)
    
    def analiz_et(self, delil: str) -> Dict[str, str]:
        """DNA analizini simüle eder."""
        sonuclar = [
            "DNA profili şüpheliyle eşleşiyor!",
            "DNA profili veritabanında kayıtlı değil.",
            "DNA örneği bozuk, analiz edilemiyor.",
            "DNA profili üçüncü bir kişiye ait!"
        ]
        
        sonuc = random.choice(sonuclar)
        detay = f"🧬 {self._isim} tamamlandı.\n📋 Sonuç: {sonuc}\n⏱️ Analiz süresi: {self._sure} saniye"
        
        return {
            "sonuc": sonuc,
            "detay": detay,
            "yontem": self._isim,
            "basari": "Başarılı" if "eşleşiyor" in sonuc else "Başarısız"
        }
    
    def basari_orani(self) -> float:
        return 0.90


class KimyasalAnaliz(AnalizYontemi):
    """Kimyasal analiz sınıfı."""
    
    def __init__(self):
        super().__init__("Kimyasal Analiz", 3)
    
    def analiz_et(self, delil: str) -> Dict[str, str]:
        """Kimyasal analizini simüle eder."""
        sonuclar = [
            "Mavi boya tespit edildi - restoratör işareti!",
            "Mor kimyasal madde - laboratuvar malzemesi!",
            "Yeşil mürekkep - gümrük müührü izi!",
            "Kırmızı kan lekesi - A grubu kan!"
        ]
        
        sonuc = random.choice(sonuclar)
        detay = f"⚗️ {self._isim} tamamlandı.\n📋 Sonuç: {sonuc}\n⏱️ Analiz süresi: {self._sure} saniye"
        
        return {
            "sonuc": sonuc,
            "detay": detay,
            "yontem": self._isim,
            "basari": "Başarılı"
        }
    
    def basari_orani(self) -> float:
        return 0.75


class DelilAnalizServisi:
    """
    Delil analiz servis sınıfı.
    OOP prensipleri: Encapsulation, Polimorphism, Composition
    """
    
    def __init__(self):
        self._analiz_yontemleri: List[AnalizYontemi] = []
        self._analiz_gecmisi: List[Dict] = []
        self._mevcut_analiz: Optional[Dict] = None
        self._analiz_sayaci = 0
        
        # Varsayılan analiz yöntemlerini ekle
        self._varsayilan_yontemleri_ekle()
    
    def _varsayilan_yontemleri_ekle(self):
        """Varsayılan analiz yöntemlerini ekler."""
        self._analiz_yontemleri.extend([
            ParmakIziAnalizi(),
            DNAAnalizi(),
            KimyasalAnaliz()
        ])
    
    def analiz_yontemi_ekle(self, yontem: AnalizYontemi):
        """Yeni analiz yöntemi ekler."""
        if isinstance(yontem, AnalizYontemi):
            self._analiz_yontemleri.append(yontem)
        else:
            raise ValueError("Sadece AnalizYontemi tipindeki nesneler eklenebilir!")
    
    def analiz_yontemlerini_getir(self) -> List[str]:
        """Mevcut analiz yöntemlerinin isimlerini döndürür."""
        return [yontem.isim for yontem in self._analiz_yontemleri]
    
    def delil_analiz_et(self, delil: str, yontem_index: int = None) -> bool:
        """
        Delili analiz eder.
        
        Args:
            delil: Analiz edilecek delil
            yontem_index: Kullanılacak analiz yönteminin indeksi
            
        Returns:
            bool: Analiz başarılı mı?
        """
        try:
            if not delil or not isinstance(delil, str):
                raise ValueError("Geçersiz delil!")
            
            # Yöntem seçimi
            if yontem_index is None:
                yontem = random.choice(self._analiz_yontemleri)
            else:
                if 0 <= yontem_index < len(self._analiz_yontemleri):
                    yontem = self._analiz_yontemleri[yontem_index]
                else:
                    raise ValueError("Geçersiz yöntem indeksi!")
            
            # Analiz başlat
            self._mevcut_analiz = {
                "delil": delil,
                "yontem": yontem.isim,
                "baslangic_zamani": time.time(),
                "durum": "devam_ediyor"
            }
            
            # Analiz simülasyonu (gerçek uygulamada async olurdu)
            time.sleep(1)  # Simülasyon için kısa bekleme
            
            # Analiz sonuçları
            analiz_sonucu = yontem.analiz_et(delil)
            
            # Analiz kaydını güncelle
            self._mevcut_analiz.update({
                "sonuc": analiz_sonucu,
                "bitis_zamani": time.time(),
                "durum": "tamamlandi"
            })
            
            # Analiz geçmişine ekle
            self._analiz_gecmisi.append(self._mevcut_analiz.copy())
            self._analiz_sayaci += 1
            
            return True
            
        except Exception as e:
            if self._mevcut_analiz:
                self._mevcut_analiz["durum"] = "hata"
                self._mevcut_analiz["hata"] = str(e)
            print(f"Analiz hatası: {e}")
            return False
        finally:
            self._mevcut_analiz = None
    
    def analiz_sonucu_getir(self) -> Optional[Dict]:
        """Son analiz sonucunu döndürür."""
        if self._analiz_gecmisi:
            return self._analiz_gecmisi[-1]
        return None
    
    def analiz_gecmisini_getir(self) -> List[Dict]:
        """Tüm analiz geçmişini döndürür."""
        return self._analiz_gecmisi.copy()
    
    def mevcut_analiz_durumu(self) -> Optional[str]:
        """Mevcut analiz durumunu döndürür."""
        if self._mevcut_analiz:
            return self._mevcut_analiz.get("durum")
        return None
    
    def analiz_istatistikleri(self) -> Dict[str, int]:
        """Analiz istatistiklerini döndürür."""
        stats = {
            "toplam_analiz": len(self._analiz_gecmisi),
            "basarili_analiz": 0,
            "basarisiz_analiz": 0
        }
        
        for analiz in self._analiz_gecmisi:
            if analiz.get("durum") == "tamamlandi":
                stats["basarili_analiz"] += 1
            else:
                stats["basarisiz_analiz"] += 1
        
        return stats
    
    def temizle(self):
        """Analiz geçmişini temizler."""
        self._analiz_gecmisi.clear()
        self._mevcut_analiz = None
        self._analiz_sayaci = 0
    
    def __len__(self) -> int:
        """Toplam analiz sayısını döndürür."""
        return len(self._analiz_gecmisi)
