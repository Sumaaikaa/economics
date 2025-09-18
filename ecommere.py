import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Economic Data Analysis")
Ufile = st.file_uploader("Upload your file here", type = ["xlsx", "xls"])

if Ufile : 
    df = pd.read_excel(Ufile)
    st.subheader("Data")
    st.write(df.head(5))

    st.subheader("Summary statistics")
    st.write(df.describe())

    st.subheader("Column-wise Analysis")
    column = st.selectbox("Select a column for analysis", df.columns)

    if pd.api.types.is_numeric_dtype(df[column]):
        st.write(f"Summary of {column}:")
        st.write(df[column].describe())

        fig, ax = plt.subplots()
        df[column].hist(ax=ax, bins=20)
        ax.set_title(f"Histogram of {column}")
        st.pyplot(fig)
    else: 
        st.write(f"Summary of {column}:")
        st.write(df[column].value_counts())

        fig, ax = plt.subplots()
        df[column].value_counts().plot(kind="bar", ax=ax)
        ax.set_title(f"Bar Chart of {column}")
        ax.set_ylabel("Count")
        ax.set_xlabel(column)
        st.pyplot(fig)

        