# Plotly Dashboard
# A Project for the IBM Data Science Professional Certificate
# Completed by Benny Mattis

# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
app = dash.Dash(__name__)
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                        5000: '5000',
                                        10000: '10000'},
                                    value=[0, 10000]),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# callback functions for dynamic display
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_pie_chart(entered_site, payloadrange):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payloadrange[0]) & (spacex_df['Payload Mass (kg)'] <= payloadrange[1])]
    if entered_site == 'ALL':
        if filtered_df[filtered_df['class'] == 1].size == 0:
            return px.pie(title='No Successful Launches in Payload Range')
        else:
            fig = px.pie(filtered_df, values='class', 
            names='Launch Site', 
            title='Total Successful Launches Over All Sites')
            return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        if filtered_df.size == 0:
            return px.pie(title='No Launch Data at Site in Payload Range')
        else:
            filtered_df = filtered_df['class']
            vc = filtered_df.value_counts()
            number_failure = 0 if not (0 in vc) else vc[0]
            number_success = 0 if not (1 in vc) else vc[1]
            fig = px.pie(vc, values = [number_failure, number_success], 
            names= ['Failure','Success'], 
            title= entered_site + ' Launch Successes and Failures')
            return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatterplot(entered_site, payloadrange):
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df, x = 'Payload Mass (kg)', 
        y = 'class', 
        color = 'Booster Version Category',
        range_x = payloadrange,
        title='Success by Payload Mass and Booster Category')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x = 'Payload Mass (kg)', 
        y = 'class', 
        color = 'Booster Version Category',
        range_x = payloadrange,
        title='Success by Payload Mass and Booster Category')
        return fig

if __name__ == '__main__':
    app.run_server()
