# Savunma Lojistiğinde Çok Noktalı Rota Optimizasyonu: TSP Tabanlı Yöntem ve Karınca Kolonisi Algoritması Karşılaştırmalı Performans Analizi

Bu proje, savunma lojistik operasyonlarında zaman kritikliği taşıyan ve kaynakların etkin kullanımını gerektiren çok noktalı teslimat görevleri için Gezgin Satıcı Problemi (TSP) tabanlı gelişmiş bir rota optimizasyon yöntemini sunmakta ve bu yöntemin performansını klasik Karınca Kolonisi Optimizasyonu (ACO) algoritması ile kapsamlı bir şekilde karşılaştırmaktadır.

## Proje Özeti ve Motivasyon

Savunma operasyonları, doğası gereği yüksek düzeyde karmaşıklık ve zaman baskısı içerir. Bu operasyonlarda, malzeme, personel veya teçhizatın belirlenen noktalara en hızlı ve en etkin şekilde ulaştırılması, görevin başarısı için hayati önem taşır. Geciken veya verimsiz yürütülen lojistik süreçler, operasyonel etkinliği düşürebilir, maliyetleri artırabilir ve en önemlisi, kritik durumlarda müdahale kapasitesini olumsuz etkileyebilir.

Bu çalışma, büyük ölçekli bir lojistik ağ üzerinde, çok sayıda sipariş veya teslimat noktasına en kısa toplam mesafeyi katederek ulaşmayı amaçlayan bir rota optimizasyon modeli geliştirmeye odaklanmıştır. Temel motivasyon, teslimat süreçlerini hızlandırmak, operasyonel maliyetleri (yakıt, zaman, aşınma vb.) düşürmek ve genel lojistik verimliliği artırmaktır.

## Problem Tanımı ve Amaçlar

**Problem:** Savunma lojistiğinde, belirlenmiş bir başlangıç noktasından çıkarak çok sayıda farklı coğrafi konuma dağılmış sipariş/teslimat noktasına uğrayıp başlangıç noktasına dönülmesi gereken en kısa rotanın bulunması problemidir (Çoklu Gezgin Satıcı Problemi - mTSP varyasyonu veya kapasite kısıtsız tek araçlı TSP olarak da düşünülebilir).

**Temel Amaçlar:**

1.  Çok sayıda sipariş noktasına en kısa toplam mesafeyle ulaşım sağlayacak bir rota optimizasyon yöntemi geliştirmek.
2.  Geliştirilen TSP tabanlı hibrit yöntemin (En Yakın Komşu + 2-Opt) performansını, yaygın bir meta-sezgisel olan Karınca Kolonisi Optimizasyonu (ACO) algoritması ile karşılaştırmak.
3.  Savunma lojistiği gibi zaman ve kaynak açısından kritik senaryolarda, önerilen yöntemin klasik yaklaşımlara göre daha etkin ve verimli çözümler sunup sunmadığını analiz etmek.
4.  Toplam kat edilen mesafeyi minimize ederek teslimat süreçlerinin hızlandırılmasına ve lojistik maliyetlerin düşürülmesine katkıda bulunmak.

## Uygulanan Metodoloji

Projede, rota optimizasyonu için aşağıdaki adımlar ve teknikler kullanılmıştır:

1.  **Veri Kaynakları:**
    * `distance.csv`: Şehirler veya lojistik noktalar arasındaki mesafeleri içeren veri seti. Bu dosyanın, noktalar arası doğrudan ulaşım mesafelerini (örneğin, kilometre veya metre cinsinden) içerdiği varsayılmaktadır.
    * `order_large.csv`: Teslimat yapılması gereken siparişlerin bilgilerini (muhtemelen teslimat noktası kimlikleri veya koordinatları) barındıran veri seti.

2.  **Veri Ön İşleme Aşaması:**
    * **Benzersiz Şehir İndekslemesi:** Veri setlerindeki tüm benzersiz şehir veya teslimat noktalarına sayısal birer indeks atanarak matris tabanlı işlemlerde kolaylık sağlanmıştır. Bu, algoritmaların konumları daha verimli işlemesine olanak tanır.
    * **Mesafe Matrisinin Simetrik Hale Getirilmesi:** İki nokta arasındaki gidiş ve dönüş mesafelerinin eşit olduğu varsayılarak (veya bu şekilde düzenlenerek) mesafe matrisinin simetrik olması sağlanmıştır. Bu, birçok TSP çözücüsünün temel bir varsayımıdır.

3.  **Önerilen Optimizasyon Yaklaşımı (TSP Tabanlı Hibrit Yöntem):**
    * **Başlangıç Çözümünün Oluşturulması: En Yakın Komşu (Nearest-Neighbor - NN) Algoritması**
        * Bu sezgisel algoritma, başlangıç noktasından başlayarak mevcut bulunulan noktaya en yakın, henüz ziyaret edilmemiş bir sonraki noktayı seçerek bir rota oluşturur. Basit ve hızlı bir başlangıç çözümü üretir.
    * **Çözümün İyileştirilmesi: 2-Opt Takas Yöntemi**
        * NN ile elde edilen başlangıç rotası üzerinde iyileştirme yapmak için kullanılır. 2-Opt, rotadaki iki kenarı kaldırıp, kalan iki alt turu farklı bir şekilde (çapraz olarak) yeniden bağlayarak daha kısa bir rota elde edilip edilemediğini kontrol eder. Bu işlem, daha fazla iyileştirme mümkün olmayana kadar tekrarlanır. Bu yerel arama tekniği, çözüm kalitesini önemli ölçüde artırabilir.

4.  **Karşılaştırma Algoritması: Klasik Karınca Kolonisi Optimizasyonu (ACO)**
    * ACO, karıncaların yiyecek ararken feromon izleri bırakarak en kısa yolu bulma davranışlarından esinlenen bir meta-sezgisel optimizasyon algoritmasıdır. Problemin çözüm uzayında yapay karıncalar dolaşır ve daha iyi çözümlere yol açan yollara daha fazla feromon bırakarak sonraki karıncaların bu yolları takip etme olasılığını artırır.

## Elde Edilen Sonuçlar ve Tartışma

Yapılan analizler sonucunda aşağıdaki performans metrikleri elde edilmiştir:

* **Önerilen Hibrit Yöntem (TSP + En Yakın Komşu + 2-Opt):**
    * Ulaşılan Toplam Rota Mesafesi: **15.329.314 metre**
* **Klasik Karınca Kolonisi Optimizasyonu (ACO):**
    * Ortalama Ulaşılan Toplam Rota Mesafesi: **Yaklaşık 19.000.000 metre**

**Karşılaştırma:**
Önerilen TSP tabanlı hibrit yöntem, klasik ACO algoritmasının ortalama sonucuna kıyasla toplam kat edilen mesafede yaklaşık **%19 oranında bir iyileştirme** sağlamıştır.

**Sonuçların Anlamı:**
Bu %19'luk iyileştirme, savunma lojistiği bağlamında önemli kazanımlar anlamına gelebilir:
* **Daha Hızlı Teslimat Süreleri:** Daha kısa mesafeler, teslimatların daha hızlı tamamlanmasını sağlar, bu da zaman-kritik operasyonlarda büyük avantajdır.
* **Azaltılmış Operasyonel Maliyetler:** Daha az mesafe, daha az yakıt tüketimi, araçların daha az yıpranması ve potansiyel olarak daha az sürücü/personel zamanı anlamına gelir.
* **Artan Kaynak Verimliliği:** Aynı kaynaklarla (araç, personel) daha fazla görevin yerine getirilebilmesi veya mevcut görevlerin daha az kaynakla tamamlanabilmesi.
* **Gelişmiş Görev Başarısı Olasılığı:** Lojistik süreçlerin etkinliği, genel görev başarısını doğrudan etkiler.

Elde edilen bu sonuçlar, önerilen yöntemin özellikle büyük ölçekli ve çok duraklı lojistik senaryolarda, klasik meta-sezgisel yaklaşımlara göre daha rekabetçi ve etkin çözümler üretebileceğini güçlü bir şekilde göstermektedir.

## Sonuç ve Değerlendirme

Bu çalışmada, savunma lojistik operasyonlarındaki çok noktalı rota optimizasyonu problemi ele alınmış, TSP tabanlı (En Yakın Komşu ile başlayıp 2-Opt ile iyileştirilen) bir hibrit yöntem geliştirilmiş ve Karınca Kolonisi Optimizasyonu algoritması ile karşılaştırılmıştır. Önerilen yöntemin, ACO'ya kıyasla %19'luk bir mesafe iyileştirmesi sağlaması, zaman ve kaynak verimliliğinin kritik olduğu savunma uygulamaları için dikkate değer bir potansiyel sunduğunu ortaya koymaktadır. Bu yaklaşım, lojistik planlamacılara daha optimize edilmiş rotalar oluşturma ve operasyonel verimliliği artırma konusunda güçlü bir araç sunabilir.

## Gelecek Çalışma ve Geliştirme Önerileri

Modelin gerçek dünya savunma lojistiği senaryolarındaki uygulanabilirliğini ve başarımını daha da artırmak için aşağıdaki konuların gelecek çalışmalarda ele alınması hedeflenmektedir:

* **Zaman Pencereleri (Time Windows) Entegrasyonu:** Her teslimat noktasının belirli bir zaman aralığında ziyaret edilmesi gerekliliğinin modele dahil edilmesi. Bu, özellikle randevulu teslimatlar veya belirli operasyonel zamanlamalara sahip görevler için önemlidir.
* **Araç Yük Kapasiteleri Kısıtlarının Eklenmesi:** Araçların taşıyabileceği maksimum yük miktarının dikkate alınarak rotaların ve araç atamalarının planlanması (Araç Rotalama Problemi - VRP'ye doğru bir evrim).
* **Dinamik Rota Güncellemeleri ve Gerçek Zamanlı Veri Entegrasyonu:** Operasyon sırasında ortaya çıkabilecek beklenmedik durumlar (örn. yol kapanmaları, trafik yoğunluğu, yeni acil siparişler) karşısında rotaların dinamik olarak güncellenebilmesi için mekanizmalar geliştirilmesi.
* **Çoklu Araç Optimizasyonu:** Tek bir araç yerine birden fazla aracın kullanıldığı senaryolar için optimizasyonun genişletilmesi.
* **Farklı Maliyet Fonksiyonları:** Sadece mesafe değil, aynı zamanda zaman, yakıt tüketimi, risk faktörleri gibi farklı maliyet unsurlarını içeren daha karmaşık amaç fonksiyonlarının değerlendirilmesi.
* **Diğer Sezgisel ve Meta-sezgisel Algoritmalarla Karşılaştırma:** Genetik Algoritmalar, Tavlama Benzetimi gibi diğer optimizasyon teknikleriyle kıyaslamalı analizlerin yapılması.

## Anahtar Kelimeler

Savunma Lojistiği, Rota Optimizasyonu, Gezgin Satıcı Problemi (TSP), Karınca Kolonisi Optimizasyonu (ACO), En Yakın Komşu Algoritması, 2-Opt Algoritması, Lojistik Verimlilik, Operasyonel Araştırma, Maliyet Düşürme.

---

_Bu README dosyası, sağlanan çalışma özetindeki bilgilere dayanarak detaylandırılmıştır. Projenin kod implementasyonu veya ek dokümantasyonu varsa, ilgili bölümler eklenebilir._