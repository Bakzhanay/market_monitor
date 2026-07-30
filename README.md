# Market Activity Monitor

Real-time market monitoring dashboard for equities and crypto assets.

## Features

- Real-time asset monitoring
- Simple and Advanced visualization modes
- Candlestick and line chart views
- Volume anomaly detection
- Price anomaly detection
- Live feed status monitoring
- Market open/closed status detection
- Data freshness tracking
- Automatic background data collection
- Local SQLite caching
- Reset chart view functionality

## Supported Assets

### Equities & ETFs
- AAPL
- NVDA
- MSFT
- TSLA
- SPY
- QQQ

### Crypto
- BTC-USD
- ETH-USD

## Architecture

feed.py
- Background data collector
- Downloads market data every minute
- Stores data in SQLite database

engine.py
- Reads cached market data
- Calculates indicators
- Detects anomalies

Dash Application
- Interactive UI
- Live charts
- Analytics dashboard
- Simple / Advanced modes

## Indicators

### Price Anomaly

Based on Z-Score analysis of price movement.

Triggers when price behavior significantly deviates from normal market conditions.

### Volume Anomaly

Based on Z-Score analysis of trading volume.

Highlights unusually high market activity.

## Data Source

Yahoo Finance (yfinance)

## Technologies

- Python
- Dash
- Plotly
- Pandas
- SQLite
- yfinance

## Screenshots

### Simple Mode

<img width="1920" height="873" alt="simple_mode" src="https://github.com/user-attachments/assets/b241843a-a2ae-422d-96f0-c6a2d68449c7" />

### Advanced Mode

<img width="1920" height="874" alt="advanced_mode" src="https://github.com/user-attachments/assets/ccd9342f-7de4-4536-82cb-2ad4806a0fce" />

## Notes

- Market data is collected in the background.
- Dashboard refreshes automatically.
- Crypto markets are tracked 24/7.
- Equity market status follows NYSE trading hours.


## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bakzhanay/market-monitor.git
   cd market-monitor
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```
   *Activate the virtual environment:*
      **Windows:**
         - .venv\Scripts\activate
      **macOS / Linux:**
         - source .venv/bin/activate

4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Note: Ensure your requirements.txt includes: dash, dash-bootstrap-components, pandas, numpy, yfinance)

5. **Initialize and run the background data collector:**
    ```bash
    python feed.py
    ```
    Keep this process running. It will generate the market_data.db and initialize the background sync logs in feed_service.log.

6. **Launch the terminal web interface:**
    **In a separate terminal window, run:**
    ```bash
    cd market-monitor
    python main.py
    ```

7. **Access the terminal:**
    **Open your browser and navigate to http://127.0.0.1:8050/**
