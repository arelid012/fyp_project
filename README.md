# 🏝️ Melaka Tourism Hotspot & Predictive Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

An interactive web dashboard for analyzing tourism patterns in **Melaka, Malaysia** using  
**spatial clustering (HDBSCAN)** and **predictive analytics (Multiple Linear Regression)**.

---

## ✨ Features

### 🔍 Spatial Analysis
- HDBSCAN clustering to identify tourist hotspots  
- Interactive **Folium heatmaps**
- Detection of high-density attraction zones

### 📈 Predictive Analytics
- Multiple Linear Regression for tourist arrival forecasting
- 5-fold cross-validation
- Performance metrics: **RMSE, MAE, R²**
- Future projections (2020–2025)

### 📊 Interactive Dashboard
- Plotly-powered real-time charts
- Choropleth map of international tourist origins
- Time series trends (2000–2019)
- Domestic vs foreign tourist comparison

---

## 🎯 Project Overview

This project analyzes **Melaka tourism data (2000–2019)** to answer:

- Where are Melaka’s main tourist hotspots?
- How will tourist arrivals change over time?
- Which countries contribute most to tourism?
- What are the spending and stay patterns of tourists?

**Tech Stack**
- Backend: Flask
- Data Analysis: Pandas, NumPy, Scikit-learn
- Visualization: Plotly, Folium
- Clustering: HDBSCAN

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation & Run

```bash
# Clone repository
git clone https://github.com/yourusername/melaka-tourism-analytics.git
cd melaka-tourism-analytics

# Create virtual environment
python -m venv venv

# Activate environment
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install flask pandas plotly numpy scikit-learn hdbscan folium openpyxl

# Run application
python app.py

## 🌐 Access the Application

Open your browser and visit:

👉 **http://localhost:5000**

```



