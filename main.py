#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOXL 주식 데이터 분석 프로젝트
2년간의 SOXL 데이터를 분석하는 메인 스크립트
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import io

# 한글 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def load_data(file_path):
    """CSV 파일을 로드하고 데이터를 정리합니다."""
    print("데이터 로딩 중...")
    
    # CSV 파일 읽기 (인코딩 명시적 지정)
    df = pd.read_csv(file_path, encoding='utf-8')
    
    # 컬럼명 정리
    df.columns = ['date', 'close', 'open', 'high', 'low', 'volume', 'change_pct']
    
    # 날짜 컬럼을 datetime으로 변환
    df['date'] = pd.to_datetime(df['date'])
    
    # 숫자 컬럼들을 적절한 타입으로 변환
    numeric_columns = ['close', 'open', 'high', 'low', 'change_pct']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.replace('%', ''), errors='coerce')
    
    # 거래량 처리 (M 단위 제거)
    df['volume'] = df['volume'].astype(str).str.replace('M', '').astype(float) * 1000000
    
    # 데이터 정렬 (날짜순)
    df = df.sort_values('date').reset_index(drop=True)
    
    print(f"데이터 로딩 완료: {len(df)}개 행, {len(df.columns)}개 컬럼")
    print(f"기간: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")
    
    return df

def basic_analysis(df):
    """기본 통계 분석을 수행합니다."""
    print("\n=== 기본 통계 정보 ===")
    print(df.describe())
    
    print("\n=== 최근 5일 데이터 ===")
    print(df.tail())
    
    print("\n=== 가격 통계 ===")
    print(f"최고가: ${df['high'].max():.2f}")
    print(f"최저가: ${df['low'].min():.2f}")
    print(f"평균 종가: ${df['close'].mean():.2f}")
    print(f"현재가: ${df['close'].iloc[-1]:.2f}")
    
    # 이동평균선 계산
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA60'] = df['close'].rolling(window=60).mean()
    
    print("\n=== 이동평균선 정보 ===")
    print(f"5일 이동평균: ${df['MA5'].iloc[-1]:.2f}")
    print(f"20일 이동평균: ${df['MA20'].iloc[-1]:.2f}")
    print(f"60일 이동평균: ${df['MA60'].iloc[-1]:.2f}")
    
    # 현재가와 이동평균선 비교
    current_price = df['close'].iloc[-1]
    ma60 = df['MA60'].iloc[-1]
    if not pd.isna(ma60):
        if current_price > ma60:
            print(f"현재가가 60일 이동평균보다 ${current_price - ma60:.2f} 높습니다 (상승 추세)")
        else:
            print(f"현재가가 60일 이동평균보다 ${ma60 - current_price:.2f} 낮습니다 (하락 추세)")
    else:
        print("60일 이동평균을 계산하기에는 데이터가 부족합니다.")

def plot_price_trend(df):
    """가격 추이를 시각화합니다."""
    plt.figure(figsize=(15, 10))
    
    # 종가 그래프 (이동평균선 포함)
    plt.subplot(2, 1, 1)
    plt.plot(df['date'], df['close'], linewidth=1.5, color='blue', alpha=0.8, label='종가')
    
    # 이동평균선 그리기
    if 'MA5' in df.columns:
        plt.plot(df['date'], df['MA5'], linewidth=1, color='red', alpha=0.7, label='5일 이동평균')
    if 'MA20' in df.columns:
        plt.plot(df['date'], df['MA20'], linewidth=1, color='orange', alpha=0.7, label='20일 이동평균')
    if 'MA60' in df.columns:
        plt.plot(df['date'], df['MA60'], linewidth=2, color='purple', alpha=0.8, label='60일 이동평균')
    
    plt.title('SOXL 종가 추이 및 이동평균선 (2년)', fontsize=16, fontweight='bold')
    plt.xlabel('날짜')
    plt.ylabel('종가 ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 거래량 그래프
    plt.subplot(2, 1, 2)
    plt.bar(df['date'], df['volume']/1000000, alpha=0.7, color='green')
    plt.title('거래량 추이', fontsize=14)
    plt.xlabel('날짜')
    plt.ylabel('거래량 (백만)')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_interactive_chart(df):
    """인터랙티브 차트를 생성합니다 (마우스 오버 시 값 표시)."""
    # 서브플롯 생성
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('SOXL 종가 추이 및 이동평균선', '거래량'),
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3]
    )
    
    # 종가 선 그래프
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['close'],
            mode='lines',
            name='종가',
            line=dict(color='blue', width=2),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         '가격: $%{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # 이동평균선들
    if 'MA5' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['MA5'],
                mode='lines',
                name='5일 이동평균',
                line=dict(color='red', width=1),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             '가격: $%{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    
    if 'MA20' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['MA20'],
                mode='lines',
                name='20일 이동평균',
                line=dict(color='orange', width=1),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             '가격: $%{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    
    if 'MA60' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['MA60'],
                mode='lines',
                name='60일 이동평균',
                line=dict(color='purple', width=2),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             '가격: $%{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    
    # 거래량 바 차트
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['volume']/1000000,
            name='거래량',
            marker_color='green',
            opacity=0.7,
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         '거래량: %{y:.1f}M<extra></extra>'
        ),
        row=2, col=1
    )
    
    # 레이아웃 설정
    fig.update_layout(
        title={
            'text': 'SOXL 주식 데이터 분석 (인터랙티브 차트)',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        height=800,
        showlegend=True,
        hovermode='x unified'
    )
    
    # X축 설정
    fig.update_xaxes(title_text="날짜", row=1, col=1)
    fig.update_xaxes(title_text="날짜", row=2, col=1)
    
    # Y축 설정
    fig.update_yaxes(title_text="가격 ($)", row=1, col=1)
    fig.update_yaxes(title_text="거래량 (백만)", row=2, col=1)
    
    # 그리드 표시
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    # 차트 표시
    fig.show()

def main():
    """메인 실행 함수"""
    print("SOXL 주식 데이터 분석 시작!")
    print("=" * 50)
    
    try:
        # 데이터 로드
        df = load_data('SOXL_2y.csv')
        
        # 기본 분석
        basic_analysis(df)
        
        # 시각화
        print("\n=== 정적 차트 생성 중... ===")
        plot_price_trend(df)
        
        print("\n=== 인터랙티브 차트 생성 중... ===")
        plot_interactive_chart(df)
        
        print("\n분석 완료!")
        
    except FileNotFoundError:
        print("오류: SOXL_2y.csv 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
