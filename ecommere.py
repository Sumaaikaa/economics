import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title(" E-commerce Data Analysis")


uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    st.subheader(" Head of the Data")
    st.write(df.head())

    st.subheader("Summary Statistics")
    st.write(df.describe())

    st.subheader("Columns in Data")
    st.write(df.columns.tolist())

    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
        st.success(" Converted `order_date` to datetime")

    if "region" in df.columns and "order_id" in df.columns:
        gr = df.groupby("region")["order_id"].count()
        st.subheader("Orders by Region")
        st.write(gr)

        fig = px.bar(gr, x=gr.index, y=gr.values, title="Orders Count by Region", labels={"x": "Region", "y": "Orders"})
        st.plotly_chart(fig)

    if "price" in df.columns:
        topmon = df.groupby("region")["price"].count()
        st.subheader("Transactions (Price Count) by Region")
        st.write(topmon)

        fig = px.pie(names=topmon.index, values=topmon.values, title="Price Count Distribution by Region")
        st.plotly_chart(fig)

    if "customer_id" in df.columns:
        topcus_id = df.groupby(["region", "customer_id"])["order_id"].count().reset_index()
        topcus_id = topcus_id.sort_values(by="order_id", ascending=False).head(10)
        st.subheader("Top 10 Customers by Region")
        st.write(topcus_id)

        fig = px.bar(topcus_id, x="customer_id", y="order_id", color="region", title="Top Customers by Orders")
        st.plotly_chart(fig)

    if "order_date" in df.columns and "order_id" in df.columns:
        st.subheader("Orders Over Time")
        monthly_orders = (
            df.groupby(df["order_date"].dt.to_period("M"))["order_id"].count().reset_index()
        )
        monthly_orders["order_date"] = monthly_orders["order_date"].dt.to_timestamp()

        fig = px.line(monthly_orders, x="order_date", y="order_id", markers=True, title="Monthly Orders Trend")
        st.plotly_chart(fig)

    if "price" in df.columns:
        st.subheader("Price Distribution")
        fig, ax = plt.subplots()
        df["price"].hist(ax=ax, bins=30, edgecolor="black")
        ax.set_title("Price Distribution")
        ax.set_xlabel("Price")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
