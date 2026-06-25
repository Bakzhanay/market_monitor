import yfinance as yf
import sqlite3
import time
import logging

# Настройка логирования — это критически важно, чтобы знать, почему все упало
logging.basicConfig(level=logging.INFO, filename='feed_service.log', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

TICKERS = ['AAPL', 'NVDA', 'MSFT', 'TSLA', 'SPY', 'QQQ', 'BTC-USD', 'ETH-USD']

def fetch_and_store():
    # Используем with для гарантии закрытия соединения
    with sqlite3.connect('market_data.db', timeout=15) as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        
        for ticker in TICKERS:
            try:
                # Добавляем timeout для yfinance, чтобы не виснуть вечно
                df = yf.Ticker(ticker).history(period="2d", interval="5m", timeout=10)
                
                if not df.empty:
                    df.to_sql(ticker, conn, if_exists='replace')
                    logging.info(f"[OK] {ticker}: {len(df)} rows updated")
                else:
                    logging.warning(f"[WARN] {ticker}: Empty data received")
                    
            except Exception as e:
                logging.error(f"[ERROR] {ticker}: {e}")

if __name__ == '__main__':
    logging.info("Сборщик запущен.")
    while True:
        try:
            fetch_and_store()
        except Exception as e:
            logging.critical(f"[CRITICAL] Глобальный сбой цикла: {e}")
        
        time.sleep(60)