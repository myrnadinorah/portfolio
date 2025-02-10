import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import os

# Load environment variable
mysql_connection_string = os.getenv("MYSQL_CONNECTION_STRING")

st.title("Portfolio Dashboard with Trades Metrics")

# Debugging connection string
if not mysql_connection_string or "MomentolyY2025" in mysql_connection_string:
    st.error("❌ MYSQL_CONNECTION_STRING is missing or incorrect! Check GitHub Secrets.")
    st.stop()

# Try connecting to MySQL
try:
    engine = create_engine(mysql_connection_string)
    st.success("✅ Connected to MySQL successfully!")
except Exception as e:
    st.error(f"❌ Failed to connect to MySQL: {e}")
    st.stop()

# Queries
query_equity = "SELECT * FROM Equity;"
query_metrics = "SELECT * FROM Metrics;"
query_trades = "SELECT * FROM Trades_Metrics;"

# Fetch data with error handling
try:
    df_equity = pd.read_sql(query_equity, con=engine)
    df_metrics = pd.read_sql(query_metrics, con=engine)
    df_trades = pd.read_sql(query_trades, con=engine)
    st.success("✅ Data successfully fetched from MySQL!")
except Exception as e:
    st.error(f"❌ An error occurred while fetching data: {e}")
    st.stop()

# Check if there are portfolios available
if df_equity.empty:
    st.warning("⚠ No portfolios available in the database.")
    st.stop()

# Extract and group portfolio IDs
portfolio_ids = df_equity['portfolio_id'].unique()
portfolio_groups = {}
for portfolio_id in portfolio_ids:
    prefix = portfolio_id.split('-')[0]
    portfolio_groups.setdefault(prefix, []).append(portfolio_id)

# Sidebar selection
st.sidebar.title("Portfolio Groups")
selected_group = st.sidebar.selectbox("Select a Group", options=list(portfolio_groups.keys()))
selected_portfolio_id = st.sidebar.radio(f"Portfolios in {selected_group}", portfolio_groups[selected_group])

# Filter data
filtered_equity = df_equity[df_equity['portfolio_id'] == selected_portfolio_id].copy()
filtered_metrics = df_metrics[df_metrics['portfolio_id'] == selected_portfolio_id].copy()
filtered_trades = df_trades[df_trades['portfolio_id'] == selected_portfolio_id].copy()

# Check if filtered data is empty
if filtered_equity.empty and filtered_metrics.empty and filtered_trades.empty:
    st.warning(f"⚠ No data available for Portfolio ID {selected_portfolio_id}.")
    st.stop()

# Convert date columns if available
if not filtered_equity.empty:
    filtered_equity['Date'] = pd.to_datetime(filtered_equity['Date'])

# Plot Equity Chart
if not filtered_equity.empty:
    st.subheader(f"📈 Equity: Date vs Value for Portfolio ID {selected_portfolio_id}")
    equity_fig = px.line(
        filtered_equity, 
        x='Date', 
        y='Value', 
        title=f'Equity: Date vs Value for Portfolio ID {selected_portfolio_id}',
        labels={'Value': 'Equity Value', 'Date': 'Date'}
    )
    equity_fig.update_layout(template="plotly_white")
    st.plotly_chart(equity_fig)

# Display Metrics Table
if not filtered_metrics.empty:
    st.subheader("📊 Portfolio Metrics")
    transposed_metrics = filtered_metrics.set_index('portfolio_id').transpose()
    st.table(transposed_metrics)

# Filter and display Trades Metrics (last 30 days)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
filtered_trades['Fecha_inicio'] = pd.to_datetime(filtered_trades['Fecha_inicio'])
trades_last_month = filtered_trades[
    (filtered_trades['Fecha_inicio'] >= start_date) & (filtered_trades['Fecha_inicio'] <= end_date)
]

if not trades_last_month.empty:
    st.subheader(f"📌 Trades Metrics for Portfolio ID {selected_portfolio_id} (Last 30 Days)")
    st.table(
        trades_last_month[
            ['Fecha_inicio', 'Fecha_salida', 'Plazo_dias', 'Asset', 'TWRR', 'MAE', 'MFE', 'TPR', 'Return_to_TPR']
        ]
    )
else:
    st.warning(f"⚠ No trade data available for the last 30 days for Portfolio ID {selected_portfolio_id}.")
