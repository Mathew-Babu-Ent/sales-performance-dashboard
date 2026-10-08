# 📊 Sales Performance Dashboard

An interactive sales analytics dashboard built using Python, Pandas, Streamlit and Plotly.

## 📌 Project Overview

This project analyzes sales data and provides an interactive dashboard to understand revenue, profit, quantity and overall sales performance.

Users can filter the data by region, product and date range, and the dashboard automatically updates the KPIs, charts and business insights.

## 🚀 Features

- Interactive region and product filters
- Date range filtering
- Total Revenue KPI
- Total Profit KPI
- Total Quantity KPI
- Profit Margin calculation
- Monthly Revenue Trend
- Revenue vs Profit analysis
- Sales by Product
- Profit by Product
- Sales by Region
- Sales by Salesperson
- Top Performing Product identification
- Automatic business insights
- Download filtered sales data as CSV
- Reset filters functionality
- Handling of empty filtered results

## 🛠️ Technologies Used

- Python
- Pandas
- Streamlit
- Plotly

## 📂 Project Structure

```text
SALES_DASHBOARD/
│
├── data/
│   └── sales.csv
│
├── dashboard.py
├── app.py
└── README.md

## ▶️ How to Run

Install the required libraries:

```bash
pip install pandas streamlit plotly

Then run the dashboard:

streamlit run dashboard.py