import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.image('e-commerce-png-ecommerce-png-png-image-510.png')
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="📊",
    layout="wide"
)
st.date_input("Select a date")

st.title(""" 📊 Welcome to our E-commerce Dashboard
This is my first time using streamlit.""")

#upload data
upload_file = st.file_uploader("ecommerce_customer_data_large.csv")

data = pd.read_csv("ecommerce_customer_data_large.csv")
summary = data[['Quantity', 'Total Purchase Amount', 'Customer Age']].agg(['min', 'max', 'mean'])
summary = summary.round(2)

st.subheader("Summary Statistics")
st.table(summary)

#histogram
st.subheader("Histogram")
column = st.selectbox("Choose a column",data.columns)
fig, ax = plt.subplots(figsize = (10,6))
data[column].plot(kind = 'hist', ax =ax)
st.pyplot(fig)
fig = px.histogram(data, x=column)
fig.update_traces( marker = {"color":"purple", "line":{"color":"black","width":2}})
st.plotly_chart(fig)

#Scatter chart
st.subheader("Scatter Chart")
x_column = st.selectbox("Choose x-axis column",df.columns)
y_column = st.selectbox("Choose y-axis column",df.columns)
fig, ax = plt.subplots(figsize = (10,6))
df.plot(kind = 'scatter', x=x_column, y=y_column, ax =ax)
st.pyplot(fig)

tab1, tab2, tab3 = st.tabs([
    "📊 Objective 1",
    "👥 Objective 2",
    "💳 Objective 3"
])

with tab1: 
    st.subheader("Objective 1 : Average Purchase Amount by Product Category")
    import pandas as pd
    data = pd.read_csv("ecommerce_customer_data_large.csv")
    summary = data [['Quantity','Total Purchase Amount', 'Customer Age']].agg (['min','max','mean'])

    revenue_summary = data.groupby ('Product Category')['Total Purchase Amount'].mean ().reset_index()

    revenue_summary.columns = ['Product Category','Average Purchase Amount']       
    revenue_summary = revenue_summary.sort_values(by = 'Average Purchase Amount', ascending = False)
                               
    revenue_summary.to_csv ('product_summary.csv',index = False)
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    DF = pd.read_csv ('product_summary.csv')
    fig, ax = plt.subplots (figsize =(10,6))
    category_colors = 'Set2'

    sns.barplot( 
        x ='Product Category',
        y ='Average Purchase Amount',
        data = revenue_summary,
        palette = 'Set2',
        hue = 'Product Category',
        legend = False,
        ax=ax
    )

    ax.set_ylim(
        revenue_summary['Average Purchase Amount'].min() - 5,
        revenue_summary['Average Purchase Amount'].max() + 5
    )

    for p in ax.patches:
        ax.annotate(
            f'{p.get_height():.2f}',
            (p.get_x() + p.get_width()/2, p.get_height()),
            ha='center',
            va='bottom'
        )
    ax.set_title('Average Purchase Amount by Product Category', fontsize=14, fontweight='bold')
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Average Purchase Amount ($)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)


    st.dataframe(
        revenue_summary.reset_index(drop=True),
        use_container_width=True
    )

    plt.tight_layout()
    st.pyplot(fig)

with tab2:
    st.subheader("OBJECTIVE 2: Demographics & Spending Behavior (Dual Chart)")
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import zipfile

    data = df.copy()
            
    data.dropna(inplace=True)

        # 1. Segment Age into clean blocks
    data['Age Group'] = pd.cut(data['Age'], 
                               bins=[0, 25, 45, 65, 120], 
                               labels=['Youth', 'Young Adult', 'Middle Aged', 'Senior'])

    # 2. Aggregations
    age_spending = data.groupby('Age Group', observed=False)['Total Purchase Amount'].sum().reset_index()
    gender_spending = data.groupby('Gender')['Total Purchase Amount'].sum().reset_index()
    core_profile = data.groupby(['Age Group', 'Gender'], observed=False)['Total Purchase Amount'].sum().reset_index()
    core_profile = core_profile.sort_values(by='Total Purchase Amount', ascending=False).reset_index(drop=True)

    # Display tables
    st.write("### 1. Spending by Age Group")
    st.dataframe(age_spending, use_container_width=True)

    st.write("### 2. Spending by Gender")
    st.dataframe(gender_spending, use_container_width=True)

    st.write("### 3. Platform Core Customer Rankings (Combined Profile) ")
    st.dataframe(core_profile)
    
    top_segment = core_profile.iloc[0]
    st.write(f" IDENTIFIED CORE CUSTOMER PROFILE: {top_segment['Age Group']} {top_segment['Gender']}s")
    st.write(f"Total Sales Contribution from Core Profile: ${top_segment['Total Purchase Amount']:,}\n")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # LEFT CHART: Pie Chart showing overall Age Group contribution
    ax1.pie(age_spending['Total Purchase Amount'], 
            labels=age_spending['Age Group'], 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    ax1.set_title('Overall Sales Contribution by Age Group', fontsize=12, fontweight='bold')
   
    # RIGHT CHART: Grouped Bar Chart showing the interaction of Age Group & Gender
    sns.barplot(data=data, x='Age Group', y='Total Purchase Amount', hue='Gender', 
                estimator=sum, errorbar=None, palette='muted', ax=ax2)
    ax2.set_title('Revenue Distribution by Combined Age & Gender', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Age Group')
    ax2.set_ylabel('Total Sales ($)')
    ax2.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    st.pyplot(fig)


with tab3:    
    st.subheader("OBJECTIVE 3: Payment Preferences and Product Returns") 

    import pandas as pd
    import matplotlib.pyplot as plt
    import zipfile

    data = df.copy()
            
    data.dropna(inplace=True)

    #  Determine the most used payment methods (Transaction Counts)
    payment_counts = data['Payment Method'].value_counts().reset_index()
    payment_counts.columns = ['Payment Method', 'Transaction Count']
    
    # Investigate if certain product categories are more prone to returns
    category_returns = data.groupby('Product Category')['Returns'].mean().reset_index()
    category_returns['Return Rate (%)'] = category_returns['Returns'] * 100

    # Investigate if certain PAYMENT TYPES are more prone to returns
    payment_returns = data.groupby('Payment Method')['Returns'].mean().reset_index()
    payment_returns['Return Rate (%)'] = payment_returns['Returns'] * 100

    # Display all tables 
    st.write("### 1. Most Used Payment Methods")
    st.dataframe(payment_counts, use_container_width=True)

    st.write("### 2. Return Rates by Product Category")
    st.dataframe(category_returns[['Product Category', 'Return Rate (%)']],
             use_container_width=True)

    st.write("### 3. Return Rates by Payment Method")
    st.dataframe(payment_returns[['Payment Method', 'Return Rate (%)']],
             use_container_width=True)

   
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Left Chart: Returns by Category
    ax1.bar(category_returns['Product Category'], category_returns['Return Rate (%)'], color='#E74C3C', edgecolor='black')
    ax1.set_title('Return Rates by Product Category (%)')
    ax1.set_xlabel('Product Category')
    ax1.set_ylabel('Return Rate (%)')
    ax1.set_ylim(
        category_returns['Return Rate (%)'].min() - 1,
        category_returns['Return Rate (%)'].max() + 1
        )
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Right Chart: Returns by Payment Method
    ax2.bar(payment_returns['Payment Method'], payment_returns['Return Rate (%)'], color='#34495E', edgecolor='black')
    ax2.set_title('Return Rates by Payment Method (%)')
    ax2.set_xlabel('Payment Method')
    ax2.set_ylabel('Return Rate (%)')
    ax2.set_ylim(
        payment_returns['Return Rate (%)'].min() - 1,
        payment_returns['Return Rate (%)'].max() + 1
    )
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)


