from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import plotly.graph_objs as go
import json
import plotly.express as px
import hdbscan
import folium
from folium.plugins import HeatMap
import numpy as np
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, make_scorer, mean_absolute_error, r2_score

app = Flask(__name__)

# Load your dataset



def generate_chart(selected_metric):
    data = pd.read_csv('D:\Codingthings\PyCharm\FYP project\static\data\MelakaTouristArrivals_Cleaned.csv')
    fig = go.Figure()

    # Define the year range
    year_range = " (2000 - 2019)"  # Adjust this based on your dataset

    if selected_metric == "Tourist Arrivals":
        fig.add_trace(go.Scatter(
            x=data['year'],
            y=data['tourist_arrivals_millions'],
            mode='lines+markers',
            name='Tourist Arrivals (millions)'
        ))
        title = "Tourist Arrivals Over the Years" + year_range
    elif selected_metric == "Average Length of Stay":
        fig.add_trace(go.Scatter(
            x=data['year'],
            y=data['avg_length_of_stay'],
            mode='lines+markers',
            name='Average Length of Stay (days)'
        ))
        title = "Average Length of Stay Over the Years" + year_range
    elif selected_metric == "Average Spend Per Day":
        fig.add_trace(go.Scatter(
            x=data['year'],
            y=data['rm_spend_day'],  # Correct column name here
            mode='lines+markers',
            name='Average Spend Per Day (RM)'
        ))
        title = "Average Spend Per Day Over the Years" + year_range

    # Set the title in the layout
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Year",
        yaxis_title="Value",
        template="plotly_white"  # Optional for a clean look
    )

    # Convert Plotly figure to JSON
    return json.loads(fig.to_json())




# Route for the landing page
@app.route('/')
def landing():
    return render_template('landingpage.html')  # Render landing page


# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    file_path = 'C:/Users/halid/OneDrive/Desktop/MelakaTouristArrivals_Cleaned.csv'
    df = pd.read_csv(file_path)

    # Exclude the year 2020
    df_filtered = df[df['year'] != 2020]

    # Calculate the Average Length of Stay
    average_length_of_stay = df_filtered['avg_length_of_stay'].mean()

    # Calculate the Total Revenue Generated and convert it to billions for simplicity
    total_revenue_generated = df_filtered['tourist_receipts_rm000'].sum() / 1000000  # Convert thousands to billions

    # Calculate the Annual Growth Rate for tourist arrivals
    df_filtered['Growth Rate'] = df_filtered['tourist_arrivals_millions'].pct_change() * 100
    average_growth_rate = df_filtered['Growth Rate'].iloc[1:].mean()

    return render_template('dashboard.html',
                           average_length_of_stay=average_length_of_stay,
                           total_revenue_generated=f"RM {total_revenue_generated:.2f}B",
                           average_growth_rate=f"{average_growth_rate:.2f}%")

# API endpoint for chart data
@app.route('/chart')
def chart_data():
    selected_metric = request.args.get('metric', 'Tourist Arrivals')  # Default to 'Tourist Arrivals'
    chart = generate_chart(selected_metric)
    return jsonify(chart)


@app.route('/choropleth')
def choropleth_map():
    # Load the data from the CSV file
    tourists_plot_df = pd.read_csv('D:\Codingthings\PyCharm\FYP project\static\data\Total_Tourists_by_Country_2000_2019.csv')
    tourists_plot_df.columns = ['Country', 'Tourists']

    # Create the choropleth map
    fig = px.choropleth(
        tourists_plot_df,
        locations="Country",
        locationmode='country names',
        color="Tourists",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Total Tourists by Country from 2000 to 2019"
    )

    # Convert the Plotly figure to JSON
    return fig.to_json()


@app.route('/piechart')
def pie_chart():
    # Load the data
    file_path = 'D:\Codingthings\PyCharm\FYP project\static\data\cleaned_tourist_data.csv'
    data = pd.read_csv(file_path)

    # If no year is provided, return the list of available years
    if 'year' not in request.args:
        years = data['TAHUN'].unique().tolist()
        return jsonify({'years': years})

    # Get the year parameter from the request
    year = request.args.get('year', None)

    # Validate the year parameter
    if year is None or int(year) not in data['TAHUN'].unique():
        return jsonify({'error': f'No data available for the year {year}.'}), 400

    # Filter data for the selected year
    filtered_data = data[data['TAHUN'] == int(year)]

    # Prepare data for the pie chart
    pie_data = {
        'Category': ['Domestic', 'Foreign'],
        'Count': [filtered_data['DOMESTIK'].values[0], filtered_data['ASING'].values[0]]
    }

    pie_df = pd.DataFrame(pie_data)

    # Create the pie chart
    fig = px.pie(
        pie_df,
        values='Count',
        names='Category',
        title=f"Tourist Distribution in {year}",
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    # Convert the Plotly figure to JSON
    return fig.to_json()


@app.route('/barchart')
def bar_chart():
    year = request.args.get('year')  # Get the year from query parameters
    data_path = 'D:/Codingthings/PyCharm/FYP project/static/data/cleaned_tourist_data.csv'
    tourist_data = pd.read_csv(data_path)

    # Define ASEAN countries excluding Malaysia
    asean_countries = tourist_data.columns[5:14].tolist()
    asean_countries.remove('Malaysia')

    # Prepare the data
    asean_tourist_data = tourist_data[tourist_data['TAHUN'] == int(year)][['TAHUN'] + asean_countries] if year else tourist_data[['TAHUN'] + asean_countries]
    asean_tourist_data_melted = asean_tourist_data.melt(id_vars=['TAHUN'], var_name='Country', value_name='Tourists')

    fig = px.bar(asean_tourist_data_melted, x='Country', y='Tourists',
                 animation_frame="TAHUN",
                 labels={'Tourists': 'Number of Tourists', 'Country': 'Country'},
                 title="Top Tourist Arrivals by ASEAN Country (Excluding Malaysia) (2000-2019)",
                 color='Country',
                 category_orders={"TAHUN": sorted(asean_tourist_data_melted['TAHUN'].unique())},
                 log_y=True)

    return fig.to_json()



@app.route('/heatmap')
def generate_heatmap():
    # Load data
    data = pd.read_excel('C:/Users/halid/OneDrive/Desktop/geotagged_data_melaka.xlsx')

    # Calculate total data collected
    total_data_collected = len(data)

    # Clustering with HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=5, min_samples=1)
    data['cluster'] = clusterer.fit_predict(data[['latitude', 'longitude']])

    # Generate a scatter plot for clustering results
    fig = px.scatter(data, x='longitude', y='latitude', color='cluster',
                     labels={'cluster': 'Cluster'}, title='HDBSCAN Clustering Results')
    fig.update_layout(autosize=True)

    # Convert the plot to HTML to embed in the Flask template
    cluster_plot_html = fig.to_html(full_html=False)

    # Filter for valid clusters
    clustered_data = data[data['cluster'] != -1]

    # Generate heatmap
    m = folium.Map(location=[clustered_data['latitude'].mean(), clustered_data['longitude'].mean()],
                   zoom_start=10, min_zoom=10, max_zoom=11)
    heat_data = clustered_data[['latitude', 'longitude']].dropna().values.tolist()
    HeatMap(heat_data, radius=50, blur=35, max_zoom=14).add_to(m)

    folium.LayerControl().add_to(m)

    # Save the map to a HTML file and serve it
    heatmap_html = 'D:/Codingthings/PyCharm/FYP project/static/geographic_heatmap.html'
    m.save(heatmap_html)
    return render_template('heatmap.html',
                           total_data_collected=total_data_collected,
                           cluster_plot_html=cluster_plot_html,
                           heatmap_url=url_for('static', filename='geographic_heatmap.html'))

# Route for the Regression Page
@app.route('/regression')
def regression():
    # Load the dataset
    file_path = 'C:/Users/halid/OneDrive/Desktop/MelakaTouristArrivals_Cleaned.csv'
    df = pd.read_csv(file_path)

    # Define independent variables and the dependent variable
    X = df[['year', 'avg_length_of_stay', 'rm_spend_day']]
    y = df['tourist_arrivals_millions']

    # Setup k-fold cross-validation
    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    model = LinearRegression()

    # Define RMSE scorer manually
    def rmse(y_true, y_pred):
        return np.sqrt(mean_squared_error(y_true, y_pred))

    rmse_scorer = make_scorer(rmse)


    # Define scoring metrics
    mse_scorer = make_scorer(mean_squared_error, squared=False)  # RMSE
    mae_scorer = make_scorer(mean_squared_error)  # MAE

    # Evaluate the model using cross-validation
    rmse_scores = cross_val_score(model, X, y, cv=kf, scoring=rmse_scorer)
    mae_scorer = make_scorer(mean_squared_error)  # MAE
    mae_scores = cross_val_score(model, X, y, cv=kf, scoring=mae_scorer)
    r2_scores = cross_val_score(model, X, y, cv=kf, scoring='r2')

    # Output cross-validation metrics
    print(f'Cross-Validation RMSE Scores: {rmse_scores}')
    print(f'Cross-Validation MAE Scores: {mae_scores}')
    print(f'Cross-Validation R² Scores: {r2_scores}')
    print(f'Average RMSE: {np.mean(rmse_scores):.3f}')
    print(f'Average MAE: {np.mean(mae_scores):.3f}')
    print(f'Average R²: {np.mean(r2_scores):.3f}')

    # Re-train the model on the entire dataset for actual future predictions
    model.fit(X, y)

    # Predict future data
    future_years = np.arange(2020, 2026)
    future_data = pd.DataFrame({
        'year': future_years,
        'avg_length_of_stay': np.linspace(X['avg_length_of_stay'].iloc[-1], X['avg_length_of_stay'].iloc[-1] + 0.1, len(future_years)),
        'rm_spend_day': np.linspace(X['rm_spend_day'].iloc[-1], X['rm_spend_day'].iloc[-1] + 10, len(future_years))
    })

    historical_predictions = model.predict(X)
    future_predictions = model.predict(future_data)

    # Data for plotting
    results_df = pd.DataFrame({
        'Year': np.concatenate((X['year'], X['year'], future_years)),
        'Tourist Arrivals': np.concatenate((y, historical_predictions, future_predictions)),
        'Type': ['Actual Data'] * len(y) + ['Historical Predictions'] * len(historical_predictions) + ['Future Predictions'] * len(future_years)
    })

    # Create interactive Plotly express line chart
    fig = px.line(results_df, x='Year', y='Tourist Arrivals', color='Type', markers=True,
                  title='Tourist Arrivals: Actual vs Predicted',
                  labels={'Tourist Arrivals': 'Tourist Arrivals (Millions)'})
    fig.update_traces(mode='lines+markers')  # Ensuring each type has both lines and markers

    # Increase chart height
    fig.update_layout(height=650)

    # Convert the figure to HTML for Flask
    plot_html = fig.to_html(full_html=False)

    # Display 80:20 metrics
    rmseScore = ", ".join([f"{score:.2f}" for score in rmse_scores])
    maeScore = ", ".join([f"{score:.2f}" for score in mae_scores])
    r2Score = ", ".join([f"{score:.2f}" for score in r2_scores])

    average_rmse = round(np.mean(rmse_scores), 2)
    average_mae = round(np.mean(mae_scores), 2)
    average_r2 = round(np.mean(r2_scores), 2)

    #Display full train metrics
    # Compute metrics for full training set predictions
    rmse_full = round(np.sqrt(mean_squared_error(y, historical_predictions)), 2)
    mae_full = round(mean_absolute_error(y, historical_predictions), 2)
    r2_full = round(r2_score(y, historical_predictions), 2)

    return render_template('regression.html',
                           plot_html=plot_html,
                           A_rmse=average_rmse,
                           A_mae=average_mae,
                           A_r_squared=average_r2,
                           rmse = rmseScore,
                           mae = maeScore,
                           r2 = r2Score,
                           rmse_full=rmse_full,
                           mae_full=mae_full,
                           r2_full=r2_full)


if __name__ == '__main__':
    app.run(debug=True)






