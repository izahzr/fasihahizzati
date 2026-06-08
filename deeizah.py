import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.image('e-commerce-png-ecommerce-png-png-image-510.png')

st.date_input("Select a date")

st.title("""Welcome to my our E-commerce Dashboard
This is my first time using streamlit.""")

#upload data
#upload_file = st.file_uploader("Please upload here:", type = 'csv')


#df = pd.read_csv(r"C:\Users\welcome\Desktop\BSMS1306\streamlit\Tips.csv")
df = pd.read_csv("ecommerce_customer_data_large.csv")
#df = pd.read_csv(upload_file)

#show data
st.subheader("Raw Data")
st.write(df)

#histogram
st.subheader("Histogram")
column = st.selectbox("Choose a column",df.columns)
fig, ax = plt.subplots(figsize = (10,6))
df[column].plot(kind = 'hist', ax =ax)
st.pyplot(fig)
#fig = px.histogram(df, x=column)
#fig.update_traces( marker = {"color":"purple", "line":{"color":"black","width":2}})
#st.plotly_chart(fig)

#Scatter chart
st.subheader("Scatter Chart")
x_column = st.selectbox("Choose x-axis column",df.columns)
y_column = st.selectbox("Choose y-axis column",df.columns)
fig, ax = plt.subplots(figsize = (10,6))
df.plot(kind = 'scatter', x=x_column, y=y_column, ax =ax)
st.pyplot(fig)

import pandas as pd

data = pd.read_csv("ecommerce_customer_data_large.csv")
print (data)
data.info ()
data.isnull().sum()
data.dropna (inplace =  True )
data.isnull().sum()
data.duplicated ().sum ()
data
data.info ()
summary = data [['Quantity','Total Purchase Amount', 'Customer Age']].agg (['min','max','mean'])

print (summary)

#Objective 1

revenue_summary = data.groupby ('Product Category')['Total Purchase Amount'].mean ().reset_index()

revenue_summary.columns = ['Product Category','Average Purchase Amount']       
revenue_summary = revenue_summary.sort_values(by = 'Average Purchase Amount', ascending = False)
                               
print (revenue_summary)
revenue_summary.to_csv ('product_summary.csv',index = False)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DF = pd.read_csv ('product_summary.csv')
DF.info()
fig, axes = plt.subplots (figsize = (10,6))
category_colors = 'Set2'

sns.barplot( 
    x = 'Product Category',
    y = 'Average Purchase Amount',
    data = revenue_summary,
    palette = category_colors,
    hue = 'Product Category',
    legend = False,
)

plt.title ('Average Purchase Amount by Product Category', fontsize = 14, pad = 15, fontweight = 'bold')
plt.xlabel('Product Category', fontsize = 12)
plt.ylabel('Average Purchase Amount ($)', fontsize = 12)

plt.tight_layout()
plt.show()
# OBJECTIVE 2: Demographics & Spending Behavior (Dual Chart)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile

zip_file_name = "archive (7).zip"

try:
    with zipfile.ZipFile(zip_file_name, 'r') as z:
        file_list = z.namelist()
        csv_files = [f for f in file_list if f.endswith('.csv')]
        target_csv = csv_files[0]
        with z.open(target_csv) as f:
            data = pd.read_csv(f)
            
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
    print("--- 1. Spending by Age Group ---")
    print(age_spending)
    print("\n--- 2. Spending by Gender ---")
    print(gender_spending)
    print("\n--- 3. Platform Core Customer Rankings (Combined Profile) ---")
    print(core_profile)
    
    top_segment = core_profile.iloc[0]
    print(f" IDENTIFIED CORE CUSTOMER PROFILE: {top_segment['Age Group']} {top_segment['Gender']}s")
    print(f"Total Sales Contribution from Core Profile: ${top_segment['Total Purchase Amount']:,}\n")

    
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
    plt.show()

except Exception as e:
    print(f" An error occurred: {e}")
    
# OBJECTIVE 3: Payment Preferences and Product Returns 

import pandas as pd
import matplotlib.pyplot as plt
import zipfile

zip_file_name = "archive (7).zip"

try:
    with zipfile.ZipFile(zip_file_name, 'r') as z:
        file_list = z.namelist()
        csv_files = [f for f in file_list if f.endswith('.csv')]
        target_csv = csv_files[0]
        with z.open(target_csv) as f:
            data = pd.read_csv(f)
            
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
    print("--- 1. Most Used Payment Methods ---")
    print(payment_counts)
    print("\n--- 2. Return Rates by Product Category ---")
    print(category_returns[['Product Category', 'Return Rate (%)']])
    print("\n--- 3. Return Rates by Payment Method ---")
    print(payment_returns[['Payment Method', 'Return Rate (%)']])

   
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Left Chart: Returns by Category
    ax1.bar(category_returns['Product Category'], category_returns['Return Rate (%)'], color='#E74C3C', edgecolor='black')
    ax1.set_title('Return Rates by Product Category (%)')
    ax1.set_xlabel('Product Category')
    ax1.set_ylabel('Return Rate (%)')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Right Chart: Returns by Payment Method
    ax2.bar(payment_returns['Payment Method'], payment_returns['Return Rate (%)'], color='#34495E', edgecolor='black')
    ax2.set_title('Return Rates by Payment Method (%)')
    ax2.set_xlabel('Payment Method')
    ax2.set_ylabel('Return Rate (%)')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f" An error occurred: {e}")


# INTERACTIVE GRAPH 
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Interactive E-Commerce Dashboard")
st.markdown("Explore customer purchase data with interactive charts and filters.")

@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_customer_data_large.csv")

    # Convert Purchase Date if available
    if "Purchase Date" in df.columns:
        df["Purchase Date"] = pd.to_datetime(
            df["Purchase Date"], errors="coerce"
        )

    return df


df = load_data()


st.sidebar.header("Filters")

filtered_df = df.copy()

# Product Category Filter
if "Product Category" in df.columns:
    categories = ["All"] + sorted(df["Product Category"].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox(
        "Product Category",
        categories
    )

    if selected_category != "All":
        filtered_df = filtered_df[
            filtered_df["Product Category"] == selected_category
        ]

# Payment Method Filter
if "Payment Method" in df.columns:
    methods = ["All"] + sorted(df["Payment Method"].dropna().unique().tolist())
    selected_method = st.sidebar.selectbox(
        "Payment Method",
        methods
    )

    if selected_method != "All":
        filtered_df = filtered_df[
            filtered_df["Payment Method"] == selected_method
        ]


st.subheader("Dashboard Summary")

col1, col2, col3 = st.columns(3)

if "Total Purchase Amount" in filtered_df.columns:
    total_sales = filtered_df["Total Purchase Amount"].sum()
    avg_sales = filtered_df["Total Purchase Amount"].mean()
else:
    total_sales = 0
    avg_sales = 0

total_customers = len(filtered_df)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Average Purchase", f"${avg_sales:,.2f}")
col3.metric("Transactions", total_customers)

st.divider()


left, right = st.columns(2)

# Sales by Category
with left:
    if (
        "Product Category" in filtered_df.columns
        and "Total Purchase Amount" in filtered_df.columns
    ):
        category_sales = (
            filtered_df.groupby("Product Category")[
                "Total Purchase Amount"
            ]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            category_sales,
            x="Product Category",
            y="Total Purchase Amount",
            color="Product Category",
            text_auto=".2s",
            title="Sales by Product Category"
        )

        st.plotly_chart(fig, use_container_width=True)

# Payment Method Distribution
with right:
    if "Payment Method" in filtered_df.columns:
        payment = (
            filtered_df.groupby("Payment Method")
            .size()
            .reset_index(name="Count")
        )

        fig = px.pie(
            payment,
            names="Payment Method",
            values="Count",
            hole=0.45,
            title="Payment Method Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

if (
    "Purchase Date" in filtered_df.columns
    and "Total Purchase Amount" in filtered_df.columns
):
    temp = filtered_df.copy()
    temp["Month"] = temp["Purchase Date"].dt.strftime("%Y-%m")

    monthly = (
        temp.groupby("Month")["Total Purchase Amount"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="Month",
        y="Total Purchase Amount",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)


if (
    "Product Price" in filtered_df.columns
    and "Total Purchase Amount" in filtered_df.columns
):
    sample_df = (
        filtered_df.sample(
            min(len(filtered_df), 5000),
            random_state=42
        )
        if len(filtered_df) > 0
        else filtered_df
    )

    hover_cols = [
        c
        for c in ["Customer Name", "Product Category", "Payment Method"]
        if c in sample_df.columns
    ]

    color_col = (
        "Product Category"
        if "Product Category" in sample_df.columns
        else None
    )

    fig = px.scatter(
        sample_df,
        x="Product Price",
        y="Total Purchase Amount",
        color=color_col,
        hover_data=hover_cols,
        title="Product Price vs Total Purchase Amount"
    )

    st.plotly_chart(fig, use_container_width=True)


if "Total Purchase Amount" in filtered_df.columns:
    fig = px.histogram(
        filtered_df,
        x="Total Purchase Amount",
        nbins=30,
        title="Distribution of Purchase Amount"
    )

    st.plotly_chart(fig, use_container_width=True)


st.subheader("Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv",
)