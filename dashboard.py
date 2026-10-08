import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

st.title("📊 Sales Performance Dashboard")

st.caption(
    "Interactive analysis of revenue, profit, products, regions and sales performance.")

st.subheader("🔎 Dashboard Filters")

col1,col2=st.columns(2)
with col1:
    region=st.selectbox(
        "Select Region",
        ["All","North","East","West","South"],
        key="region_filter"
    )
with col2:
    product=st.selectbox(
        "Select Product",
        ["All", "Keyboard", "Laptop", "Monitor", "Mouse", "Phone"],  key="product_filter"
    )


sales=pd.read_csv("data/sales.csv")


sales["Date"]=pd.to_datetime(sales["Date"])
date_col1, date_col2 = st.columns(2)

with date_col1:
    start_date = st.date_input(
        "Start Date",
        sales["Date"].min(),
        key="start_date_filter"
    )

with date_col2:
    end_date = st.date_input(
        "End Date",
        sales["Date"].max(), key="end_date_filter"
    )   

def reset_filters():
    st.session_state["region_filter"] = "All"
    st.session_state["product_filter"] = "All"
    st.session_state["start_date_filter"] = sales["Date"].min().date()
    st.session_state["end_date_filter"] = sales["Date"].max().date()

st.button(
    "🔄 Reset Filters",
    on_click=reset_filters)

if start_date>end_date:
    st.error("Start date cannot be after end date")
    st.stop()


filetered_sales=sales.copy()
if region !="All":
    filetered_sales=filetered_sales[filetered_sales["Region"]==region]

if product !="All":
    filetered_sales=filetered_sales[filetered_sales["Product"]==product]

filetered_sales = filetered_sales[
    (filetered_sales["Date"] >= pd.to_datetime(start_date)) &
    (filetered_sales["Date"] <= pd.to_datetime(end_date))
]

if filetered_sales.empty:
    st.warning("No sales data available for the selected filters.")
    st.stop()

# Download Filters
csv_data = filetered_sales.to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="filtered_sales.csv",
    mime="text/csv"
)

filetered_sales["Profit"]=(filetered_sales["Revenue"]-filetered_sales["Cost"])

total_revenue=filetered_sales["Revenue"].sum()
total_profit=filetered_sales["Profit"].sum()
total_quantity=filetered_sales["Quantity"].sum()

profit_margin=(total_profit/total_revenue)*100

product_revenue = filetered_sales.groupby("Product")["Revenue"].sum()

if not product_revenue.empty:
    top_product = product_revenue.idxmax()
    top_product_revenue = product_revenue.max()
else:
    top_product = "N/A"
    top_product_revenue = 0

if len(product_revenue) > 1:
    second_product = product_revenue.sort_values(
        ascending=False
    ).index[1]
    second_product_revenue = product_revenue.sort_values(
        ascending=False
    ).iloc[1]
else:
    second_product = "N/A"
    second_product_revenue = 0

st.subheader("💡 Business Insight")

if second_product == "N/A":
    st.info(
        f"{top_product} is the only product in the selected filters, "
        f"generating ₹{top_product_revenue:,.0f} in revenue."
    )
else:
    st.info(
        f"{top_product} leads revenue with ₹{top_product_revenue:,.0f}, "
        f"followed by {second_product} at ₹{second_product_revenue:,.0f}."
    )

if total_revenue > 0:
    top_product_percentage = (
        top_product_revenue / total_revenue
    ) * 100
else:
    top_product_percentage = 0

st.subheader("📊 Key Performance Indicators")

st.caption(
    "Key metrics for the selected region, product and date range."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "📈 Total Profit",
        f"₹{total_profit:,.0f}"
    )

with col3:
    st.metric(
        "📦 Total Quantity",
        f"{total_quantity:,}"
    )

with col4:
    st.metric(
        "📊 Profit Margin",
        f"{profit_margin:.2f}%"
    )

st.subheader("🏆 Top Performing Product")

st.write(
    f"**{top_product}** generated **₹{top_product_revenue:,.0f}** "
    f"in revenue, contributing **{top_product_percentage:.2f}%** "
    f"of total revenue."
)

st.subheader("📈 Sales Analysis")

# Monthly Sales Revenue Chart
monthly_sales = filetered_sales.groupby(
    filetered_sales["Date"].dt.month
)["Revenue"].sum()


if not monthly_sales.empty:

    chart_data = monthly_sales.reset_index()

    chart_data.columns = ["Month_Number", "Revenue"]

    chart_data["Month"] = chart_data["Month_Number"].map(
        lambda x: calendar.month_name[x]
    )

    fig = px.line(
    chart_data,
    x="Month",
    y="Revenue",
    title="Monthly Revenue Trend",
    markers=True
)

fig.update_traces(
    hovertemplate="Month: %{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>"
)

fig.update_layout(

    xaxis_title="Month",
    yaxis_title="Revenue (₹)",
    height=450,
    hovermode="x unified",
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(
    fig
)

st.subheader("📊 Revenue & Profit Trends")

monthly_performance = filetered_sales.groupby(
    filetered_sales["Date"].dt.month
)[["Revenue", "Profit"]].sum()

performance_data = monthly_performance.reset_index()
performance_data.columns = ["Month_Number", "Revenue", "Profit"]

performance_data["Month"]=performance_data["Month_Number"].map(
    lambda x:calendar.month_name[x]
)

performance_fig=px.line(
    performance_data, x="Month",
    y=["Revenue", "Profit"],
    title="Revenue vs Profit",
    markers=True
)

performance_fig.update_traces(
    hovertemplate="Month: %{x}<br>Amount: ₹%{y:,.0f}<extra></extra>"
)

performance_fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Amount (₹)",
    height=450,
    hovermode="x unified",
    legend_title_text="",
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(performance_fig)


product_sales = filetered_sales.groupby("Product")["Revenue"].sum()

product_fig = px.bar(
    x=product_sales.index,
    y=product_sales.values,
    title="Sales by Product"
)

product_fig.update_traces(
    hovertemplate="Product: %{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>"
)

product_fig.update_layout(
    xaxis_title="Product",
    yaxis_title="Revenue (₹)",
    height=450,
    margin=dict(l=20, r=20, t=50, b=20))


profit_by_product = filetered_sales.groupby("Product")["Profit"].sum()
profit_product_fig = px.bar(
    x=profit_by_product.index,
    y=profit_by_product.values,
    title="Profit by Product"
)

profit_product_fig.update_traces(
    hovertemplate="Product: %{x}<br>Profit: ₹%{y:,.0f}<extra></extra>"
)

profit_product_fig.update_layout(
    xaxis_title="Product",
    yaxis_title="Profit (₹)",
     height=450,
    margin=dict(l=20, r=20, t=50, b=20)
)

profit_product_fig.update_layout(
    xaxis_title="Product",
    yaxis_title="Profit (₹)",
    height=450,
    margin=dict(l=20, r=20, t=50, b=20)
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(product_fig)

with col2:
    st.plotly_chart(profit_product_fig)

region_sales = filetered_sales.groupby("Region")["Revenue"].sum()

region_fig = px.bar(
    x=region_sales.index,
    y=region_sales.values,
    title="Sales by Region")

region_fig.update_traces(
    hovertemplate="Region: %{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>"
)

region_fig.update_layout(
     xaxis_title="Region",
    yaxis_title="Revenue (₹)",
    height=450,
    margin=dict(l=20, r=20, t=50, b=20))

col1, col2 = st.columns(2)


salesperson_sales=filetered_sales.groupby("Salesperson")["Revenue"].sum()

salesperson_fig=px.bar(
    x=salesperson_sales.index,
    y=salesperson_sales.values,
    title="Sales by Salesperson"
)

salesperson_fig.update_traces(
    hovertemplate="Salesperson: %{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>"
)

salesperson_fig.update_layout(
    xaxis_title="Salesperson",
    yaxis_title="Revenue (₹)",
    height=450,
    margin=dict(l=20, r=20, t=50, b=20)
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(region_fig)

with col2:
    st.plotly_chart(salesperson_fig)