#THIS IS WORKING PERFECTLY
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Select Statistics',
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': str(i), 'value': i} for i in range(1980, 2024)],
        disabled=True
    )),
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
])

# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Define the callback function to update the output container based on the selected statistics and year
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        R_chart1 = dcc.Graph(figure=px.bar(recession_data, x='Year', y='Automobile_Sales', title='Automobile sales fluctuate over Recession Period (year wise)'))

        # Plot 2: Calculate the average number of vehicles sold by vehicle type
        new_recession_data = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(new_recession_data, x='Vehicle_Type', y='Automobile_Sales', title='Average Automobile Sales by Vehicle Type'))

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        new_recession_expenditure_data = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(new_recession_expenditure_data, names='Vehicle_Type', values='Advertising_Expenditure', title='Total Advertisement Expenditure Share by Vehicle Type'))

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        R_chart4 = dcc.Graph(figure=px.bar(recession_data, x='Vehicle_Type', y='unemployment_rate', color='Automobile_Sales', title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)])
        ]

    elif selected_statistics == 'Yearly Statistics':
        # Filter the data for the selected year
        yearly_data = data[data['Year'] == selected_year]

        # Plot 1: Yearly Automobile sales using line chart for the whole period.
        Y_chart1 = dcc.Graph(figure=px.line(yearly_data, x='Year', y='Automobile_Sales', title='Yearly Average Automobile Sales'))

        # Plot 2: Total Monthly Automobile sales using line chart.
        Y_chart2 = dcc.Graph(figure=px.line(yearly_data, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales'))

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year)))

        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, names='Vehicle_Type', values='Advertising_Expenditure', title='Total Advertisement Expenditure Share by Vehicle Type'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)])
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
