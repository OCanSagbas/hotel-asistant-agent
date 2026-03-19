# 🏨 Güral Premier Hotels - AI Asistanı

Bu proje, bir otele ait oda arama, rezervasyon yapma ve ek hizmet alma (Transfer, SPA) senaryolarını otomatize eden bir LangGraph & Gemini (Yapay Zeka) asistanıdır.

## 🚀 Kurulum ve Çalıştırma

1. Python ortamını kurun ve bağımlılıkları yükleyin:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gradio  # Web arayüzü için
```

2. `.env` dosyasını oluşturun ve Gemini API key'inizi girin:
```bash
cp .env.example .env
# .env içine GOOGLE_API_KEY=your_key_here yazın.
```

3. Uygulamayı Başlatın:
```bash
python app.py
```
Arayüze [http://0.0.0.0:7860](http://0.0.0.0:7860) üzerinden erişebilirsiniz.

### 🐳 Docker ile Çalıştırma (Tavsiye Edilen)
Ortam kurmakla uğraşmadan tek satırda projeyi ayağa kaldırmak için Docker kullanabilirsiniz:

1. `.env` dosyanızı oluşturduğunuzdan emin olun (İçinde `GOOGLE_API_KEY` olmalı).
2. İmajı derleyin (build):
```bash
docker build -t hotel-assistant .
```
3. Konteyneri başlatın:
```bash
docker run -d -p 7860:7860 --env-file .env --name hotel-agent hotel-assistant
```
Arayüze anında [http://localhost:7860](http://localhost:7860) adresinden ulaşabilirsiniz. Konteyneri durdurmak için `docker stop hotel-agent` yazmanız yeterlidir.

---

## 📂 Klasör Yapısı (Folder Architecture)
Proje, kurumsal seviyede *Separation of Concerns* (Sorumlulukların Ayrılığı) prensiplerine göre tasarlanmıştır:
```text
📦hotel-asistant-agent
 ┣ 📂agent                   # LangGraph AI Beyni (Mimarinin Kalbi)
 ┃ ┣ 📂mappers               # API yanıtlarını özetleyen, ID'leri gizleyen filtre katmanı
 ┃ ┣ 📂nodes                 # Akış adımları: LLM karar (agent_node) ve araç çalıştırma (tool_node)
 ┃ ┣ 📂tools                 # Dış dünya fonksiyonları (Oda Arama, Rezervasyon, Transfer)
 ┃ ┣ 📜graph.py              # Tüm düğümleri bağlayan LangGraph iş akışı şeması
 ┃ ┗ 📜state.py              # Hafıza yapısı (Sohbet geçmişi ve ID'lerin ayrıştırılması)
 ┣ 📜.dockerignore           # Docker derlemesinde hariç tutulacaklar
 ┣ 📜.gitignore              # Git geçmişinden gizlenecek şifre ve çöpler (.env vb.)
 ┣ 📜Dockerfile              # Uygulamayı izole çalıştıran konteyner talimatları
 ┣ 📜README.md               # Proje belgelendirme ve kullanım kılavuzu
 ┣ 📜app.py                  # Gradio ile yazılmış Web Arayüzü (Kullanıcı Ekranı)
 ┣ 📜main.py                 # Konsol veya alternatif API giriş noktası
 ┗ 📜requirements.txt        # Proje bağımlılıkları ve Python kütüphaneleri
```

---

## 🎯 Problem Tanımı ve Görev İsterlerinin Karşılanması

Bu proje, dış API'lerin döndürdüğü uzun spesifik JSON yanıtlarının doğrudan mesaj geçmişine eklenmesinin neden olduğu operasyonel sorunları çözmek üzere **LangGraph** ile geliştirilmiştir. İstenen problemlere şu mimari çözümler getirilmiştir:

**Problemlerin Çözümü (Context Rot, Halüsinasyon ve Gecikme):**
Uzun JSON'lar hiçbir zaman LLM mesaj geçmişine (chat history) sızmaz. **Mapper (Özetleyici)** dosyalar, API'den dönen karmaşık listeleri tek satırlık akıllı özetlere dönüştürür (*Maliyet/Gecikme/Context Rot çözüldü*). Karmaşık ve alakasız API ID'leri (`room_type_id` vb.) LLM ekranından gizlenir, böylece modelin kafası karışıp uydurma ID üretmesi engellenir (*Halüsinasyon çözüldü*). 

**İstenen 3 Görevin (Tasks) Karşılanma Durumu:**
1. **Gelişmiş State Tasarımı:** LangGraph state yapısı (`agent/state.py`) ikiye bölünmüştür: `messages` (saf diyalog) ve `booking_context` (yapısal verilerin / ID'lerin gizli tutulduğu bölüm).
2. **Tool Çıktılarının Filtrelenmesi:** Agent bir tool çağırdığında (örn: check_availability), dönen JSON mapper'a girer. Gerekli ID'ler gizlice State'e yazılırken mesaj geçmişine sadece "N oda bulundu, En iyisi X..." şeklinde minik bir özet bırakılır.
3. **Kısa Senaryonun İşletilmesi:** *"Oda ara"* -> *"Bu odayı ayırt ve transfer ekle"* senaryosu; hiçbir şekilde manuel ID sormadan, arka planda yapısal verilerden çekilerek Web UI üzerinden kusursuzca desteklenmektedir.

---

## 🏗️ Mimari Tasarım (Puanlama & Mapper Akışı)

Yapay zeka modelleriyle çalışırken en büyük problemler olan **Context Rot (bağlamın şişip bozulması)**, **Halüsinasyon** ve **Yüksek Token Maliyeti** sorunlarını aşmak için sistem 3 katmanlı bir filtreleme mimarisine sahiptir:

### 1. Akıllı Arama Motoru (Tool Katmanı - `search_rooms.py`)
Yapay zeka, odaları aramak için aracı (tool'u) tetiklediğinde devasa JSON listesini kendi başına işlemez. Python içindeki kod; 
* Müşterinin istediği "Kişi Sayısı" ile odanın maksimum kapasitesini kıyaslayıp oda boyutu israfı/küçüklüğüne göre **Puan** verir.
* Müşterinin "Deniz manzarası, jakuzi vb." özel isteklerini (preference) string bazlı kontrol edip odalara **Bonus Puan** verir veya ceza keser.
* Bulunan odaları *en iyi eşleşmeden en kötüye doğru* **Sıralar (Sort)**.

### 2. Özetleyici Filtre (Mapper Katmanı - `search_mapper.py`)
Arka plandaki araç 5-10 odalık devasa bir JSON sonucunu (fotoğraflar, poliçeler vs.) döndürdüğünde, bu veriler **asla yapay zekaya (LLM) gönderilmez.** 
* Mapper devreye girer. Yalnızca puanlaması en yüksek olan ilk `[:5]` odayı cımbızla çeker.
* Çektiği odaların sadece isimlerini, fiyatlarını ve rezervasyon ID'lerini kısa bir `string` haline getirerek mesaj geçmişine (`ToolMessage`) yazar. 

### 3. Yapay Zeka (LLM Katmanı - `agent_node.py`)
Yapay zeka; devasa JSON objelerini okuyup token limitlerini doldurmak veya gereksiz bilgileri unutup halüsinasyon görmek yerine sadece "En uygun N oda bulundu" diyen o kısacık metni (yaklaşık 50 token) okur. 
Böylece maliyet artmaz, AI sadece müşterinin hayalindeki odalarla konuşur ve son derece tutarlı bir rezervasyon akışı başlatır.

### 4. Sayfalama ve Alternatif Sunma (Limit & Offset)
Müşteri "Başka oda var mı?" diye sorduğunda eski sistemde (Mapper filtrelediği için) yapay zeka diğer odaları tekrar göremiyordu. Bu sorunu aşmak için sisteme sayfalama mantığı eklendi:
* `search_rooms` aracı `limit` ve `offset` parametreleri alır.
* Yapay zeka ilk aramada her zaman **`limit=1` ve `offset=0`** (Sadece en iyi 1 numaralı oda) diyerek arama yapar.
* Eğer müşteri başka seçenek isterse, yapay zeka kendi kendine **`limit=2` ve `offset=1`** (ilk odayı atla, sıradaki 2 odayı getir) diyerek gizli bir Tool Call daha yapar. Böylece API gereksiz yere büyük verilerle yorulmaz, müşteri de pürüzsüz bir şekilde tikelden tümele doğru seçeneklerle karşılaşır.


### Rezervasyon Hafızası (`booking_context`)
Müşteri odayı onayladığında veya bir SPA/Transfer paketi eklettiğinde oluşan teknik kimlik numaraları (ID'ler) müşteriye gösterilmez. Sistemin State belleğinde (`booking_context`) gizli kalır ce rezervasyonu tamamlarken sadece arka planda kullanılır.
# hotel-asistant-agent
