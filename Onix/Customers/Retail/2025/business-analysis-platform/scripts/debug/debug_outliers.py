import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pandas as pd
import numpy as np
from src.building_blocks.data.smart_data_profiler import SmartDataProfiler
import asyncio

async def test_outlier_detection():
    np.random.seed(42)  # For reproducibility
    
    no_outliers = np.random.normal(50, 5, size=100)
    
    df = pd.DataFrame({
        'no_outliers': no_outliers
    })
    
    profiler = SmartDataProfiler()
    
    data = {'dataframe': df}
    config = {'enable_learning': False}
    
    result = await profiler.execute(data, config)
    
    profile = result['data']['profile']['no_outliers']
    
    print(f"Mean: {profile['mean']}")
    print(f"Std dev: {profile['std_dev']}")
    print(f"Q1: {profile['q1']}")  
    print(f"Q3: {profile['q3']}")
    print(f"IQR: {profile['q3'] - profile['q1']}")
    
    iqr = profile['q3'] - profile['q1']
    lower_bound = profile['q1'] - 1.5 * iqr
    upper_bound = profile['q3'] + 1.5 * iqr
    
    print(f"Lower bound: {lower_bound}")
    print(f"Upper bound: {upper_bound}")
    
    # Count outliers
    outliers = no_outliers[(no_outliers < lower_bound) | (no_outliers > upper_bound)]
    print(f"Number of outliers: {len(outliers)}")
    print(f"Outlier values: {outliers}")
    
    print(f"Detected outliers: {profile['outliers']['count']}")

asyncio.run(test_outlier_detection())