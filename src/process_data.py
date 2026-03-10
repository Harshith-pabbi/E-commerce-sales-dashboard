import pandas as pd
import os

def load_data(filepath='data/raw/transactions.csv'):
    """Loads raw data from CSV."""
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    """Cleans and preprocesses the transaction data."""
    print("Initial shape:", df.shape)
    
    # 1. Handle missing values (if any)
    # Our mock data shouldn't have any, but good practice
    df.dropna(subset=['transaction_id', 'date', 'product_id'], inplace=True)
    
    # 2. Correct Data Types
    df['date'] = pd.to_datetime(df['date'])
    
    # 3. Handle outliers or incorrect values
    # Filtering out any extremely high quantities or negative prices that might exist
    df = df[(df['quantity'] > 0) & (df['unit_price'] > 0)]
    df = df[df['discount'] <= 1.0] # Discount shouldn't be more than 100%
    
    # 4. Feature Engineering
    df['year_month'] = df['date'].dt.to_period('M').astype(str)
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Ensure calculated columns are mathematically correct to avoid raw data issues
    df['calculated_revenue'] = round(df['quantity'] * df['unit_price'] * (1 - df['discount']), 2)
    # Could check if calculated_revenue matches revenue, but we'll trust revenue column for now
    
    print("Cleaned shape:", df.shape)
    return df

def save_processed_data(df, output_path='data/processed/cleaned_transactions.csv'):
    """Saves cleaned data to CSV."""
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

def main():
    raw_df = load_data()
    cleaned_df = clean_data(raw_df)
    save_processed_data(cleaned_df)

if __name__ == '__main__':
    main()
