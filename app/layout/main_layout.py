from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return dbc.Container([
        html.H1("Real-Time Table Manager", className='mb-4'),
        dbc.Table([
            html.Thead(html.Tr([
                html.Th("multi"),
                html.Th("is_active")
            ])),
            html.Tbody(id='table-body', children=[]),
        ], bordered=True, hover=True, className='mb-4'),
        dbc.Button("Add Row", id='add-row-button', color='primary', className='mb-4'),
        dcc.Store(id='data-store', storage_type='memory'),
        dcc.Interval(id='sync-interval', interval=1000),
        html.Div(id='socket-trigger', style={'display': 'none'})
    ], fluid=True)
