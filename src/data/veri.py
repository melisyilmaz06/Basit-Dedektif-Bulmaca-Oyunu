# veri.py — Oyun Verisi: Bölümler, Şüpheliler, Deliller

BOLUMLER = [
    {
        "num": 1,
        "title": "MÜZEDEKİ CİNAYET",
        "location": "📍 Şehir Tarih Müzesi, İstanbul",
        "sahne_turu": "muze",
        "hikaye": (
            "Şehir Tarih Müzesi'nde değerli Osmanlı madalyaları çalındı!\n"
            "Müze bekçisi Ahmet Bey bayıltılmış halde bulundu.\n\n"
            "Gece yarısı gerçekleşen bu soygunun faillini bulmak için\n"
            "müzeyi dikkatlice incele, delilleri topla ve\n"
            "laboratuvarda analiz et. Suçluyu yakala!"
        ),
        "supheliler": [
            {
                "isim": "Prof. Kaplan",
                "rol": "Baş Küratör",
                "renk": "#dc2626",
                "emoji": "🎓",
                "suclu": False,
                "biyografi": "25 yıllık tecrübeli küratör.\nÇok dürüst ve düzgün biri\nolarak tanınıyor.",
                "deliller": ["Profesörün not defteri", "Kırmızı boya lekesi"],
            },
            {
                "isim": "Zeynep Avcı",
                "rol": "Güvenlik Şefi",
                "renk": "#7c3aed",
                "emoji": "🔐",
                "suclu": False,
                "biyografi": "Tüm güvenlik kodlarını biliyor.\nO gece alarmı neden\nkapattı?",
                "deliller": ["Zeynep'in anahtarı", "Mor iplik"],
            },
            {
                "isim": "Mert Demir",
                "rol": "Restoratör",
                "renk": "#0284c7",
                "emoji": "🎨",
                "suclu": True,
                "biyografi": "2 ay önce işe başladı.\nGeçmişi pek temiz değil...\nBorçları olduğu söyleniyor.",
                "deliller": ["Mert'in parmak izi", "Mavi boya tüpü", "Mert'e ait çanta"],
            },
        ],
        "tum_deliller": [
            "🔍 Kırık Cam Parçası",    "🩸 Kan Lekesi",
            "📌 Düşmüş Rozet",          "🧵 Yırtık Kumaş",
            "👣 Ayak İzi",              "🚬 Sigara İzmariti",
            "📝 Şifreli Not",           "🎨 Mavi Boya Tüpü",
            "👆 Parmak İzi",            "⚗️ Kimyasal Leke",
            "🔘 Kopuk Düğme",           "💡 Yanık Tel",
        ],
        "suclu_deliller": ["🎨 Mavi Boya Tüpü", "👆 Parmak İzi", "📌 Düşmüş Rozet"],
        "min_delil": 5,
    },
    {
        "num": 2,
        "title": "LİMANDAKİ ŞIFRE",
        "location": "📍 Eski İstanbul Limanı",
        "sahne_turu": "liman",
        "hikaye": (
            "Eski İstanbul Limanı'nda bir gemi gece yarısı karaya oturdu!\n"
            "Kaptan ortada yok, değerli kargo tamamen çalınmış.\n\n"
            "Şifreli mesajları çöz, gizli belgeleri bul ve bu\n"
            "karanlık operasyonun arkasındaki kişiyi ortaya çıkar!\n"
            "Zaman daralıyor..."
        ),
        "supheliler": [
            {
                "isim": "Kaptan Yıldız",
                "rol": "Eski Kaptan",
                "renk": "#d97706",
                "emoji": "⚓",
                "suclu": False,
                "biyografi": "30 yıllık denizci.\nSigortacılarla sorunları var\nama hep dürüst biri oldu.",
                "deliller": ["Kaptanın günlüğü", "Turuncu halat"],
            },
            {
                "isim": "Selma Koç",
                "rol": "Gümrük Müdürü",
                "renk": "#059669",
                "emoji": "📋",
                "suclu": True,
                "biyografi": "Tüm gümrük belgelerini\ndüzenliyor. Banka hesabında\nşüpheli para var.",
                "deliller": ["Selma'nın mühürü", "Gizli belge", "Yeşil mürekkep"],
            },
            {
                "isim": "Hakan Bulut",
                "rol": "Liman Bekçisi",
                "renk": "#be185d",
                "emoji": "🔦",
                "suclu": False,
                "biyografi": "10 yıldır limanı koruyor.\nO gece nöbetini erken\nbıraktı. Neden?",
                "deliller": ["Hakan'ın el feneri", "Pembe boya izi"],
            },
        ],
        "tum_deliller": [
            "💧 Islak Ayak İzi",        "📦 Hasar Görmüş Sandık",
            "📜 Şifreli Mesaj",         "🪝 Metal Kanca",
            "🌿 Deniz Yosunu",          "📋 Sahte Belge",
            "🧭 Kırık Pusula",          "🔏 Mühür Baskısı",
            "⛽ Gemi Yağı",             "🖊️ Yeşil Mürekkep",
            "🪢 Kopuk Halat",           "🔑 Yedek Anahtar",
        ],
        "suclu_deliller": ["📋 Sahte Belge", "🔏 Mühür Baskısı", "🖊️ Yeşil Mürekkep"],
        "min_delil": 6,
    },
    {
        "num": 3,
        "title": "KARANLIK ORMAN SIRRI",
        "location": "📍 Belgrad Ormanı Derinlikleri",
        "sahne_turu": "orman",
        "hikaye": (
            "Belgrad Ormanı'nın derinliklerinde insan kemikleri bulundu!\n"
            "DNA analizi 10 yıl öncesine işaret ediyor.\n\n"
            "Bu soğuk dava kapandı sanılıyordu. Ama sen\n"
            "gerçeği gün yüzüne çıkarmak için son bir şansa sahipsin.\n"
            "Delilleri topla, suçluyu mahkûm et!"
        ),
        "supheliler": [
            {
                "isim": "Dr. Şahin",
                "rol": "Orman Mühendisi",
                "renk": "#6d28d9",
                "emoji": "🧪",
                "suclu": True,
                "biyografi": "Eski bir araştırmacı.\nO dönemde ormanda çok\nzaman geçiriyordu.",
                "deliller": ["Dr. Şahin'in rozeti", "Mor ilaç şişesi", "Şahin'e ait DNA"],
            },
            {
                "isim": "Leyla Yurt",
                "rol": "Botanik Uzmanı",
                "renk": "#15803d",
                "emoji": "🌿",
                "suclu": False,
                "biyografi": "Ormandaki bitkileri\naraştırıyor. Çok sakin\nve nazik biri.",
                "deliller": ["Leyla'nın not defteri", "Yeşil boya"],
            },
            {
                "isim": "Rıza Kara",
                "rol": "Avcı Rehberi",
                "renk": "#92400e",
                "emoji": "🏹",
                "suclu": False,
                "biyografi": "Ormanda yıllardır rehberlik\nyapıyor. O gece ormanda\nmıydı gerçekten?",
                "deliller": ["Rıza'nın çakısı", "Kahve renkli tüy"],
            },
        ],
        "tum_deliller": [
            "🦴 Eski Kemik",            "🔪 Pas Tutmuş Bıçak",
            "📷 Solmuş Fotoğraf",       "👕 Yırtık Giysi",
            "🌱 Toprak Örneği",         "🧬 DNA İzi",
            "⌚ Kırık Saat",            "📦 Gömülü Kutu",
            "💊 İlaç Şişesi",          "🟣 Mor Leke",
            "📛 Rozet Parçası",         "📰 Eski Gazete",
        ],
        "suclu_deliller": ["🧬 DNA İzi", "💊 İlaç Şişesi", "📛 Rozet Parçası"],
        "min_delil": 7,
    },
]
