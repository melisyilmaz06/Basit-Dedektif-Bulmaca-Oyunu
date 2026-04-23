# hata_yonetimi.py — Hata Yönetimi ve Loglama Sistemi

import logging
import traceback
from datetime import datetime
from typing import Optional, Dict, Any
from functools import wraps
import os

# Loglama ayarları
class Logger:
    """
    Loglama sınıfı. Singleton pattern kullanır.
    Tüm uygulama genelinde loglama işlemlerini yönetir.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.logger = logging.getLogger("DedektifOyunu")
        self.logger.setLevel(logging.DEBUG)
        
        # Log dosyası oluştur
        log_dosyasi = "logs/game.log"
        os.makedirs(os.path.dirname(log_dosyasi), exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(log_dosyasi, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Handler'ları ekle
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, mesaj: str):
        self.logger.debug(mesaj)
    
    def info(self, mesaj: str):
        self.logger.info(mesaj)
    
    def warning(self, mesaj: str):
        self.logger.warning(mesaj)
    
    def error(self, mesaj: str):
        self.logger.error(mesaj)
    
    def critical(self, mesaj: str):
        self.logger.critical(mesaj)


# Global logger instance
logger = Logger()


# Özel Hata Sınıfları
class DedektifOyunuHatasi(Exception):
    """Dedektif oyunu temel hata sınıfı."""
    
    def __init__(self, mesaj: str, hata_kodu: str = None):
        super().__init__(mesaj)
        self.mesaj = mesaj
        self.hata_kodu = hata_kodu
        self.zaman = datetime.now()
        logger.error(f"DedektifOyunuHatasi: {mesaj} (Kod: {hata_kodu})")


class VeriYuklemeHatasi(DedektifOyunuHatasi):
    """Veri yükleme hatası için özel sınıf."""
    
    def __init__(self, mesaj: str, dosya_yolu: str = None):
        super().__init__(mesaj, "VERI_YUKLEME_HATASI")
        self.dosya_yolu = dosya_yolu


class OyunDurumHatasi(DedektifOyunuHatasi):
    """Oyun durumu hatası için özel sınıf."""
    
    def __init__(self, mesaj: str, mevcut_durum: str = None):
        super().__init__(mesaj, "OYUN_DURUM_HATASI")
        self.mevcut_durum = mevcut_durum


class AnalizHatasi(DedektifOyunuHatasi):
    """Analiz hatası için özel sınıf."""
    
    def __init__(self, mesaj: str, delil: str = None, yontem: str = None):
        super().__init__(mesaj, "ANALIZ_HATASI")
        self.delil = delil
        self.yontem = yontem


class UIHatasi(DedektifOyunuHatasi):
    """Kullanıcı arayüzü hatası için özel sınıf."""
    
    def __init__(self, mesaj: str, widget: str = None):
        super().__init__(mesaj, "UI_HATASI")
        self.widget = widget


# Hata Yönetimi Decorator'ları
def hata_yakala(hata_tipi: type = Exception, logla: bool = True, varsayilan_deger=None):
    """
    Hata yakalama decorator'ı.
    
    Args:
        hata_tipi: Yakalanacak hata tipi
        logla: Hata loglansın mı?
        varsayilan_deger: Hata durumunda döndürülecek değer
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except hata_tipi as e:
                if logla:
                    logger.error(f"Fonksiyon {func.__name__} hata verdi: {str(e)}")
                    logger.debug(f"Traceback: {traceback.format_exc()}")
                return varsayilan_deger
        return wrapper
    return decorator


def oyun_durumu_kontrolu(gerekli_durum: str):
    """
    Oyun durumu kontrolü decorator'ı.
    
    Args:
        gerekli_durum: Gerekli oyun durumu
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, 'oyun_durumu'):
                if self.oyun_durumu != gerekli_durum:
                    raise OyunDurumHatasi(
                        f"Bu işlem için oyun durumu '{gerekli_durum}' olmalıdır. "
                        f"Mevcut durum: '{self.oyun_durumu}'"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def parametre_kontrolu(**parametreler):
    """
    Parametre kontrolü decorator'ı.
    
    Args:
        parametreler: Kontrol edilecek parametreler ve tipleri
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Fonksiyon parametrelerini al
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Parametreleri kontrol et
            for param, tip in parametreler.items():
                if param in bound_args.arguments:
                    deger = bound_args.arguments[param]
                    if not isinstance(deger, tip):
                        raise ValueError(
                            f"Parametre '{param}' {tip.__name__} tipinde olmalı, "
                            f"ancak {type(deger).__name__} tipinde verildi"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Hata Raporlama Sistemi
class HataRaporlayici:
    """Hata raporlama ve takip sistemi."""
    
    def __init__(self):
        self._hata_raporlari: List[Dict[str, Any]] = []
        self.logger = Logger()
    
    def hata_raporla(self, hata: Exception, ek_bilgiler: Dict = None):
        """
        Hata raporlar.
        
        Args:
            hata: Oluşan hata
            ek_bilgiler: Ek bilgiler
        """
        rapor = {
            "zaman": datetime.now().isoformat(),
            "hata_tipi": type(hata).__name__,
            "mesaj": str(hata),
            "traceback": traceback.format_exc(),
            "ek_bilgiler": ek_bilgiler or {}
        }
        
        # Özel hata sınıfları için ek bilgiler
        if isinstance(hata, DedektifOyunuHatasi):
            rapor.update({
                "hata_kodu": hata.hata_kodu,
                "olusma_zamani": hata.zaman.isoformat()
            })
        
        self._hata_raporlari.append(rapor)
        self.logger.error(f"Hata raporlandı: {rapor['mesaj']}")
    
    def hata_raporlarini_getir(self, son_n: int = None) -> List[Dict]:
        """
        Hata raporlarını döndürür.
        
        Args:
            son_n: Son n raporu döndürür
        """
        if son_n:
            return self._hata_raporlari[-son_n:]
        return self._hata_raporlari.copy()
    
    def raporlari_temizle(self):
        """Tüm raporları temizler."""
        self._hata_raporlari.clear()
        self.logger.info("Hata raporları temizlendi")
    
    def istatistikler(self) -> Dict[str, int]:
        """Hata istatistiklerini döndürür."""
        stats = {}
        for rapor in self._hata_raporlari:
            hata_tipi = rapor["hata_tipi"]
            stats[hata_tipi] = stats.get(hata_tipi, 0) + 1
        return stats


# Global hata raporlayıcı
hata_raporlayici = HataRaporlayici()


# Genel hata yakalama fonksiyonu
def guvenli_calistir(func, *args, varsayilan_deger=None, hata_mesaji: str = None, **kwargs):
    """
    Fonksiyonu güvenli bir şekilde çalıştırır.
    
    Args:
        func: Çalıştırılacak fonksiyon
        varsayilan_deger: Hata durumunda döndürülecek değer
        hata_mesaji: Özel hata mesajı
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if hata_mesaji:
            logger.error(f"{hata_mesaji}: {str(e)}")
        else:
            logger.error(f"Fonksiyon {func.__name__} hata verdi: {str(e)}")
        
        hata_raporlayici.hata_raporla(e)
        return varsayilan_deger


# Kullanıcı için hata mesajı formatlayıcı
def kullanicicasi_hata_mesaji(hata: Exception) -> str:
    """
    Teknik hatayı kullanıcı dostu mesaja dönüştürür.
    
    Args:
        hata: Oluşan hata
        
    Returns:
        str: Kullanıcı dostu hata mesajı
    """
    if isinstance(hata, VeriYuklemeHatasi):
        return "⚠️ Oyun verileri yüklenirken bir hata oluştu. Lütfen oyun dosyalarını kontrol edin."
    elif isinstance(hata, OyunDurumHatasi):
        return "⚠️ Oyun durumunda bir sorun var. Lütfen oyunu yeniden başlatın."
    elif isinstance(hata, AnalizHatasi):
        return "⚠️ Delil analizi sırasında bir hata oluştu. Lütfen tekrar deneyin."
    elif isinstance(hata, UIHatasi):
        return "⚠️ Arayüzde bir hata oluştu. Lütfen pencereyi yenileyin."
    elif isinstance(hata, FileNotFoundError):
        return "⚠️ Gerekli dosya bulunamadı. Lütfen oyun kurulumunu kontrol edin."
    elif isinstance(hata, PermissionError):
        return "⚠️ Dosya erişim izni yok. Lütfen yönetici olarak çalıştırın."
    elif isinstance(hata, ValueError):
        return "⚠️ Geçersiz değer girildi. Lütfen girdilerinizi kontrol edin."
    else:
        return "⚠️ Beklenmedik bir hata oluştu. Lütfen oyunu yeniden başlatın."
