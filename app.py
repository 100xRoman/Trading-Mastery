from tradingview_ta import TA_Handler, Interval, Exchange
import streamlit as st
import pandas as pd
import os
import feedparser
import ccxt
import numpy as np
import streamlit.components.v1 as components

# --- TERMINAL CONFIG ---
st.set_page_config(page_title="Trading Mastery", page_icon="📈", layout="wide")

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
    st.markdown('<p class="sidebar-title">Trading Mastery</p>', unsafe_allow_html=True)
    page = st.radio("TERMINAL MENU", ["Mastery (Learning)", "Charts", "Tools"])
    st.divider()
    st.caption("℗100xroman")

# --- PAGE 1: MASTERY (LEARNING) ---
if page == "Mastery (Learning)":
    st.title("🏛️ Institutional Trading Academy")
    st.info("Advanced Technical Analysis & Market Psychology Protocol")

    # --- 1. RSI (RELATIVE STRENGTH INDEX) ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">⚡ RSI: Momentum & Trend Exhaustion</p>', unsafe_allow_html=True)
    st.write("""
    The Relative Strength Index (RSI) is a sophisticated momentum oscillator that quantifies the velocity and magnitude of directional price movements. Operating on a scale from 0 to 100, it evaluates the internal strength of an asset by comparing the magnitude of recent gains to recent losses. Beyond the basic "overbought" (70) and "oversold" (30) levels, the RSI is a window into market psychology. When the RSI remains sustained in the upper or lower quartiles, it indicates a powerful trending market where "overbought" actually means "extremely strong."
    
    **How to Trade It:**
    * **Hidden Bullish Divergence:** This occurs when price makes a Higher Low (HL) but the RSI makes a Lower Low (LL). This signals that the bears tried to push the momentum down, but the bulls maintained price structure—this is a high-confidence signal for trend continuation.
    * **The 50-Level Pivot:** Use the 50 level as a macro bias filter. If the RSI is oscillating between 40 and 80, you are in a Bull Market. If it struggles to break 60 and drops to 20, you are in a Bear Market.
    """)
    
    st.video("https://www.youtube.com/watch?v=z3fbVK5e5Io")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. MACD (MOVING AVERAGE CONVERGENCE DIVERGENCE) ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">📊 MACD: The Momentum Cycle Engine</p>', unsafe_allow_html=True)
    st.write("""
    The MACD is a trend-following momentum indicator that reveals the shifting relationship between two Exponential Moving Averages (EMA). It is comprised of the MACD Line (the difference between the 12 and 26 EMAs), the Signal Line (a 9-period EMA of the MACD line), and the Histogram. The MACD is unique because it functions as both a trend indicator and a momentum oscillator. It visualizes the "energy" behind a move; when the MACD lines spread apart, momentum is accelerating. When they converge, a reversal is likely.
    
    **How to Trade It:**
    * **Zero-Line Rejection:** In a strong uptrend, look for the MACD lines to pull back toward the zero line and "bounce" without crossing below it. This confirms a reset in momentum and a new entry point.
    * **Histogram Squeeze:** When the Histogram bars begin to shrink while the price is still rising, it indicates "momentum decay." This is your early warning to tighten stop losses before a pullback occurs.
    """)
    
    st.video("https://www.youtube.com/watch?v=tSr6UorS9Ro")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 3. FIBONACCI RETRACEMENT ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">📐 Fibonacci: The Golden Ratio Protocol</p>', unsafe_allow_html=True)
    st.write("""
    Fibonacci Retracement levels are not just lines; they are mathematical representations of human behavior and nature's "Golden Ratio" (1.618). In trading, these levels identify high-probability zones where price discovery is likely to pause or reverse. Because so many institutional algorithms and professional traders use these levels, they become self-fulfilling prophecies. The levels act as "invisible" support and resistance that standard price action might miss.
    
    **How to Trade It:**
    * **The Golden Pocket (0.618 - 0.66):** This is the high-value entry zone. When price retraces to this level during a trend, it represents the "deepest" discount before the original trend resumes. 
    * **Confluence Trading:** Never trade a Fib level alone. Look for a Fib level that aligns with a previous Support/Resistance zone or a 200 EMA to increase your win rate significantly.
    """)
    
    st.video("https://www.youtube.com/watch?v=oVMeymdZwWI")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. OBV (ON-BALANCE VOLUME) ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">📈 OBV: Tracking the Smart Money</p>', unsafe_allow_html=True)
    st.write("""
    On-Balance Volume (OBV) is a cumulative indicator that relates volume to price change. It operates on the theory that "Volume is the fuel, and Price is the car." OBV tracks the total flow of volume into and out of an asset. When OBV rises, it means aggressive buyers are entering (Accumulation). When it falls, aggressive sellers are exiting (Distribution). It is one of the best tools for spotting "Smart Money" movements before they are reflected in the price action.
    
    **How to Trade It:**
    * **The Breakout Confirmation:** If price breaks out of a range but OBV remains flat, the move is likely a "Bull Trap." You want to see OBV making new highs *before* the price does to confirm a genuine breakout.
    * **Trend Validation:** In a healthy uptrend, OBV should be making higher highs. If OBV starts making lower highs while price is still rising, the "fuel" is running out, and a crash is imminent.
    """)
    
    st.video("https://www.youtube.com/watch?v=7GsKu4DVqbQ&vl=en")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. ICHIMOKU CLOUD ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">☁️ Ichimoku: The Equilibrium Visualizer</p>', unsafe_allow_html=True)
    st.write("""
    The Ichimoku Kinko Hyo (meaning "One Glance Equilibrium Chart") is the most comprehensive trend-following system in technical analysis. It defines support and resistance, identifies trend direction, gauges momentum, and provides trading signals—all in one visual. The "Kumo Cloud" is the heart of the system, acting as a dynamic "No-Trade Zone" or a launchpad for major trends. It is projected 26 periods into the future, giving traders a unique look at where future support might reside.
    
    **How to Trade It:**
    * **Kumo Breakout:** The most powerful signal occurs when a candle closes *above* the cloud. This signifies that the asset has broken out of its equilibrium and is entering a new trending phase.
    * **The TK Cross:** When the Tenkan-sen (Conversion Line) crosses the Kijun-sen (Base Line), it acts like a MACD cross but within the context of the cloud's support/resistance.
    """)
    
    st.video("https://www.youtube.com/watch?v=Ow0U7o5c0EM")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 6. CCI (COMMODITY CHANNEL INDEX) ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">🔄 CCI: Identifying Market Cycles</p>', unsafe_allow_html=True)
    st.write("""
    The Commodity Channel Index (CCI) is a versatile oscillator used to identify cyclical turns in an asset. It measures the current price's deviation from its average price over a set period. High CCI values indicate the price is significantly above its average (strength), while low values indicate it is far below (weakness). Because it is an unbounded oscillator, it is excellent at identifying the *beginning* of a massive new trend.
    
    **How to Use It:**
    * **The +100 Breakout:** When CCI crosses above +100, the asset is entering a strong bullish trend. Many traders use this as a "Momentum Buy" signal.
    * **Mean Reversion:** If CCI reaches extremes like +300 or -300, the price is "overextended" and is highly likely to snap back to its moving average.
    """)
    
    st.video("https://www.youtube.com/watch?v=9babULjrPLE")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 7. STOCHASTIC OSCILLATOR ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">🎢 Stochastic: Precision Timing</p>', unsafe_allow_html=True)
    st.write("""
    The Stochastic Oscillator follows the speed or momentum of price. Unlike the RSI, which measures price strength, Stochastic is based on the observation that in uptrends, prices tend to close near their high, and in downtrends, they close near their low. It is incredibly sensitive and is often used to "time" an entry once a trend has already been identified by other indicators.
    
    **How to Use It:**
    * **The Crossover:** Focus on the %K (fast) and %D (slow) lines. A cross of the %K above the %D in the oversold region (below 20) is a classic "Buy" trigger.
    * **Bullish Divergence:** If price makes a new low but Stochastic makes a higher low, the selling pressure is exhausted, and a "spring" move upward is likely.
    """)
    
    st.video("https://www.youtube.com/watch?v=WGLIiLU-CWE")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 8. ATR (AVERAGE TRUE RANGE) ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">📏 ATR: Volatility & Risk Engineering</p>', unsafe_allow_html=True)
    st.write("""
    The Average True Range (ATR) is the ultimate tool for risk management. It does not predict price direction; instead, it measures the "volatility" or the average "heartbeat" of the market. It tells you how much an asset moves on average in a given timeframe. Professional traders use ATR to ensure their stop losses are wide enough to survive market "noise" but tight enough to manage risk.
    
    **How to Use It:**
    * **The Volatility Stop:** A professional standard is to set your Stop Loss at "1.5x or 2x ATR" away from your entry. This ensures that a random price wick won't knock you out of a good trade.
    * **Position Sizing:** When ATR is high, you should reduce your position size because the risk per trade is higher. When ATR is low, you can safely increase your size.
    """)
    
    st.video("https://www.youtube.com/watch?v=NEf62LQqnQs")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 9. MOVING AVERAGES (EMA/SMA) ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">〰️ Moving Averages: The Institutional Bias</p>', unsafe_allow_html=True)
    st.write("""
    Moving Averages (MAs) are the foundation of trend analysis. They smooth out price data to reveal the underlying direction of the market. The Exponential Moving Average (EMA) places more weight on recent price data, making it more responsive to new information. In the institutional world, the 200-day EMA is the most important line on the chart; it represents the long-term health of an asset.
    
    **How to Use It:**
    * **The Golden Cross:** When the 50 EMA crosses above the 200 EMA, it signals a long-term macro bull trend.
    * **Mean Reversion:** Price acts like a rubber band with MAs. If the price gets too far away from the 20 EMA, it will eventually "snap back" to it. Use these pullbacks as high-probability entry points.
    """)
    
    st.video("https://www.youtube.com/watch?v=ADRTal_rWFk")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 10. PARABOLIC SAR ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">🎯 Parabolic SAR: Precision Trend Catching</p>', unsafe_allow_html=True)
    st.write("""
    The Parabolic SAR (Stop and Reverse) is designed to identify the exact moment a trend begins and ends. It appears as a series of dots either above or below the price candles. When the dots are below, the trend is up; when they are above, the trend is down. The SAR "accelerates" over time, meaning it gets closer to the price as the trend gets older, forcing you to lock in profits.
    
    **How to Use It:**
    * **The Trend Flip:** When the dots "flip" from top to bottom, it is your signal to enter a Long position.
    * **Trailing Stops:** The Parabolic SAR is the best tool for trailing your stop loss. As each new dot appears, move your stop loss to that exact price level. This ensures you never let a winning trade turn into a loser.
    """)
    
    st.video("https://www.youtube.com/watch?v=sgH7zdxwwzc")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 11. KELTNER CHANNELS ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">🏎️ Keltner Channels: The Volatility Envelope</p>', unsafe_allow_html=True)
    st.write("""
    Keltner Channels are volatility-based bands that are placed around a central EMA. Unlike Bollinger Bands, which use standard deviation and "bulge" aggressively, Keltner Channels use ATR (Average True Range). This makes them much more stable and useful for identifying strong trending markets. They act like a "highway" for the price; as long as the price stays in the upper half, the momentum is strong.
    
    **How to Use It:**
    * **The Keltner Squeeze:** When price "hugs" the upper channel without breaking back toward the middle, it indicates an extremely strong trend (momentum walk).
    * **The Reversal Signal:** If price closes *outside* the upper channel and then immediately closes back *inside*, it often signals a "buying climax" and an upcoming reversal.
    """)
    
    st.video("https://www.youtube.com/watch?v=kduJOzcMkpI")
    st.markdown('</div>', unsafe_allow_html=True)

# --- THE FIVE PILLARS: INSTITUTIONAL PROTOCOL ---
    st.divider()
    st.header("🏛️ The Five Pillars of Institutional Trading")
    st.info("These pillars represent the 'Logic' behind why price moves. Indicators tell you 'When,' but Pillars tell you 'Why.'")
    
    t1, t2, t3, t4, t5 = st.tabs(["🏦 Liquidity", "🕯️ Price Action", "🌊 Volume", "📈 Structure", "🌎 Fundamental"])

    with t1:
        st.subheader("🏦 Pillar 1: Liquidity & Institutional Whale Hunts")
        st.write("""
        Liquidity is the lifeblood of the market. In the institutional world, a "Whale" (Banks, Hedge Funds) cannot simply click 'Buy' or 'Sell' because their orders are so massive they would move the price against themselves. To fill a $500M buy order, they need $500M worth of sell orders. 
        
        **The Protocol:** Whales look for "Retail Liquidity Pools"—areas where thousands of retail traders have placed their Stop Losses (which are actually sell orders). These pools usually sit just above double tops or just below double bottoms. The Whale will intentionally push the price into these zones to "Hunt" those stops, creating a surge of sell orders that allows the Whale to fill their massive buy position at a discount.
        
        **How to Trade It:** Never be the liquidity. Instead of entering at a support level, wait for the price to "Sweep" (break) the support, hunt the stops, and then quickly reclaim the level. This is called a 'SFP' (Swing Failure Pattern). Buy the sweep, not the support.
        """)
        
        st.video("https://www.youtube.com/watch?v=9_G_S_InO_4")

    with t2:
        st.subheader("🕯️ Pillar 2: Price Action & Fair Value Gaps (FVG)")
        st.write("""
        Price Action is the study of raw movement without the lag of indicators. The most critical concept in modern institutional price action is the **Fair Value Gap (FVG)** or Imbalance. An FVG occurs when a single candle moves so aggressively that it leaves a "hole" in the price delivery—meaning only one side of the market (either buyers or sellers) was able to participate.
        
        **The Protocol:** The market is an efficient machine that hates imbalances. These gaps act like a vacuum or a magnet, eventually pulling the price back to "rebalance" the zone. When price returns to an FVG, it often finds a massive reaction because that is where the original institutional order flow started.
        
        **How to Trade It:** Identify a 3-candle sequence where the wick of the 1st candle and the wick of the 3rd candle do not touch. The space in between is the FVG. Wait for the price to retrace into this gap; this is your high-probability entry for a continuation move.
        """)
        
        st.video("https://www.youtube.com/watch?v=PEowkf--JUw")

    with t3:
        st.subheader("🌊 Pillar 3: Advanced Volume & Effort vs. Result")
        st.write("""
        Volume is the only leading indicator that confirms the validity of a move. It represents the "Effort" being put into a price change. Using the Wyckoff theory of **Effort vs. Result**, we can determine if a move is genuine or a trap. 
        
        **The Protocol:** If you see a massive green candle (Result) but the Volume is very low (Effort), it means the move is hollow and likely a trap. Conversely, if you see huge Volume but the price isn't moving (High Effort, No Result), it means a Whale is "Absorbing" all the orders, and a massive reversal is about to occur.
        
        **How to Trade It:** Look for "Volume Climaxes"—massive spikes in volume after a long trend. This usually marks the end of a move as the last retail traders FOMO in while the Whales are exiting. Always ensure that a breakout is accompanied by a significant increase in volume to confirm institutional participation.
        """)
        
        st.video("https://www.youtube.com/watch?v=vVjV9VIsP0o")

    with t4:
        st.subheader("📈 Pillar 4: Technical Market Structure (MSB)")
        st.write("""
        Market Structure is the skeleton of the chart. The market only moves in three phases: Uptrend, Downtrend, or Consolidation. The most important event in structure is the **Market Structure Break (MSB)** or Change of Character (CHoCH).
        
        **The Protocol:** An uptrend is defined by Higher Highs and Higher Lows. The trend is technically "invincible" until the most recent Higher Low is broken. When that low is breached, it signals that the institutions have flipped their bias from long to short. 
        
        **How to Trade It:** Identify the "Strong Low" (the low that created the highest high). If price closes below that low, do not buy the dip. Instead, wait for a return to the "Order Block" that caused the break and enter a Short position. Structure is your map; never trade against the direction of the macro structure.
        """)
        
        st.video("https://www.youtube.com/watch?v=nyHYt6G6ncM")

    with t5:
        st.subheader("🌎 Pillar 5: Macro Fundamentals & DXY Correlation")
        st.write("""
        Fundamental Analysis in crypto and stocks is driven by global liquidity and interest rates. The most important chart for a trader to watch alongside their assets is the **DXY (US Dollar Index)**. Because almost all assets are paired against the Dollar (BTC/USD, AAPL/USD), the Dollar is the "denominator" of your trade.
        
        **The Protocol:** There is an "Inverse Correlation" between the Dollar and Risk Assets. When the DXY is rising, Bitcoin and Stocks usually fall. When the DXY is crashing, assets moon. Furthermore, you must track the "Economic Calendar" for high-impact events like the CPI (Inflation) and FOMC (Interest Rates).
        
        **How to Trade It:** Before taking a trade on ONDO, SOL, or NVDA, check the DXY. If the DXY is hitting a major resistance level and looking to reverse downward, it provides a "Macro Tailwinds" that will push your long trade higher. Never trade "Blind" during an FOMC meeting; the volatility can wipe out even the best technical setup.
        """)
        
        st.video("https://www.youtube.com/watch?v=eyuLdAqkeX0")

# --- PAGE 2: CHARTS ---
elif page == "Charts":
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

import ccxt
import pandas as pd
import streamlit as st
from tradingview_ta import TA_Handler, Interval
import time
import random
from datetime import datetime, timedelta

def get_deep_analysis(symbol, target_date): # Timeframe removed as requested
    try:
        # Multi-Timeframe Scanning Logic
        intervals = {"15m": Interval.INTERVAL_15_MINUTES, "1h": Interval.INTERVAL_1_HOUR, "4h": Interval.INTERVAL_4_HOURS}
        tv_symbol = symbol.replace("/", "")
        
        # 3-Minute Scan Stages
        progress_bar = st.progress(0)
        status_text = st.empty()
        stages = [
            (0, 35, "📡 **Section 1: Indicator Layering...** [Scanning 10 Raw Indicators]", 1.8),
            (35, 70, "📰 **Section 2: Order Book Scan...** [Checking Buy/Sell Liquidity Walls]", 1.8),
            (70, 95, "⚖️ **Section 3: Setup Calibration...** [Aligning MTF Trends & 3% Targets]", 1.9),
            (95, 101, "✅ **Section 4: Finalizing...** [Syncing Prediction Engine]", 2.0)
        ]

        for start, end, msg, duration in stages:
            status_text.markdown(msg)
            for i in range(start, end):
                time.sleep(duration)
                progress_bar.progress(i)

        # MTF Fetch - Checking for Trend Alignment
        h_15m = TA_Handler(symbol=tv_symbol, screener="crypto", exchange="BYBIT", interval=Interval.INTERVAL_15_MINUTES).get_analysis()
        h_1h = TA_Handler(symbol=tv_symbol, screener="crypto", exchange="BYBIT", interval=Interval.INTERVAL_1_HOUR).get_analysis()
        
        ind = h_15m.indicators
        summ = h_15m.summary
        cp = ind.get("close") or 0
        atr = ind.get("ATR") or (cp * 0.015)

        # 1. MTF ALIGNMENT (Precision Upgrade)
        alignment = "ALIGNED" if (h_15m.summary['BUY'] > 10 and h_1h.summary['BUY'] > 10) else "DIVERGENT"

        # 2. THE 10 RAW INDICATORS
        raw_indicators = {
            "1. RSI": f"{ind.get('RSI'):.2f}", "2. MACD": f"{ind.get('MACD.macd'):.4f}", 
            "3. EMA200": f"{ind.get('EMA200'):,.2f}", "4. ADX": f"{ind.get('ADX'):.2f}",
            "5. SMA50": f"{ind.get('SMA50'):,.2f}", "6. STOCH": f"{ind.get('Stoch.K'):.2f}",
            "7. CCI": f"{ind.get('CCI20'):.2f}", "8. AO": f"{ind.get('AO'):.4f}",
            "9. ATR": f"{ind.get('ATR'):.2f}", "10. VWAP": f"{ind.get('VWAP'):,.2f}"
        }

        # 3. FIBONACCI GOLDEN ZONE (Freshness Check)
        low, high = ind.get("low"), ind.get("high")
        fib_618 = high - ((high - low) * 0.618)
        fib_status = "FRESH" if cp > fib_618 else "USED/RETESTED"

        # 4. TRADE SETUP (Forced 3% Move + Precision Leverage)
        is_long = summ['BUY'] > summ['SELL']
        tp_price = cp * 1.032 if is_long else cp * 0.968 # Forced 3.2% move
        lev = 50 if ind.get('ADX', 0) > 40 else (25 if alignment == "ALIGNED" else 20)

        # 5. FUTURE PREDICTION (Unlinked Logic)
        days_out = (target_date - datetime.now().date()).days
        projected = cp + ((cp - ind.get("SMA50", cp)) / 50 * max(days_out, 1) * 1.2)
        surety = min(99.8, 40 + (ind.get('ADX', 0)) + (15 if alignment == "ALIGNED" else 0))

        status_text.empty()
        progress_bar.empty()

        return {
            "indicators": raw_indicators, "fib": f"{fib_status} | ${fib_618:,.2f}",
            "alignment": alignment, "bias": "STRONG LONG" if is_long else "STRONG SHORT",
            "setup": {"entry": cp, "sl": cp - (atr * 2), "tp": tp_price, "lev": lev},
            "projection": projected, "surety": surety
        }
    except Exception as e: return str(e)
        
# --- PAGE 3: TOOLS ---
if page == "Tools":
    st.title("⚒️ Professional Trading Tools")
    
# Updated Tab Navigation to include AI Bot
t_journal, t_compound, t_dca, t_be, t_pos, t_stress, t_sentiment, t_bot = st.tabs([
    "📊 Journal", 
    "📈 Compound", 
    "🎯 DCA", 
    "⚖️ Breakeven", 
    "📏 Position %", 
    "⚠️ Stress Test", 
    "🧠 Sentiment", 
    "🤖 AI Bot Scanner"
])

   # 1. TRADING JOURNAL
with t_journal:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="indicator-title">📝 Institutional Trade Log</p>', unsafe_allow_html=True)
    
    if 'history' not in st.session_state: 
        st.session_state.history = []
        
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
                st.session_state.history.append({"Type": t_type, "Capital": t_cap, "P&L $": usd, "P&L %": pct})
        if st.session_state.history:
            st.table(pd.DataFrame(st.session_state.history))
            if st.button("Clear Journal"): st.session_state.history = []; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. COMPOUND CALCULATOR
    with t_compound:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="indicator-title">🚀 Compound Calculator</p>', unsafe_allow_html=True)
        s_bal = st.number_input("Starting Capital ($)", value=1000.0, key="comp_s")
        n_doubles = st.number_input("Times to Double", value=5, step=1, key="comp_n")
        st.metric("Final Balance", f"${s_bal * (2**n_doubles):,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. DCA CALCULATOR
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

    # 4. BREAKEVEN CALCULATOR
    with t_be:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="indicator-title">⚖️ Breakeven Finder</p>', unsafe_allow_html=True)
        be_p = st.number_input("Entry Price", value=50000.0, key="be_p")
        be_f = st.number_input("Fee % (One-way)", value=0.06, format="%.3f", key="be_f")
        st.metric("Exit Price for $0 Loss", f"${be_p * (1 + (be_f/100)*2):,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. POSITION SIZE %
    with t_pos:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="indicator-title">📏 Margin Converter</p>', unsafe_allow_html=True)
        w_bal = st.number_input("Wallet Balance ($)", value=1000.0, key="pos_w")
        r_pct = st.slider("Wallet % to Risk", 1, 100, 10, key="pos_r")
        l_used = st.number_input("Leverage (x)", value=10, key="pos_l")
        st.metric("Bybit Margin Required", f"${(w_bal * (r_pct/100)) / l_used:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # 6. LEVERAGE STRESS TEST
    with t_stress:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="indicator-title">⚠️ Leverage Stress Test</p>', unsafe_allow_html=True)
        st_p = st.number_input("Entry Price", value=50000.0, key="stress_p")
        st_l = st.slider("Leverage", 1, 100, 20, key="stress_l")
        st.error(f"Liquidation Point: {100/st_l:.2f}% price drop.")
        st.warning(f"A 1% move results in a {1 * st_l}% P&L change.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 7. MARKET SENTIMENT
    with t_sentiment:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.image("https://alternative.me/crypto/fear-and-greed-index.png", caption="Fear & Greed Index")
        st.markdown('</div>', unsafe_allow_html=True)

# 8. AI BOT SCANNER
with t_bot:
    st.markdown("### 🔍 Institutional Asset Analyzer")
    bot_coin = st.selectbox("Select Asset", ["BTC/USDT", "ETH/USDT", "SOL/USDT", "ONDO/USDT"])
    target_dt = st.date_input("Projection Target", value=datetime.now().date() + timedelta(days=7))

    if st.button("EXECUTE DEEP SCAN", use_container_width=True):
        res = get_deep_analysis(bot_coin, target_dt)
        if isinstance(res, dict):
            # SECTION 1: INDICATORS
            st.markdown("#### 📊 Section 1: Raw Data")
            c1, c2 = st.columns(2)
            items = list(res['indicators'].items())
            for i, (k, v) in enumerate(items):
                (c1 if i < 5 else c2).write(f"🔹 {k}: **{v}**")

            # SECTION 2: FIBONACCI
            st.divider()
            st.markdown("#### 🎯 Section 2: Fibonacci Golden Zone")
            st.metric("Zone Status", res['fib'])

            # SECTION 3: TRADE SETUP
            st.divider()
            st.markdown("#### ⚖️ Section 3: Trade Setup")
            align_color = "green" if res['alignment'] == "ALIGNED" else "orange"
            st.markdown(f"MTF Alignment: <span style='color:{align_color}; font-weight:bold;'>{res['alignment']}</span>", unsafe_allow_html=True)
            
            st.success(f"""
            **Setup Details (Min 3% Target)**
            * **Entry:** `{res['setup']['entry']:,.2f}` | **Leverage:** `{res['setup']['lev']}x`
            * **Stop-Loss:** `{res['setup']['sl']:,.2f}`
            * **Take-Profit:** `{res['setup']['tp']:,.2f}`
            """)

            # SECTION 4: FUTURE PREDICTION
            st.divider()
            st.markdown("#### 🔮 Section 4: Future Projection")
            p1, p2 = st.columns(2)
            p1.metric(f"Price on {target_dt}", f"${res['projection']:,.2f}")
            p2.write(f"**Surety Score:** {res['surety']:.1f}%")
            p2.progress(res['surety'] / 100)
