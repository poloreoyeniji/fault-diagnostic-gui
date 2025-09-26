import dash
from dash import Dash, dcc, html, dash_table, Input, Output
import pandas as pd

# Load dataframe
df_clean = pd.read_csv("cleaned_faults.csv")

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Fault Diagnostic GUI"),
    
    dcc.Dropdown(
        id="machine-dropdown",
        options=[{"label": m, "value": m} for m in df_clean["machine"].unique()],
        placeholder="Select Machine"
    ),
    dcc.Dropdown(id="factory-dropdown", placeholder="Select Factory"),
    dcc.Dropdown(id="fault-dropdown", placeholder="Select Fault"),
    dcc.Dropdown(id="root-dropdown", placeholder="Select Root Cause"),
    
    html.Div(id="table-container")
])

@app.callback(
    [Output("factory-dropdown", "options"),
     Output("fault-dropdown", "options"),
     Output("root-dropdown", "options"),
     Output("table-container", "children")],
    [Input("machine-dropdown", "value"),
     Input("factory-dropdown", "value"),
     Input("fault-dropdown", "value"),
     Input("root-dropdown", "value")]
)
def update_dropdowns(machine, factory, fault, root):
    if not machine:
        return [], [], [], ""
    
    dff = df_clean[df_clean["machine"] == machine]
    factories = [{"label": f, "value": f} for f in dff["factory"].unique()]
    
    if factory:
        dff = dff[dff["factory"] == factory]
    faults = [{"label": f, "value": f} for f in dff["fault"].unique()]
    
    if fault:
        dff = dff[dff["fault"] == fault]
    roots = [{"label": r, "value": r} for r in dff["root_cause"].unique()]
    
    table = ""
    if root:
        dff = dff[dff["root_cause"] == root]
        table = dash_table.DataTable(
            data=dff.to_dict("records"),
            columns=[{"name": i, "id": i} for i in dff.columns],
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "whiteSpace": "normal"},
            page_size=10
        )
    
    return factories, faults, roots, table

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)
