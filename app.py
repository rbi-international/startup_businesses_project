import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis')

df = pd.read_csv('startup_funding_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')
    
    # Total invested amount
    total_invested_amount = round(df['amount'].sum())
    # Max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # Average ticket size
    average_funding = df.groupby('startup')['amount'].sum().mean()
    # Total number of startups funded
    number_of_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric('Total Invested Amount', f'₹{total_invested_amount} Cr')
    with col2:
        st.metric('Maximum Invested Amount', f'₹{max_funding} Cr')
    with col3:
        st.metric('Average Ticket Size', f'₹{round(average_funding)} Cr')
    with col4:
        st.metric('Number of Startups Funded', number_of_startups)

    # **🔹 Fixing the MoM Graph**
    st.header('MoM Graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])

    # 🔹 Fix: Ensure `amount` column has no NaN values
    df['amount'] = df['amount'].fillna(0)

    # 🔹 Fix: Correct Grouping for Count and Total
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'], as_index=False)['amount'].sum()
    else:
        temp_df = df.groupby(['year', 'month'], as_index=False).size().rename(columns={'size': 'amount'})

    # Debugging: Show the grouped data in Streamlit before plotting
    st.write("Debugging Data:")
    st.dataframe(temp_df)

    # Convert `year` and `month` into a proper datetime object
    temp_df['date'] = pd.to_datetime(temp_df[['year', 'month']].assign(day=1))

    # 🔹 Fix: Sorting ensures x-axis is displayed correctly
    temp_df = temp_df.sort_values('date')

    # 🔹 Fix: Avoid empty plots by ensuring there's data
    if temp_df['amount'].sum() == 0:
        st.warning("No data available for the selected option.")
        return

    # Plot the graph
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(temp_df['date'], temp_df['amount'], marker='o', linestyle='-', color='b')

    # Improve visualization
    ax3.set_xlabel('Year-Month')
    ax3.set_ylabel('Total Investment' if selected_option == 'Total' else 'Investment Count')
    ax3.set_title(f'{selected_option} Investment Over Time')
    ax3.grid(True)
    plt.xticks(rotation=45)  # 🔹 Fix: Rotate x-axis labels

    # Display in Streamlit
    st.pyplot(fig3)




def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col2:
        verical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series,labels=verical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)

    print(df.info())

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)

    st.pyplot(fig2)

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)

