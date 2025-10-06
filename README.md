# 🔥 FIRE Project - SOXL Trading Analysis

SOXL(반도체 3배 레버리지 ETF) 주식 데이터 분석 및 트레이딩 시뮬레이션 프로젝트입니다.

## 📊 프로젝트 개요

이 프로젝트는 SOXL의 2년간 주식 데이터를 분석하고, 다양한 트레이딩 전략을 시뮬레이션하여 최적의 매매 방법을 찾는 것을 목표로 합니다.

## 🚀 주요 기능

### 1. 데이터 분석
- **기본 통계 분석**: 가격, 거래량, 변동률 분석
- **이동평균선 분석**: 5일, 20일, 60일 이동평균선 계산
- **시각화**: 인터랙티브 차트로 데이터 시각화

### 2. 트레이딩 시뮬레이션
- **백테스트**: 2024년 1월부터 실제 데이터로 전략 검증
- **다양한 전략**: 이동평균선 기반 매매 전략
- **성과 분석**: 수익률, 최대 낙폭, 거래 통계 분석

### 3. 인터랙티브 차트
- **실시간 호버**: 마우스 오버 시 상세 정보 표시
- **색상 코딩**: 60일 이동평균 대비 차이를 색상으로 표시
- **줌/팬**: 차트 확대/축소 및 이동 가능

## 📁 프로젝트 구조

```
FIRE_Prj/
├── main.py                          # 메인 분석 스크립트
├── trading_simulator.py             # 기본 트레이딩 시뮬레이터
├── improved_trading_simulator.py    # 개선된 트레이딩 시뮬레이터
├── requirements.txt                 # 필요한 패키지 목록
├── .gitignore                       # Git 제외 파일 목록
└── README.md                        # 프로젝트 설명서
```

## 🛠️ 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/Marus505/fire_prj.git
cd fire_prj
```

### 2. 가상환경 생성 (권장)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 실행
```bash
python main.py
```

## 📈 사용된 기술

- **Python 3.13**
- **Pandas**: 데이터 분석 및 처리
- **Matplotlib**: 정적 차트 생성
- **Plotly**: 인터랙티브 차트 생성
- **NumPy**: 수치 계산
- **Seaborn**: 통계 시각화

## 🎯 트레이딩 전략

### 기본 전략
- **매수**: 60일 이동평균선 2% 이상 돌파
- **매도**: 60일 이동평균선 1% 이하 이탈
- **자본 관리**: 20분할 투자

### 개선된 전략
- **추세 확인**: 20일 이평 > 60일 이평
- **리스크 관리**: 손절매 및 이익실현 설정
- **동적 조정**: 시장 상황에 따른 전략 수정

## 📊 시뮬레이션 결과

### 원래 전략
- 초기 자본: $20,000
- 최종 가치: $3,123 (-84.38%)
- 최대 낙폭: 86.41%

### 개선된 전략
- 초기 자본: $20,000
- 최종 가치: $18,262 (-8.69%)
- 최대 낙폭: 9.47%

## ⚠️ 주의사항

- **고위험 투자**: SOXL은 3배 레버리지 ETF로 매우 높은 변동성
- **단기 투자**: 장기 보유 시 예상과 다른 결과 발생 가능
- **자본 관리**: 전체 자산의 5-10% 이하로 제한 권장
- **실시간 모니터링**: 일일 체크 및 적극적 관리 필요

## 📝 라이선스

이 프로젝트는 개인 학습 및 연구 목적으로 제작되었습니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 연락처

프로젝트 관련 문의사항이 있으시면 이슈를 생성해주세요.

---

**⚡ FIRE (Financial Independence, Retire Early)를 위한 투자 분석 도구**