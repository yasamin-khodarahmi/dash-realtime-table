from dash import html, dcc
import dash_bootstrap_components as dbc

class TableComponentFactory:
    @staticmethod
    def create_dropdown(row_id, values):
        return dcc.Dropdown(
            id={'type': 'multi-select', 'index': row_id},
            options=['Select 1', 'Select 2'],
            value=values,
            multi=True,
            className='mb-2'
        )

    @staticmethod
    def create_radioitems(row_id, value):
        return dbc.RadioItems(
            id={'type': 'is-active', 'index': row_id},
            options=[
                {'label': 'True', 'value': True},
                {'label': 'False', 'value': False},
            ],
            value=value,
            inline=True
        )

def create_table_row(row_id, row_data):
    return html.Tr([
        html.Td(TableComponentFactory.create_dropdown(row_id, row_data['multi']), 
                style={'min-width': '200px'}),
        html.Td(TableComponentFactory.create_radioitems(row_id, row_data['active']))
    ])
