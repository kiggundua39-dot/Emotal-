from dataclasses import dataclass
from typing import List


@dataclass
class Analysis:
    signal: str
    reason: str
    ema_fast: float
    ema_slow: float
    rsi: float


def calculate_ema(values: List[float], period: int) -> float:
    if len(values) < period:
        raise ValueError("Not enough candles")

    multiplier = 2 / (period + 1)
    ema = sum(values[:period]) / period

    for price in values[period:]:
        ema = (price - ema) * multiplier + ema

    return ema


def calculate_rsi(values: List[float], period: int = 14) -> float:
    if len(values) <= period:
        raise ValueError("Not enough candles")

    changes = [
        values[i] - values[i - 1]
        for i in range(1, len(values))
    ]

    gains = [max(change, 0) for change in changes]
    losses = [max(-change, 0) for change in changes]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (
            avg_gain * (period - 1) + gains[i]
        ) / period
        avg_loss = (
            avg_loss * (period - 1) + losses[i]
        ) / period

    if avg_loss == 0:
        return 100.0

    return 100 - (100 / (1 + avg_gain / avg_loss))


def analyse_market(closes: List[float]) -> Analysis:
    fast = calculate_ema(closes, 9)
    slow = calculate_ema(closes, 21)
    rsi = calculate_rsi(closes, 14)

    signal = "HOLD"
    reason = "No clear trading opportunity"

    if fast > slow and 50 < rsi < 65:
        signal = "BUY"
        reason = "Bullish EMA alignment and RSI confirmation"

    elif fast < slow and 35 < rsi < 50:
        signal = "SELL"
        reason = "Bearish EMA alignment and RSI confirmation"

    return Analysis(signal, reason, fast, slow, rsi)


if __name__ == "__main__":
    print("Market Analyst initialized.")
    print("Execution mode: DISABLED")
  
