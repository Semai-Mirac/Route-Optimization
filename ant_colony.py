# Import necessary libraries
import pandas as pd

# Load CSV files
distance_df = pd.read_csv("C:\Users\smaze\Desktop\Proje\Route-Optimization\distance.csv")
order_small_df = pd.read_csv("C:\Users\smaze\Desktop\Proje\Route-Optimization\order_small.csv")
order_large_df = pd.read_csv("C:\Users\smaze\Desktop\Proje\Route-Optimization\order_large.csv")

import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Combine all orders to explore cities
all_orders_df = pd.concat([order_small_df, order_large_df], ignore_index=True)
all_cities = pd.unique(all_orders_df[['Source', 'Destination']].values.ravel('K'))

import numpy as np

# Step 1: Get unique cities involved in orders (we'll use order_small_df for now)
cities = pd.unique(order_large_df[['Source', 'Destination']].values.ravel('K'))
cities = sorted(cities)

# Step 2: Map each city to an index
city_to_index = {city: idx for idx, city in enumerate(cities)}
index_to_city = {idx: city for city, idx in city_to_index.items()}
num_cities = len(cities)

print("📍 Number of cities for distance matrix:", num_cities)

# Step 3: Initialize a distance matrix with large values (inf for unreachable)
distance_matrix = np.full((num_cities, num_cities), np.inf)

# Step 4: Fill in distances from the CSV
for _, row in distance_df.iterrows():
    src, dst, dist = row['Source'], row['Destination'], row['Distance(M)']
    if src in city_to_index and dst in city_to_index:
        i, j = city_to_index[src], city_to_index[dst]
        distance_matrix[i][j] = dist
        distance_matrix[j][i] = dist  # Assume symmetry unless otherwise stated

# Step 5: Set diagonal to a very large value to avoid self-loops
np.fill_diagonal(distance_matrix, 1e6)

# Check shape and a preview
print("\n🧾 Distance matrix shape:", distance_matrix.shape)
print("\n📊 Preview of distance matrix:")
print(pd.DataFrame(distance_matrix, index=cities, columns=cities).round(0))

import random

class AntColonyOptimizer:
    def _init_(self, distance_matrix, num_ants=5, num_iterations=100, alpha=1.0, beta=2.0, rho=0.5):
        self.distances = distance_matrix
        self.pheromones = np.ones_like(distance_matrix)
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha  # Pheromone importance
        self.beta = beta    # Distance heuristic importance
        self.rho = rho      # Evaporation rate
        self.num_cities = distance_matrix.shape[0]
        self.depot = 0      # Start from first city by default

    def _calculate_probabilities(self, current, visited):
        allowed = [i for i in range(self.num_cities) if i not in visited and i != self.depot]
        probs = np.zeros(self.num_cities)

        for j in allowed:
            tau = self.pheromones[current][j] ** self.alpha
            eta = (1.0 / self.distances[current][j]) ** self.beta
            probs[j] = tau * eta

        total = np.sum(probs)
        return probs / total if total > 0 else np.ones(self.num_cities) / self.num_cities

    def _construct_solution(self):
        route = [self.depot]
        visited = set(route)
        total_distance = 0
        current = self.depot

        while len(visited) < self.num_cities:
            probs = self._calculate_probabilities(current, visited)
            next_city = np.random.choice(range(self.num_cities), p=probs)

            if next_city in visited:
                continue  # Prevent looping

            visited.add(next_city)
            route.append(next_city)
            total_distance += self.distances[current][next_city]
            current = next_city

        # Return to depot
        total_distance += self.distances[current][self.depot]
        route.append(self.depot)

        return route, total_distance

    def run(self):
        best_route = None
        best_distance = float('inf')

        for _ in range(self.num_iterations):
            routes = []
            distances = []

            for _ in range(self.num_ants):
                route, dist = self._construct_solution()
                routes.append(route)
                distances.append(dist)

            min_idx = np.argmin(distances)
            if distances[min_idx] < best_distance:
                best_distance = distances[min_idx]
                best_route = routes[min_idx]

            # Evaporate and reinforce pheromones
            self.pheromones *= (1 - self.rho)
            for i in range(len(best_route) - 1):
                a, b = best_route[i], best_route[i + 1]
                self.pheromones[a][b] += 1.0 / best_distance

        return best_route, best_distance
    
    # Run ACO on the distance matrix
aco = AntColonyOptimizer(
    distance_matrix=distance_matrix,
    num_ants=10,
    num_iterations=200,
    alpha=1,
    beta=2,
    rho=0.5
)

# Run optimization
best_route_indices, best_distance = aco.run()

# Convert index route to city names
best_route_cities = [index_to_city[i] for i in best_route_indices]

# Print results
print("📍 Best Route (City Names):")
print(" ➡ ".join(best_route_cities))
print(f"\n📏 Total Distance: {best_distance:,.0f} meters")

# Visualize the route (step-by-step path)
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 3))
plt.plot(best_route_cities, marker='o', linestyle='--', color='teal')
plt.title("🚚 Best Delivery Route (ACO on Order Small)")
plt.xlabel("Step")
plt.ylabel("City")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
