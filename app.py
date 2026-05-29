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
        "title": "⚡ RSI (Relative Strength Index)",
        "desc": """
    The Relative Strength Index (RSI) is a sophisticated momentum oscillator that quantifies the velocity and magnitude of directional price movements. Operating on a scale from 0 to 100, it evaluates the internal strength of an asset by comparing the magnitude of recent gains to recent losses. Beyond the basic "overbought" (70) and "oversold" (30) levels, the RSI is a window into market psychology. When the RSI remains sustained in the upper or lower quartiles, it indicates a powerful trending market where "overbought" actually means "extremely strong."
    
    **How to Trade It:**
    * **Hidden Bullish Divergence:** This occurs when price makes a Higher Low (HL) but the RSI makes a Lower Low (LL). This signals that the bears tried to push the momentum down, but the bulls maintained price structure—this is a high-confidence signal for trend continuation.
    * **The 50-Level Pivot:** Use the 50 level as a macro bias filter. If the RSI is oscillating between 40 and 80, you are in a Bull Market. If it struggles to break 60 and drops to 20, you are in a Bear Market.
    """,
        "video": "https://www.youtube.com/watch?v=z3fbVK5e5Io"
    },
    "MACD": {
        "title": "📊 MACD (Moving Average Convergence Divergence)",
        "desc": """
    The MACD is a trend-following momentum indicator that reveals the shifting relationship between two Exponential Moving Averages (EMA). It is comprised of the MACD Line (the difference between the 12 and 26 EMAs), the Signal Line (a 9-period EMA of the MACD line), and the Histogram. The MACD is unique because it functions as both a trend indicator and a momentum oscillator. It visualizes the "energy" behind a move; when the MACD lines spread apart, momentum is accelerating. When they converge, a reversal is likely.
    
    **How to Trade It:**
    * **Zero-Line Rejection:** In a strong uptrend, look for the MACD lines to pull back toward the zero line and "bounce" without crossing below it. This confirms a reset in momentum and a new entry point.
    * **Histogram Squeeze:** When the Histogram bars begin to shrink while the price is still rising, it indicates "momentum decay." This is your early warning to tighten stop losses before a pullback occurs.
    """,
        "video": "https://www.youtube.com/watch?v=tSr6UorS9Ro"
    },
    "MA": {
        "title": "📊 MA (Moving Average)",
        "desc": """
    Moving Averages (MAs) are the foundation of trend analysis. They smooth out price data to reveal the underlying direction of the market. The Exponential Moving Average (EMA) places more weight on recent price data, making it more responsive to new information. In the institutional world, the 200-day EMA is the most important line on the chart; it represents the long-term health of an asset.
    
    **How to Use It:**
    * **The Golden Cross:** When the 50 EMA crosses above the 200 EMA, it signals a long-term macro bull trend.
    * **Mean Reversion:** Price acts like a rubber band with MAs. If the price gets too far away from the 20 EMA, it will eventually "snap back" to it. Use these pullbacks as high-probability entry points.
    """,
        "video": "https://www.youtube.com/watch?v=ADRTal_rWFk"
    },
    "FIBONACCI": {
        "title": "📐 Fibonacci Retracement",
        "desc": """
    Fibonacci Retracement levels are not just lines; they are mathematical representations of human behavior and nature's "Golden Ratio" (1.618). In trading, these levels identify high-probability zones where price discovery is likely to pause or reverse. Because so many institutional algorithms and professional traders use these levels, they become self-fulfilling prophecies. The levels act as "invisible" support and resistance that standard price action might miss.
    
    **How to Trade It:**
    * **The Golden Pocket (0.618 - 0.66):** This is the high-value entry zone. When price retraces to this level during a trend, it represents the "deepest" discount before the original trend resumes. 
    * **Confluence Trading:** Never trade a Fib level alone. Look for a Fib level that aligns with a previous Support/Resistance zone or a 200 EMA to increase your win rate significantly.
    """,
        "video": "https://www.youtube.com/watch?v=oVMeymdZwWI"
    },
    "OBV": {
        "title": "📈 OBV (On-Balance Volume)",
        "desc": """
    On-Balance Volume (OBV) is a cumulative indicator that relates volume to price change. It operates on the theory that "Volume is the fuel, and Price is the car." OBV tracks the total flow of volume into and out of an asset. When OBV rises, it means aggressive buyers are entering (Accumulation). When it falls, aggressive sellers are exiting (Distribution). It is one of the best tools for spotting "Smart Money" movements before they are reflected in the price action.
    
    **How to Trade It:**
    * **The Breakout Confirmation:** If price breaks out of a range but OBV remains flat, the move is likely a "Bull Trap." You want to see OBV making new highs *before* the price does to confirm a genuine breakout.
    * **Trend Validation:** In a healthy uptrend, OBV should be making higher highs. If OBV starts making lower highs while price is still rising, the "fuel" is running out, and a crash is imminent.
    """,
        "video": "https://www.youtube.com/watch?v=7GsKu4DVqbQ&vl=en"
    },
    "ICHIMOKU CLOUD": {
        "title": "☁️ Ichimoku Cloud",
        "desc": """
    The Ichimoku Kinko Hyo (meaning "One Glance Equilibrium Chart") is the most comprehensive trend-following system in technical analysis. It defines support and resistance, identifies trend direction, gauges momentum, and provides trading signals—all in one visual. The "Kumo Cloud" is the heart of the system, acting as a dynamic "No-Trade Zone" or a launchpad for major trends. It is projected 26 periods into the future, giving traders a unique look at where future support might reside.
    
    **How to Trade It:**
    * **Kumo Breakout:** The most powerful signal occurs when a candle closes *above* the cloud. This signifies that the asset has broken out of its equilibrium and is entering a new trending phase.
    * **The TK Cross:** When the Tenkan-sen (Conversion Line) crosses the Kijun-sen (Base Line), it acts like a MACD cross but within the context of the cloud's support/resistance.
    """,
        "video": "https://www.youtube.com/watch?v=Ow0U7o5c0EM"
    },
    "CCI": {
        "title": "🔄 CCI (Commodity Channel Index)",
        "desc": """
    The Commodity Channel Index (CCI) is a versatile oscillator used to identify cyclical turns in an asset. It measures the current price's deviation from its average price over a set period. High CCI values indicate the price is significantly above its average (strength), while low values indicate it is far below (weakness). Because it is an unbounded oscillator, it is excellent at identifying the *beginning* of a massive new trend.
    
    **How to Use It:**
    * **The +100 Breakout:** When CCI crosses above +100, the asset is entering a strong bullish trend. Many traders use this as a "Momentum Buy" signal.
    * **Mean Reversion:** If CCI reaches extremes like +300 or -300, the price is "overextended" and is highly likely to snap back to its moving average.
    """,
        "video": "https://www.youtube.com/watch?v=9babULjrPLE"
    },
    "STOCHASTIC OSCILLATOR": {
        "title": "🎢 Stochastic Oscillator",
        "desc": """
    The Stochastic Oscillator follows the speed or momentum of price. Unlike the RSI, which measures price strength, Stochastic is based on the observation that in uptrends, prices tend to close near their high, and in downtrends, they close near their low. It is incredibly sensitive and is often used to "time" an entry once a trend has already been identified by other indicators.
    
    **How to Use It:**
    * **The Crossover:** Focus on the %K (fast) and %D (slow) lines. A cross of the %K above the %D in the oversold region (below 20) is a classic "Buy" trigger.
    * **Bullish Divergence:** If price makes a new low but Stochastic makes a higher low, the selling pressure is exhausted, and a "spring" move upward is likely.
    """,
        "video": "https://www.youtube.com/watch?v=WGLIiLU-CWE"
    },
    "ATR": {
        "title": "📏 ATR (Average True Range)",
        "desc": """
    The Average True Range (ATR) is the ultimate tool for risk management. It does not predict price direction; instead, it measures the "volatility" or the average "heartbeat" of the market. It tells you how much an asset moves on average in a given timeframe. Professional traders use ATR to ensure their stop losses are wide enough to survive market "noise" but tight enough to manage risk.
    
    **How to Use It:**
    * **The Volatility Stop:** A professional standard is to set your Stop Loss at "1.5x or 2x ATR" away from your entry. This ensures that a random price wick won't knock you out of a good trade.
    * **Position Sizing:** When ATR is high, you should reduce your position size because the risk per trade is higher. When ATR is low, you can safely increase your size.
    """,
        "video": "https://www.youtube.com/watch?v=NEf62LQqnQs"
    },
    "PARABOLIC SAR": {
        "title": "🎯 Parabolic SAR",
        "desc": """
    The Parabolic SAR (Stop and Reverse) is designed to identify the exact moment a trend begins and ends. It appears as a series of dots either above or below the price candles. When the dots are below, the trend is up; when they are above, the trend is down. The SAR "accelerates" over time, meaning it gets closer to the price as the trend gets older, forcing you to lock in profits.
    
    **How to Use It:**
    * **The Trend Flip:** When the dots "flip" from top to bottom, it is your signal to enter a Long position.
    * **Trailing Stops:** The Parabolic SAR is the best tool for trailing your stop loss. As each new dot appears, move your stop loss to that exact price level. This ensures you never let a winning trade turn into a loser.
    """,
        "video": "https://www.youtube.com/watch?v=sgH7zdxwwzc"
    },
    "KELTNER CHANNEL": {
        "title": "🏎️ Keltner Channels",
        "desc": """
    Keltner Channels are volatility-based bands that are placed around a central EMA. Unlike Bollinger Bands, which use standard deviation and "bulge" aggressively, Keltner Channels use ATR (Average True Range). This makes them much more stable and useful for identifying strong trending markets. They act like a "highway" for the price; as long as the price stays in the upper half, the momentum is strong.
    
    **How to Use It:**
    * **The Keltner Squeeze:** When price "hugs" the upper channel without breaking back toward the middle, it indicates an extremely strong trend (momentum walk).
    * **The Reversal Signal:** If price closes *outside* the upper channel and then immediately closes back *inside*, it often signals a "buying climax" and an upcoming reversal.
    """,
        "video": "https://www.youtube.com/watch?v=kduJOzcMkpI"
    }
}

# --- TERMINAL CONFIG ---
st.set_page_config(page_title="Crypto Mastery", page_icon="📈", layout="wide")

# --- CUSTOM CSS ---
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
    .wallet-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .wallet-label { color: #f1c40f; font-size: 18px; font-weight: 700; margin-bottom: 8px; }
    .wallet-addr {
        background: #0D1117;
        border: 1px solid #30363D;
        border-radius: 6px;
        padding: 12px;
        font-family: monospace;
        font-size: 14px;
        color: #58A6FF;
        word-break: break-all;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">Crypto Mastery</p>', unsafe_allow_html=True)
    page = st.radio("MENU", ["Basics", "Technical Analysis", "Types of Trading", "Indicators", "Charts", "Tools", "Donate", "Contact"])
    st.divider()
    st.caption("℗Romanstrades")
    st.caption("x.com/romanstrades")

# --- Initialize session state ---
if "active_video" not in st.session_state:
    st.session_state.active_video = None
if "selected_indicator" not in st.session_state:
    st.session_state.selected_indicator = None


# ============================================================
# --- PAGE: INDICATORS ---
# ============================================================
if page == "Indicators":
    st.title("🧭 Indicators")

    # --- Browse / detail view ---
    if st.session_state.selected_indicator:
        key = st.session_state.selected_indicator
        if st.button("← Back to Indicators", key="back_btn"):
            st.session_state.selected_indicator = None
            st.rerun()

        if key in indicators:
            data = indicators[key]
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(f'<p class="indicator-title">{data["title"]}</p>', unsafe_allow_html=True)
            st.write(data["desc"])
            st.video(data["video"])
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("**Select an indicator to learn more:**")
        for key, data in indicators.items():
            if st.button(f"{data['title']}", key=f"browse_{key}", use_container_width=True):
                st.session_state.selected_indicator = key
                st.rerun()


# ============================================================
# --- PAGE: BASICS ---
# ============================================================
if page == "Basics":
    st.title("🏫 Basics")
    
    b1, b2, b3, b4, b5 = st.tabs([
        "💰 What is Trading",
        "📊 Market Conditions",
        "⚖️ Risk Management",
        "📈 Long vs Short",
        "🧠 Psychology"
    ])

    with b1:
        st.subheader("💰 What is Trading?")
        st.write("""
Trading is the process of buying and selling assets to profit from changes in price.

At a surface level, it looks simple — buy low, sell high. But in reality, trading is about understanding **how and why price moves**, and positioning yourself ahead of those movements.

Unlike long-term investing, trading focuses on **short- to medium-term opportunities**, using price action, liquidity, and market behavior to make decisions.
""")
        st.write("""
**Key Shift in Thinking:**  
You are not trading coins, stocks, or assets — you are trading **price movement and behavior**.
""")
        st.write("""
### How Traders Make Money
There are only two ways to profit in any market:

- Buying an asset and selling it at a higher price  
- Selling an asset and buying it back at a lower price  

Everything else — indicators, strategies, signals — is just a tool to help you do this more effectively.

### The Reality of Trading
Markets are driven by **liquidity, emotions, and large players**, not by opinions or guesses.  
This means trading is not about being right — it's about being **consistently better than the average participant**.

### Key Takeaways
- Trading is probability-based, not guaranteed  
- You are competing against other traders  
- Understanding price behavior is more important than predictions  
""")

    with b2:
        st.subheader("📊 Market Conditions")
        st.write("""
Before entering any trade, you need to understand **what type of market you are in**.

Most beginners lose money because they apply the same strategy in every condition — but markets behave very differently depending on structure and volatility.
""")
        st.write("""
### 📈 Trending Market
A trending market moves clearly in one direction:
- Uptrend → higher highs and higher lows  
- Downtrend → lower highs and lower lows  

These conditions favor **trend-following strategies**, where you trade in the direction of momentum.

### 🔄 Ranging Market
A ranging market moves sideways between support and resistance levels.

Price repeatedly:
- Bounces from the bottom (support)
- Rejects from the top (resistance)

This favors **buy low / sell high** strategies instead of chasing breakouts.

### ⚡ Volatile Market
Volatility increases during news, major events, or liquidity grabs.

- Fast, aggressive moves  
- Unpredictable spikes and wicks  
- Higher risk but also higher opportunity  

This is where most traders get trapped due to emotional decisions.
""")
        st.write("""
**Professional Rule:**  
Identify the market condition first — then apply the strategy that fits it.  
Not the other way around.
""")

    with b3:
        st.subheader("⚖️ Risk Management")
        st.write("""
Risk management is the single most important skill in trading.

You can have a great strategy and still lose everything if your risk is not controlled.  
Professional traders focus on **protecting capital first**, and profits come as a result of consistency.
""")
        st.write("""
### Core Concepts

**Stop Loss (SL):**  
Your predefined exit if the trade goes against you.

**Take Profit (TP):**  
Where you lock in gains.

**Risk-to-Reward Ratio (R:R):**  
How much you risk compared to how much you aim to make.
""")
        st.write("""
**Example:**  
Risk $100 to make $200 → 1:2 R:R  

Even if you only win 50% of trades, you are still profitable.
""")
        st.write("""
### Why Most Traders Fail
- Risking too much per trade  
- Not using stop losses  
- Letting emotions override rules  

### Key Takeaways
- Never risk more than 1–2% per trade  
- Survival is the goal — profits come after  
- Consistency beats big wins  
""")

    with b4:
        st.subheader("📈 Long vs Short")
        st.write("""
One of the biggest advantages in trading is that you can profit in **both directions**.

You are not limited to markets going up — you can also take advantage of falling prices.
""")
        st.write("""
### 📈 Long (Buy)
You enter a long position when you expect price to rise.

- Buy at a lower price  
- Sell at a higher price  
- Profit from upward movement  

### 📉 Short (Sell)
You enter a short position when you expect price to fall.

- Sell at a higher price  
- Buy back at a lower price  
- Profit from downward movement  
""")
        st.write("""
**Example:**  
BTC at $80,000  

- Long → profit if it rises to $85,000  
- Short → profit if it drops to $75,000  
""")
        st.write("""
### Key Takeaways
- You don't need a bullish market to make money  
- Direction matters more than bias  
- Always trade what the market is doing, not what you think it should do  
""")

    with b5:
        st.subheader("🧠 Trading Psychology")
        st.write("""
Trading is not just technical — it is psychological.

Most traders don't lose because of bad strategies.  
They lose because they cannot control their emotions.
""")
        st.write("""
### Common Emotional Mistakes
- Overtrading after wins  
- Revenge trading after losses  
- Fear of missing out (FOMO)  
- Moving stop losses to avoid being wrong  
""")
        st.write("""
**Professional Mindset:**  
Think in probabilities, not certainties.  

Losses are part of the system — not something to avoid at all costs.
""")
        st.write("""
### What Separates Professionals
- Discipline over emotion  
- Consistency over excitement  
- Process over outcome  

### Key Takeaways
- Psychology is often more important than strategy  
- One mistake can wipe multiple good trades  
- Your edge only works if you follow it  
""")


# ============================================================
# --- PAGE: TECHNICAL ANALYSIS ---
# ============================================================
if page == "Technical Analysis":
    st.header("⚙ Technical Analysis")

    t1, t2, t3, t4, t5 = st.tabs([
        "🏦 Liquidity",
        "🕯️ Price Action",
        "🌊 Volume",
        "📈 Market Structure",
        "🧲 Supply and Demand"
    ])

    with t1:
        st.subheader("Liquidity & Whale Behavior")
        st.write("""
Liquidity is the lifeblood of markets — it's what allows trades to be filled with minimal price disruption. 
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

Key principle: **Don't trade the liquidity target — trade the reaction.**

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
2. **Wait for price to approach:** Don't enter on the first impulse; wait for a retracement.
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

    with t3:
        st.subheader("🌊 Advanced Volume & Effort vs. Result")
        st.write("""
Volume is one of the clearest ways to see what the smart money is doing. But raw volume alone isn't enough — understanding the relationship between **effort (volume)** and **result (price movement)** gives you a window into supply and demand dynamics.

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
- Institutional players create **fake breakouts** to capture liquidity — volume gives clues if they're absorbing or pushing.

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
- Using volume with **liquidity concepts and FVGs** gives a complete picture of the market's hidden order flow.
""")
        st.video("https://www.youtube.com/watch?v=4C9F9R3QK2E")
        st.video("https://www.youtube.com/watch?v=L9zKkeo3BjQ")
        st.video("https://www.youtube.com/watch?v=8F7g5yHn3h0")

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
- Don't just trade breakouts — wait for **retests after BOS/CHoCH**.
- Align entries with **high-probability setups**: liquidity pool sweeps, reclaimed levels, and supporting volume.
- Use MSB to **filter trades**: avoid trading against dominant structure unless there's strong liquidity/volume evidence.

### Key Takeaways
- Market structure identifies **trend direction and hidden liquidity targets**.
- BOS and CHoCH are your signals to watch for **institutional involvement**.
- Always combine **MSB + FVG + Liquidity + Volume** for the most reliable setups.
- Trading in alignment with market structure reduces risk and increases probability of success.
""")
        st.video("https://www.youtube.com/watch?v=EJ3W0fJZP1A")
        st.video("https://www.youtube.com/watch?v=6sXvMvRLF5o")

    with t5:
        st.subheader("🧲 Supply & Demand Dynamics")
        st.write("""
Supply and demand are the foundation of all market movement. 
Price moves because of an imbalance between buyers and sellers — when demand exceeds supply, price rises; when supply exceeds demand, price falls.

### Understanding Supply & Demand Zones
Supply and demand zones are areas where institutions previously entered the market with significant volume.

- **Demand Zone:** Area where aggressive buying caused price to rally
- **Supply Zone:** Area where aggressive selling caused price to decline

These zones represent institutional interest and often become areas where price reacts again in the future.

### Why Institutions Use Supply & Demand
Large institutions cannot enter full positions instantly. 
Instead, they accumulate positions over time within key zones where enough opposing orders exist.

This creates:
- Sharp impulsive moves away from zones
- Strong reactions when price revisits them
- Repeated institutional participation

### Characteristics of Strong Zones

#### Strong Demand Zone
- Explosive bullish move away
- Large bullish candles
- High volume expansion
- Minimal time spent at base

#### Strong Supply Zone
- Aggressive bearish move away
- Strong displacement candles
- Heavy selling pressure
- Quick rejection from highs

### How Supply & Demand Works
Price constantly searches for balance between buyers and sellers.

When imbalance becomes extreme:
- Demand overwhelms supply → price rallies
- Supply overwhelms demand → price drops

The stronger the imbalance, the stronger the move.

### Trading Supply & Demand

Instead of chasing price:
- Wait for price to revisit a high-quality zone
- Look for confirmation/rejection
- Enter as institutions defend the level

Confluences that strengthen a setup:
- Liquidity sweep into zone
- Volume spike
- Market structure shift
- Strong rejection candle
- Trend alignment

### Common Mistakes
- Trading weak zones with no displacement
- Ignoring higher timeframe context
- Entering before confirmation
- Chasing after price already moved

### Institutional Supply & Demand Setups

| Setup | What It Implies |
|-------|----------------|
| Strong rally from demand zone | Institutional accumulation |
| Sharp selloff from supply zone | Institutional distribution |
| Return into unmitigated zone | Potential high-probability reaction |
| Liquidity sweep into zone | Smart money entry opportunity |

### Key Takeaways
- Supply & demand drive all markets  
- Institutions leave footprints through imbalances  
- Strong zones create explosive reactions  
- Wait for price to return into key areas  
- Trade confirmation, not emotion
""")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        st.video("https://www.youtube.com/watch?v=QwZT7T-TXT0")
        st.video("https://www.youtube.com/watch?v=0kK7CFK2S8A")
        st.video("https://www.youtube.com/watch?v=6Lx8g0P8Y8I")


# ============================================================
# --- PAGE: TYPES OF TRADING ---
# ============================================================
if page == "Types of Trading":
    st.header("🎯 Types of Trading")

    tt1, tt2, tt3, tt4, tt5, tt6, tt7 = st.tabs([
        "⚡ Scalping",
        "📅 Day Trading",
        "🌊 Swing Trading",
        "📈 Position Trading",
        "🤖 Algorithmic",
        "📰 News Trading",
        "🔄 Copy Trading"
    ])

    with tt1:
        st.subheader("⚡ Scalping")
        st.write("""
Scalping is the fastest style of trading, where traders aim to profit from tiny price movements over seconds to minutes. It is one of the most demanding disciplines in the markets — requiring extreme focus, fast execution, and an almost robotic level of emotional control.

### What is Scalping?
Scalpers enter and exit dozens or even hundreds of trades per day, targeting small gains on each. The goal is not a big win on any single trade — it's consistent accumulation of small profits that add up over time.

Unlike swing or position traders who can step away from the screen, scalpers are glued to real-time charts and order flow for the entire session.

### Key Characteristics
- **Timeframe:** 1-minute to 5-minute charts  
- **Hold Time:** Seconds to a few minutes  
- **Trade Frequency:** 10 to 100+ trades per day  
- **Profit Target per Trade:** 0.1% to 0.5%  
- **Risk per Trade:** Very tight stop losses — often just a few ticks

### How Scalping Works
Scalpers exploit short-term inefficiencies — tiny imbalances between buyers and sellers that create quick bursts of momentum. Common setups include:

- **Bid-Ask Spread Exploitation:** Buying at the bid and selling at the ask repeatedly in liquid markets.
- **Momentum Scalps:** Jumping into a strong directional move after a consolidation breakout and riding the first wave.
- **Liquidity Grabs:** Waiting for a quick spike to sweep a nearby liquidity pool and fading the reversal immediately.
- **Order Book Scalping:** Reading the live order book to see where large buy/sell walls exist and positioning ahead of them.

### Requirements for Scalping
- **Low latency execution** — every millisecond counts
- **Tight spreads** — high fees will destroy scalping profitability
- **High liquidity** — you need to enter and exit instantly without slippage
- **Laser focus** — one distraction can turn a winning trade into a loss

### Pros and Cons

| Pros | Cons |
|------|------|
| Fast feedback loop | Extremely stressful |
| Small capital needed | Fees can erode profits |
| Many opportunities daily | Requires full-time attention |
| No overnight risk | Mistakes happen fast |

### Is Scalping Right for You?
Scalping suits traders who thrive in fast-paced environments, can make decisions in seconds, and have the emotional resilience to shake off losses immediately. It is not suited for beginners.

### Key Takeaways
- Scalping profits from speed and volume, not size  
- Tight risk management is absolutely critical  
- Fees and spreads must be minimized  
- Requires a structured, repeatable system — not gut feeling  
- Best suited to highly liquid markets (BTC, ETH, major forex pairs)
""")
        st.video("https://www.youtube.com/watch?v=nS5uSDI1Uy4")

    with tt2:
        st.subheader("📅 Day Trading")
        st.write("""
Day trading is the practice of opening and closing all positions within the same trading day. Day traders never hold overnight, eliminating the risk of unexpected news or price gaps while the market is closed. It is one of the most popular and widely practiced trading styles.

### What is Day Trading?
Day traders work on intraday timeframes — typically 5-minute to 1-hour charts — looking for clear directional moves that can be captured and closed before the session ends. The style combines the speed of scalping with the strategic patience of swing trading.

### Key Characteristics
- **Timeframe:** 5-minute to 1-hour charts  
- **Hold Time:** Minutes to several hours  
- **Trade Frequency:** 2 to 10 trades per day  
- **Profit Target per Trade:** 0.5% to 3%  
- **Risk per Trade:** Typically 0.5% to 2% of capital

### How Day Trading Works
Day traders look for high-probability setups that align with the day's dominant trend or a clear range. Common approaches include:

- **Opening Range Breakout (ORB):** Trading the breakout of the first 15-30 minutes of the session, which often sets the tone for the day.
- **Trend Following:** Identifying the intraday trend direction and only taking trades in that direction.
- **Reversal Trading:** Spotting exhausted moves and fading them at key support/resistance levels.
- **News Catalysts:** Capitalizing on price moves triggered by economic data, earnings, or breaking news.

### The Day Trader's Routine
A professional day trader is not randomly trading — they follow a strict daily routine:

1. **Pre-market preparation:** Review overnight price action, key levels, and news events.
2. **Session open:** Identify the bias — bullish, bearish, or ranging.
3. **Trade execution window:** Most opportunities occur in the first 2 hours and the last hour of the session.
4. **Review:** Analyze trades, log results, and identify mistakes.

### Pros and Cons

| Pros | Cons |
|------|------|
| No overnight risk | Requires full-day attention |
| Daily feedback on performance | High screen time and mental load |
| Clear trading sessions | Tax implications in some countries |
| Suitable for most liquid markets | Easy to overtrade |

### Key Takeaways
- Day trading requires a clear, pre-planned strategy — not improvisation  
- Session timing matters — the best setups cluster around market opens and closes  
- Discipline to stop trading after a loss limit is essential  
- Most successful day traders focus on 1 to 3 specific setups they know extremely well
""")
        st.video("https://www.youtube.com/watch?v=mxAOUPxlqF0")

    with tt3:
        st.subheader("🌊 Swing Trading")
        st.write("""
Swing trading is the art of capturing medium-term price "swings" — moves that develop over days to weeks. It is widely considered the most accessible trading style for people who cannot dedicate full-time hours to watching charts, as it requires only a few hours of analysis per day.

### What is Swing Trading?
Swing traders aim to enter at the beginning of a significant price move and exit near the end before it reverses. They rely on higher-timeframe structure and key levels, using daily and 4-hour charts as their primary tools.

### Key Characteristics
- **Timeframe:** 4-hour to daily charts  
- **Hold Time:** 2 days to several weeks  
- **Trade Frequency:** 2 to 10 trades per month  
- **Profit Target per Trade:** 3% to 15%+  
- **Risk per Trade:** Typically 1% to 2% of capital

### How Swing Trading Works
Swing traders are not chasing every small move. They wait for the market to set up a high-probability scenario and then strike decisively. Core approaches include:

- **Trend Pullback Entries:** Waiting for price to pull back to a key support level (EMA, demand zone, Fibonacci level) within a larger uptrend, then entering long with the trend.
- **Breakout Swings:** Entering after price breaks through a major resistance level with strong volume, targeting the next significant resistance.
- **Range Trading:** Buying at the low of an established range and selling at the high — repeat until the range breaks.
- **Catalyst-Driven Swings:** Entering ahead of or just after a fundamental catalyst (earnings, protocol upgrade, macro event) that is likely to drive sustained directional movement.

### The Swing Trader's Edge
The swing trader's biggest advantage is **patience and selectivity**. They are not forced to trade every day. By waiting for only the best setups, they achieve a higher win rate and a better risk-to-reward ratio than traders who over-trade.

### Pros and Cons

| Pros | Cons |
|------|------|
| Low time commitment | Exposed to overnight and weekend gaps |
| Better R:R ratios | Requires patience — fewer trades |
| Less affected by noise | Positions can reverse before target |
| Suitable for part-time traders | Needs strong conviction in thesis |

### Key Takeaways
- Swing trading rewards patience — the best setups are worth waiting for  
- Higher timeframe structure should always guide entry timing  
- Position sizing and stop placement are more important than entry timing  
- Combine technical levels with market structure and volume for the highest-probability trades
""")
        st.video("https://www.youtube.com/watch?v=mxAOUPxlqF0")

    with tt4:
        st.subheader("📈 Position Trading")
        st.write("""
Position trading is the longest-term active trading style, sitting between traditional investing and swing trading. Position traders hold trades for weeks, months, or even years — riding the full length of a major market trend. It is the most patient discipline in active trading.

### What is Position Trading?
Position traders focus on the macro picture. They are not concerned with daily volatility or short-term noise — they look for major structural shifts in the market and position themselves to profit from the entire move. Think of it as "catching the full wave" rather than a ripple.

### Key Characteristics
- **Timeframe:** Weekly and monthly charts  
- **Hold Time:** Weeks to years  
- **Trade Frequency:** A few trades per year  
- **Profit Target per Trade:** 20% to 500%+  
- **Risk per Trade:** 2% to 5% of capital (wider stops, longer timeframe)

### How Position Trading Works
Position traders use a combination of fundamental and technical analysis to identify assets at a structural turning point. They then enter with wide stops and hold through volatility, trusting the macro thesis.

Core approaches include:

- **Macro Trend Following:** Identifying major bull or bear markets and positioning early using weekly/monthly chart breakouts.
- **Accumulation Zone Entries:** Entering near historically significant support areas — often the same zones where institutions are quietly accumulating.
- **Fundamental Catalyst Thesis:** A strong narrative (e.g., Bitcoin halving cycle, ETF approval, institutional adoption) drives the trade thesis and is confirmed by technical structure.
- **Dollar-Cost Averaging (DCA) Into Positions:** Position traders often scale into positions over time rather than entering all at once.

### Managing a Position Trade
Because position trades are held for so long, management is key:

- **Scale-in:** Enter in tranches as the thesis confirms.
- **Trail your stop:** Move stop losses up as price advances to protect gains.
- **Take partial profits:** Sell portions at key resistance levels while keeping the core position running.
- **Review regularly:** Re-evaluate the fundamental thesis weekly/monthly. If the reason for the trade no longer exists, exit.

### Pros and Cons

| Pros | Cons |
|------|------|
| Massive potential gains | Very long time to realize profits |
| Low time commitment | Requires high conviction and patience |
| Rides full macro trends | Wide stops mean larger initial risk |
| Less affected by noise | Fundamental thesis can change |

### Key Takeaways
- Position trading is about macro conviction, not short-term price action  
- Wide stops are normal — don't let volatility shake you out of a good trade  
- The best position trades are identified at the start of a new macro trend  
- Fundamental understanding of the asset is just as important as technical analysis
""")
        st.video("https://www.youtube.com/watch?v=mxAOUPxlqF0")

    with tt5:
        st.subheader("🤖 Algorithmic Trading")
        st.write("""
Algorithmic trading — commonly called "algo trading" or "automated trading" — uses computer programs and pre-coded rules to execute trades automatically, without human intervention in each individual trade. It is the dominant form of trading in institutional markets and is growing rapidly in crypto.

### What is Algorithmic Trading?
Instead of manually watching charts and clicking buy/sell, an algo trader writes a program that defines exactly when, how, and at what size to enter and exit trades. The computer executes these rules at machine speed, without emotion.

### Key Characteristics
- **Timeframe:** Any — from microseconds (HFT) to daily  
- **Hold Time:** Microseconds to weeks, depending on strategy  
- **Trade Frequency:** Fully automated — can execute thousands of trades per day  
- **Skills Required:** Programming (Python, C++, Pine Script), statistics, and trading knowledge

### How Algorithmic Trading Works
An algo trader builds a **strategy** — a set of rules that define:

1. **Entry conditions:** e.g., "Buy when the 9 EMA crosses above the 21 EMA and RSI is below 60."
2. **Exit conditions:** e.g., "Sell when price hits +3% from entry or crosses back below the 9 EMA."
3. **Position sizing:** e.g., "Risk exactly 1% of capital per trade."
4. **Risk filters:** e.g., "Do not trade if market volatility (ATR) is above X."

The algorithm monitors the market 24/7 and fires trades the moment conditions are met.

### Types of Algorithmic Strategies
- **Trend Following:** Automated entry in the direction of a moving average crossover or breakout.
- **Mean Reversion:** Identifies when price is statistically overextended from its average and bets on a return.
- **Market Making:** Places buy and sell orders simultaneously to profit from the bid-ask spread.
- **Arbitrage:** Exploits price differences of the same asset across different exchanges simultaneously.
- **High-Frequency Trading (HFT):** Executes thousands of trades per second, profiting from tiny price differences at extreme speed.

### Backtesting — The Foundation of Algo Trading
Before deploying any algorithm with real money, traders **backtest** it — running the strategy against historical price data to see how it would have performed. Key metrics:

- **Win Rate:** Percentage of profitable trades
- **Sharpe Ratio:** Return relative to risk
- **Max Drawdown:** Worst peak-to-trough loss period
- **Expectancy:** Average profit per trade over time

### Pros and Cons

| Pros | Cons |
|------|------|
| No emotional decision-making | Requires programming skills |
| Runs 24/7 without supervision | Overfitting risk during backtesting |
| Executes at machine speed | Can fail catastrophically if not monitored |
| Completely rule-based and consistent | Markets change — strategies need updating |

### Key Takeaways
- Algorithmic trading removes human emotion from execution — but adds technical complexity  
- A strategy that backtests perfectly is not guaranteed to work live — always paper trade first  
- Risk management rules must be hard-coded — the algorithm should never bypass them  
- Start simple: a profitable, simple algo beats a complex one that breaks
""")
        st.video("https://www.youtube.com/watch?v=CpKFhPSJ0Fo")

    with tt6:
        st.subheader("📰 News Trading")
        st.write("""
News trading is the strategy of taking positions based on the impact of economic data releases, corporate announcements, geopolitical events, or breaking news that causes sudden, significant price movements. It is one of the most high-risk, high-reward styles of trading.

### What is News Trading?
Markets are fundamentally driven by information. When new, unexpected information hits the market — a surprise interest rate decision, a major hack, a regulatory announcement — price can move 5%, 10%, or even 50% in minutes. News traders try to be positioned for these explosive moves.

### Key Characteristics
- **Timeframe:** 1-minute to 15-minute charts (intraday reaction) or daily for longer-term repositioning  
- **Hold Time:** Minutes to a few days  
- **Trade Frequency:** Event-driven — trade only when a catalyst exists  
- **Key Skill:** Speed, news interpretation, and understanding market expectations vs. reality

### How News Trading Works
The key insight in news trading is: **it's not about what the news IS — it's about what the news IS RELATIVE TO EXPECTATIONS.**

If the market expects strong GDP growth and the actual number comes in even stronger, price rallies. If it comes in slightly below the already-high expectation, price can crash even if the absolute number is "good." This is the concept of **"buy the rumor, sell the news."**

#### Two Main Approaches:

**1. Pre-News Positioning (High Risk)**
Taking a position before the news release based on your forecast of the outcome. This is essentially speculation on a binary event — if you're right, rewards are huge. If you're wrong, stop-outs can be severe.

**2. Post-News Reaction Trading (Lower Risk)**
Waiting for the initial volatility spike after the news release, letting the market show its true hand, then trading in the direction of the confirmed move. This avoids the chaotic "first spike" and trades the more sustainable follow-through.

### Types of High-Impact News Events

| Category | Examples |
|----------|---------|
| Macroeconomic | CPI, FOMC rate decisions, NFP, GDP |
| Crypto-Specific | ETF approvals, exchange hacks, protocol upgrades, regulatory bans |
| Corporate | Earnings reports, CEO resignations, partnerships |
| Geopolitical | Wars, sanctions, political elections |

### Managing Risk Around News
- **Reduce position size** before known high-impact events — volatility spikes unpredictably.
- **Widen stops** to account for the initial spike before true direction is established.
- **Use limit orders** not market orders — spreads widen dramatically during news.
- **Never trade all major news events** — only those where you have a genuine edge or thesis.

### Pros and Cons

| Pros | Cons |
|------|------|
| Explosive short-term opportunities | Unpredictable outcomes even with good analysis |
| Clear catalyst for the move | Spreads widen and slippage is common |
| Well-defined event timing | Requires very fast execution |
| Can profit in any direction | "Buy the rumor, sell the news" reversals are common |

### Key Takeaways
- News trading profits from the **gap between expectation and reality** — not just the news itself  
- The post-news reaction is often safer than pre-news speculation  
- Always reduce size and widen stops around major events  
- Know your catalyst calendars — economic, crypto, and geopolitical events are your map
""")
        st.video("https://www.youtube.com/watch?v=uUBpU5Nue6M")

    with tt7:
        st.subheader("🔄 Copy Trading")
        st.write("""
Copy trading is a method of trading where you automatically replicate the trades of an experienced trader in real time. It allows beginners to participate in the markets and generate returns without needing to develop their own trading skills — though it comes with its own significant risks and limitations.

### What is Copy Trading?
Copy trading platforms connect "strategy providers" (experienced traders) with "followers" (investors who copy them). When the strategy provider opens or closes a trade, the same trade is automatically mirrored in the follower's account, proportional to their allocated capital.

### Key Characteristics
- **Timeframe:** Depends entirely on the trader being copied  
- **Skill Required:** Low for the copier — high for the provider  
- **Capital Needed:** Usually low minimums ($100–$500 on most platforms)  
- **Platforms:** eToro, Bybit Copy Trading, Bitget, OKX, BingX

### How Copy Trading Works

1. **Choose a strategy provider:** Browse ranked traders by performance metrics — ROI, win rate, drawdown, number of followers, trading style.
2. **Allocate capital:** Decide how much of your portfolio to assign to copying this trader.
3. **Set risk parameters:** Many platforms let you set a maximum drawdown at which the copy is automatically stopped.
4. **Monitor:** Copy trading is not entirely passive — you should regularly review performance and be prepared to stop copying if results deteriorate.

### What to Look For in a Trader to Copy

| Metric | What It Tells You |
|--------|------------------|
| ROI (Return on Investment) | Total profit percentage over the tracked period |
| Max Drawdown | Worst loss from peak to trough — measures risk |
| Win Rate | Percentage of profitable trades |
| Sharpe Ratio | Return relative to risk taken |
| Trade History Length | Longer is more reliable — avoid traders with <3 months of data |
| Risk Score | Platform-assigned score for overall aggressiveness |

### The Hidden Risks of Copy Trading
Copy trading appears passive and safe, but carries major risks that beginners overlook:

- **Past performance is not a guarantee:** A trader with 6 months of incredible results can blow up on month 7.
- **Drawdown is real:** If you copy a trader who enters a 40% drawdown, you lose 40% of your allocated capital.
- **Slippage:** Your copied trade may execute at a slightly different price than the original, especially on fast moves.
- **No learning:** Copy trading without studying *why* the trader takes positions means you never develop your own edge.
- **Provider incentives:** Some platforms pay providers per follower, not per profit — creating conflicts of interest.

### Copy Trading vs. Learning to Trade

| Copy Trading | Learning to Trade |
|-------------|------------------|
| Immediate market participation | Takes months to years to develop |
| No skill required | Builds a transferable, lasting skill |
| Returns dependent on someone else | Full control of your own performance |
| Risk of total loss if provider fails | Risk managed by your own rules |

### Key Takeaways
- Copy trading is a tool, not a strategy — always understand the risk of who you're copying  
- Diversify across multiple traders rather than concentrating all capital on one  
- Set a strict maximum drawdown limit and honor it  
- Use copy trading as a way to study professional behavior — observe what they trade and why  
- Never invest money you cannot afford to lose, even in copy trading
""")
        st.video("https://www.youtube.com/watch?v=CvkF5LumEgo")


# ============================================================
# --- PAGE: CHARTS ---
# ============================================================
if page == "Charts":
    st.title("📊 Chart")

    symbol_map = {
        "BTC": "BINANCE:BTCUSDT", "ETH": "BINANCE:ETHUSDT", "SOL": "BINANCE:SOLUSDT",
        "XRP": "BINANCE:XRPUSDT", "ONDO": "BYBIT:ONDOUSDT", "BNB": "BINANCE:BNBUSDT",
        "Silver": "TVC:SILVER", "Gold": "TVC:GOLD", "Oil": "TVC:UKOIL",
        "S&P 500": "SPY", "AAPL": "NASDAQ:AAPL", "NVDA": "NASDAQ:NVDA"
    }

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


# ============================================================
# --- PAGE: TOOLS ---
# ============================================================
if page == "Tools":
    st.title("⚒️ Professional Trading Tools")

    t_pl, t_journal, t_compound, t_dca, t_be, t_pos, t_stress, t_sentiment = st.tabs([
        "💰 P&L Calculator",
        "📊 Journal",
        "📈 Compound",
        "🎯 DCA",
        "⚖️ Breakeven",
        "📏 Position %",
        "⚠️ Stress Test",
        "🧠 Sentiment"
    ])

    with t_pl:
        st.markdown('<p class="indicator-title">💰 P&L Calculator</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            coin = st.text_input("Coin Symbol", placeholder="e.g., BTC").upper()
            capital = st.number_input("Capital (USD)", min_value=0.0)
            leverage = st.number_input("Leverage", min_value=1.0, value=1.0)

        with col2:
            entry = st.number_input("Entry Price", min_value=0.0, format="%.4f")
            sl = st.number_input("Stop Loss Price", min_value=0.0, format="%.4f")
            tp = st.number_input("Take Profit Price", min_value=0.0, format="%.4f")

        st.markdown("###")

        if st.button("Calculate", use_container_width=True, key="pnl_btn"):
            if not coin or capital <= 0 or entry <= 0:
                st.error("Fill in all fields.")
            else:
                is_long = tp > entry

                if (is_long and sl >= entry) or (not is_long and sl <= entry):
                    st.error("Invalid Stop Loss")
                else:
                    position_size = capital * leverage
                    amount_coin = position_size / entry

                    pnl_tp = (tp - entry) * amount_coin if is_long else (entry - tp) * amount_coin
                    pnl_sl = (entry - sl) * amount_coin if is_long else (sl - entry) * amount_coin

                    percent_gain = (pnl_tp / capital) * 100
                    percent_loss = (pnl_sl / capital) * 100
                    rrr = abs(pnl_tp / pnl_sl) if pnl_sl != 0 else 0

                    st.subheader(f"{coin} {'LONG' if is_long else 'SHORT'}")

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Gain", f"${abs(pnl_tp):.2f}", f"{percent_gain:.2f}%")
                    c2.metric("Loss", f"-${abs(pnl_sl):.2f}", f"-{abs(percent_loss):.2f}%")
                    c3.metric("R:R", f"1 : {rrr:.2f}")

                    if rrr < 2:
                        st.warning("Low R:R")
                    else:
                        st.success("Good R:R")

    with t_journal:
        st.markdown('<p class="indicator-title">📊 Trade Journal</p>', unsafe_allow_html=True)

        if 'history' not in st.session_state:
            st.session_state.history = []

        with st.form("log_trade"):
            c1, c2, c3 = st.columns(3)

            t_type = c1.selectbox("Type", ["LONG", "SHORT"])
            t_cap = c1.number_input("Capital ($)", value=100.0)

            t_lev = c2.number_input("Leverage", value=10)
            p_mode = c2.radio("Input", ["%", "$"])

            t_val = c3.number_input("P&L Value", value=0.0)

            if st.form_submit_button("Log Trade"):
                usd = t_val if p_mode == "$" else (t_val / 100) * t_cap
                pct = t_val if p_mode == "%" else (t_val / t_cap) * 100

                st.session_state.history.append({
                    "Type": t_type,
                    "Capital": t_cap,
                    "P&L $": usd,
                    "P&L %": pct
                })

        st.markdown("###")

        if st.session_state.history:
            st.table(pd.DataFrame(st.session_state.history))

        if st.button("Clear Journal"):
            st.session_state.history = []
            st.rerun()

    with t_compound:
        st.markdown('<p class="indicator-title">🚀 Compound Calculator</p>', unsafe_allow_html=True)

        start = st.number_input("Starting Capital ($)", value=0.0)
        doubles = st.number_input("Times to Double", value=0)

        if st.button("Calculate", key="compound_btn"):
            if start > 0 and doubles > 0:
                val = start
                data = []

                for i in range(doubles + 1):
                    data.append({"Step": i, "Balance": val})
                    val *= 2

                st.dataframe(pd.DataFrame(data), use_container_width=True)
                st.metric("Final Balance", f"${val/2:,.2f}")
            else:
                st.warning("Enter valid values.")

    with t_dca:
        st.markdown('<p class="indicator-title">🎯 DCA Calculator</p>', unsafe_allow_html=True)

        p1 = st.number_input("Price 1", value=60000.0)
        a1 = st.number_input("Amount 1", value=500.0)
        p2 = st.number_input("Price 2", value=55000.0)
        a2 = st.number_input("Amount 2", value=500.0)

        if p1 > 0 and p2 > 0:
            avg = (a1 + a2) / ((a1 / p1) + (a2 / p2))
            st.metric("Average Entry", f"${avg:,.2f}")

    with t_be:
        st.markdown('<p class="indicator-title">⚖️ Breakeven</p>', unsafe_allow_html=True)

        price = st.number_input("Entry Price", value=50000.0)
        fee = st.number_input("Fee %", value=0.06)

        st.metric("Breakeven Price", f"${price * (1 + (fee/100)*2):,.2f}")

    with t_pos:
        st.markdown('<p class="indicator-title">📏 Position Size</p>', unsafe_allow_html=True)

        bal = st.number_input("Wallet ($)", value=1000.0)
        risk = st.slider("Risk %", 1, 100, 10)
        lev = st.number_input("Leverage", value=10)

        st.metric("Margin Used", f"${(bal * (risk/100)) / lev:,.2f}")

    with t_stress:
        st.markdown('<p class="indicator-title">⚠️ Stress Test</p>', unsafe_allow_html=True)

        lev = st.slider("Leverage", 1, 100, 20)

        st.error(f"Liquidation: {100/lev:.2f}% move")
        st.warning(f"1% move = {lev}% P&L")

    with t_sentiment:
        st.image("https://alternative.me/crypto/fear-and-greed-index.png")


# ============================================================
# --- PAGE: DONATE ---
# ============================================================
if page == "Donate":
    st.title("💛 Support Roman's Trades")
    st.write("If this platform has helped your trading journey, consider sending a donation. Every contribution keeps this project alive and growing. Thank you! 🙏")
    st.divider()

    wallets = [
        {
            "label": "₿ Bitcoin (BTC)",
            "network": "Bitcoin Network",
            "address": "bc1q84lxedy3gjfecy52lfw2pdyw2puedd5v876ek0",
            "color": "#F7931A"
        },
        {
            "label": "Ξ Ethereum (ETH)",
            "network": "ERC-20 Network",
            "address": "0xF4fbB1A81ed4b8aee4FB8c225311f3F535A9958F",
            "color": "#627EEA"
        },
        {
            "label": "◎ Solana (SOL)",
            "network": "Solana Network",
            "address": "8SedZgSzvYBrGckq6ySKqHXDRBKBYPgS1VhUipZua4fZ",
            "color": "#9945FF"
        },
    ]

    for w in wallets:
        st.markdown(f"""
        <div class="wallet-card" style="border-left: 4px solid {w['color']};">
            <div class="wallet-label">{w['label']}</div>
            <div style="color: #8B949E; font-size: 13px; margin-bottom: 10px;">Network: {w['network']}</div>
            <div class="wallet-addr">{w['address']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.code(w["address"], language=None)

    st.divider()
    st.info("⚠️ Always double-check the wallet address and network before sending. Crypto transactions are irreversible.")


# ============================================================
# --- PAGE: CONTACT ---
# ============================================================
if page == "Contact":
    st.title("📬 Contact & Support")
    st.write("Have a question, suggestion, or issue? Fill out the form below and I'll get back to you as soon as possible.")
    st.divider()

    with st.form("contact_form", clear_on_submit=True):
        st.markdown("### Submit a Ticket")

        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input("Full Name *", placeholder="e.g. John Smith")
            gmail = st.text_input("Your Gmail Address *", placeholder="yourname@gmail.com")

        with col2:
            subject = st.selectbox("Subject *", [
                "General Question",
                "Bug / Technical Issue",
                "Feature Request",
                "Indicator Question",
                "Strategy Help",
                "Other"
            ])
            urgency = st.selectbox("Priority", ["Low", "Medium", "High"])

        message = st.text_area(
            "Message *",
            placeholder="Describe your question or issue in detail...",
            height=180
        )

        agree = st.checkbox("I confirm this is my Gmail address and I consent to being contacted.")

        submitted = st.form_submit_button("Send Ticket 🚀", use_container_width=True)

        if submitted:
            if not full_name or not gmail or not message:
                st.error("Please fill in all required fields (Name, Gmail, and Message).")
            elif "@gmail.com" not in gmail.lower():
                st.error("Please enter a valid Gmail address (must contain @gmail.com).")
            elif not agree:
                st.error("Please check the confirmation box before submitting.")
            else:
                email_subject = f"[Crypto Mastery Ticket] {subject} — {urgency} Priority"
                email_body = (
                    f"Name: {full_name}\n"
                    f"Gmail: {gmail}\n"
                    f"Subject: {subject}\n"
                    f"Priority: {urgency}\n\n"
                    f"Message:\n{message}"
                )
                import urllib.parse
                mailto_link = (
                    f"mailto:romanstrades@protonmail.com"
                    f"?subject={urllib.parse.quote(email_subject)}"
                    f"&body={urllib.parse.quote(email_body)}"
                )

                st.success("✅ Ticket ready! Click the button below to open your email client and send.")
                st.markdown(f"""
                <a href="{mailto_link}" target="_blank">
                    <button style="
                        background-color: #238636;
                        color: white;
                        border: none;
                        padding: 14px 28px;
                        font-size: 16px;
                        font-weight: 700;
                        border-radius: 8px;
                        cursor: pointer;
                        width: 100%;
                        margin-top: 10px;
                    ">
                        📧 Open Email Client to Send
                    </button>
                </a>
                """, unsafe_allow_html=True)

    st.divider()
    st.markdown("📩 You can also reach out directly at **romanstrades@protonmail.com**")
