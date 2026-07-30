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


## Installation and Setup

The application uses two long-running Python processes:

1. `feed.py` downloads market data and writes it to a local SQLite database.
2. `main.py` starts the Dash web interface and reads the collected data.

Both processes must run from the same project directory. Start the collector
before starting the dashboard.

### Prerequisites

- Python 3.12 is recommended and has been tested with the pinned dependencies.
- Git is required to clone the repository.
- An internet connection is required for Yahoo Finance market data.

### 1. Clone the repository

```bash
git clone https://github.com/Bakzhanay/market-monitor.git
cd market-monitor
```

### 2. Create and activate a virtual environment

Create the environment once:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Your terminal prompt should now include `(.venv)`. Confirm that the correct
Python interpreter is active:

```bash
python -c "import sys; print(sys.executable)"
```

The displayed path should point to the `.venv` directory inside this project.

> If the project directory was renamed or moved after `.venv` was created,
> delete the old `.venv`, create it again, and reselect the interpreter in
> VS Code. Virtual environments can contain paths from their original location.

### 3. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

Verify that `yfinance` is installed in the active environment:

```bash
python -c "import yfinance; print(yfinance.__version__)"
```

The pinned requirements currently install `yfinance 1.4.1`.

### 4. Start the background collector — Terminal 1

From the project directory with `.venv` activated, run:

```bash
python feed.py
```

Keep this terminal open. The collector downloads all supported tickers,
creates `market_data.db`, and refreshes the data approximately once per minute.

`feed.py` normally does not print progress to the terminal. Status messages are
written to `feed_service.log`. A quiet terminal therefore does not mean that
the collector is broken.

To watch the collector log in another Windows PowerShell terminal:

```powershell
Get-Content .\feed_service.log -Wait
```

On macOS or Linux:

```bash
tail -f feed_service.log
```

A successful cycle contains messages similar to:

```text
[OK] AAPL: 156 rows updated
[OK] BTC-USD: 393 rows updated
```

Stop the collector with `Ctrl+C`. Python may display `KeyboardInterrupt` while
the process is waiting in `time.sleep(60)`. This is an expected manual
shutdown, not a `yfinance` failure.

### 5. Start the dashboard — Terminal 2

Open a separate terminal, return to the project directory, and activate the
same virtual environment again.

Windows PowerShell:

```powershell
cd path\to\market-monitor
.\.venv\Scripts\Activate.ps1
python main.py
```

macOS or Linux:

```bash
cd path/to/market-monitor
source .venv/bin/activate
python main.py
```

Open the dashboard at:

```text
http://127.0.0.1:8050/
```

After at least one successful collector cycle, the dashboard should display
recent market data and report the feed as online.

## Troubleshooting

### VS Code underlines `import yfinance`

If the script runs but VS Code reports that `yfinance` cannot be resolved, the
editor and terminal are probably using different Python interpreters.

1. Open the Command Palette with `Ctrl+Shift+P`.
2. Select **Python: Select Interpreter**.
3. Choose `market-monitor\.venv\Scripts\python.exe` on Windows or
   `market-monitor/.venv/bin/python` on macOS/Linux.
4. Run **Developer: Reload Window** if the warning remains.

### The collector appears to do nothing

This is expected when no error is shown. Check `feed_service.log` because the
collector logs to a file instead of standard output. Also confirm that the
terminal remains open and that the process has not been stopped.

### The dashboard reports `FEED OFFLINE`

- Start `feed.py` before `main.py`.
- Wait for the first collection cycle to finish.
- Confirm that both terminals use the same project directory.
- Check `feed_service.log` for Yahoo Finance network errors or empty responses.
- Confirm that `market_data.db` was created in the repository directory.

### `KeyboardInterrupt` appears in `feed.py`

`KeyboardInterrupt` is expected after pressing `Ctrl+C`. It only indicates that
the continuous collector loop was stopped manually.

### Runtime files

The following files are generated locally and are intentionally ignored by
Git:

- `market_data.db` — cached market data used by the dashboard;
- `feed_service.log` — collector status and error messages.
