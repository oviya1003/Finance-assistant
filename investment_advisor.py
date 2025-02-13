import pandas as pd

# Load dataset (you can customize this to load a dataset path dynamically)
def load_dataset(file_path):
    dataset = pd.read_excel(file_path)
    
    # Handle missing values if needed
    dataset['returns_3yr'].fillna(dataset['returns_3yr'].mean(), inplace=True)
    dataset['PE_ratio'].fillna(dataset['PE_ratio'].mean(), inplace=True)
    dataset['occupation'].fillna('Unknown', inplace=True)
    
    return dataset

# Function to get investment suggestions based on risk tolerance
def get_investment_suggestions(risk_tolerance):
    investment_suggestions = {
        "Low": """
        - Fixed Deposits (FDs): Safe with guaranteed returns.
        - Government Bonds: Lower risk with steady returns.
        - Public Provident Fund (PPF): Long-term savings with tax benefits.
        - Savings Accounts: Low return, but liquid and safe.
        """,
        "Medium": """
        - Balanced Mutual Funds: Mix of equity and debt for moderate risk.
        - Real Estate: Invest in property for steady growth.
        - Corporate Bonds: Moderate risk with better returns than government bonds.
        - Index Funds: Diversified equity fund for medium-risk tolerance.
        """,
        "High": """
        - Stocks (Equities): High risk but potential for high returns.
        - Equity Mutual Funds: Invest in high-growth sectors for higher returns.
        - Cryptocurrencies: Highly volatile, suitable for aggressive investors.
        - Venture Capital: Invest in start-ups or private equity for high risk/reward.
        """
    }
    
    return investment_suggestions.get(risk_tolerance, "Invalid risk tolerance.")

# Function to process financial data and make investment recommendations
def process_financial_data(dataset, income, expenditure, savings, risk_tolerance):
    # Calculate the financial overview and display chart (in app.py, this will be used directly for plotting)
    # Example: Calculate savings rate
    savings_rate = (savings / income) * 100 if income else 0
    
    # Filter dataset based on risk tolerance
    filtered_data = dataset[dataset["risk_level"] == risk_tolerance].copy()
    
    # Calculate investment growth based on risk tolerance
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
    
    return savings_rate, yearly_data, investment_suggestions.get(risk_tolerance)

# If you need to return a full investment growth prediction, return it here
def get_investment_growth(filtered_data, risk_tolerance):
    if risk_tolerance == "Low":
        returns_column = "returns_1yr"
    elif risk_tolerance == "Medium":
        returns_column = "returns_3yr"
    else:  # High risk
        returns_column = "returns_5yr"
    
    # Calculate the investment growth over time
    yearly_data = filtered_data.groupby('Year').agg({returns_column: 'mean'}).reset_index()
    yearly_data['cumulative_return'] = (1 + yearly_data[returns_column] / 100).cumprod() - 1
    
    return yearly_data
