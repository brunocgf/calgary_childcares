# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

colors = {
    'background': '#BFCAD0',
    'text': '#970C10',
    'coolgray': '#474440',
    'gunmetalgray': '#738580'
}

df = pd.read_feather("./data/clean.feather")
df = df[df['inspection_date'] > '2018-01-01']

# Get all programs
programs = df['program_name'].unique()
programs.sort()


app.layout = html.Div(
    
    style={'backgroundColor': colors['background']}, 
    
    children=[
        
        html.H1(
            children='Calgary Daycares',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(children='Daycare inspections.', 
                style={
                    'textAlign': 'center',
                    'color': colors['text']
        }),
        
        html.Div(children = [
            dcc.Dropdown(
                programs,
                'select the program',
                id = 'program-filter')
        ],
                style={'color': colors['text']}
                ),

        dcc.Graph(id='program-graph')
])

@app.callback(
    Output('program-graph', 'figure'),
    Input('program-filter', 'value')
)
def update_graph(program_filter):
    df_filtered = df[df['program_name'].str.contains(program_filter)]
    df_plot = df_filtered.groupby(['inspection_reason', pd.Grouper(key='inspection_date', freq='MS')]).index.count().reset_index()

    fig = px.bar(df_plot, x="inspection_date", y="index", color = "inspection_reason")

    fig.update_layout(
        plot_bgcolor=colors['gunmetalgray'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=colors['coolgray'])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=colors['coolgray'])
    
    return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)
