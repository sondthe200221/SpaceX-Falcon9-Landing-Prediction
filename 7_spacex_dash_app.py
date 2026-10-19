import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("dataset_part_2.csv")
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("SpaceX Launch Records Dashboard", style={"textAlign": "center"}),
    dcc.Dropdown(
        id="site-dropdown",
        options=[{"label": "All Sites", "value": "ALL"}] + 
                [{"label": site, "value": site} for site in spacex_df["LaunchSite"].unique()],
        value="ALL",
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),
    html.Div(dcc.Graph(id="success-pie-chart")),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id="payload-slider",
        min=0, max=10000, step=1000,
        marks={0: "0", 2500: "2500", 5000: "5000", 7500: "7500", 10000: "10000"},
        value=[0, 10000]
    ),
    html.Div(dcc.Graph(id="success-payload-scatter-chart")),
])

@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value")
)
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        fig = px.pie(spacex_df, values="Class", names="LaunchSite", title="Total Success Launches By Site")
    else:
        filtered_df = spacex_df[spacex_df["LaunchSite"] == entered_site]
        fig = px.pie(filtered_df, names="Class", title=f"Total Success Launches for site {entered_site}")
    return fig

@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [Input(component_id="site-dropdown", component_property="value"),
     Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df["PayloadMass"] >= low) & (spacex_df["PayloadMass"] <= high)
    filtered_df = spacex_df[mask]
    if entered_site != "ALL":
        filtered_df = filtered_df[filtered_df["LaunchSite"] == entered_site]
    fig = px.scatter(
        filtered_df, x="PayloadMass", y="Class",
        color="BoosterVersion",
        title="Correlation between Payload and Success for selected site"
    )
    return fig

if __name__ == "__main__":
    app.run_server(port=8050)
