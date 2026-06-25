import pandas as pd
import numpy as np
import sqlite3

REQUIRED_COLUMNS = {'Open', 'High', 'Low', 'Close', 'Volume'}

def get_market_data(ticker: str) -> pd.DataFrame:
    """Читает рыночные данные из локальной БД и вычисляет статистику."""
    if not ticker:
        return pd.DataFrame()

    ticker = ticker.strip().upper()

    try:
        conn = sqlite3.connect('market_data.db', timeout=15)
        # Читаем данные. parse_dates=['Datetime'] обязательно, чтобы восстановить временной ряд.
        df = pd.read_sql(
            f'SELECT * FROM "{ticker}"', 
            conn, 
            index_col='Datetime', 
            parse_dates=['Datetime']
        )
        conn.close()
    except Exception:
        # Срабатывает, если файл БД еще не создан или таблицы нет
        return pd.DataFrame()

    if df.empty or not REQUIRED_COLUMNS.issubset(df.columns):
        return df

    df = df.copy()
        
    # Базовые индикаторы
    df['SMA9'] = df['Close'].rolling(window=9, min_periods=1).mean()
    
    # 1. Аномалии объема (Окно 20 периодов)
    roll_vol_mean = df['Volume'].rolling(window=20, min_periods=20).mean()
    roll_vol_std = df['Volume'].rolling(window=20, min_periods=20).std().replace(0, np.nan)
    df['Volume_Z'] = (df['Volume'] - roll_vol_mean) / roll_vol_std
    df['Is_Volume_Anomaly'] = (df['Volume_Z'] > 3.0).fillna(False)
    
    # 2. Аномалии ценовой волатильности (по доходности)
    df['Returns'] = df['Close'].pct_change()
    roll_ret_mean = df['Returns'].rolling(window=20, min_periods=20).mean()
    roll_ret_std = df['Returns'].rolling(window=20, min_periods=20).std().replace(0, np.nan)
    df['Price_Z'] = (df['Returns'] - roll_ret_mean) / roll_ret_std
    df['Is_Price_Anomaly'] = (df['Price_Z'].abs() > 3.0).fillna(False)
    
    return df