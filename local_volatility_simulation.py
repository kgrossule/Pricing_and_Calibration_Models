import numpy as np
import matplotlib.pyplot as plt

# --- 1. PARAMETRI ---
S0 = 100.0      # Prezzo iniziale
mu = 0.05       # Drift (trend di crescita del 5%)
T = 1.0         # 1 anno
N_steps = 252   # Giorni lavorativi in un anno
dt = T / N_steps
N_paths = 10000 # 10.000 scenari (Particelle)

# --- 2. LA FUNZIONE DI VOLATILITÀ LOCALE ---
# Questa è la novità! Non è più un numero, è una funzione.
# Formula: sigma(S) = 20% * radice(100 / S)
# - Se S = 100, sigma = 20%
# - Se S = 50 (crollo), sigma sale al 28% (Panico!)
# - Se S = 200 (boom), sigma scende al 14% (Calma)
def local_vol_function(S_current):
    # Usiamo np.maximum per evitare divisioni per zero se S va a 0
    valore_sicuro = np.maximum(S_current, 0.001)
    return 0.2 * np.sqrt(100.0 / valore_sicuro)

# --- 3. INIZIALIZZAZIONE ---
S = np.zeros((N_steps + 1, N_paths))
S[0, :] = S0

# --- 4. SIMULAZIONE (PARTICLE METHOD STEP-BY-STEP) ---
np.random.seed(42)

for t in range(N_steps):
    # Generiamo il caso
    Z = np.random.normal(0, 1, N_paths)
    
    # Prendiamo i prezzi attuali di tutte le particelle
    S_t = S[t, :]
    
    # >>> IL CUORE DEL MODELLO <<<
    # Calcoliamo una volatilità diversa per OGNI particella
    sigma_t = local_vol_function(S_t)
    
    # Evoluzione (Moto Browniano Geometrico con Volatilità Locale)
    # dS = S * mu * dt + S * sigma(S) * dW
    drift = S_t * mu * dt
    diffusion = S_t * sigma_t * np.sqrt(dt) * Z
    
    S_new = S_t + drift + diffusion
    
    # Barriera: impediamo ai prezzi di diventare negativi
    S[t+1, :] = np.maximum(S_new, 0.001)

# --- 5. VISUALIZZAZIONE ---
plt.figure(figsize=(12, 6))

# GRAFICO A: I Percorsi
plt.subplot(1, 2, 1)
# Ne mostriamo solo 50
plt.plot(np.linspace(0, T, N_steps+1), S[:, :50], alpha=0.4, lw=1)
plt.plot(np.linspace(0, T, N_steps+1), np.mean(S, axis=1), 'k--', lw=2, label='Media')
plt.title('Percorsi con Volatilità Locale (Inverse Leverage)')
plt.xlabel('Tempo (Giorni)')
plt.ylabel('Prezzo')
plt.legend()
plt.grid(True, alpha=0.3)

# GRAFICO B: La Distribuzione Finale (Skew)
plt.subplot(1, 2, 2)
final_prices = S[-1, :]
plt.hist(final_prices, bins=60, density=True, alpha=0.6, color='orange', edgecolor='black')
plt.axvline(S0, color='red', linestyle='--', label='Start (100)')
plt.title('Distribuzione Finale Asimmetrica')
plt.xlabel('Prezzo a 1 anno')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()




