import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pandas as pd
import numpy as np
from src.building_blocks.data.smart_data_profiler import SmartDataProfiler
import asyncio

async def test_categorical():
    df = pd.DataFrame({
        'category': ['Type A', 'Type B', 'Type A', 'Type C'],
    })
    
    profiler = SmartDataProfiler()
    
    # Check the unique ratio
    unique_ratio = df['category'].nunique() / len(df['category'])
    print(f"Unique ratio: {unique_ratio}")
    print(f"0.05 threshold: {unique_ratio < 0.05}")
    
    data = {'dataframe': df}
    config = {'enable_learning': False, 'pattern_threshold': 0.6}
    
    result = await profiler.execute(data, config)
    
    pattern = result['data']['patterns']['category']
    print(f"Is categorical: {pattern['is_categorical']}")

asyncio.run(test_categorical())