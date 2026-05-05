from tradingview_ta import TA_Handler, Interval, Exchange
import streamlit as st
import pandas as pd
import os
import feedparser
import ccxt
import numpy as np
import streamlit.components.v1 as components

indicators = {
    "RSI": {
        "title": "⚡ RSI: Momentum & Trend Exhaustion",
        "desc": "The Relative Strength Index (RSI) is a momentum oscillator...",
        "video": "https://www.youtube.com/watch?v=z3fbVK5e5Io"
    },
    "MACD": {
        "title": "📊 MACD: The Momentum Cycle Engine",
        "desc": "The MACD is a trend-following momentum indicator...",
        "video": "https://www.youtube.com/watch?v=tSr6UorS9Ro"
    },
    "Fibonacci": {
        "title": "📐 Fibonacci: The Golden Ratio Protocol",
        "desc": "Fibonacci retracement levels are key reaction zones...",
        "video": "https://www.youtube.com/watch?v=oVMeymdZwWI"
    }
}

# --- TERMINAL CONFIG ---
st.set_page_config(page_title="Crypto Mastery", page_icon="📈", layout="wide")

# --- CUSTOM CSS (PREMIUM DARK TERMINAL) ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1117; color: #C9D1D9; }
    [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
    .section-card { 
        background-color: #161B22; padding: 35px; border-radius: 15px; 
        border: 1px solid #30363D; margin-bottom: 35px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .pillar-title { color: #f1c40f; font-size: 32px; font-weight: 800; margin-bottom: 15px; text-transform: uppercase; }
    .indicator-title { color: #58A6FF; font-size: 28px; font-weight: 800; margin-bottom: 10px; }
    .strategy-box { 
        background-color: #23863622; border-left: 5px solid #238636; 
        padding: 20px; margin: 20px 0; border-radius: 8px; font-size: 16px; line-height: 1.6;
    }
    .sidebar-title { color: #58A6FF; font-size: 22px; font-weight: 800; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">Crypto Mastery</p>', unsafe_allow_html=True)
    page = st.radio("MENU", ["Mastery (Learning)", "Indicators", "Charts", "Tools"])
    st.divider()
    st.caption("℗Romanstrades")

# --- Initialize session state ---
if "active_video" not in st.session_state:
    st.session_state.active_video = None

# --- Function to set active video ---
def load_video(url):
    st.session_state.active_video = url

# --- PAGE: INDICATORS ---
if page == "Indicators":
    st.markdown('<p class="pillar-title">Indicator Intelligence</p>', unsafe_allow_html=True)

    # --- Search (exact match only) ---
    search = st.text_input(
        "Search for an indicator (e.g. RSI, MACD)...",
        key="indicator_search"
    )

    # --- Only show result if exact match ---
    if search:
        key = search.strip().upper()

        if key in indicators:
            data = indicators[key]

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(f'<p class="indicator-title">{data["title"]}</p>', unsafe_allow_html=True)
            st.write(data["desc"])
            st.video(data["video"])
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.warning("Indicator not found. Make sure you type it exactly (e.g. RSI).")
    
# --- PAGE 1: MASTERY (LEARNING) ---
if page == "Mastery (Learning)":
    st.title("🏛️ Indicators")
    st.info("Advanced Technical Analysis & Market Psychology Protocol")
    
# --- PAGE 1: TECHNICAL ANALYSIS ---
if page == "Mastery (Learning)":
    st.divider()
    st.header("🏛️ Technical Analysis")

    # Define tabs here
    t1, t2, t3, t4, t5 = st.tabs([
        "🏦 Liquidity", 
        "🕯️ Price Action", 
        "🌊 Volume", 
        "📈 Structure", 
        "🌎 Fundamental"
    ])

    # =========================
    # 🏦 TAB 1: LIQUIDITY
    # =========================
    with t1:
        st.subheader("Liquidity & Whale Behavior")
        
        st.write("""
Liquidity is the lifeblood of markets — it’s what allows trades to be filled with minimal price disruption. 
Without liquidity, markets freeze, spreads widen, and execution becomes unpredictable.

### Why Liquidity Matters to Institutions
Large players such as banks, hedge funds, and whales cannot simply execute massive orders without harvesting enough opposing liquidity. 
To execute multi-million dollar trades without slippage, they look for layers of resting orders in the market — often around swing highs, swing lows, psychological round numbers, and retail stop clusters.

### How Liquidity Actually Works
Liquidity clusters where traders place orders:

- **Retail Stop Orders:** Many retail traders place stop losses above resistance (for shorts) and below support (for longs), creating liquidity pools — high-value targets for larger players.
- **Institutional Entry / Exit:** Big players often push price into liquidity pools, trigger stops, absorb the order flow, and then reverse direction. This is often misread as a breakout but is actually liquidity collection.

### Liquidity Sweeps (Liquidity Hunts)
A liquidity sweep occurs when price:
1. Pushes beyond a previous high/low to collect stops
2. Quickly reverses after liquidity is taken

Indicators of a liquidity sweep on the chart:
- Break beyond a structural high/low
- Quick rejection (wick + absorption)
- Volume spikes as stops are collected
- Sharp reversal into the previous structure

### How to Trade Liquidity
Instead of entering at obvious levels and risking stops:
- Wait for a liquidity sweep beyond a key level
- Look for quick rejection and reclaim
- Enter after liquidity is taken, trading the reaction

Key principle: **Don’t trade the liquidity target — trade the reaction.**

### Institutional Liquidity Setups

| Setup | What It Implies |
|-------|----------------|
| Break above old high with fast rejection | Liquidity sweep + smart money entry |
| Break below old low and reclaim | Bullish liquidity sweep |
| Pullback into prior imbalance after sweep | High-quality entry with institutional interest |

### Key Takeaways
- Liquidity drives price, not indicators  
- Institutions hunt clustered liquidity before big moves  
- Retail stops = targets for smart money  
- True edges occur after liquidity is captured  
- Wait for reaction, not touch
""")
        
        st.video("https://www.youtube.com/watch?v=6E__nsyA0a8")
        st.video("https://www.youtube.com/watch?v=qrLJgQUOceY")
        st.video("https://www.youtube.com/watch?v=nJqOwTHVA60")
        st.video("https://www.youtube.com/watch?v=X9bz--vwhvo")
        
    # =========================
    # 🕯️ TAB 2: PRICE ACTION
    # =========================
    with t2:
        st.subheader("🕯️ Price Action & Fair Value Gaps (FVG)")
        st.write("""
Price action is the purest reflection of supply and demand in the market, and Fair Value Gaps (FVGs) are one of the most powerful tools to identify imbalances and institutional activity.

### What is a Fair Value Gap?
A Fair Value Gap occurs when price moves so quickly that there is a space between candlesticks where no trading occurred. Essentially, it represents an imbalance in supply and demand.

- **Bullish FVG:** Appears after a strong upward move where the gap between two candles leaves a void below. Price often returns to fill this gap before continuing higher.
- **Bearish FVG:** Appears after a strong downward move where the gap between two candles leaves a void above. Price often returns to fill this gap before continuing lower.

FVGs are essentially footprints of institutional order flow — they indicate areas where smart money left orders unfilled.

### How to Spot FVGs on a Chart
1. Identify a strong impulse candle (long body) followed by another candle that does not overlap.
2. Mark the high and low of the first candle.
3. The area between these two candles is your Fair Value Gap.
4. Watch how price reacts when it returns to this area — these are high-probability trade zones.

### Price Action Principles Around FVGs
- **Imbalance Reclaim:** When price comes back to fill a gap, it usually retests with reduced momentum. This retest is an opportunity to trade with institutional flow.
- **Confirmation:** Look for rejection wicks, candlestick patterns, or confluence with previous support/resistance.
- **Trend Alignment:** FVG trades are stronger when aligned with the higher timeframe trend.

### How to Trade Fair Value Gaps
1. **Identify the gap:** Spot strong moves leaving an imbalance.
2. **Wait for price to approach:** Don’t enter on the first impulse; wait for a retracement.
3. **Look for reaction:** Candlestick rejection, confluence with key levels, or liquidity pools nearby.
4. **Enter with tight stop:** Place your stop just beyond the gap or beyond the next liquidity level.
5. **Target continuation:** Price often moves back in the original direction after filling the FVG.

### Example Scenarios
| Scenario | FVG Setup | Trade Idea |
|----------|-----------|-----------|
| Uptrend | Bullish FVG created | Wait for retracement to FVG, enter long after rejection |
| Downtrend | Bearish FVG created | Wait for retracement to FVG, enter short after rejection |
| Range Breakout | Gap forms after breakout | Use FVG as a pullback entry for continuation |

### Key Takeaways
- FVGs are footprints of institutional activity and liquidity imbalances.  
- Always trade the reaction to the gap, not the initial impulse.  
- Combine FVG analysis with trend direction and other liquidity concepts for the highest probability setups.  
- Fair Value Gaps exist across all timeframes — higher timeframes often provide more reliable signals.  
""")
        
        st.video("https://www.youtube.com/watch?v=3x4FQqf7X0E")
        st.video("https://www.youtube.com/watch?v=jLxGqGZhzq4")
        st.video("https://www.youtube.com/watch?v=7eU0kZyZejk")
    
    # =========================
    # 🌊 TAB 3: VOLUME
    # =========================
    with t3:
        st.subheader("🌊 Advanced Volume & Effort vs. Result")
        st.write("""
Volume is one of the clearest ways to see what the smart money is doing. But raw volume alone isn’t enough — understanding the relationship between **effort (volume)** and **result (price movement)** gives you a window into supply and demand dynamics.

### Effort vs. Result (Wyckoff Principle)
- **Effort:** Measured by the size of the volume bars.
- **Result:** Measured by the actual price movement that volume produces.
- The key idea: **large effort with little result indicates absorption**, while **small effort with large result indicates momentum**.

### How to Interpret Volume
1. **High Volume + Big Move:** Confirms trend continuation.
2. **High Volume + Small Move:** Shows absorption — smart money is buying/selling without letting price run.
3. **Low Volume + Big Move:** Low participation — likely weak and unsustainable.
4. **Low Volume + Small Move:** Market is consolidating; waiting for liquidity.

### Liquidity Insights with Volume
- Watch where volume spikes occur — usually near **support/resistance, FVGs, or liquidity pools**.  
- Institutional players create **fake breakouts** to capture liquidity — volume gives clues if they’re absorbing or pushing.

### Practical Trading Ideas
- **Accumulation Phase:** High effort with little price drop → potential long setup.
- **Distribution Phase:** High effort with little price rise → potential short setup.
- **Breakouts:** Validate with volume. A real breakout usually shows **effort aligned with result**.
- **Liquidity Sweeps:** Price moves rapidly to trigger stops; look for corresponding volume spikes for confirmation.

### Volume + Price Action Confluence
- Combine with **FVGs, support/resistance, and liquidity pools**.  
- Example: Price returns to a bullish FVG with a **volume spike showing absorption** → high-probability long trade.

### Key Takeaways
- Never trade volume alone — always analyze **effort vs. result**.  
- Institutional activity is often revealed through **disproportionate effort**.  
- Look for areas where volume confirms or contradicts price movement to find high-probability setups.  
- Using volume with **liquidity concepts and FVGs** gives a complete picture of the market’s hidden order flow.
""")
        
        st.video("https://www.youtube.com/watch?v=4C9F9R3QK2E")
        st.video("https://www.youtube.com/watch?v=L9zKkeo3BjQ")
        st.video("https://www.youtube.com/watch?v=8F7g5yHn3h0")
    
    # =========================
    # 📈 TAB 4: STRUCTURE
    # =========================
    with t4:
        st.subheader("📈 Technical Market Structure (MSB)")
        st.write("""
Understanding **market structure** is essential for trading like smart money. Market structure tells you **where price is likely headed**, and where liquidity might be targeted.

### Basics of Market Structure
- **Higher Highs / Higher Lows (HH/HL):** Bullish trend
- **Lower Highs / Lower Lows (LH/LL):** Bearish trend
- **Break of Structure (BOS):** When price breaks a previous high or low, indicating a potential trend change
- **Change of Character (CHoCH):** A shift in trend momentum; often confirms liquidity sweep or smart money activity

### Liquidity & Market Structure
- Smart money targets **clusters of liquidity**, often just beyond obvious highs or lows.
- BOS or CHoCH moves are often **fakeouts designed to capture liquidity** before reversing.
- Watch for **stop hunts**: price triggers retail stop losses at obvious levels, then reverses in line with institutional positioning.

### Combining MSB with Price Action & Liquidity
1. Identify **key swing highs and lows** to map market structure.
2. Look for **FVGs** or gaps near these swings for potential entries.
3. Monitor **volume** to confirm institutional activity — effort vs. result gives clues if a move is real or a liquidity sweep.
4. Confirm trend continuation or reversal by analyzing if **price respects or breaks structure** with confluence from liquidity zones.

### Practical Tips
- Don’t just trade breakouts — wait for **retests after BOS/CHoCH**.
- Align entries with **high-probability setups**: liquidity pool sweeps, reclaimed levels, and supporting volume.
- Use MSB to **filter trades**: avoid trading against dominant structure unless there’s strong liquidity/volume evidence.

### Key Takeaways
- Market structure identifies **trend direction and hidden liquidity targets**.
- BOS and CHoCH are your signals to watch for **institutional involvement**.
- Always combine **MSB + FVG + Liquidity + Volume** for the most reliable setups.
- Trading in alignment with market structure reduces risk and increases probability of success.
""")
        
        st.video("https://www.youtube.com/watch?v=EJ3W0fJZP1A")
        st.video("https://www.youtube.com/watch?v=6sXvMvRLF5o")
    
    # =========================
    # 🌎 TAB 5: FUNDAMENTALS
    # =========================
    with t5:
        st.subheader("🌎 Macro Fundamentals & DXY Correlation")
        st.write("""
Understanding **macro fundamentals** is crucial for anticipating market moves and aligning with smart money flows. Large institutions pay attention to global economic conditions, interest rates, and currency strength, especially the **US Dollar Index (DXY)**.

### Why Macro Matters
- Interest rate changes, central bank policies, and economic data releases influence liquidity and volatility.
- Major macro events can **cause sudden moves**, triggering stop hunts and liquidity sweeps.
- Aligning trades with macro context increases the probability of success and reduces risk of trading against institutional flow.

### DXY Correlation
- Many markets, especially crypto and commodities, are inversely correlated with the DXY.
    - **DXY up → USD strengthens → risk assets (crypto, gold) often fall**
    - **DXY down → USD weakens → risk assets often rise**
- Monitoring DXY helps predict potential **liquidity targeting** zones, as institutional traders may rotate capital based on USD strength.

### Combining Macro + Liquidity + Structure
1. Identify **key macro events** (Fed decisions, CPI, employment reports, etc.) on your calendar.
2. Observe **DXY movements** for trend alignment.
3. Map **market structure and liquidity zones** in your target asset.
4. Confirm trades with **volume and FVGs** for high-probability setups.

### Practical Tips
- Don’t trade large macro events blindly — wait for price to **react to liquidity and structure**.
- Use DXY as a **guide**, not a sole signal; combine with liquidity analysis.
- Historical patterns around economic releases can highlight **where liquidity pools may form**.

### Key Takeaways
- Macro fundamentals set the **context for institutional flow**.
- DXY correlation is a powerful tool to **predict directional bias** in risk assets.
- Combine macro analysis with liquidity, MSB, and FVGs for **well-aligned trades**.
""")
        
        st.video("https://www.youtube.com/watch?v=xU1S0DxrNJM")
        st.video("https://www.youtube.com/watch?v=8jK3dDBhK0Y")

# --- PAGE 2: CHARTS ---
if page == "Charts":
    st.title("📊 Chart")

    symbol_map = {
        "BTC": "BINANCE:BTCUSDT", "ETH": "BINANCE:ETHUSDT", "SOL": "BINANCE:SOLUSDT",
        "XRP": "BINANCE:XRPUSDT", "ONDO": "BYBIT:ONDOUSDT", "BNB": "BINANCE:BNBUSDT",
        "Silver": "TVC:SILVER", "Gold": "TVC:GOLD", "Oil": "TVC:UKOIL",
        "S&P 500": "SPY", "AAPL": "NASDAQ:AAPL", "NVDA": "NASDAQ:NVDA"
    }

    st.markdown("### 🖥️ Watchlist")
    cols = st.columns(4)
    asset_keys = list(symbol_map.keys())

    if 'selected_asset' not in st.session_state:
        st.session_state.selected_asset = "BTC"

    for i, asset in enumerate(asset_keys):
        if cols[i % 4].button(f" {asset} ", use_container_width=True):
            st.session_state.selected_asset = asset
            st.rerun()

    target_symbol = symbol_map[st.session_state.selected_asset]

    chart_html = f"""
    <div id="tradingview_widget"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "width": "100%", "height": 600, "symbol": "{target_symbol}",
      "interval": "D", "timezone": "Asia/Kuala_Lumpur",
      "theme": "dark", "style": "1", "container_id": "tradingview_widget"
    }});
    </script>
    """
    components.html(chart_html, height=620)

    # --- POSITION SIZER & RISK CALCULATOR ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">🧮 100x Position Sizer</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        coin = st.text_input("Coin Symbol", placeholder="e.g., XRP").upper()
        capital = st.number_input("Capital (USD)", min_value=0.0, help="Your balance before leverage")
        leverage = st.number_input("Leverage", min_value=1.0, value=1.0, step=1.0)
        
    with col2:
        entry = st.number_input("Entry Price", min_value=0.0, step=0.0001, format="%.4f")
        sl = st.number_input("Stop Loss Price", min_value=0.0, step=0.0001, format="%.4f")
        tp = st.number_input("Take Profit Price", min_value=0.0, step=0.0001, format="%.4f")

    if st.button("Calculate Risk & Reward", use_container_width=True):
        if not coin or capital <= 0 or entry <= 0:
            st.error("Please fill in all fields with valid numbers.")
        else:
            # Determine trade type (Logic from popup.js)
            is_long = tp > entry
            
            # Validate Stop Loss (Logic from popup.js)
            if (is_long and sl >= entry) or (not is_long and sl <= entry):
                st.error("🚨 Invalid Stop Loss for this trade!")
            else:
                # Calculations including leverage
                position_size = capital * leverage
                amount_coin = position_size / entry
                
                # P&L in USD based on direction
                pnl_tp = (tp - entry) * amount_coin if is_long else (entry - tp) * amount_coin
                pnl_sl = (entry - sl) * amount_coin if is_long else (sl - entry) * amount_coin
                
                # Percentage gain/loss relative to actual capital
                percent_gain = (pnl_tp / capital) * 100
                percent_loss = (pnl_sl / capital) * 100
                
                # Risk:Reward ratio
                rrr = abs(pnl_tp / pnl_sl) if pnl_sl != 0 else 0

                # Professional Terminal Output
                st.markdown("---")
                st.subheader(f"📈 {coin} {'LONG' if is_long else 'SHORT'} Overview")
                
                res_col1, res_col2, res_col3 = st.columns(3)
                res_col1.metric("Potential Gain", f"${abs(pnl_tp):.2f}", f"{percent_gain:.2f}%")
                res_col2.metric("Potential Loss", f"-${abs(pnl_sl):.2f}", f"-{abs(percent_loss):.2f}%", delta_color="inverse")
                res_col3.metric("R:R Ratio", f"1 : {rrr:.2f}")
                
                if rrr < 2.0:
                    st.warning("⚠️ Low Risk:Reward ratio. Ensure this aligns with your Pillars.")
                else:
                    st.success("✅ High R:R trade detected.")
    st.markdown('</div>', unsafe_allow_html=True)
        
# --- PAGE 3: TOOLS ---
if page == "Tools":
    st.title("⚒️ Professional Trading Tools")
    
    # Create tabs
    t_journal, t_compound, t_dca, t_be, t_pos, t_stress, t_sentiment = st.tabs([
        "📊 Journal",
        "📈 Compound",
        "🎯 DCA",
        "⚖️ Breakeven",
        "📏 Position %",
        "⚠️ Stress Test",
        "🧠 Sentiment"
    ])

    # -----------------------------
    # 1. TRADING JOURNAL
    # -----------------------------
    with t_journal:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="indicator-title">📝 Institutional Trade Log</p>', unsafe_allow_html=True)

        # Initialize session state
        if 'history' not in st.session_state:
            st.session_state.history = []

        # Trade log form
        with st.form("log_trade"):
            c1, c2, c3 = st.columns(3)
            t_type = c1.selectbox("Type", ["LONG", "SHORT"])
            t_cap = c1.number_input("Capital ($)", min_value=0.0, value=100.0)
            t_lev = c2.number_input("Leverage", min_value=1, value=10)
            p_mode = c2.radio("Input", ["%", "$"])
            t_val = c3.number_input("P&L Value", value=0.0)

            if st.form_submit_button("Log Position"):
                usd = t_val if p_mode == "$" else (t_val/100)*t_cap
                pct = t_val if p_mode == "%" else (t_val/t_cap)*100
                st.session_state.history.append({
                    "Type": t_type,
                    "Capital": t_cap,
                    "P&L $": usd,
                    "P&L %": pct
                })

        # Display trade history table
        if st.session_state.history:
            st.table(pd.DataFrame(st.session_state.history))

        # Clear button (outside the form)
        if st.button("Clear Journal"):
            st.session_state.history = []
            st.experimental_rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # 2. COMPOUND CALCULATOR
    # -----------------------------
    with t_compound:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="indicator-title">🚀 Compound Calculator</p>', unsafe_allow_html=True)

        s_bal = st.number_input("Starting Capital ($)", min_value=0.0, value=0.0, key="comp_s")
        n_doubles = st.number_input("Times to Double", min_value=0, step=1, value=0, key="comp_n")

        if st.button("Enter", key="compound_btn"):
            if s_bal <= 0 or n_doubles <= 0:
                st.warning("Please enter valid values for both fields.")
            else:
                data = []
                current = s_bal

                for i in range(n_doubles + 1):
                    data.append({
                        "Step": i,
                        "Balance ($)": current
                    })
                    current *= 2

                df = pd.DataFrame(data)

                st.markdown("### Growth Table")
                st.dataframe(df, use_container_width=True)

                st.metric("Final Balance", f"${df.iloc[-1]['Balance ($)']:,.2f}")

        st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # 3. DCA CALCULATOR
    # -----------------------------
    with t_dca:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="indicator-title">🎯 DCA Average Entry</p>', unsafe_allow_html=True)
        col_d1, col_d2 = st.columns(2)
        p1 = col_d1.number_input("Price 1", value=60000.0, key="dca_p1")
        a1 = col_d1.number_input("Amount 1", value=500.0, key="dca_a1")
        p2 = col_d2.number_input("Price 2", value=55000.0, key="dca_p2")
        a2 = col_d2.number_input("Amount 2", value=500.0, key="dca_a2")
        if p1 > 0 and p2 > 0:
            avg = (a1 + a2) / ((a1/p1) + (a2/p2))
            st.metric("Weighted Average", f"${avg:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # 4. BREAKEVEN CALCULATOR
    # -----------------------------
    with t_be:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="indicator-title">⚖️ Breakeven Finder</p>', unsafe_allow_html=True)
        be_p = st.number_input("Entry Price", value=50000.0, key="be_p")
        be_f = st.number_input("Fee % (One-way)", value=0.06, format="%.3f", key="be_f")
        st.metric("Exit Price for $0 Loss", f"${be_p * (1 + (be_f/100)*2):,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # 5. POSITION SIZE %
    # -----------------------------
    with t_pos:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="indicator-title">📏 Margin Converter</p>', unsafe_allow_html=True)
        w_bal = st.number_input("Wallet Balance ($)", value=1000.0, key="pos_w")
        r_pct = st.slider("Wallet % to Risk", 1, 100, 10, key="pos_r")
        l_used = st.number_input("Leverage (x)", value=10, key="pos_l")
        st.metric("Bybit Margin Required", f"${(w_bal * (r_pct/100)) / l_used:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # 6. LEVERAGE STRESS TEST
    # -----------------------------
    with t_stress:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="indicator-title">⚠️ Leverage Stress Test</p>', unsafe_allow_html=True)
        st_p = st.number_input("Entry Price", value=50000.0, key="stress_p")
        st_l = st.slider("Leverage", 1, 100, 20, key="stress_l")
        st.error(f"Liquidation Point: {100/st_l:.2f}% price drop.")
        st.warning(f"A 1% move results in a {1 * st_l}% P&L change.")
        st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # 7. MARKET SENTIMENT
    # -----------------------------
    with t_sentiment:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.image("https://alternative.me/crypto/fear-and-greed-index.png", caption="Fear & Greed Index")
        
        st.markdown('</div>', unsafe_allow_html=True)
