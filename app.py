import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout='wide', page_title='Startup Funding Analysis')

df = pd.read_csv('startup_funding_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')
    
    try:
        total_invested_amount = round(df['amount'].sum())
        max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        average_funding = df.groupby('startup')['amount'].sum().mean()
        number_of_startups = df['startup'].nunique()
    except Exception as e:
        st.error(f"Error calculating metrics: {e}")
        return

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric('Total Invested Amount', f'₹{total_invested_amount} Cr')
    with col2:
        st.metric('Maximum Invested Amount', f'₹{max_funding} Cr')
    with col3:
        st.metric('Average Ticket Size', f'₹{round(average_funding)} Cr')
    with col4:
        st.metric('Number of Startups Funded', number_of_startups)

    st.header('MoM Investment Trend')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    df['amount'] = df['amount'].fillna(0)

    try:
        if selected_option == 'Total':
            temp_df = df.groupby(['year', 'month'], as_index=False)['amount'].sum()
        else:
            temp_df = df.groupby(['year', 'month'], as_index=False).size().rename(columns={'size': 'amount'})
        temp_df['date'] = pd.to_datetime(temp_df[['year', 'month']].assign(day=1))
        temp_df = temp_df.sort_values('date')

        if temp_df.empty:
            st.warning("No data available for the selected option.")
            return

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(temp_df['date'], temp_df['amount'], marker='o', linestyle='-', color='b')
        ax.set_xlabel('Year-Month')
        ax.set_ylabel('Total Investment' if selected_option == 'Total' else 'Investment Count')
        ax.set_title(f'{selected_option} Investment Over Time')
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error generating graph: {e}")

def load_startup_details(startup):
    st.title(startup)
    try:
        startup_df = df[df['startup'] == startup]
        if startup_df.empty:
            st.warning("No data available for this startup.")
            return
        st.subheader('Recent Investments')
        st.dataframe(startup_df[['date', 'investors', 'vertical', 'city', 'round', 'amount']].head())
        total_funding = startup_df['amount'].sum()
        st.metric("Total Funding Received", f'₹{total_funding} Cr')
        st.subheader("Sector-wise Investment Distribution")
        vertical_series = startup_df.groupby('vertical')['amount'].sum()
        if vertical_series.empty:
            st.warning("No sector-wise investment data available.")
            return
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.1f%%")
        st.pyplot(fig1)
    except Exception as e:
        st.error(f"Error loading startup details: {e}")

def load_investor_details(investor):
    st.title(investor)
    try:
        investor_df = df[df['investors'].str.contains(investor, na=False)]
        if investor_df.empty:
            st.warning("No data available for this investor.")
            return
        last5_df = investor_df.head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
        st.subheader('Most Recent Investments')
        st.dataframe(last5_df)

        col1, col2 = st.columns(2)
        with col1:
            big_series = investor_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head()
            if not big_series.empty:
                st.subheader('Biggest Investments')
                fig, ax = plt.subplots()
                ax.bar(big_series.index, big_series.values)
                st.pyplot(fig)
            else:
                st.warning("No big investment data available.")

        with col2:
            vertical_series = investor_df.groupby('vertical')['amount'].sum()
            if not vertical_series.empty:
                st.subheader('Sectors invested in')
                fig1, ax1 = plt.subplots()
                ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.1f%%")
                st.pyplot(fig1)
            else:
                st.warning("No sector investment data available.")
    except Exception as e:
        st.error(f"Error loading investor details: {e}")

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'StartUp', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp', sorted(df['startup'].dropna().unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_details(selected_startup)

else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].dropna().str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
