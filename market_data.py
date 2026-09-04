from datetime import datetime


INDEX_ORDER = ("VNINDEX", "VN30", "HNXINDEX", "UPCOMINDEX")


def build_market_week(index_rows, trading_values, foreign_rows):
    indices = []
    for name in INDEX_ORDER:
        rows = index_rows[name]
        first_close = float(rows[0][1])
        last_close = float(rows[-1][1])
        change = last_close - first_close
        percent = change / first_close * 100
        indices.append({
            "name": name,
            "close": f"{last_close:,.2f}",
            "change": f"{change:+,.2f}",
            "percent": f"{percent:+.2f}%",
        })

    average_value = sum(float(value) for value in trading_values) / len(trading_values) / 1_000_000_000
    flow = [
        {"date": datetime.fromisoformat(str(day)).strftime("%d/%m"), "value": round(float(value) / 1_000_000_000)}
        for day, value in sorted(foreign_rows)[-5:]
    ]
    return {"indices": indices, "trading_value": f"{average_value:,.0f}", "foreign_flow": flow}

def fetch_market_week(start, end):
    from vnstock_data import Market, Trading
    market = Market(); rows = {}
    for symbol in INDEX_ORDER:
        frame = market.index(symbol).ohlcv(start=start, end=end)
        if frame.empty: raise ValueError(f"Không có dữ liệu {symbol} trong khoảng đã chọn.")
        rows[symbol] = [(str(day), close) for day, close in zip(frame["time"], frame["close"])]
    trades = market.index("VNINDEX").trade_history(start=start, end=end)
    foreign = Trading(source="cafef", symbol="VNINDEX").foreign_trade(start=start, end=end)
    if trades.empty or foreign.empty: raise ValueError("Không có đủ dữ liệu thanh khoản hoặc khối ngoại.")
    result = build_market_week(rows, trades["total_value"].tolist(), list(zip(foreign.index, foreign["fr_net_value"])))
    result["meta"] = {"updated_at": datetime.now().strftime("%d/%m/%Y"), "source": "vnstock Silver (KBS, CafeF)"}
    return result
