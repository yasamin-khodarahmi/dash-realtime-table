import dash
from dash import Input, Output, State, callback, clientside_callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import eventlet
import eventlet.wsgi

from .data.data_handler import DataHandler
from .websocket.manager import WebSocketManager
from .components.table import create_table_row
from .layout.main_layout import create_layout

# Initialize components
data_handler = DataHandler()
websocket_manager = WebSocketManager()

# Create Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set layout
app.layout = create_layout()

@app.callback(
    Output('data-store', 'data'),
    Input('sync-interval', 'n_intervals')
)
def initialize_data(n):
    return data_handler.load_data()

@app.callback(
    Output('table-body', 'children'),
    Input('data-store', 'data'),
)
def update_table(data):
    if not data:
        raise PreventUpdate
    return [create_table_row(idx, row_data) for idx, row_data in enumerate(data)]

@app.callback(
    Output('data-store', 'data', allow_duplicate=True),
    Input('add-row-button', 'n_clicks'),
    Input({'type': 'multi-select', 'index': dash.ALL}, 'value'),
    Input({'type': 'is-active', 'index': dash.ALL}, 'value'),
    State('data-store', 'data'),
    prevent_initial_call=True
)
def handle_user_updates(n_clicks, multi_values, active_values, stored_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'add-row-button':
        stored_data.append({'multi': [], 'active': False})
    else:
        for idx in range(len(stored_data)):
            if idx < len(multi_values):
                stored_data[idx]['multi'] = multi_values[idx] or []
            if idx < len(active_values):
                stored_data[idx]['active'] = active_values[idx] if active_values[idx] is not None else False

    data_handler.save_data(stored_data)
    return stored_data

clientside_callback(
    """
    function(divData) {
        const event = new Event('data-updated');
        document.dispatchEvent(event);
        return divData;
    }
    """,
    Output('socket-trigger', 'children'),
    Input('data-store', 'data')
)

@app.callback(
    Output('data-store', 'data', allow_duplicate=True),
    Input('socket-trigger', 'children'),
    State('data-store', 'data'),
    prevent_initial_call=True
)
def handle_external_updates(trigger, current_data):
    return data_handler.load_data()

@server.route('/socket.io/')
def socketio_route():
    return websocket_manager.app

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8050)), app.server)