from dash import Input, Output, html, dash_table, callback_context
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from app import app
from engine import get_market_data
from datetime import datetime

@app.callback(
    [Output('header-title', 'children'),
     Output('price-graph', 'figure'),
     Output('live-price-block', 'children'),
     Output('anomaly-table-container', 'children'),
     Output('advanced-components', 'style'),
     Output('feed-status', 'children'),
     Output('market-status', 'children'),
     Output('data-age', 'children'),
     Output('last-sync', 'children'),
     Output('anomaly-counter', 'children')],
    [Input('ticker-input', 'value'),
     Input('refresh-interval', 'n_intervals'),
     Input('mode-switch', 'value'),
     Input('reset-btn', 'n_clicks')]
)
def update_terminal(selected_ticker, _n_intervals, is_advanced, reset_clicks):
    ctx = callback_context
    trigger = ctx.triggered[0]['prop_id'] if ctx.triggered else ""
    
    # Управление сбросом зума: меняем uirevision только если нажата кнопка Reset
    uirevision_val = reset_clicks if trigger == 'reset-btn.n_clicks' else 'constant_zoom'

    df = get_market_data(selected_ticker)
    header_title = f"MARKET ACTIVITY MONITOR // {selected_ticker}"
    
    if df.empty:
        fig = go.Figure()
        fig.update_layout(title=f"Data stream offline: {selected_ticker}", template='plotly_dark', height=450)

        offline_status = html.Span(
                "● FEED OFFLINE",
                style={"color": "#e71d36", "fontWeight": "bold"}
            )
        return header_title, fig, html.Div("No connection"), html.P("No anomalies detected", className="text-muted small"), {'display': 'none'}, offline_status, "", "", "", ""
    
    # 1. Сводка Sidebar Analytics
    last_row = df.iloc[-1]

    all_anomalies = df[
        df['Is_Volume_Anomaly'] |
        df['Is_Price_Anomaly']
    ].copy()

    anomaly_count = len(all_anomalies)

    anomaly_counter = html.Div([

        html.Div(
            "ANOMALIES DETECTED",
            style={
                "fontSize": "11px",
                "color": "#A3AED0"
            }
        ),

        html.Div(
            str(anomaly_count),
            style={
                "fontSize": "24px",
                "fontWeight": "bold",
                "color": "#ff9f1c" if anomaly_count > 0 else "#2ec4b6"
            }
        )
])

    last_update = df.index[-1]

    last_sync = html.Span(
        f"Last DB Sync: {last_update.strftime('%H:%M:%S')}",
        style={"color": "#A3AED0"}
    )

    if last_update.tzinfo:
        now = datetime.now(last_update.tzinfo)
    else:
        now = datetime.now()

    age_minutes = (now - last_update).total_seconds() / 60
    age_seconds = int((now - last_update).total_seconds())

    if age_minutes < 10:
        feed_status = html.Span(
            "● FEED ONLINE",
            style={"backgroundColor": "#198754",
                "color": "white",
                "padding": "4px 8px",
                "borderRadius": "6px",
                "fontWeight": "bold",
                "fontSize": "11px"}
            )
    else:
        feed_status = html.Span(
            "● FEED OFFLINE",
            style={"backgroundColor": "#dc3545",
                "color": "white",
                "padding": "4px 8px",
                "borderRadius": "6px",
                "fontWeight": "bold",
                "fontSize": "11px"}
            )

    if age_seconds < 60:

        data_age = html.Span(
            f"Data Age: {age_seconds} sec",
            style={"color": "#2ec4b6"}
        )

    elif age_seconds < 3600:

        data_age = html.Span(
            f"Data Age: {age_seconds // 60} min",
            style={"color": "#ff9f1c"}
        )

    else:

        data_age = html.Span(
            f"Data Age: {age_seconds // 3600} hr",
            style={"color": "#e71d36"}
        )

    if selected_ticker in ['BTC-USD', 'ETH-USD']:

        market_status = html.Span(
            "CRYPTO MARKET (24/7)",
            style={"color": "#4cc9f0", "fontWeight": "bold"}
        )

    else:

        now_utc = datetime.utcnow()

        weekday = now_utc.weekday()  # 0=Mon ... 6=Sun
        hour = now_utc.hour

        # Выходные
        if weekday >= 5:
            market_status = html.Span(
                "NYSE CLOSED (Weekend)",
                style={"color": "#e71d36", "fontWeight": "bold"}
            )

        # Будние дни
        elif 14 <= hour < 21:
            market_status = html.Span(
                "NYSE OPEN",
                style={"color": "#2ec4b6", "fontWeight": "bold"}
            )

        else:
            market_status = html.Span(
                "NYSE CLOSED",
                style={"color": "#ff9f1c", "fontWeight": "bold"}
            )

    price_diff = last_row['Close'] - last_row['Open']
    price_color = '#2ec4b6' if price_diff >= 0 else '#e71d36'
    sign = '+' if price_diff >= 0 else ''
    
    tz_label = "UTC" if "-" in selected_ticker else "NY Time"
    time_str = df.index[-1].strftime(f'%d %b %H:%M {tz_label}')
    
    price_html = html.Div([
        html.P("Last Traded Price:", className="text-muted mb-1 small"),
        html.H2(f"${last_row['Close']:.2f}", className="text-white font-weight-bold m-0"),
        html.P(f"Price Change: {sign}{price_diff:.2f}", style={'color': price_color}, className="small font-weight-bold mb-0"),
        html.Small(f"Last Update: {time_str}", className="text-muted d-block mt-3")
    ])
    
    # 2. Построение графика в зависимости от режима
    if not is_advanced:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Close'], mode='lines', name='Price', line=dict(color='#2ec4b6', width=2)
        ))
        fig.update_layout(
            template='plotly_dark', height=450, margin=dict(l=45, r=15, t=10, b=10),
            uirevision=uirevision_val,
            font=dict(family="'Space Mono', monospace", size=12, color="#A3AED0"),
            xaxis=dict(rangeslider=dict(visible=False))
        )
        return header_title, fig, price_html, [], {'display': 'none'}, feed_status, market_status, data_age, last_sync, html.Div()  

    # Логика Advanced Mode
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.05)
    
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name='Price (OHLC)', increasing_line_color='#2ec4b6', decreasing_line_color='#e71d36'
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df.index, y=df['SMA9'], mode='lines', name='SMA (9)', line=dict(color='#ff9f1c', width=1.5)
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=df.index, y=df['Volume'], name='Volume', marker_color='#4cc9f0', opacity=0.4
    ), row=2, col=1)
    
    vol_anomalies = df[df['Is_Volume_Anomaly']]
    price_anomalies = df[df['Is_Price_Anomaly']]
    
    if not vol_anomalies.empty:
        fig.add_trace(go.Scatter(
            x=vol_anomalies.index, y=vol_anomalies['Volume'], mode='markers',
            name='Unusual Trading Volume', marker=dict(color='#e0115f', size=9, symbol='triangle-up')
        ), row=2, col=1)
        
    if not price_anomalies.empty:
        fig.add_trace(go.Scatter(
            x=price_anomalies.index, y=price_anomalies['High'], mode='markers',
            name='Rapid Price Movement', marker=dict(color='#9b5de5', size=9, symbol='diamond')
        ), row=1, col=1)
    
    fig.update_layout(
        template='plotly_dark', height=450, margin=dict(l=45, r=15, t=10, b=10),
        showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        uirevision=uirevision_val,
        font=dict(family="'Space Mono', monospace", size=12, color="#A3AED0"),
        xaxis=dict(rangeslider=dict(visible=False)), xaxis2=dict(rangeslider=dict(visible=True), type='date')
    )


    if all_anomalies.empty:
        table_html = html.P("No structural anomalies detected.", className="text-muted small fst-italic pt-2")
    else:
        all_anomalies['Timestamp'] = all_anomalies.index.strftime('%d %b %H:%M')
        all_anomalies['Type'] = all_anomalies.apply(
            lambda r: "Rapid Price Movement" if r['Is_Price_Anomaly'] and not r['Is_Volume_Anomaly']
            else ("Unusual Trading Volume" if r['Is_Volume_Anomaly'] and not r['Is_Price_Anomaly'] else "High Market Activity"), axis=1
        )
        all_anomalies['Z-Score Metrics'] = all_anomalies.apply(
            lambda r: f"Price Z: {r['Price_Z']:.2f}" if r['Is_Price_Anomaly'] and not r['Is_Volume_Anomaly']
            else (f"Vol Z: {r['Volume_Z']:.2f}" if r['Is_Volume_Anomaly'] and not r['Is_Price_Anomaly'] else f"P.Z: {r['Price_Z']:.2f} / V.Z: {r['Volume_Z']:.2f}"), axis=1
        )
        
        table_data = all_anomalies[['Timestamp', 'Type', 'Z-Score Metrics']].tail(5).to_dict('records')
        table_html = dash_table.DataTable(
            data=table_data,
            columns=[{"name": i, "id": i} for i in ['Timestamp', 'Type', 'Z-Score Metrics']],
            style_header={'backgroundColor': '#111111', 'color': '#00adb5', 'fontWeight': 'bold', 'border': '1px solid #333'},
            style_cell={'backgroundColor': '#1e1e1e', 'color': '#ffffff', 'border': '1px solid #333', 'padding': '6px', 'fontSize': '12px', 'textAlign': 'center'},
            style_data_conditional=[
                {'if': {'column_id': 'Type', 'filter_query': '{Type} eq "Rapid Price Movement"'}, 'color': '#9b5de5', 'fontWeight': 'bold'},
                {'if': {'column_id': 'Type', 'filter_query': '{Type} eq "Unusual Trading Volume"'}, 'color': '#e0115f', 'fontWeight': 'bold'},
                {'if': {'column_id': 'Type', 'filter_query': '{Type} eq "High Market Activity"'}, 'color': '#ff9f1c', 'fontWeight': 'bold'}
            ]
        )
    
    return header_title, fig, price_html, table_html, {'display': 'block'}, feed_status, market_status, data_age, last_sync, anomaly_counter