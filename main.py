from fastapi import FastAPI
from indicators import get_prices, ema, rsi, parabolic_sar
from datetime import datetime

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "running"}

@app.get("/signal")
def signal(symbol: str = "BTCUSDT"):
    closes, highs, lows = get_prices(symbol)

    ema_fast = ema(closes[-20:], 9)
    ema_slow = ema(closes[-20:], 21)
    rsi_val = rsi(closes)
    sar_ok = parabolic_sar(highs, lows)

    action = "WAIT"
    confidence = 0

    if ema_fast > ema_slow and rsi_val < 70 and sar_ok:
        action = "BUY"
        confidence = 85

    elif ema_fast < ema_slow and rsi_val > 30 and not sar_ok:
        action = "SELL"
        confidence = 85

    return {
        "pair": symbol,
        "signal": action,
        "ema_fast": round(ema_fast, 4),
        "ema_slow": round(ema_slow, 4),
        "rsi": round(rsi_val, 2),
        "confidence": confidence,
        "timeframe": "1 MIN",
        "time": datetime.utcnow()
    }
