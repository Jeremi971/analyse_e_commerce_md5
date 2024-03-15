import dash
from layout import layout
from callback import register_callbacks

app = dash.Dash(__name__)

app.layout = layout
register_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True)
