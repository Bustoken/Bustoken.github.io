import json
import os
import yfinance as yf

# 국내외 대표 ETF 및 테마 종목 구성
THEMES = {
    "AI & 반도체/전력": [
        {"ticker": "QQQ", "name": "미국 나스닥100 (QQQ)", "market": "US"},
        {"ticker": "381180.KS", "name": "TIGER 미국배당다우존스", "market": "KR"},
        {"ticker": "NVDA", "name": "엔비디아 (NVDA)", "market": "US"},
        {"ticker": "VST", "name": "비스트라 전력 (VST)", "market": "US"}
    ],
    "고배당 & 금리 피봇": [
        {"ticker": "SCHD", "name": "미국 배당성장 (SCHD)", "market": "US"},
        {"ticker": "TLT", "name": "미국 20년이상 채권 (TLT)", "market": "US"},
        {"ticker": "273130.KS", "name": "KODEX 종합채권(AA-이상)액티브", "market": "KR"}
    ],
    "글로벌 방산 & 인프라": [
        {"ticker": "ITA", "name": "미국 방산 (ITA)", "market": "US"},
        {"ticker": "PAVE", "name": "미국 인프라 (PAVE)", "market": "US"}
    ]
}

data = {}

for theme, etfs in THEMES.items():
    for item in etfs:
        ticker = item["ticker"]
        name = item["name"]
        market = item["market"]
        
        try:
            etf = yf.Ticker(ticker)
            hist = etf.history(period="1y")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                m1_price = hist['Close'].iloc[-21] if len(hist) >= 21 else hist['Close'].iloc[0]
                y1_price = hist['Close'].iloc[0]
                
                m1_return = ((current_price / m1_price) - 1) * 100
                y1_return = ((current_price / y1_price) - 1) * 100
                
                # 원화/달러 표시 구분
                price_str = f"₩{int(current_price):,}" if market == "KR" else f"${current_price:.2f}"
                
                data[ticker] = {
                    "name": name,
                    "theme": theme,
                    "market": market,
                    "price": price_str,
                    "m1_return": round(float(m1_return), 2),
                    "y1_return": round(float(y1_return), 2),
                    "history": [round(float(p), 2) for p in hist['Close'].tail(30).tolist()]
                }
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

# data 폴더 저장
os.makedirs('data', exist_ok=True)
with open('data/etf_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("국내외 ETF 데이터 수집 완료!")
