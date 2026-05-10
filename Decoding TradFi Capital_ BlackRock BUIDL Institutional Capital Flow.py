# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.23.5",
#     "matplotlib==3.10.9",
#     "pandas==3.0.2",
#     "requests==2.33.1",
# ]
# ///

import marimo

__generated_with = "0.23.5"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    import requests

    # ==========================================
    # 1. DUNE API CONFIGURATION
    # ==========================================
    # Replace with your BUIDL SQL Query ID from Dune Analytics
    QUERY_ID = '7463852'  # Example: '3541238'

    # Replace with your Dune Analytics API Key
    API_KEY = 'iEuaSNBZeMLZcwoqQdAqWa1uVUgyQ8d3'

    # Dune API v1 endpoint to fetch the latest query results
    url = f"https://api.dune.com/api/v1/query/{QUERY_ID}/results"
    headers = {"x-dune-api-key": API_KEY}

    print("Fetching data from Dune Analytics API...")
    response = requests.get(url, headers=headers)
    data = response.json()

    # ==========================================
    # 2. DATA EXTRACTION & PANDAS TRANSFORMATION
    # ==========================================
    if 'result' in data and 'rows' in data['result']:
        # Convert the API JSON response into a Pandas DataFrame
        df = pd.DataFrame(data['result']['rows'])
        print(f"Successfully fetched {len(df)} rows of on-chain data!")
    else:
        raise ValueError(f"Failed to fetch data. Please check your API Key/Query ID. Error: {data}")

    # Ensure the date column is in datetime format and sorted chronologically
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # If your SQL only outputs daily_mint_usd and daily_burn_usd,
    # we can perform the transformation programmatically in Python:
    if 'net_flow_usd' not in df.columns:
        # Net Flow = Institutional Inflows (Mint) - Outflows (Burn)
        df['net_flow_usd'] = df['daily_mint_usd'] - df['daily_burn_usd']

    if 'total_tvl_usd' not in df.columns:
        # Total Value Locked = Cumulative Sum of daily Net Flow
        df['total_tvl_usd'] = df['net_flow_usd'].cumsum()

    # ==========================================
    # 3. DUAL-AXIS VISUALIZATION V2 (CLEANER & INSIGHTFUL)
    # ==========================================
    plt.style.use('dark_background')

    # Widen the canvas so the 462 days of data don't look cluttered
    fig, ax1 = plt.subplots(figsize=(15, 8))

    color_net_flow = '#30e3ca'  # Cyan for Net Flow
    color_tvl = '#ff4b5c'       # Bright pink/red for TVL

    # --- Left Y-Axis (Bar Chart: Daily Net Flow) ---
    # Use width=1.5 to make the bars more visible
    ax1.bar(df['date'], df['net_flow_usd'], color=color_net_flow, alpha=0.6, width=1.5, label='Daily Net Flow (Mint/Burn)')
    ax1.set_ylabel('Daily Net Flow (USD)', color=color_net_flow, fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color_net_flow)

    # Add a horizontal line at Zero (0) as a neutral baseline
    ax1.axhline(0, color='white', linewidth=1, alpha=0.5, linestyle='--')

    # --- Right Y-Axis (Line Chart: Cumulative TVL) ---
    # This is the core insight!
    ax2 = ax1.twinx()
    ax2.plot(df['date'], df['total_tvl_usd'], color=color_tvl, linewidth=3.5, label='Total TVL (Accumulation)')
    ax2.set_ylabel('Total Value Locked (USD)', color=color_tvl, fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=color_tvl)

    # --- Format Numbers (e.g., Convert 100000000 to $100M) ---
    def millions(x, pos):
        return f'${x*1e-6:.0f}M'

    ax1.yaxis.set_major_formatter(FuncFormatter(millions))
    ax2.yaxis.set_major_formatter(FuncFormatter(millions))

    # --- Overall Aesthetics & Formatting ---
    plt.title('BlackRock BUIDL: Institutional Capital Flow & Macro TVL', fontsize=18, fontweight='bold', pad=25)
    ax1.grid(color='gray', alpha=0.15, linestyle='-')

    # Combine legends from both axes for a cleaner look
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', frameon=True, facecolor='black')

    # Improve date formatting on x-axis
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()

    # Display the plot
    plt.show()


    return


if __name__ == "__main__":
    app.run()
