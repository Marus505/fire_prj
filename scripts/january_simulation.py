#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2024년 1월 SOXL 트레이딩 시뮬레이션
60일 이평선 기반 매매 전략
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import io

# 한글 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class SOXLTradingSimulator:
    def __init__(self, initial_capital=10000, position_size=20):
        self.initial_capital = initial_capital
        self.position_size = position_size
        self.cash_per_trade = initial_capital / position_size  # $500 per trade
        
        # 계좌 관리
        self.accounts = {}
        for i in range(1, 21):
            self.accounts[i] = {
                'cash': self.cash_per_trade,
                'shares': 0,
                'avg_price': 0,
                'status': 'empty',  # empty, filled
                'buy_price': 0,
                'target_profit_rate': 0.05,  # 5%
                'stop_loss_rate': 0.03,      # 3%
                'target_price': 0,
                'stop_loss_price': 0
            }
        
        # 거래 기록
        self.trades = []
        self.daily_results = []
        
    def load_data(self, file_path):
        """데이터 로드"""
        df = pd.read_csv(file_path, encoding='utf-8')
        df.columns = ['date', 'close', 'open', 'high', 'low', 'volume', 'change_pct']
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        
        # 60일 이동평균선 계산
        df['MA60'] = df['close'].rolling(window=60).mean()
        
        return df
    
    def calculate_step(self, prev_close):
        """등차 계산"""
        return round(prev_close * 0.01, 1)
    
    def get_empty_accounts(self):
        """빈 계좌 목록 반환"""
        return [i for i in range(1, 21) if self.accounts[i]['status'] == 'empty']
    
    def get_filled_accounts(self):
        """매수된 계좌 목록 반환"""
        return [i for i in range(1, 21) if self.accounts[i]['status'] == 'filled']
    
    def buy_account(self, account_num, price, date):
        """계좌 매수"""
        if self.accounts[account_num]['status'] != 'empty':
            return False
            
        shares = self.accounts[account_num]['cash'] / price
        self.accounts[account_num]['shares'] = shares
        self.accounts[account_num]['avg_price'] = price
        self.accounts[account_num]['buy_price'] = price
        self.accounts[account_num]['status'] = 'filled'
        
        # 목표가/손절가 설정
        self.accounts[account_num]['target_price'] = price * 1.05
        self.accounts[account_num]['stop_loss_price'] = price * 0.97
        
        # 거래 기록
        self.trades.append({
            'date': date,
            'account': account_num,
            'action': 'BUY',
            'price': price,
            'shares': shares,
            'amount': self.accounts[account_num]['cash']
        })
        
        return True
    
    def sell_account(self, account_num, price, date):
        """계좌 매도"""
        if self.accounts[account_num]['status'] != 'filled':
            return False
            
        shares = self.accounts[account_num]['shares']
        amount = shares * price
        
        self.accounts[account_num]['cash'] = amount
        self.accounts[account_num]['shares'] = 0
        self.accounts[account_num]['avg_price'] = 0
        self.accounts[account_num]['status'] = 'empty'
        
        # 거래 기록
        self.trades.append({
            'date': date,
            'account': account_num,
            'action': 'SELL',
            'price': price,
            'shares': shares,
            'amount': amount
        })
        
        return True
    
    def execute_trading(self, df):
        """트레이딩 실행"""
        print("2024년 1월 트레이딩 시뮬레이션 시작...")
        
        # 2024년 1월 데이터 필터링
        jan_2024 = df[(df['date'] >= '2024-01-01') & (df['date'] <= '2024-01-31')].copy()
        
        for i in range(len(jan_2024)):
            current_date = jan_2024.iloc[i]['date']
            current_open = jan_2024.iloc[i]['open']
            current_close = jan_2024.iloc[i]['close']
            current_ma60 = jan_2024.iloc[i]['MA60']
            
            if pd.isna(current_ma60):
                continue
                
            # 전날 종가
            if i > 0:
                prev_close = jan_2024.iloc[i-1]['close']
            else:
                # 1월 2일의 경우 전날(12월 29일) 종가 사용
                prev_close = 31.40
            
            # 등차 계산
            step = self.calculate_step(prev_close)
            
            # A: 60일 이평선, B: 전날 종가, C: 계좌 평균가, D: 시가
            A = current_ma60
            B = prev_close
            D = current_open
            
            # 매매 로직 실행
            if A > B:  # 이평선이 전날 종가보다 위
                # B가 A보다 5% 위면 매수
                if B > A * 1.05:
                    self.execute_buy_sequence(current_open, step, current_date)
                
                # 매수된 계좌들 중 C가 D보다 9% 위면 매도
                self.execute_sell_condition(current_open, 0.09, current_date)
                
            else:  # 이평선이 전날 종가보다 아래
                # B가 A보다 5% 아래면 매수
                if B < A * 0.95:
                    self.execute_buy_sequence(current_open, step, current_date)
                
                # 매수된 계좌들 중 C가 D보다 6% 아래면 매도
                self.execute_sell_condition(current_open, 0.06, current_date)
            
            # 일일 결과 기록
            self.record_daily_result(current_date, current_close)
        
        print(f"시뮬레이션 완료: {len(self.trades)}회 거래")
        return self.trades, self.daily_results
    
    def execute_buy_sequence(self, open_price, step, date):
        """등차수열 매수 실행"""
        empty_accounts = self.get_empty_accounts()
        if not empty_accounts:
            return
            
        # 기준가 설정 (시가의 102%)
        base_price = open_price * 1.02
        
        # 등차수열로 매수
        for i, account_num in enumerate(empty_accounts):
            buy_price = base_price - (step * i)
            if buy_price > 0:  # 가격이 양수일 때만 매수
                self.buy_account(account_num, buy_price, date)
    
    def execute_sell_condition(self, open_price, threshold_rate, date):
        """매도 조건 실행"""
        filled_accounts = self.get_filled_accounts()
        sell_price = open_price * 0.99  # 시가의 99%
        
        for account_num in filled_accounts:
            account = self.accounts[account_num]
            C = account['avg_price']  # 계좌 평균가
            D = open_price  # 시가
            
            # 조건 확인
            if C > D * (1 + threshold_rate):
                self.sell_account(account_num, sell_price, date)
    
    def record_daily_result(self, date, close_price):
        """일일 결과 기록"""
        total_value = 0
        filled_count = 0
        
        for account in self.accounts.values():
            if account['status'] == 'filled':
                total_value += account['shares'] * close_price
                filled_count += 1
            else:
                total_value += account['cash']
        
        self.daily_results.append({
            'date': date,
            'close_price': close_price,
            'total_value': total_value,
            'filled_accounts': filled_count,
            'empty_accounts': 20 - filled_count,
            'total_return_pct': (total_value - self.initial_capital) / self.initial_capital * 100
        })
    
    def save_results(self):
        """결과를 CSV 파일로 저장"""
        # 거래 기록 저장
        trades_df = pd.DataFrame(self.trades)
        trades_df.to_csv('january_trades.csv', index=False, encoding='utf-8-sig')
        
        # 일일 결과 저장
        daily_df = pd.DataFrame(self.daily_results)
        daily_df.to_csv('january_daily_results.csv', index=False, encoding='utf-8-sig')
        
        # 계좌별 최종 상태 저장
        account_status = []
        for i, account in self.accounts.items():
            account_status.append({
                'account_number': i,
                'status': account['status'],
                'cash': account['cash'],
                'shares': account['shares'],
                'avg_price': account['avg_price'],
                'current_value': account['cash'] + (account['shares'] * daily_df.iloc[-1]['close_price'] if len(daily_df) > 0 else 0)
            })
        
        account_df = pd.DataFrame(account_status)
        account_df.to_csv('january_account_status.csv', index=False, encoding='utf-8-sig')
        
        print("결과 파일 저장 완료:")
        print("- january_trades.csv: 거래 기록")
        print("- january_daily_results.csv: 일일 결과")
        print("- january_account_status.csv: 계좌별 최종 상태")

def main():
    """메인 실행 함수"""
    print("2024년 1월 SOXL 트레이딩 시뮬레이션")
    print("=" * 50)
    
    # 시뮬레이터 초기화
    simulator = SOXLTradingSimulator(initial_capital=10000, position_size=20)
    
    try:
        # 데이터 로드
        df = simulator.load_data('SOXL_2y.csv')
        
        # 트레이딩 실행
        trades, daily_results = simulator.execute_trading(df)
        
        # 결과 저장
        simulator.save_results()
        
        # 요약 출력
        if daily_results:
            final_value = daily_results[-1]['total_value']
            total_return = (final_value - 10000) / 10000 * 100
            print(f"\n=== 시뮬레이션 결과 요약 ===")
            print(f"초기 자본: $10,000")
            print(f"최종 가치: ${final_value:,.2f}")
            print(f"총 수익률: {total_return:.2f}%")
            print(f"총 거래 횟수: {len(trades)}회")
        
        print("\n시뮬레이션 완료!")
        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
