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
1. 1만불을 20분할 하여, 500불씩 계좌에 넣는다.
2. 2024년 1월 2일 부터 시작한다. 전날 종가는 $28.04, 시가는 $29.89, 60이평선은 $22.38 이다.
3. (첫날) 1번 계좌에서 현재가로 전액 매수한다.
4. (첫날) 2번 ~ 20번 계좌에서 1번 매수단가에 대한 등차수열*로 LOC 매수를 걸어둔다.
5. 1번 매수단가가 20$ 였을 경우, 2번은 19.7$, 3번은 19.4$, 4번은 19.1$, ••• 20번은 14.3$
6. 등차는 round(전날 종가*1%, 1) 으로 한다.
훌륭한 단타 매매 전략이네요! 체계적으로 정리해드리겠습니다.

## 벤치 마킹
### 김수달 - 4개월 장단점
https://blog.naver.com/godhorong/223787954941

### 포포티 - 매매법
https://blog.naver.com/PostView.naver?blogId=for40s&logNo=223125738158&categoryNo=16&parentCategoryNo=0&viewDate=&currentPage=9&postListTopCurrentPage=1&from=postList&userTopListOpen=true&userTopListCount=30&userTopListManageOpen=false&userTopListCurrentPage=9

### 궁그미
https://gunggeume.tistory.com/48?category=1258559