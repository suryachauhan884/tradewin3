import rrequestsimport math

BINANCE_URL = "https://api.binance.com/api/v3/klines"

def get_prices(symbol="BTCUSDT", interval="1m", limit=100):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    r = requests.get(BINANCE_URL, params=params, timeout=10)
    data = r.json()

    closes = [float(c[4]) for c in data]
    highs = [float(c[2]) for c in data]
    lows  = [float(c[3]) for c in data]
    return closes, highs, lows


def ema(values, period):
    k = 2 / (period + 1)
    ema_val = values[0]
    for price in values[1:]:
        ema_val = price * k + ema_val * (1 - k)
    return ema_val


def rsi(values, period=14):
    gains, losses = [], []
    for i in range(1, len(values)):
        diff = values[i] - values[i-1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def parabolic_sar(highs, lows):
    return highs[-1] > lows[-2]   # simplified SAR logic
