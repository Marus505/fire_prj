#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOXL 단기 트레이딩 시뮬레이션 프로그램
60일 이동평균선 기반 트레이딩 전략 백테스트
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class SOXLTradingSimulator:
    def __init__(self, initial_capital=20000, position_size=20):
        """
        SOXL 트레이딩 시뮬레이터 초기화
        
        Args:
            initial_capital (int): 초기 자본 ($20,000)
            position_size (int): 분할 매수 횟수 (20회)
        """
        self.initial_capital = initial_capital
        self.position_size = position_size
        self.cash_per_trade = initial_capital / position_size  # $1,000 per trade
        
        # 트레이딩 기록
        self.trades = []
        self.portfolio_value = []
        self.dates = []
        self.cash = initial_capital
        self.shares = 0
        self.total_shares = 0
        
    def load_data(self, file_path):
        """데이터 로드 및 전처리"""
        print("데이터 로딩 중...")
        
        df = pd.read_csv(file_path)
        df.columns = ['date', 'close', 'open', 'high', 'low', 'volume', 'change_pct']
        df['date'] = pd.to_datetime(df['date'])
        
        # 숫자 컬럼 정리
        numeric_columns = ['close', 'open', 'high', 'low', 'change_pct']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.replace('%', ''), errors='coerce')
        
        df['volume'] = df['volume'].astype(str).str.replace('M', '').astype(float) * 1000000
        
        # 60일 이동평균선 계산
        df['MA60'] = df['close'].rolling(window=60).mean()
        
        # 데이터 정렬
        df = df.sort_values('date').reset_index(drop=True)
        
        print(f"데이터 로딩 완료: {len(df)}개 행")
        print(f"기간: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")
        
        return df
    
    def calculate_signals(self, df):
        """매수/매도 신호 계산"""
        df['signal'] = 0  # 0: 보유, 1: 매수, -1: 매도
        df['position'] = 0  # 현재 포지션 크기
        
        for i in range(60, len(df)):  # 60일 이평선 계산 후부터
            current_price = df.iloc[i]['close']
            ma60 = df.iloc[i]['MA60']
            
            if pd.isna(ma60):
                continue
                
            # 이평선 대비 비율 계산
            price_ratio = (current_price - ma60) / ma60 * 100
            
            # 매수 신호: 이평선 돌파 (+1% 이상)
            if price_ratio >= 1.0 and df.iloc[i-1]['signal'] != 1:
                df.iloc[i, df.columns.get_loc('signal')] = 1
                
            # 매도 신호: 이평선 이탈 (-2% 이하)
            elif price_ratio <= -2.0 and df.iloc[i-1]['signal'] != -1:
                df.iloc[i, df.columns.get_loc('signal')] = -1
        
        return df
    
    def execute_trading(self, df):
        """트레이딩 실행"""
        print("트레이딩 시뮬레이션 시작...")
        
        for i in range(len(df)):
            current_date = df.iloc[i]['date']
            current_price = df.iloc[i]['close']
            signal = df.iloc[i]['signal']
            
            # 포트폴리오 가치 계산
            portfolio_value = self.cash + (self.total_shares * current_price)
            self.portfolio_value.append(portfolio_value)
            self.dates.append(current_date)
            
            # 매수 신호
            if signal == 1 and self.cash >= self.cash_per_trade:
                shares_to_buy = self.cash_per_trade / current_price
                self.shares = shares_to_buy
                self.total_shares += shares_to_buy
                self.cash -= self.cash_per_trade
                
                trade_record = {
                    'date': current_date,
                    'action': 'BUY',
                    'price': current_price,
                    'shares': shares_to_buy,
                    'amount': self.cash_per_trade,
                    'cash_remaining': self.cash,
                    'total_shares': self.total_shares
                }
                self.trades.append(trade_record)
                
            # 매도 신호
            elif signal == -1 and self.total_shares > 0:
                sell_amount = self.total_shares * current_price
                self.cash += sell_amount
                
                trade_record = {
                    'date': current_date,
                    'action': 'SELL',
                    'price': current_price,
                    'shares': self.total_shares,
                    'amount': sell_amount,
                    'cash_remaining': self.cash,
                    'total_shares': 0
                }
                self.trades.append(trade_record)
                self.total_shares = 0
        
        print(f"트레이딩 완료: {len(self.trades)}회 거래")
        return self.trades
    
    def calculate_performance(self):
        """성과 계산"""
        if not self.portfolio_value:
            return {}
        
        initial_value = self.initial_capital
        final_value = self.portfolio_value[-1]
        final_cash = self.cash
        final_shares_value = self.total_shares * self.portfolio_value[-1] / (self.total_shares + 1e-10)
        
        total_return = (final_value - initial_value) / initial_value * 100
        
        # 최대 낙폭 계산
        peak = initial_value
        max_drawdown = 0
        for value in self.portfolio_value:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # 거래 통계
        buy_trades = [t for t in self.trades if t['action'] == 'BUY']
        sell_trades = [t for t in self.trades if t['action'] == 'SELL']
        
        performance = {
            'initial_capital': initial_value,
            'final_value': final_value,
            'total_return_pct': total_return,
            'max_drawdown_pct': max_drawdown,
            'total_trades': len(self.trades),
            'buy_trades': len(buy_trades),
            'sell_trades': len(sell_trades),
            'final_cash': final_cash,
            'final_shares': self.total_shares
        }
        
        return performance
    
    def print_results(self):
        """결과 출력"""
        performance = self.calculate_performance()
        
        print("\n" + "="*60)
        print("SOXL 트레이딩 시뮬레이션 결과")
        print("="*60)
        print(f"초기 자본: ${performance['initial_capital']:,.2f}")
        print(f"최종 가치: ${performance['final_value']:,.2f}")
        print(f"총 수익률: {performance['total_return_pct']:.2f}%")
        print(f"최대 낙폭: {performance['max_drawdown_pct']:.2f}%")
        print(f"총 거래 횟수: {performance['total_trades']}회")
        print(f"매수 거래: {performance['buy_trades']}회")
        print(f"매도 거래: {performance['sell_trades']}회")
        print(f"현금 잔고: ${performance['final_cash']:,.2f}")
        print(f"보유 주식: {performance['final_shares']:.2f}주")
        
        # 수익/손실
        if performance['total_return_pct'] > 0:
            print(f"💰 수익: ${performance['final_value'] - performance['initial_capital']:,.2f}")
        else:
            print(f"💸 손실: ${performance['initial_capital'] - performance['final_value']:,.2f}")
    
    def plot_results(self, df):
        """결과 시각화"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('SOXL 가격 및 매매 신호', '포트폴리오 가치'),
            vertical_spacing=0.1,
            row_heights=[0.6, 0.4]
        )
        
        # 가격 차트
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['close'],
                mode='lines',
                name='SOXL 종가',
                line=dict(color='blue', width=2)
            ),
            row=1, col=1
        )
        
        # 60일 이동평균선
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['MA60'],
                mode='lines',
                name='60일 이동평균',
                line=dict(color='red', width=2)
            ),
            row=1, col=1
        )
        
        # 매수 신호
        buy_signals = df[df['signal'] == 1]
        if not buy_signals.empty:
            fig.add_trace(
                go.Scatter(
                    x=buy_signals['date'],
                    y=buy_signals['close'],
                    mode='markers',
                    name='매수 신호',
                    marker=dict(color='green', size=10, symbol='triangle-up')
                ),
                row=1, col=1
            )
        
        # 매도 신호
        sell_signals = df[df['signal'] == -1]
        if not sell_signals.empty:
            fig.add_trace(
                go.Scatter(
                    x=sell_signals['date'],
                    y=sell_signals['close'],
                    mode='markers',
                    name='매도 신호',
                    marker=dict(color='red', size=10, symbol='triangle-down')
                ),
                row=1, col=1
            )
        
        # 포트폴리오 가치
        fig.add_trace(
            go.Scatter(
                x=self.dates,
                y=self.portfolio_value,
                mode='lines',
                name='포트폴리오 가치',
                line=dict(color='purple', width=2)
            ),
            row=2, col=1
        )
        
        # 초기 자본선
        fig.add_hline(
            y=self.initial_capital,
            line_dash="dash",
            line_color="gray",
            annotation_text="초기 자본",
            row=2, col=1
        )
        
        fig.update_layout(
            title='SOXL 트레이딩 시뮬레이션 결과',
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="날짜", row=1, col=1)
        fig.update_xaxes(title_text="날짜", row=2, col=1)
        fig.update_yaxes(title_text="가격 ($)", row=1, col=1)
        fig.update_yaxes(title_text="포트폴리오 가치 ($)", row=2, col=1)
        
        fig.show()

def main():
    """메인 실행 함수"""
    print("SOXL 트레이딩 시뮬레이션 시작!")
    print("="*50)
    
    # 시뮬레이터 초기화
    simulator = SOXLTradingSimulator(initial_capital=20000, position_size=20)
    
    try:
        # 데이터 로드
        df = simulator.load_data('SOXL_2y.csv')
        
        # 2024년 1월 2일부터 시작
        start_date = pd.to_datetime('2024-01-02')
        df = df[df['date'] >= start_date].reset_index(drop=True)
        
        print(f"백테스트 기간: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")
        
        # 신호 계산
        df = simulator.calculate_signals(df)
        
        # 트레이딩 실행
        trades = simulator.execute_trading(df)
        
        # 결과 출력
        simulator.print_results()
        
        # 시각화
        simulator.plot_results(df)
        
        print("\n시뮬레이션 완료!")
        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
