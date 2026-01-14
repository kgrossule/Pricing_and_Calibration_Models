# Financial Volatility Simulations 📈

This repository contains Python experiments to explore how different volatility assumptions affect financial simulations. 

The goal is to compare "textbook" models (constant volatility) with more realistic approaches (local volatility) and visualize the difference in risk distributions.

## 📂 Project Structure

### 1. Vasicek Model (Interest Rates)
* **File:** `vasicek_simulation.py`
* **Concept:** Mean Reversion.
* **The Model:** Simulates interest rates that fluctuate but tend to return to a long-term target (Mean Reversion).
* **Key Assumption:** Volatility is **constant**.
* **Visual Output:**
    * Paths show a "funnel" of uncertainty over time.
    * The final distribution is a perfect **Normal (Gaussian) curve**.
    * *Limitation observed:* The model allows rates to become negative and treats upside/downside risk symmetrically.

### 2. Local Volatility Model (Stock Prices)
* **File:** `local_volatility_simulation.py`
* **Concept:** Inverse Leverage Effect & Fat Tails.
* **The Model:** Simulates stock prices using a geometric framework where volatility depends on the price level.
* **Key Assumption:** Volatility is **dynamic**.
    * **Formula used:**
      $$\sigma(S_t) = 0.20 \times \sqrt{\frac{100}{S_t}}$$
    * *Logic:* When prices drop ($S < 100$), the term under the square root becomes $>1$, increasing volatility (panic). When prices rise, volatility decreases (calm).
* **Visual Output:**
    * Downside paths appear more "nervous" than upside paths.
    * The final distribution is **Asymmetric (Skewed)** with a fatter left tail.
    * *Reality check:* This better represents the "crash risk" seen in real equity markets compared to the Normal distribution.

## 🛠️ Requirements

* Python 3.x
* NumPy
* Matplotlib

To run the simulations:
```bash
python vasicek_simulation.py
python local_volatility_simulation.py
