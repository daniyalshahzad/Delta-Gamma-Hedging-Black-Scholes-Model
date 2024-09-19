# Delta-Gamma Hedging in the Black-Scholes Model
## Project Overview
This project investigates Delta and Delta-Gamma hedging strategies within the Black-Scholes model. The goal is to understand how these hedging techniques mitigate risks associated with changes in the underlying asset price and the option's delta. The project involves selling 10,000 at-the-money call options and hedging them by trading in the asset, another at-the-money call with a different maturity, and the bank account. Transaction costs and real-world volatility are accounted for in the analysis, providing practical insight into these hedging strategies under different market conditions.

## Abstract
This report presents a comprehensive analysis of delta and delta-gamma hedging strategies within the Black-Scholes framework. We look at the foundational theories of delta and gamma hedging and illustrate their roles in offsetting option price changes due to movements in the underlying asset. Our analysis utilizes the Black-Scholes model to construct delta-neutral and gamma-neutral portfolios, aiming to mitigate risks associated with both price changes in the underlying asset and variations in the option’s delta. We explore the implications of these hedging strategies through empirical simulations and examine the distribution of profit and loss under different market conditions and assumptions. We study the impacts of varying transaction costs, real-world volatility of the underlying asset, and different values of real-world drift. This report provides an understanding of these hedging techniques and highlights their practical applications in real-world financial scenarios.

## Key Results
Delta vs Delta-Gamma Hedging: Profit and loss distributions were compared between Delta and Delta-Gamma hedging using 5,000 simulated paths. The results show how these strategies vary with changes in the drift parameter (μ).

Position Analysis: For two sample paths—one that ends in the money and one out of the money—the positions held in the asset and the hedging option were analyzed for both Delta and Delta-Gamma hedging.

Impact of Real-World Volatility: Simulations were conducted with real-world volatilities (σ) varying between 20% and 30%. The analysis compared the P&L under Delta and Delta-Gamma hedging while assuming that the hedger uses volatility of 25%.

## Methodology
Simulations: 5,000 Monte Carlo simulations of asset price paths were run to study the hedging strategies. Hedging was performed daily over a 63-day period.
Transaction Costs: A transaction cost of $0.005 per share and per option was applied in all hedging strategies.
Volatility Testing: Real-world volatilities in the range of 20% to 30% were compared to the assumed volatility of 25%, providing insights into the effectiveness of the hedging strategies when volatility assumptions are incorrect.
## How to Run
The project implementation can be found in the main.ipynb and its dependencies. All simulations, plots, and analysis are included in the notebook.

For more detailed results, refer to the report.pdf file.