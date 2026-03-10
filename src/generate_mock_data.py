import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_mock_data(num_records=55000, output_path='data/raw/transactions.csv'):
    np.random.seed(42)
    random.seed(42)
    
    # Categories and Regions
    categories = ['Electronics', 'Home & Kitchen', 'Fashion', 'Books', 'Toys', 'Beauty', 'Sports']
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Australia']
    
    # Products
    products = [f'Product_{i}' for i in range(1, 101)]
    product_categories = {p: random.choice(categories) for p in products}
    product_base_price = {p: round(random.uniform(10.0, 500.0), 2) for p in products}
    
    # Dates
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = (end_date - start_date).days
    
    print(f"Generating {num_records} transaction records...")
    
    data = []
    
    for i in range(num_records):
        # Generate varied dates (simulate some seasonality)
        days_offset = int(np.random.beta(2, 2) * date_range)
        order_date = start_date + timedelta(days=days_offset)
        
        product = random.choice(products)
        category = product_categories[product]
        base_price = product_base_price[product]
        
        # Quantity follows a right-skewed distribution
        quantity = int(np.random.exponential(scale=1.5)) + 1
        if quantity > 10: quantity = 10
        
        # Price fluctuations
        price_multiplier = np.random.normal(1.0, 0.05)
        unit_price = round(base_price * price_multiplier, 2)
        
        # Discounts
        discount = round(random.choice([0.0, 0.0, 0.0, 0.1, 0.15, 0.2]), 2)
        
        total_price = round(quantity * unit_price * (1 - discount), 2)
        revenue = total_price
        
        # Profit margin varies by category
        margin = random.uniform(0.1, 0.4)
        profit = round(revenue * margin, 2)
        
        region = random.choice(regions)
        
        data.append({
            'transaction_id': f"TRX-{random.randint(1000000, 9999999)}-{i}",
            'date': order_date.strftime('%Y-%m-%d'),
            'product_id': product,
            'category': category,
            'region': region,
            'quantity': quantity,
            'unit_price': unit_price,
            'discount': discount,
            'revenue': revenue,
            'profit': profit
        })
        
    df = pd.DataFrame(data)
    
    # Sort by date
    df.sort_values(by='date', inplace=True)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"Successfully generated mock data and saved to {output_path} ({df.shape[0]} rows)")

if __name__ == '__main__':
    generate_mock_data()
