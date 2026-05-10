-- ======================================================================
-- BLACKROCK BUIDL: ON-CHAIN INSTITUTIONAL CAPITAL FLOW
-- Description: Tracking daily Mint (Inflows) and Burn (Outflows) events 
--              to calculate Net Flow and Total Value Locked (TVL).
-- ======================================================================

WITH buidl_transfers AS (
    -- Extract raw ERC-20 transfer logs specifically for the BUIDL token
    SELECT
        DATE_TRUNC('day', evt_block_time) AS block_date,
        "from",
        "to",
        value / 1e6 AS amount -- BUIDL token uses 6 decimals
    FROM erc20_ethereum.evt_Transfer
    WHERE contract_address = 0x7712c34205737192402172409a8F7ccef8aA2AEc -- BlackRock BUIDL Smart Contract
),

daily_inflow AS (
    -- Calculate Daily Institutional Inflows (Minting)
    -- Tokens transferred FROM the null address indicate new fiat capital entering the fund
    SELECT 
        block_date, 
        SUM(amount) AS minted_volume_usd
    FROM buidl_transfers
    WHERE "from" = 0x0000000000000000000000000000000000000000
    GROUP BY block_date
),

daily_outflow AS (
    -- Calculate Daily Institutional Outflows (Burning / Redemptions)
    -- Tokens transferred TO the null address indicate capital returning to TradFi (fiat)
    SELECT 
        block_date, 
        SUM(amount) AS burned_volume_usd
    FROM buidl_transfers
    WHERE "to" = 0x0000000000000000000000000000000000000000
    GROUP BY block_date
)

-- Aggregate inflows and outflows to calculate Net Flow and Continuous TVL
SELECT 
    COALESCE(i.block_date, o.block_date) AS date,
    COALESCE(i.minted_volume_usd, 0) AS daily_mint_usd,
    COALESCE(o.burned_volume_usd, 0) AS daily_burn_usd,
    
    -- Net Flow = Minted Volume - Burned Volume
    COALESCE(i.minted_volume_usd, 0) - COALESCE(o.burned_volume_usd, 0) AS net_flow_usd,
    
    -- Total Value Locked (TVL): Cumulative sum of Net Flow over time using Window Function
    SUM(COALESCE(i.minted_volume_usd, 0) - COALESCE(o.burned_volume_usd, 0)) 
        OVER (ORDER BY COALESCE(i.block_date, o.block_date)) AS total_tvl_usd
        
FROM daily_inflow i
FULL OUTER JOIN daily_outflow o ON i.block_date = o.block_date
ORDER BY date DESC;