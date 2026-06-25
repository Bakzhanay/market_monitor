from dash import dcc, html
import dash_bootstrap_components as dbc

def create_layout():
    return dbc.Container([
        dcc.Interval(id='refresh-interval', interval=60_000, n_intervals=0),
        dbc.Row([
            dbc.Col(html.H1(id="header-title", children="Market Activity Monitor", className="text-center my-4 header-title"), width=12)
        ]),
        dbc.Row([
            # Левая панель
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("ASSET CONTROL", className="card-title-custom"),
                        html.Label("Select Instrument:", className="text-muted small d-block mb-2"),
                        dcc.Dropdown(
                            id='ticker-input',
                            options=[
                                {'label': 'Apple Inc. (AAPL)', 'value': 'AAPL'},
                                {'label': 'Nvidia Corp. (NVDA)', 'value': 'NVDA'},
                                {'label': 'Microsoft Corp. (MSFT)', 'value': 'MSFT'},
                                {'label': 'Tesla Inc. (TSLA)', 'value': 'TSLA'},
                                {'label': 'S&P 500 ETF (SPY)', 'value': 'SPY'},
                                {'label': 'Nasdaq 100 ETF (QQQ)', 'value': 'QQQ'},
                                {'label': 'Bitcoin / USD (BTC-USD)', 'value': 'BTC-USD'},
                                {'label': 'Ethereum / USD (ETH-USD)', 'value': 'ETH-USD'}
                            ],
                            value='AAPL',
                            clearable=False,
                            className="mb-3 text-dark"
                        ),
                        dbc.Switch(
                            id="mode-switch",
                            label="Advanced Mode",
                            value=True,
                            className="mb-3 text-white"
                        ),
                        dbc.Button("Reset View", id="reset-btn", color="secondary", size="sm", className="mb-4 w-100"),

                        html.Div(id='live-price-block'),

                        html.Hr(),

                        html.H6(
                            "SYSTEM STATUS",
                            className="text-uppercase text-muted"
                        ),

                        html.Div(
                            "Loading...",
                            id='feed-status',
                            className="small text-muted mt-2"
                        ),

                        html.Div(
                            "Loading...",
                            id='market-status',
                            className="small text-muted mt-1"
                        ),

                        html.Div(
                            "Loading...",
                            id='data-age',
                            className="small text-muted mt-1"
                        ),

                        html.Div(
                            "Loading...",
                            id='last-sync',
                            className="small text-muted mt-1"
                        ),

                        html.Div(
                            "Loading...",
                            id='anomaly-counter',
                            className="small text-muted mt-2"
                        ),

                        html.Hr(),

                        html.Div(
                            "5-Minute Market Data",
                            className="small text-info"
                        ),

                        html.Div(
                            "Auto-updated every 60 seconds",
                            className="small text-muted"
                        ),
                    ])
                ], className="sidebar-card h-100")
            ], md=3, xs=12),

            # Основной экран графиков и логов
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Loading(
                            id="graph-loader",
                            type="circle",
                            children=[
                                dcc.Graph(id='price-graph')
                            ]
                        )
                    ])
                ], className="graph-card mb-3"),

                html.Div(id="advanced-components", children=[
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("REAL-TIME ANOMALY LOG", className="card-title-custom text-warning"),
                            dcc.Loading(
                                id="table-loader",
                                type="circle",
                                children=[
                                    html.Div(
                                    id='anomaly-table-container'
                                    )
                                ]
                            )
                        ])
                    ], className="anomaly-card")
                ])
            ], md=9, xs=12)
        ], className="match-height-row"),

        # Блок для новичков
       # Блок для новичков
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("What am I looking at?", className="text-info mb-2"),
                        html.P("This graph tracks real-time market activity. In 'Simple' mode, you observe only the general price direction of the asset. 'Advanced' mode engages professional metrics: trading volumes and automatic detection of structural anomalies (rapid price movements or unusual volume spikes).", className="text-white small mb-3"),
                        
                        html.H6("System Metrics & Specifications", className="text-muted mt-3"),
                        dbc.Row([
                            dbc.Col([
                                html.P("• Anomalies are detected using a rolling Gaussian Z-score on a 20-period window. Values breaking the +/-3.0 boundary are flagged with markers.", className="text-muted small m-0"),
                            ], md=6),
                            dbc.Col([
                                html.P("• Use the 'Reset View' button or double-click the chart to restore the default scale after zooming.", className="text-muted small m-0"),

                                html.P("• Market data is collected automatically every 5 minutes. Charts and analytics are based on 5-minute candlestick intervals and may not reflect tick-by-tick price movements.",className="text-muted small mt-2")
                            ], md=6),
                        ])
                    ])
                ], className="my-4 footer-card")
            ], width=12)
        ])

    ], fluid=True, className="terminal-container")
