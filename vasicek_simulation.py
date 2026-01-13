import numpy as np
import matplotlib.pyplot as plt

# --- 1. PARAMETRI DEL MODELLO (Vasicek) ---
r0 = 0.03       # Tasso iniziale (3%)
kappa = 0.5     # Velocità di mean reversion
theta = 0.05    # Tasso target di lungo periodo (5%)
sigma = 0.02    # Volatilità costante

# --- 2. PARAMETRI SIMULAZIONE ---
T = 5.0         # Orizzonte temporale (anni)
N_steps = 100   # Numero di step temporali
dt = T / N_steps
N_paths = 5000  # Numero di "particelle"

# --- 3. INIZIALIZZAZIONE ---
rates = np.zeros((N_steps + 1, N_paths))
rates[0, :] = r0

# --- 4. CALCOLO (Simulazione) ---
np.random.seed(42) # Seed fisso per risultati riproducibili

for t in range(N_steps):
    Z = np.random.normal(0, 1, N_paths)
    r_t = rates[t, :]
    
    # Eulero: r(t+1) = r(t) + drift + diffusion
    drift = kappa * (theta - r_t) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    
    rates[t+1, :] = r_t + drift + diffusion

# --- 5. VISUALIZZAZIONE "SIDE-BY-SIDE" ---
plt.figure(figsize=(12, 6)) # Allarghiamo la figura per farcene stare due

# GRAFICO DI SINISTRA: I Percorsi
plt.subplot(1, 2, 1) # (1 riga, 2 colonne, grafico n.1)
time_grid = np.linspace(0, T, N_steps+1)
# Disegniamo solo i primi 50 percorsi
plt.plot(time_grid, rates[:, :50], alpha=0.3, lw=1)
# Disegniamo la media di tutte le particelle (linea nera tratteggiata)
plt.plot(time_grid, np.mean(rates, axis=1), 'k--', lw=2, label='Media Particelle')
# Linea rossa per il target teorico (Theta)
plt.axhline(theta, color='r', linestyle=':', label='Target (Theta)')

plt.title(f'Percorsi Vasicek (Mean Reversion)')
plt.xlabel('Tempo (Anni)')
plt.ylabel('Tasso di Interesse')
plt.legend()
plt.grid(True, alpha=0.3)

# GRAFICO DI DESTRA: La Distribuzione Finale
plt.subplot(1, 2, 2) # (1 riga, 2 colonne, grafico n.2)
final_rates = rates[-1, :]
plt.hist(final_rates, bins=50, density=True, alpha=0.6, color='skyblue', edgecolor='black', label='Simulazione')

# Linee di riferimento
plt.axvline(theta, color='red', linestyle='--', linewidth=2, label=f'Target ({theta})')
plt.axvline(np.mean(final_rates), color='green', linestyle='-', linewidth=2, label='Media Finale')

plt.title('Distribuzione Finale (T=5 anni)')
plt.xlabel('Tasso')
plt.ylabel('Densità')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout() # Evita che le scritte si sovrappongano
plt.show()