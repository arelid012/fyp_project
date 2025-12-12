import pandas as pd
import plotly.graph_objects as go
from ipywidgets import widgets, VBox, interact

# Load the dataset
data = pd.read_csv('D:\Codingthings\PyCharm\FYP project\static\data\MelakaTouristArrivals_Cleaned.csv')

# Function to plot the chart based on selected metric
def plot_chart(selected_metric):
    fig = go.Figure()

    if selected_metric == 'Tourist Arrivals':
        fig.add_trace(go.Scatter(
            x=data['year'],
            y=data['tourist_arrivals_millions'],
            mode='lines+markers',
            name='Tourist Arrivals (millions)'
        ))

    elif selected_metric == 'Average Length of Stay':
        fig.add_trace(go.Scatter(
            x=data['year'],
            y=data['avg_length_of_stay'],
            mode='lines+markers',
            name='Average Length of Stay (days)'
        ))

    elif selected_metric == 'Average Spend Per Day':
        fig.add_trace(go.Scatter(
            x=data['year'],
            y=data['rm_spend_day'],
            mode='lines+markers',
            name='Average Spend Per Day (RM)'
        ))

    # Update layout
    fig.update_layout(
        title='Tourism Trends (2000-2019)',
        xaxis_title='Year',
        yaxis_title='Value',
        template='plotly_white',
        legend=dict(title="Metrics")
    )

    fig.show()

# Create radio buttons for selecting metrics
radio_buttons = widgets.RadioButtons(
    options=['Tourist Arrivals', 'Average Length of Stay', 'Average Spend Per Day'],
    description='Metric:',
    style={'description_width': 'initial'}
)

# Interactive control
interact(plot_chart, selected_metric=radio_buttons)
