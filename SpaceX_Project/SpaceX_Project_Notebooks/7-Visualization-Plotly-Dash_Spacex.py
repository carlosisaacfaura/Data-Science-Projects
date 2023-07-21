# Import required libraries
import pandas as pd
import dash
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites = launch_sites['Launch Site']

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': launch_sites[0], 'value': launch_sites[0]},
                                                 {'label': launch_sites[1], 'value': launch_sites[1]},
                                                 {'label': launch_sites[2], 'value': launch_sites[2]},
                                                 {'label': launch_sites[3], 'value': launch_sites[3]},
                                             ],
                                             value='ALL',
                                             placeholder='Launch Site',
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0',
                                        1000: '1000',
                                        2000: '2000',
                                        3000: '3000',
                                        4000: '4000',
                                        5000: '5000',
                                        6000: '6000',
                                        7000: '7000',
                                        8000: '8000',
                                        9000: '9000',
                                        10000: '10000'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Successful Launches Per Launch Site')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # sort the data by 'class' before passing it to the pie chart
        filtered_df = filtered_df.sort_values(by='class')
        fig = px.pie(filtered_df, names='class',
        title=f'Success and Failure Ratio for {entered_site}')
    fig.update_traces(marker=dict(colors=['red', 'blue']))  # assign the colors
    return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])

def check(site, payload):
    min, max = payload
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min) & (spacex_df['Payload Mass (kg)'] <= max)]
    if site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Payload Mass VS Landing Outcome')
        return fig
    else:
        fig = px.scatter(filtered_df[filtered_df['Launch Site']==site], x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f'Payload Mass VS Landing Outcome for {site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
