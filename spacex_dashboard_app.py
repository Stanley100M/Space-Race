# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = spacex_df['Launch Site'].unique()
# Create the options for the dropdown
options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
        id='site-dropdown',
        options=options,  # List of options (including 'All Sites')
        value='ALL',  # Default value is 'ALL'
        placeholder="Select a Launch Site here",  # Placeholder text
        searchable=True  # Make the dropdown searchable
    ),
                                # Extract unique launch sites from the spacex_df dataframe
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # Callback to generate pie chart based on selected site
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={i: str(i) for i in range(0,10000 + 1, 5000)},
                                    value=[0,10000],  # Initial range for the slider
    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Group by launch outcome and count launches for all sites
        launch_counts = spacex_df.groupby('class')['class'].count().reset_index(name='count')
        fig = px.pie(launch_counts, names='class', values='count', title='Launch Success vs Failure (All Sites)')
    else:
        # Filter by selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        launch_counts = site_data.groupby('class')['class'].count().reset_index(name='count')
        fig = px.pie(launch_counts, names='class', values='count', title=f'Launch Success vs Failure ({selected_site})')
    
    return fig
# Callback function for the scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    min_payload, max_payload = payload_range
    
    if selected_site == 'ALL':
        # Filter by payload range for all sites
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & 
                                  (spacex_df['Payload Mass (kg)'] <= max_payload)]
    else:
        # Filter by site and payload range
        filtered_data = spacex_df[(spacex_df['Launch Site'] == selected_site) & 
                                  (spacex_df['Payload Mass (kg)'] >= min_payload) & 
                                  (spacex_df['Payload Mass (kg)'] <= max_payload)]
    
    fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='class',
                     title=f'Payload vs. Launch Success ({selected_site if selected_site != "ALL" else "All Sites"})',
                     labels={'class': 'Launch Success (1=Success, 0=Failure)', 'Payload Mass (kg)': 'Payload Mass (kg)'})
    
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server(port=8070)


## Author
Stanley Eric
