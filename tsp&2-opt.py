# Gerekli kütüphaneleri içe aktar
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CSV dosyalarını yükle
try:
    mesafe_df = pd.read_csv("C:\Users\smaze\Desktop\Proje\Route-Optimization\distance.csv")
    siparis_kucuk_df = pd.read_csv("C:\Users\smaze\Desktop\Proje\Route-Optimization\order_large.csv")
except FileNotFoundError:
    print("Hata: distance.csv veya order_large.csv C:/Users/smaze/Desktop/Proje/Route-Optimization/ klasöründe bulunamadı.")
    exit()

# --- Veri Ön İşleme ---
# Adım 1: Siparişlerde yer alan benzersiz şehirleri al
sehirler = pd.unique(siparis_kucuk_df[['Source', 'Destination']].values.ravel('K'))
sehirler = sorted(sehirler)

# Adım 2: Her şehri bir indekse eşle
sehir_indeks_eslesme = {sehir: idx for idx, sehir in enumerate(sehirler)}
indeks_sehir_eslesme = {idx: sehir for sehir, idx in sehir_indeks_eslesme.items()}
sehir_sayisi = len(sehirler)

print(f"Optimize edilecek şehir sayısı: {sehir_sayisi}")
print(f"Şehirler: {sehirler}")

# Adım 3: Mesafe matrisi başlat
mesafe_matrisi = np.full((sehir_sayisi, sehir_sayisi), 1e6)

# Adım 4: CSV'den mesafeleri doldur
for _, satir in mesafe_df.iterrows():
    kaynak, hedef, mesafe = satir['Source'], satir['Destination'], satir['Distance(M)']
    if kaynak in sehir_indeks_eslesme and hedef in sehir_indeks_eslesme:
        i, j = sehir_indeks_eslesme[kaynak], sehir_indeks_eslesme[hedef]
        mesafe_matrisi[i][j] = int(mesafe)
        mesafe_matrisi[j][i] = int(mesafe)

np.fill_diagonal(mesafe_matrisi, 0)

print("\nSeçilen şehirler için mesafe matrisi önizlemesi:")
print(pd.DataFrame(mesafe_matrisi, index=sehirler, columns=sehirler).round(0))

class Cozucu:
    def _init_(self, mesafe_matrisi, p=1):
        self.mesafe_matrisi = mesafe_matrisi
        self.sehir_sayisi = mesafe_matrisi.shape[0]
        self.p = p
        
        # Store the full matrix for classical algorithm
        self.tam_mesafe_matrisi = mesafe_matrisi.copy()
        
        print(f"Toplam şehir sayısı: {self.sehir_sayisi}")
        print("Tam veri setiyle çalışılıyor...")
        
        # For large datasets, we'll use classical algorithm with QAOA principles
        # No city limit anymore - process all cities
        
    def optimize(self):
        """Optimize rota"""
        print("\nRota optimizasyonu başlatılıyor...")
        
        # For large datasets, use improved nearest neighbor with 2-opt
        print("Geliştirilmiş en yakın komşu + 2-opt algoritması kullanılıyor...")
        route = self.improved_tsp_solver()
        
        # Calculate the total cost
        total_cost = self.calculate_route_cost(route)
        
        return route, total_cost
    
    def calculate_route_cost(self, route):
        """Rota maliyetini hesapla"""
        total_cost = 0
        for i in range(len(route)):
            total_cost += self.tam_mesafe_matrisi[route[i]][route[(i+1) % len(route)]]
        return total_cost
    
    def nearest_neighbor_tsp(self):
        """Klasik en yakın komşu algoritması"""
        baslangic = 0  # İlk şehirden başla
        ziyaret_edilmis = {baslangic}
        rota = [baslangic]
        
        while len(ziyaret_edilmis) < self.sehir_sayisi:
            mevcut = rota[-1]
            en_yakin = None
            en_kisa_mesafe = float('inf')
            
            for sonraki in range(self.sehir_sayisi):
                if sonraki not in ziyaret_edilmis:
                    mesafe = self.tam_mesafe_matrisi[mevcut][sonraki]
                    if mesafe < en_kisa_mesafe:
                        en_kisa_mesafe = mesafe
                        en_yakin = sonraki
            
            if en_yakin is not None:
                rota.append(en_yakin)
                ziyaret_edilmis.add(en_yakin)
            else:
                break  # Tüm şehirler ziyaret edilmiş
                
        return rota
    
    def two_opt_swap(self, route, i, j):
        """2-opt swap: i ve j arasındaki rotayı tersine çevirir"""
        new_route = route.copy()
        new_route[i:j+1] = route[i:j+1][::-1]
        return new_route
    
    def two_opt_improve(self, route, max_iterations=1000):
        """2-opt iyileştirmesi"""
        best_route = route.copy()
        improved = True
        iterations = 0
        best_cost = self.calculate_route_cost(best_route)
        
        while improved and iterations < max_iterations:
            improved = False
            iterations += 1
            
            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route) - 1):
                    new_route = self.two_opt_swap(best_route, i, j)
                    new_cost = self.calculate_route_cost(new_route)
                    
                    if new_cost < best_cost:
                        best_route = new_route
                        best_cost = new_cost
                        improved = True
                        break
                
                if improved:
                    break
        
        print(f"2-opt iyileştirmesi {iterations} iterasyonda tamamlandı.")
        return best_route
    
    def improved_tsp_solver(self):
        """Geliştirilmiş TSP çözücü"""
        # Use nearest neighbor to get initial route
        route = self.nearest_neighbor_tsp()
        
        # Improve with 2-opt
        improved_route = self.two_opt_improve(route)
        
        return improved_route

# --- Ana Yürütme ---
if sehir_sayisi > 0:
    # çözücüyü başlat ve çalıştır
    solver = Cozucu(mesafe_matrisi, p=1)
    route, cost = solver.optimize()
    
    if route is not None:
        # Rota indekslerini şehir isimlerine çevir
        sehir_rotasi = [sehirler[i] for i in route]
        sehir_rotasi.append(sehir_rotasi[0])  # Başlangıç noktasına dön
        
        print("\n--- Rota Optimizasyon Sonuçları ---")
        print(f"Optimize edilen toplam şehir sayısı: {len(route)}")
        print("\nEn İyi Rota (Şehir İsimleri):")
        print(" ➡ ".join(sehir_rotasi))
        
        print(f"\nToplam Maliyet: {cost:,.0f}")
        
        # Toplam mesafeyi hesapla
        toplam_mesafe = 0
        for i in range(len(sehir_rotasi)-1):
            kaynak_idx = sehirler.index(sehir_rotasi[i])
            hedef_idx = sehirler.index(sehir_rotasi[i+1])
            toplam_mesafe += mesafe_matrisi[kaynak_idx][hedef_idx]
        
        print(f"Toplam Mesafe: {toplam_mesafe:,.0f} metre")
        
        # Rotayı görselleştir
        plt.figure(figsize=(12, 8))
        plt.title(f"En İyi Teslimat Rotası (Toplam {len(route)} şehir)")
        
        # Çok fazla şehir olduğunda grafiği temiz tutmak için
        if len(route) > 20:
            # Örnekleme yap - ilk ve son 10 şehri göster
            ilk_10 = [sehirler.index(city) for city in sehir_rotasi[:10]]
            son_10 = [sehirler.index(city) for city in sehir_rotasi[-11:-1]]
            
            plt.plot(range(10), ilk_10, marker='o', linestyle='--', color='purple')
            plt.plot([10, 11], [ilk_10[-1], son_10[0]], linestyle=':', color='gray')
            plt.plot(range(11, 21), son_10, marker='o', linestyle='--', color='purple')
            
            plt.xticks(list(range(10)) + list(range(11, 21)), 
                      sehir_rotasi[:10] + sehir_rotasi[-11:-1], rotation=45)
            plt.annotate('...', xy=(10.5, 0), fontsize=20)
        else:
            plt.plot(range(len(sehir_rotasi)), [sehirler.index(city) for city in sehir_rotasi], 
                    marker='o', linestyle='--', color='purple')
            plt.xticks(range(len(sehir_rotasi)), sehir_rotasi, rotation=45)
        
        plt.xlabel("Adım")
        plt.ylabel("Şehir")
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.tight_layout()
        plt.show()
    else:
        print("\nGeçerli bir rota bulunamadı.")
else:
    print("\nOptimize edilecek şehir bulunamadı.")
