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

# Create a dash application
app = dash.Dash(__name__)

launch_sites = spacex_df['Launch Site'].unique()
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=dropdown_options,  # Options with 'All Sites' and each unique launch site
                                    value='ALL',  # Default value to display 'All Sites'
                                    placeholder="Select a Launch Site here",  # Placeholder text
                                    searchable=True  # Enables searching within dropdown
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,          # Starting point of the slider (0 kg)
                                    max=10000,      # Ending point of the slider (10000 kg)
                                    step=1000,      # Interval of the slider (1000 kg)
                                    marks={i: f'{i}' for i in range(0, 10001, 1000)},  # Labels at each 1000 kg interval
                                    value=[min_payload, max_payload]  # Current selected range
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Callback function to update the pie chart based on dropdown selection
# Callback function to update the pie chart based on dropdown selection
# Callback function to update the pie chart based on dropdown selection
# Callback function to update the pie chart based on dropdown selection
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    # Check if ALL sites are selected
    if selected_site == 'ALL':
        # Group by 'Launch Site' and calculate the success count for each site
        success_counts = spacex_df[spacex_df['class'] == 1].groupby('Launch Site').size().reset_index(name='Success Count')
        
        # Create a pie chart showing success counts for each launch site
        fig = px.pie(
            success_counts,
            names='Launch Site',
            values='Success Count',
            title="Total Success Launches by Site",
            hole=.3
        )
        
    else:
        # Filter dataframe to include data for the selected site only
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        
        # Create a pie chart showing success vs. failure for the selected site
        fig = px.pie(
            filtered_df,
            names='class',
            title=f"Success vs Failure Launches for {selected_site}",
            hole=.3
        )
        # Map class values for better labels
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(
            legend_title_text='Outcome',
            legend=dict(
                itemsizing='constant'
            )
        )

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(selected_site, selected_payload_range):
    # Filter the dataframe based on the payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])
    ]
    
    # Check if ALL sites are selected
    if selected_site == 'ALL':
        # Generate scatter plot for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Launch Outcome for All Sites',
            labels={'class': 'Launch Outcome (1=Success, 0=Failure)'}
        )
    else:
        # Filter the dataframe for the selected site
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        
        # Generate scatter plot for the specific site
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Launch Outcome for {selected_site}',
            labels={'class': 'Launch Outcome (1=Success, 0=Failure)'}
        )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
