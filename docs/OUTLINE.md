# TITLE: FIRE Project

# WHY ? 이거 왜함?
### I want FIRE(Financial Independence, Retire Early)
### FIRE: 재무적 독립을 위해 조기 은퇴를 목표로 돈을 모은다.

# WHAT ? 그래서 무얼 할겐데?
### 얼마를 모을 건가? 부동산 제외 10억
### 연간 생활비의 25배에 해당하는 금액을 은퇴 자금으로 확보하고, 연간 4% 미만으로 지출하면 원금을 유지하며 생활을 이어갈 수 있음.
### SOXL EFT 를 분할 매매 방식으로 2만불로 시작하여 월 500만원의 수익을 낼 수 있는 금액 40만불(6억)을 만들어 은퇴한다.
### 목표 생활비 월 500만원

# HOW ? 어떻게 할건데?
초기 자금 2만불 - 20분할 하여 1000불 준비.
SOXL 60 이평선 이용

## 프로그램 실행
python main.py

## 전술
### 7분할
SOXL 로 단기 트레이딩 프로그램을 만들고 싶어. 일단 지난 2년간 데이터를 이용해 시뮬레이션을 할거야

### 20분할 단타
[시뮬레이션 시나리오]
1. 총 1만불이 시드머니야. 이를 20분할 하여, 한 계좌에 500불씩 들어 있어.
2. 2024년 1월 2일 부터 시작해. 
3. 매매 방법: 60일 이평선(A), 시가(B), n번 계좌 평균가(C), 전날 종가(D)를 비교.
   2023-12-29 / A: $22.18 / B: $32.17 / D: $32.22
   2024-01-02 / A: $22.38 / B: $29.89 / D: $31.40
   2024-01-02 / A: $21.68 / B: $26.59 / D: $28.04
    1. A < B 일때(상승추세)
        1. B와 D가 5% 차이가 나면, (B*102%) 가격으로 빈 계좌 마다 등차 매수
        2. B와 D가 9% 차이가 나면, (B*99%) 가격으로 조건에 해당하는 계좌 등차 매도
    1. A > B 일때(하락추세)
        1. B와 D가 7% 차이가 나면, (B*102%) 가격으로 빈 계좌 마다 등차 매수
        2. B와 D가 6% 차이가 나면, (B*99%) 가격으로 조건에 해당하는 계좌 등차 매도
4. 등차 매수는: 빈 계좌의 기준가를 등차수열로 만들어 두어 매매하는 것이다. 등차는 round(전날 종가*1%, 1) 으로 한다.
5. 구매된 계좌마다 목표이익률과 목표가, 손절률 손절가를 설정한다. ​
6. 이 방법으로 무한반복한다.


## 벤치 마킹
### 김수달 - 4개월 장단점
https://blog.naver.com/godhorong/223787954941

### 포포티 - 매매법
https://blog.naver.com/PostView.naver?blogId=for40s&logNo=223125738158&categoryNo=16&parentCategoryNo=0&viewDate=&currentPage=9&postListTopCurrentPage=1&from=postList&userTopListOpen=true&userTopListCount=30&userTopListManageOpen=false&userTopListCurrentPage=9

### 궁그미
https://gunggeume.tistory.com/48?category=1258559