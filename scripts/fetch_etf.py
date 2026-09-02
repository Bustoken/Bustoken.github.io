import json
import os
import yfinance as yf

# Track할 ETF 테마 및 종목 목록
tickers = ['QQQ', 'SCHD', 'TLT', 'VST', 'ITA']

data = {}
for ticker in tickers:
    try:
        etf = yf.Ticker(ticker)
        hist = etf.history(period="1y")
        
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            m1_price = hist['Close'].iloc[-21] if len(hist) >= 21 else hist['Close'].iloc[0]
            y1_price = hist['Close'].iloc[0]
            
            m1_return = ((current_price / m1_price) - 1) * 100
            y1_return = ((current_price / y1_price) - 1) * 100
            
            data[ticker] = {
                "price": round(float(current_price), 2),
                "m1_return": round(float(m1_return), 2),
                "y1_return": round(float(y1_return), 2),
                "history": [round(float(p), 2) for p in hist['Close'].tail(30).tolist()]
            }
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")

# data 폴더가 없으면 생성
os.makedirs('data', exist_ok=True)

# 결과를 JSON 파일로 저장
with open('data/etf_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("ETF Data successfully saved!")
