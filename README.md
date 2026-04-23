# 🔍 Criminal Case: İstanbul Dosyaları

## Proje Hakkında

**Criminal Case: İstanbul Dosyaları**, BGT 132 Yazılım Geliştirme Teknolojileri dersi için geliştirilen bir dedektif bulmaca oyunudur. Oyuncular, İstanbul'un farklı bölgelerinde gerçekleşen gizemli cinayetleri çözmek için deliller toplar, analiz eder ve suçluyu bulmaya çalışır.

## 🎮 Oyun Hakkında

Oyun 3 ana bölümden oluşur:
1. **Müzede Cinayet** - Değerli Osmanlı madalyalarının çalındığı dava
2. **Limandaki Şifre** - Gemi kargo soygunu ve kayıp kaptan davası  
3. **Karanlık Orman Sırrı** - 10 yıl öncesine ait soğuk bir dava

Her bölümde:
- Olay yeri incelemesi
- Delil toplama ve analiz
- Şüpheli sorgulama
- Suçlu teşhis etme

## 🛠️ Teknik Özellikler

### Kullanılan Teknolojiler
- **Programlama Dili**: Python 3.8+
- **Arayüz**: Tkinter
- **Veri Yapıları**: JSON
- **Version Control**: Git

### OOP Özellikleri
- **3+ Sınıf Yapısı**: `Karakter`, `Supheli`, `DelilAnalizServisi`, `OyunYardimcisi`
- **Kalıtım**: `Supheli` → `Karakter`
- **Polimorfizm**: `Karakter.bilgi_ver()` metodu
- **Encapsulation**: Private属性 ve getter/setter metotları

## 📁 Proje Yapısı

```
Basit Dedektif Bulmaca Oyunu/
├── docs/                           # Dokümantasyon
│   ├── GereksinimAnalizi.pdf
│   └── UML_Diyagramlari.pdf
├── src/                            # Kaynak Kodlar
│   ├── core/                       # Ana Mantık
│   │   ├── oyun.py                 # Ana oyun sınıfı
│   │   └── karakter.py             # Karakter sınıfları
│   ├── services/                   # İş Mantığı
│   │   └── delil_analiz_servisi.py # Analiz servisi
│   ├── data/                       # Veri Yönetimi
│   │   └── veri.py                 # Oyun verileri
│   ├── ui/                         # Kullanıcı Arayüzü
│   │   ├── renkler.py
│   │   └── ekranlar/
│   ├── utils/                      # Yardımcı Fonksiyonlar
│   │   ├── hata_yonetimi.py        # Hata yönetimi
│   │   └── oyun_yardimcilari.py    # Oyun yardımcıları
│   └── modules/                    # Modüller
├── assets/                         # Görseller ve Sesler
├── data/                           # Oyun Verileri
├── tests/                          # Test Dosyaları
├── main.py                         # Başlangıç Noktası
├── README.md                       # Bu dosya
└── .gitignore                      # Git İgnore
```

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.8 veya üzeri
- Tkinter (genellikle Python ile birlikte gelir)

### Adım 1: Projeyi İndirme
```bash
git clone https://github.com/kullanici-adi/dedektif-oyunu.git
cd dedektif-oyunu/Basit\ Dedektif\ Bulmaca\ Oyunu
```

### Adım 2: Gerekli Kütüphaneler
```bash
pip install -r requirements.txt
```

### Adım 3: Oyunu Başlatma
```bash
python main.py
```

Veya doğrudan çalıştırın:
```bash
python "Basit Dedektif Bulmaca Oyunu/main.py"
```

## 🎯 Oyun Nasıl Oynanır

### 1. Başlangıç
- Oyunu başlattığınızda ana menü açılır
- "Yeni Oyun" butonuna tıklayarak başlayın

### 2. Bölüm Seçimi
- 3 bölümden birini seçin
- Her bölümün farklı bir hikayesi ve şüphelileri vardır

### 3. Olay Yeri İncelemesi
- "🔍 Olay Yerini İncele" butonuna tıklayın
- Rastgele deliller bulunur
- Deliller envanterinize eklenir

### 4. Delil Analizi
- "⚗️ Laboratuvar" butonuna tıklayın
- Analiz etmek için bir delil seçin
- Analiz sonuçları size ipuçları verir

### 5. Şüpheli Sorgulama
- Sağ taraftaki şüphelilere tıklayın
- Biyografilerini ve delillerini inceleyin
- Topladığınız bilgilerle suçluyu belirleyin

### 6. Suçlama
- "🚨 Suçla" butonuna tıklayın
- Suçlu olduğuna inandığınız kişiyi seçin
- Doğru tahmin için bonus puan kazanın!

## 📊 Skor Sistemi

- **Delil Bulma**: Her delil için 10 puan
- **Analiz Başarısı**: Her analiz için 20 puan  
- **Doğru Suçlama**: 200 puan + bonus
- **Yanlış Suçlama**: -50 puan
- **Yıldız Sistemi**: 1-3 yıldız

## 🧪 Testler

Testleri çalıştırmak için:
```bash
python -m pytest tests/
```

Veya tek test dosyası:
```bash
python tests/test_oyun.py
```

## 🐛 Hata Yönetimi

Oyun kapsamlı hata yönetimi içerir:
- **Veri Yükleme Hataları**: JSON dosya sorunları
- **Oyun Durum Hataları**: Geçersiz durum geçişleri
- **Analiz Hataları**: Laboratuvar analiz sorunları
- **Arayüz Hataları**: Tkinter widget sorunları

Tüm hatalar `logs/game.log` dosyasına kaydedilir.

## 📝 Kod Kalitesi

### Uygulanan Standartlar
- **Anlamlı Değişken İsimleri**: `oyun_durumu`, `bulunan_deliller`
- **Yorum Satırları**: Her fonksiyon ve sınıf açıklamalı
- **Fonksiyonel Ayrıştırma**: Tek sorumluluk ilkesi
- **Maksimum Dosya Uzunluğu**: 1000 satır sınırı

### OOP İlkeleri
- **Encapsulation**: Private属性 ve kontrollü erişim
- **Inheritance**: `Karakter` temel sınıfı
- **Polymorphism**: `bilgi_ver()` metodu farklı sınıflarda farklı çalışır
- **Abstraction**: Soyut `Karakter` sınıfı

## 🔄 Git Kullanımı

### Anlamlı Commit Mesajları
```
feat: karakter sistemi eklendi
fix: analiz servisi hataları düzeltildi  
docs: README güncellendi
refactor: hata yönetimi yenilendi
test: birim testleri eklendi
```

### Branch Yapısı
- `main`: Ana geliştirme dalı
- `feature/ozellik-adi`: Yeni özellikler
- `bugfix/hata-aciklamasi`: Hata düzeltmeleri

## 🤝 Katkıda Bulunma

1. Projeyi fork edin
2. Yeni branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişiklikleri yapın ve commit edin
4. Push edin (`git push origin feature/yeni-ozellik`)
5. Pull request oluşturun

## 📄 Lisans

Bu proje eğitim amaçlıdır ve BGT 132 dersi kapsamında geliştirilmiştir.

## 👥 Geliştirici

- **Ad**: [Öğrenci Adı]
- **Bölüm**: [Bölüm Adı]
- **Ders**: BGT 132 Yazılım Geliştirme Teknolojileri
- **Proje**: Final Projesi

## 📞 İletişim

Sorularınız ve önerileriniz için:
- E-posta: [öğrenci-email@universite.edu.tr]
- GitHub: [github.com/kullanici-adi]

---

**Not**: Bu proje BGT 132 dersi final projesi olarak geliştirilmiştir ve tüm ders gereksinimlerini karşılamaktadır.
