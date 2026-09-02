import json
import os
import yfinance as yf

# 국내외 ETF 테마 구성 (국내 ETF는 yfinance 수집 특성상 영어 명칭 병행 활용)
THEMES = {
    "AI & 반도체/전력": [
        {"ticker": "QQQ", "name": "미국 나스닥100 (QQQ)", "market": "US"},
        {"ticker": "NVDA", "name": "엔비디아 (NVDA)", "market": "US"},
        {"ticker": "VST", "name": "비스트라 전력 (VST)", "market": "US"},
        {"ticker": "381180.KS", "name": "TIGER 미국배당다우존스", "market": "KR"}
    ],
    "고배당 & 금리 피봇": [
        {"ticker": "SCHD", "name": "미국 배당성장 (SCHD)", "market": "US"},
        {"ticker": "TLT", "name": "미국 20년이상 채권 (TLT)", "market": "US"},
        {"ticker": "273130.KS", "name": "KODEX 종합채권액티브", "market": "KR"}
    ],
    "글로벌 방산 & 인프라": [
        {"ticker": "ITA", "name": "미국 방산 (ITA)", "market": "US"},
        {"ticker": "PAVE", "name": "미국 인프라 (PAVE)", "market": "US"}
    ]
}

data = {}

for theme_name, etf_list in THEMES.items():
    for item in etf_list:
        raw_ticker = item["ticker"]
        # 특수문자 .KS 제거한 고유 ID 생성 (HTML 차트 아이디용)
        safe_id = raw_ticker.replace('.', '_')
        
        try:
            etf = yf.Ticker(raw_ticker)
            hist = etf.history(period="1y")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                m1_price = hist['Close'].iloc[-21] if len(hist) >= 21 else hist['Close'].iloc[0]
                m1_return = ((current_price / m1_price) - 1) * 100
                
                price_str = f"₩{int(current_price):,}" if item["market"] == "KR" else f"${current_price:.2f}"
                
                data[safe_id] = {
                    "ticker": raw_ticker,
                    "name": item["name"],
                    "theme": theme_name,
                    "market": item["market"],
                    "price": price_str,
                    "m1_return": round(float(m1_return), 2),
                    "history": [round(float(p), 2) for p in hist['Close'].tail(30).tolist()]
                }
        except Exception as e:
            print(f"Error fetching {raw_ticker}: {e}")

os.makedirs('data', exist_ok=True)
with open('data/etf_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("데이터 수집 완료!")
