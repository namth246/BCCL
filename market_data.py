from datetime import datetime, timedelta


INDEX_ORDER = ("VNINDEX", "VN30", "HNXINDEX", "UPCOMINDEX")


def foreign_trade_query_start(week_start):
    """CafeF treats the start date as exclusive for foreign-trade history."""
    return (datetime.fromisoformat(week_start).date() - timedelta(days=1)).isoformat()


def build_foreign_rankings(ranking_rows):
    totals = {}
    for row in ranking_rows:
        symbol = str(row["symbol"])
        totals[symbol] = totals.get(symbol, 0) + float(row["net_value"])

    def normalize(rows):
        return [
            {"ticker": symbol, "value": round(value / 1_000_000_000)}
            for symbol, value in rows[:5]
        ]

    buys = sorted(((symbol, value) for symbol, value in totals.items() if value > 0), key=lambda row: row[1], reverse=True)
    sells = sorted(((symbol, value) for symbol, value in totals.items() if value < 0), key=lambda row: row[1])
    return {"top_buy": normalize(buys), "top_sell": normalize(sells)}


def select_latest_five_sessions(trading_days):
    sessions = [datetime.fromisoformat(str(day)).date().isoformat() for day in trading_days]
    if len(sessions) < 5:
        raise ValueError("Không có đủ 5 phiên giao dịch để xếp hạng dòng tiền khối ngoại.")
    return sessions[-5:]


def fetch_foreign_rankings(trading_days, ranking=None):
    if ranking is None:
        from vnstock_data import Insights
        ranking = Insights().ranking

    rows = []
    successful_sessions = 0
    sessions = sorted({datetime.fromisoformat(str(day)).date().isoformat() for day in trading_days}, reverse=True)
    for trading_date in sessions:
        buys = ranking.foreign_buy(date=trading_date, limit=1000)
        sells = ranking.foreign_sell(date=trading_date, limit=1000)
        if buys.empty or sells.empty:
            continue
        rows.extend(buys[["symbol", "net_value"]].to_dict("records"))
        rows.extend(sells[["symbol", "net_value"]].to_dict("records"))
        successful_sessions += 1
        if successful_sessions == 5:
            break
    if not rows:
        raise ValueError("Không có dữ liệu xếp hạng khối ngoại cho các phiên đã chọn.")
    return build_foreign_rankings(rows)


def build_market_week(index_rows, trading_values, foreign_rows, week_start):
    start_date = datetime.fromisoformat(week_start).date()
    indices = []
    for name in INDEX_ORDER:
        previous_close = None
        current_close = None
        for day, close in sorted(index_rows[name], key=lambda row: str(row[0])):
            if datetime.fromisoformat(str(day)).date() < start_date:
                previous_close = float(close)
            else:
                current_close = float(close)
        if previous_close is None or current_close is None:
            raise ValueError(f"Thiếu dữ liệu để tính thay đổi tuần của {name}.")
        change = current_close - previous_close
        percent = change / previous_close * 100
        indices.append({
            "name": name,
            "close": f"{current_close:,.2f}",
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
    history_start = (datetime.fromisoformat(start).date() - timedelta(days=14)).isoformat()
    market = Market(); rows = {}
    for symbol in INDEX_ORDER:
        frame = market.index(symbol).ohlcv(start=history_start, end=end)
        if frame.empty: raise ValueError(f"Không có dữ liệu {symbol} trong khoảng đã chọn.")
        rows[symbol] = [(str(day), close) for day, close in zip(frame["time"], frame["close"])]
    trades = market.index("VNINDEX").trade_history(start=start, end=end)
    foreign = Trading(source="cafef", symbol="VNINDEX").foreign_trade(start=foreign_trade_query_start(start), end=end)
    foreign_history = Trading(source="cafef", symbol="VNINDEX").foreign_trade(start=history_start, end=end)
    if trades.empty or foreign.empty: raise ValueError("Không có đủ dữ liệu thanh khoản hoặc khối ngoại.")
    result = build_market_week(rows, trades["total_value"].tolist(), list(zip(foreign.index, foreign["fr_net_value"])), start)
    result.update(fetch_foreign_rankings(select_latest_five_sessions(foreign_history.index)))
    result["meta"] = {"updated_at": datetime.now().strftime("%d/%m/%Y"), "source": "vnstock Silver (KBS, CafeF, VND)"}
    return result
