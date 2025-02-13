import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from alpha_vantage.timeseries import TimeSeries

# Set the background color and font color for all text, including input box labels and dropdowns
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #ADD8E6, #D3D3D3, #FFFFFF, #4682B4);
    }
    .stMarkdown, .stText, .stSubheader, .stHeader, .stWrite, .stSelectbox, .stTextArea, .stButton, .stRadio, .stSlider, .stLabel, .stInput input {
        color: black;
    }
    .stInput input, .stTextArea textarea {
        color: black; /* Black text color inside input and text area */
    }
    .stLabel {
        color: black; /* Black color for input box and dropdown labels */
    }
    /* Style for selectboxes (dropdowns) */
    .stSelectbox select {
        background: linear-gradient(to bottom, #ADD8E6, #D3D3D3, #FFFFFF, #4682B4) !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load dataset (you can customize this to load a dataset path dynamically)
@st.cache_data
def load_dataset(file_path):
    try:
        dataset = pd.read_excel(file_path)
    except FileNotFoundError:
        raise ValueError(f"File not found at {file_path}. Please check the path.")
    except Exception as e:
        raise ValueError(f"Error loading dataset: {e}")
    
    # Instead of inplace=True, assign the result back to the column
    dataset['returns_3yr'] = dataset['returns_3yr'].fillna(dataset['returns_3yr'].mean())
    dataset['PE_ratio'] = dataset['PE_ratio'].fillna(dataset['PE_ratio'].mean())
    dataset['occupation'] = dataset['occupation'].fillna('Unknown')

    
    # Ensure Year column exists
    if 'Year' not in dataset.columns:
        dataset['Year'] = pd.to_datetime(dataset['Date']).dt.year  # Create Year from Date if missing
    
    return dataset

# Load the dataset
dataset = load_dataset(r"C:\\Users\\Sheid_heda\\Desktop\\Oviya\\Datasets\\FINAL_DATASET.xlsx")

# Title and description
st.markdown('<h1 style="color:black;">Personal Investment Advice using AI</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="color:black;">Welcome to the Personal Investment Advisor. Please provide your details below.</h3>', unsafe_allow_html=True)

# User inputs for financial data
st.markdown('<h5 style="color:black;">Enter your monthly income</h5>', unsafe_allow_html=True)
income = st.text_input("")
st.markdown('<h5 style="color:black;">Enter your monthly expenditure</h5>', unsafe_allow_html=True)
expenditure = st.text_input("", key="expenditure_input")
st.markdown('<h5 style="color:black;">Enter your monthly savings</h5>', unsafe_allow_html=True)
savings = st.text_input("", key="savings_input")


# Convert to float for calculation (if needed)
income = float(income) if income else 0
expenditure = float(expenditure) if expenditure else 0
savings = float(savings) if savings else 0

# Display financial overview chart: Income vs Expenditure vs Savings
st.markdown('<h3 style="color:black;">Income vs Expenditure vs Savings</h3>', unsafe_allow_html=True)
def plot_income_expenditure_savings(income, expenditure, savings):
    data = {"Category": ["Income", "Expenditure", "Savings"],
            "Amount": [income, expenditure, savings]}
    df = pd.DataFrame(data)
    
    # Create a bar plot using Plotly for interactive tooltips
    fig = px.bar(df, x="Category", y="Amount", color="Category", 
                 labels={"Amount": "Amount", "Category": "Category"},
                 title="Income vs Expenditure vs Savings")
    st.plotly_chart(fig)

plot_income_expenditure_savings(income, expenditure, savings)

# Change the color of the "Select your Risk Tolerance Level" label to black
st.markdown('<h3 style="color:black;">Select Risk Tolerance Level</h3>', unsafe_allow_html=True)

# Display the selectbox with the correct label
risk_tolerance = st.selectbox("", ["Low", "Medium", "High"])

# Investment suggestions based on risk tolerance
investment_suggestions = {
    "Low": """
    - Fixed Deposits (FDs): Safe with guaranteed returns.
    - Sovereign Gold Bonds (SGBs):  Safe and tangible, but includes storage costs and risks like theft.
    - Government Bonds: Lower risk with steady returns.
    - Public Provident Fund (PPF): Long-term savings with tax benefits.
    - Savings Accounts: Low return, but liquid and safe.
    """,
    "Medium": """
    - Balanced Mutual Funds: Mix of equity and debt for moderate risk.
    - Gold Mutual Funds: Subject to gold price volatility and fund management strategies.
    - Real Estate: Invest in property for steady growth.
    - Corporate Bonds: Moderate risk with better returns than government bonds.
    - Index Funds: Diversified equity fund for medium-risk tolerance.
    """,
    "High": """
    - Stocks (Equities): High risk but potential for high returns.
    - Gold Mining Stocks:  Risk depends on company performance and gold prices.
    - Equity Mutual Funds: Invest in high-growth sectors for higher returns.
    - Cryptocurrencies: Highly volatile, suitable for aggressive investors.
    - Venture Capital: Invest in start-ups or private equity for high risk/reward.
    """
}

# Display investment suggestions based on selected risk tolerance
st.markdown('<h3 style="color:black;">Investment Suggestions Based on Your Risk Tolerancel</h3>', unsafe_allow_html=True)

st.write(f"Based on your selected risk tolerance level ({risk_tolerance}), we suggest the following investment options:")
st.write(investment_suggestions[risk_tolerance])

# Filter data based on selected risk tolerance level
filtered_data = dataset[dataset["risk_level"] == risk_tolerance].copy()

# Extract Year from Date
filtered_data['Year'] = pd.to_datetime(filtered_data['Date']).dt.year

# Investment Growth based on risk tolerance
def plot_investment_growth(filtered_data, risk_tolerance):
    # Filter data based on risk tolerance (if not done already)
    if risk_tolerance == "Low":
        returns_column = "returns_1yr"
    elif risk_tolerance == "Medium":
        returns_column = "returns_3yr"
    else:  # High risk
        returns_column = "returns_5yr"
    
    # Group by Year and calculate the mean returns
    yearly_data = filtered_data.groupby('Year').agg({
        returns_column: 'mean'
    }).reset_index()
    
    # Calculate the cumulative return for the selected risk level
    yearly_data['cumulative_return'] = (1 + yearly_data[returns_column] / 100).cumprod() - 1
    
    # Create a plot with tooltips using Plotly
    fig = px.line(yearly_data, x='Year', y='cumulative_return', 
                  title=f'Investment Growth Based on Risk Tolerance: {risk_tolerance}',
                  labels={"Year": "Year", "cumulative_return": "Cumulative Investment Growth (%)"})
    fig.update_traces(mode='lines+markers', hoverinfo='x+y')  # Show hover info on points
    st.plotly_chart(fig)

# Ensure filtered data is passed to the function when plotting
if filtered_data.empty:
    st.warning(f"No data available for the selected Risk Tolerance Level: {risk_tolerance}. Please check your dataset.")
else:
    plot_investment_growth(filtered_data, risk_tolerance)

# Explanation of the investment growth graph (after displaying the graph)
st.markdown('<h3 style="color:black;">What Does This Graph represent?</h3>', unsafe_allow_html=True)

st.write(""" 
The graph above represents the *cumulative investment growth* based on your selected *Risk Tolerance* level. Here's how to interpret it:

- *X-axis (Year)*: Represents the time period over which the investment growth is tracked.
- *Y-axis (Cumulative Investment Growth in %)*: Represents the cumulative return on investment as a percentage. This shows how your investment would have grown over time if you had followed a strategy corresponding to your risk tolerance.
- *Blue Line*: Shows the progression of your investment growth over time. The steeper the slope, the higher the growth.

For example:
- If you're in a *low-risk* strategy, your investment growth will likely be steadier and less volatile.
- In contrast, a *high-risk* strategy will show more fluctuations and the potential for higher growth (or loss). 

By analyzing this graph, you can visualize the effect of your chosen investment strategy over time.
""")

# Expense Ratio vs Returns Analysis
st.markdown('<h3 style="color:black;">Expense Ratio VS Returns</h3>', unsafe_allow_html=True)
st.markdown('<p style="color:black; font-size:16px;">Select the Return Period:</p>', unsafe_allow_html=True)

return_period = st.selectbox("", ["1 Year", "3 Year", "5 Year"])

# Add a styled label for the chart type selection
st.markdown('<p style="color:black; font-size:16px;">Select the chart type for Expense Ratio vs Returns:</p>', unsafe_allow_html=True)

chart_type = st.selectbox("", ["Bar Chart", "Scatter Plot"])

def plot_expense_ratio_vs_returns(return_period):
    if return_period == "1 Year":
        returns_column = "returns_1yr"
    elif return_period == "3 Year":
        returns_column = "returns_3yr"
    else:
        returns_column = "returns_5yr"

    if chart_type == "Bar Chart":
        # Use Plotly bar chart for interactivity
        fig = px.bar(dataset, x="expense_ratio", y=returns_column,
                     labels={"expense_ratio": "Expense Ratio", returns_column: f"Returns ({return_period})"},
                     title=f"Expense Ratio vs {return_period} Returns")
        st.plotly_chart(fig)
    elif chart_type == "Scatter Plot":
        # Use Plotly scatter plot for interactivity
        fig = px.scatter(dataset, x="expense_ratio", y=returns_column,
                         labels={"expense_ratio": "Expense Ratio", returns_column: f"Returns ({return_period})"},
                         title=f"Expense Ratio vs {return_period} Returns")
        st.plotly_chart(fig)

plot_expense_ratio_vs_returns(return_period)


# Alpha Vantage stock data integration
st.markdown('<h3 style="color:black;">Stock Data From ALpha Vantage</h3>', unsafe_allow_html=True)

# Change the color of the "Enter stock symbol" label to black
st.markdown('<h6 style="color:black;">Enter stock symbol (e.g., AAPL, MSFT, TSLA)</h6>', unsafe_allow_html=True)

# Display the text input for the stock symbol with a unique key
stock_symbol = st.text_input("", key="stock_symbol_input")


def get_stock_data(stock_symbol):
    api_key = 'your_alpha_vantage_api_key'  # Replace with your Alpha Vantage API key
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if 'Time Series (Daily)' in data:
        time_series = data['Time Series (Daily)']
        dates = list(time_series.keys())
        closing_prices = [float(time_series[date]['4. close']) for date in dates]
        return pd.DataFrame({'Date': dates, 'Close': closing_prices})
    else:
        return None

if stock_symbol:
    stock_data = get_stock_data(stock_symbol)
    if stock_data is not None:
        st.write(f"Stock data for {stock_symbol}:")
        st.dataframe(stock_data)
        # Plot stock data
        fig = px.line(stock_data, x='Date', y='Close', title=f'{stock_symbol} Stock Price Over Time')
        st.plotly_chart(fig)
    else:
        st.warning("Could not retrieve stock data. Please check the symbol or try again later.")
        
# Frequently Asked Questions (FAQs) Section
st.markdown('<h3 style="color:black;">Frequently Asked Questions (FAQs)</h3>', unsafe_allow_html=True)

faqs = {
    "What is a mutual fund?": "A mutual fund is a pool of funds collected from investors to invest in securities like stocks and bonds.",
    "What are safe investment options?": "Safe options include Fixed Deposits, Government Bonds, and PPF.",
    "How to invest in high-risk options?": "High-risk options include Stocks, Cryptocurrencies, and Venture Capital investments.",
    "How can I increase my savings?": "You can increase savings by reducing unnecessary expenses, budgeting, and automating savings.",
    "What is SIP?": "A Systematic Investment Plan (SIP) allows you to invest a fixed amount regularly in a mutual fund scheme.",
    "What is risk tolerance?": "Risk tolerance is the level of risk you are willing to take in your investments, based on your financial goals and stability.",
    "How do I diversify my portfolio?": "Diversification can be achieved by investing in a mix of assets like stocks, bonds, and real estate to reduce risk.",
    "What are the tax benefits of investing?": "Investments like PPF, ELSS, and NPS provide tax benefits under Section 80C of the Income Tax Act.",
    "What is equity?": "Equity refers to ownership in a company, usually through stocks or shares. Investors in equity participate in the company’s growth and profits.",
    "How to choose the right loan?": "When choosing a loan, consider factors like the interest rate, loan term, repayment schedule, and your ability to repay.",
    "How to create a financial plan?": "A financial plan involves setting goals, assessing your current financial situation, and creating strategies for saving, investing, and managing debt.",
    "What is liquidity?": "Liquidity refers to how easily an asset can be converted into cash without affecting its price. Cash is the most liquid asset.",
    "How do I calculate returns on investment (ROI)?": "ROI is calculated as: (Current Value of Investment - Initial Investment) / Initial Investment * 100.",
}

# Use multiselect to display questions
st.markdown('<h5 style="color:black;">Select a question to view the answer:</h5>', unsafe_allow_html=True)

# The selectbox with black text for the placeholder
faq_question = st.selectbox(
    "", 
    ["-- Select a question --"] + list(faqs.keys())
)

# Only display the answer if a question is selected
if faq_question != "-- Select a question --":
    st.write(f"Answer: {faqs[faq_question]}")



# User feedback for the investment advice system
st.markdown('<h3 style="color:black;">User feedback</h3>', unsafe_allow_html=True)

# Change the color of the "Provide your feedback for improvement:" label to black
st.markdown('<h4 style="color:black;">Provide your feedback for improvement:</h4>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .stTextArea textarea {
        color: #f0f0f5;
        background-color: black;
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
    }

    .stButton button {
        background-color: #4CAF50; /* Green background */
        color: white; /* White text */
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        border: none;
    }
      </style>
    """,
    unsafe_allow_html=True
)

feedback = st.text_area("")

if st.button("Submit Feedback"):
    if feedback:
        st.write("Thank you for your valuable feedback!")
    else:
        st.warning("Please provide your feedback before submitting.")
