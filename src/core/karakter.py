# karakter.py — Karakter Sınıfları ve Polimorfizm Örneği

from abc import ABC, abstractmethod
from typing import List, Dict

# Base Class - Soyut Sınıf
class Karakter(ABC):
    """
    Oyundaki tüm karakterler için temel arayüz.
    Polimorfizm örneği: Tüm karakterler aynı metotları farklı şekillerde uygular.
    """
    
    def __init__(self, isim: str, rol: str, suclu: bool = False):
        self._isim = isim  # Encapsulation: Private attribute
        self._rol = rol
        self._suclu = suclu
        self._deliller: List[str] = []
        self._biyografi: str = ""
    
    # Encapsulation: Getter metotları
    @property
    def isim(self) -> str:
        return self._isim
    
    @property
    def rol(self) -> str:
        return self._rol
    
    @property
    def suclu(self) -> bool:
        return self._suclu
    
    @property
    def deliller(self) -> List[str]:
        return self._deliller.copy()  # Kopya döndürerek encapsulation
    
    @property
    def biyografi(self) -> str:
        return self._biyografi
    
    # Setter metotları ile kontrollü erişim
    @deliller.setter
    def deliller(self, yeni_deliller: List[str]):
        if isinstance(yeni_deliller, list):
            self._deliller = yeni_deliller
        else:
            raise ValueError("Deliller bir liste olmalıdır!")
    
    @biyografi.setter
    def biyografi(self, metin: str):
        if isinstance(metin, str) and len(metin) > 0:
            self._biyografi = metin
        else:
            raise ValueError("Biyografi boş olamaz!")
    
    # Soyut metot - Polimorfizm için
    @abstractmethod
    def bilgi_ver(self) -> str:
        """Karakterin kendini tanıtma metodu. Her karakter farklı şekilde uygular."""
        pass
    
    @abstractmethod
    def suclu_mu(self) -> bool:
        """Karakterin suçlu olup olmadığını döndürür."""
        pass
    
    def __str__(self) -> str:
        return f"{self._isim} ({self._rol})"


# Somut Sınıflar - Kalıtım ve Polimorfizm
class Supheli(Karakter):
    """Şüpheli karakterler için somut sınıf."""
    
    def __init__(self, isim: str, rol: str, suclu: bool = False, emoji: str = "👤", renk: str = "#000000"):
        super().__init__(isim, rol, suclu)
        self._emoji = emoji
        self._renk = renk
    
    @property
    def emoji(self) -> str:
        return self._emoji
    
    @property
    def renk(self) -> str:
        return self._renk
    
    def bilgi_ver(self) -> str:
        """Şüpheli kendini tanıtır."""
        return f"Ben {self._isim}, {self._rol}. Bu dava hakkında bilgilerim var."
    
    def suclu_mu(self) -> bool:
        """Şüphelinin suçlu olup olmadığını kontrol eder."""
        return self._suclu
    
    def savunma_yap(self) -> str:
        """Şüphelinin savunması."""
        if self._suclu:
            return "Ben yapmadım! Yanlış kişiye bakıyorsunuz!"
        else:
            return "Masumum. Gerçek suçluyu bulun lütfen."


class Kurbun(Karakter):
    """Kurban karakterler için somut sınıf."""
    
    def __init__(self, isim: str, rol: str = "Kurban", olum_sebebi: str = "Bilinmiyor"):
        super().__init__(isim, rol, False)
        self._olum_sebebi = olum_sebebi
    
    @property
    def olum_sebebi(self) -> str:
        return self._olum_sebebi
    
    def bilgi_ver(self) -> str:
        """Kurban bilgisi verir."""
        return f"Maalesef {self._isim} hayatını kaybetti. Ölüm sebebi: {self._olum_sebebi}"
    
    def suclu_mu(self) -> bool:
        """Kurbanlar suçlu olamaz."""
        return False


class Tanik(Karakter):
    """Tanık karakterler için somut sınıf."""
    
    def __init__(self, isim: str, rol: str = "Tanık", ifadeler: List[str] = None):
        super().__init__(isim, rol, False)
        self._ifadeler = ifadeler or []
    
    @property
    def ifadeler(self) -> List[str]:
        return self._ifadeler.copy()
    
    def ifade_ekle(self, ifade: str):
        """Yeni ifade ekler."""
        if isinstance(ifade, str) and len(ifade.strip()) > 0:
            self._ifadeler.append(ifade.strip())
    
    def bilgi_ver(self) -> str:
        """Tanık ifadesini verir."""
        if self._ifadeler:
            return f"Ben {self._isim}. Gördüğüm şeyler: {self._ifadeler[0]}"
        return f"Ben {self._isim}. Ne yazık ki fazla bir şey göremedim."
    
    def suclu_mu(self) -> bool:
        """Tanıklar genellikle suçlu olmaz."""
        return False
    
    def tum_ifadeler(self) -> str:
        """Tüm ifadeleri döndürür."""
        return "\n".join(f"- {ifade}" for ifade in self._ifadeler)


# Polimorfizm Örneği: Karakter Yöneticisi
class KarakterYoneticisi:
    """Tüm karakterleri yöneten sınıf. Polimorfizm kullanır."""
    
    def __init__(self):
        self._karakterler: List[Karakter] = []
    
    def karakter_ekle(self, karakter: Karakter):
        """Yeni karakter ekler."""
        if isinstance(karakter, Karakter):
            self._karakterler.append(karakter)
        else:
            raise ValueError("Sadece Karakter tipindeki nesneler eklenebilir!")
    
    def tum_karakterleri_tanit(self) -> str:
        """Tüm karakterleri tanıtır. Polimorfizm örneği."""
        tanitimlar = []
        for karakter in self._karakterler:
            tanitimlar.append(karakter.bilgi_ver())
        return "\n".join(tanitimlar)
    
    def suphelileri_getir(self) -> List[Supheli]:
        """Sadece şüpheli karakterleri döndürür."""
        return [k for k in self._karakterler if isinstance(k, Supheli)]
    
    def sucluyu_bul(self) -> Supheli:
        """Suçlu olan şüpheliyi bulur."""
        for karakter in self._karakterler:
            if isinstance(karakter, Supheli) and karakter.suclu_mu():
                return karakter
        return None
    
    def karakter_sayisi(self) -> int:
        return len(self._karakterler)
    
    def __len__(self) -> int:
        return self.karakter_sayisi()
