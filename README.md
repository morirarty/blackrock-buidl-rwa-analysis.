# 🏦 Decoding TradFi Capital: BlackRock BUIDL On-Chain Flow

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Dune Analytics](https://img.shields.io/badge/Dune_API-000000?style=for-the-badge&logo=dune&logoColor=white)

## 📌 Executive Summary
While retail markets focus on price action, institutional capital is quietly building infrastructure via **Real World Assets (RWA)**. This project tracks the on-chain footprint of the largest player in the space: **BlackRock’s BUIDL Fund**. 

By bypassing standard aggregators and querying raw smart contract logs directly from the Ethereum mainnet via the **Dune API**, this project models the continuous Total Value Locked (TVL) and daily capital flows (Minting/Burning) of institutional money.

## 📊 Dashboard & Visualizations
*(Upload your generated chart `blackrock_buidl_analysis.png` to your GitHub repo, and replace this text with the image. Example: `![BUIDL Chart](blackrock_buidl_analysis.png)` )*

### Key Macro Insights:
1. **Capital Inflows (Minting):** Identifies specific periods of heavy institutional accumulation, mapped against broader macroeconomic events.
2. **Capital Flight (Burning):** Tracks major redemption events where institutions pulled liquidity back to fiat, visually represented by sharp downward spikes in Net Flow.
3. **Macro TVL Trend:** The cumulative pink line visualizes the relentless, fundamental growth of BlackRock's tokenized treasury fund despite market volatility.

## 🛠️ Architecture & Methodology
Instead of relying on third-party APIs, this pipeline extracts fundamental truth directly from the EVM logs:

* **Data Extraction:** Utilized **SQL** on Dune Analytics to query `erc20_ethereum.evt_Transfer` specifically for the BUIDL contract (`0x7712c...`).
* **On-Chain Logic:**
  * **Minting (Inflows):** Detected when tokens are transferred **FROM** the null address (`0x0000000000000000000000000000000000000000`).
  * **Burning (Outflows):** Detected when tokens are transferred **TO** the null address.
* **Data Transformation:** Leveraged **Python (Pandas)** via the Dune API to calculate Daily Net Flow and the cumulative sum (TVL).
* **Visualization:** Engineered a dual-axis financial chart using **Matplotlib** with a dark-mode aesthetic suitable for Web3 analytics.

## 🚀 How to Run the Pipeline
1. Clone this repository.
2. Ensure you have your `DUNE_API_KEY` and the specific `QUERY_ID`.
3. Install dependencies: `pip install pandas matplotlib requests`
4. Run the Python notebook/script to fetch live on-chain data and generate the chart.

---
