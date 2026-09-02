import os
import json
import pandas as pd
import FinanceDataReader as fdr

# ==============================================================================
# 1. 다변화된 국내 ETF 테마 자동 분류 규칙 (키워드 기반)
# ==============================================================================
THEME_RULES = {
    "AI & 반도체": [
        "반도체", "AI", "인공지능", "SOXX", "NVDA", "소부장", "빅테크", "IT", "테크"
    ],
    "전력인프라 & 원자력": [
        "전력", "원자력", "원자력선물", "인프라", "GRID", "전력설비", "에너지인프라"
    ],
    "2차전지 & 친환경": [
        "2차전지", "배터리", "전기차", "신재생", "태양광", "풍력", "친환경", "클린에너지"
    ],
    "고배당 & 커버드콜": [
        "배당", "고배당", "다우존스", "커버드콜", "프리미엄", "리츠", "SCHD", "배당성장"
    ],
    "채권 & 금리피봇": [
        "채권", "국채", "회사채", "금리", "CD금리", "KOFR", "SOFR", "통화", "단기자금", "파킹"
    ],
    "글로벌 방산 & 조선": [
        "방산", "K-방산", "조선", "우주", "항공", "중공업"
    ],
    "바이오 & 헬스케어": [
        "바이오", "헬스케어", "제약", "의료기기"
    ],
    "금 & 원자재": [
        "금현물", "금선물", "원유", "원자재", "구리", "농산물", "원자유"
    ]
}

def classify_theme(name):
    """종목명(name)을 분석하여 위 규칙 중 매칭되는 테마를 자동 반환하는 함수"""
    name_upper = name.upper()
    for theme, keywords in THEME_RULES.items():
        if any(keyword in name_upper for keyword in keywords):
            return theme
    return "기타/일반"

etf_result = {}

print("=== [국내 상장 전체 ETF 자동 수집 및 다변화 테마 분류 시작] ===")

try:
    # 2. 한국거래소(KRX) 전체 ETF 목록 데이터베이스 가져오기
    df_krx = fdr.StockListing('ETF/KR')
    print(f"-> 총 {len(df_krx)}개 국내 ETF 종목 탐색 완료.")

    success_count = 0

    # 3. 전체 종목 스캐닝 및 테마 분류 실행
    for idx, row in df_krx.iterrows():
        ticker = str(row['Symbol'])
        name = str(row['Name'])
        theme = classify_theme(name)

        # 8대 주요 테마 중 하나에 해당하는 종목만 자동 수집
        if theme == "기타/일반":
            continue

        try:
            # 최근 30일 가격 추이 데이터 가져오기
            df_price = fdr.DataReader(ticker)
            if len(df_price) >= 30:
                df_price = df_price.tail(30)
                prices = [int(p) for p in df_price['Close'].tolist()]
                current_price = prices[-1]
                first_price = prices[0]
                
                # 1개월 수익률 계산 (%)
                m1_return = round(((current_price - first_price) / first_price) * 100, 2)

                etf_result[ticker] = {
                    "ticker": ticker,
                    "name": name,
                    "theme": theme,
                    "market": "KR",
                    "price": f"{current_price:,}원",
                    "m1_return": m1_return,
                    "history": prices
                }
                success_count += 1
                print(f"[{success_count}] {name} ({ticker}) -> [{theme}] 분류 완료")
        except Exception as e:
            continue

    print(f"\n-> 총 {success_count}개 종목이 8개 테마로 자동 수집/분류되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")

# 4. JSON 데이터 파일 저장 (data/etf_data.json)
os.makedirs("data", exist_ok=True)
with open("data/etf_data.json", "w", encoding="utf-8") as f:
    json.dump(etf_result, f, ensure_ascii=False, indent=2)

print("-> data/etf_data.json 파일 저장 완료!")
