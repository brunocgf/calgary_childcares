# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = pd.read_feather("./data/clean.feather")
df = df[df['inspection_date'] > '2018-01-01']
program_name = "KINDERHAUS MONTESSORI ACADEMY"
df_filtered = df[df['program_name'].str.contains(program_name)]
df_plot = df_filtered.groupby(['inspection_reason', pd.Grouper(key='inspection_date', freq='MS')]).index.count().reset_index()

fig = px.bar(df_plot, x="inspection_date", y="index", color = "inspection_reason")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Calgary Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
