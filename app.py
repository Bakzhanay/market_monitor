import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True
)
app.title = "Market Activity Monitor"
server = app.server