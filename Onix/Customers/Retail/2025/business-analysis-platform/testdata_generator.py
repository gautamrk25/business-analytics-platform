import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Create date range for 2 years of daily data
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Initialize the dataset
data = []

for date in date_range:
    # Seasonal factors
    month = date.month
    day_of_year = date.timetuple().tm_yday
    seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * day_of_year / 365)
    
    # Holiday boost (Christmas, Black Friday, etc.)
    holiday_boost = 1.0
    if month == 12 or (month == 11 and date.day >= 24):  # Holiday season
        holiday_boost = 1.5
    elif month == 7:  # Summer boost
        holiday_boost = 1.2
    
    # Weekend effect
    weekend_factor = 1.1 if date.weekday() >= 5 else 1.0
    
    # Generate data for each region
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    for region in regions:
        regional_factor = {
            'North': 1.2, 'South': 0.9, 'East': 1.1, 
            'West': 1.0, 'Central': 0.8
        }[region]
        
        # Base metrics with trends and seasonality
        base_sales = 10000 * regional_factor * seasonal_factor * holiday_boost * weekend_factor
        base_sales *= (1 + 0.02 * (date - start_date).days / 365)  # 2% annual growth
        
        # Add some noise
        daily_sales = max(0, base_sales * np.random.normal(1, 0.15))
        
        # Product categories (with different seasonality)
        categories = {
            'Electronics': 0.3,
            'Clothing': 0.25,
            'Home & Garden': 0.2,
            'Sports': 0.15,
            'Books': 0.1
        }
        
        for category, weight in categories.items():
            category_seasonal = seasonal_factor
            if category == 'Clothing' and month in [11, 12, 3, 4]:
                category_seasonal *= 1.3
            elif category == 'Home & Garden' and month in [4, 5, 6]:
                category_seasonal *= 1.4
            elif category == 'Sports' and month in [6, 7, 8]:
                category_seasonal *= 1.2
            
            category_sales = daily_sales * weight * category_seasonal * np.random.normal(1, 0.1)
            
            # Related metrics
            avg_order_value = 85 + np.random.normal(0, 15)
            orders = max(1, int(category_sales / avg_order_value))
            customers = max(1, int(orders * np.random.uniform(0.7, 0.95)))
            
            # Marketing spend (with lag effect on sales)
            marketing_spend = category_sales * np.random.uniform(0.08, 0.15)
            
            # Inventory metrics
            units_sold = max(1, int(category_sales / (avg_order_value * 0.7)))
            inventory_level = max(0, 1000 + np.random.normal(0, 200) - units_sold * np.random.uniform(0.8, 1.2))
            
            # Customer metrics
            new_customers = max(0, int(customers * np.random.uniform(0.1, 0.3)))
            customer_satisfaction = max(1, min(5, 4.2 + np.random.normal(0, 0.3)))
            
            # Website metrics (for ecommerce)
            website_visits = max(1, int(customers * np.random.uniform(8, 15)))
            conversion_rate = max(0.01, min(0.15, customers / website_visits))
            cart_abandonment = max(0.3, min(0.8, 0.6 + np.random.normal(0, 0.1)))
            
            # External factors
            temperature = 70 + 20 * np.sin(2 * np.pi * day_of_year / 365) + np.random.normal(0, 5)
            competitor_price_index = 100 + np.random.normal(0, 5)
            
            # Add some missing values occasionally (2% chance)
            if random.random() < 0.02:
                inventory_level = None
            if random.random() < 0.01:
                customer_satisfaction = None
            
            # Add more extreme scenarios
            if date.month in [3, 4] and date.year == 2023:  # Recession simulation
                base_sales *= 0.7  # 30% drop
            
            # Add supply chain disruptions
            if date.month == 10 and date.year == 2022:  # Supply shortage
                if inventory_level is not None:
                    inventory_level *= 0.3
            
            # Add more data quality issues
            if random.random() < 0.005:  # 0.5% completely anomalous data
                daily_sales *= random.uniform(0.1, 5.0)
            
            # Add competitor actions
            competitor_promotion = random.random() < 0.1  # 10% chance
            if competitor_promotion:
                daily_sales *= 0.85  # 15% sales drop due to competitor
            
            # Add product lifecycle stages
            product_age_days = (date - start_date).days
            if category == 'Electronics':
                lifecycle_factor = 1 + 0.1 * np.sin(2 * np.pi * product_age_days / 180)  # 6-month cycles
                category_sales *= lifecycle_factor
            
            data.append({
                'date': date,
                'region': region,
                'product_category': category,
                'daily_sales': round(category_sales, 2),
                'orders': orders,
                'customers': customers,
                'new_customers': new_customers,
                'avg_order_value': round(avg_order_value, 2),
                'units_sold': units_sold,
                'inventory_level': inventory_level,
                'marketing_spend': round(marketing_spend, 2),
                'website_visits': website_visits,
                'conversion_rate': round(conversion_rate, 4),
                'cart_abandonment_rate': round(cart_abandonment, 4),
                'customer_satisfaction': customer_satisfaction,
                'temperature': round(temperature, 1),
                'competitor_price_index': round(competitor_price_index, 2),
                'day_of_week': date.strftime('%A'),
                'month': month,
                'quarter': f'Q{(month-1)//3 + 1}',
                'is_weekend': date.weekday() >= 5,
                'is_holiday_season': month == 12 or (month == 11 and date.day >= 24)
            })

# Create DataFrame and save to CSV
df = pd.DataFrame(data)

# Convert date column to string for Streamlit compatibility
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

# Add some derived metrics
df['revenue_per_customer'] = df['daily_sales'] / df['customers']
df['marketing_roi'] = (df['daily_sales'] - df['marketing_spend']) / df['marketing_spend']
df['inventory_turnover'] = df['units_sold'] / (df['inventory_level'].fillna(df['inventory_level'].mean()) + 1)

# Save to CSV
df.to_csv('business_analysis_test_data.csv', index=False)

print("Test CSV file 'business_analysis_test_data.csv' created successfully!")
print(f"Dataset contains {len(df)} rows and {len(df.columns)} columns")
print("\nColumns:", list(df.columns))
print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")
print(f"Regions: {df['region'].unique()}")
print(f"Product categories: {df['product_category'].unique()}")