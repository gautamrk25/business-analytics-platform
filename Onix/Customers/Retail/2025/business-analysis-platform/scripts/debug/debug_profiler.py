import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pandas as pd
import numpy as np
from src.building_blocks.data.smart_data_profiler import SmartDataProfiler
import asyncio

async def test_patterns():
    profiler = SmartDataProfiler()
    
    df = pd.DataFrame({
        'email': ['user1@example.com', 'user2@example.com', 'invalid', None],
        'phone': ['+1-555-123-4567', '+1-555-987-6543', '555-111-2222', 'invalid'],
        'date_string': ['2024-01-01', '2024-02-01', '2024/03/01', 'not a date'],
        'id_column': ['ID001', 'ID002', 'ID003', 'ID004'],
        'category': ['Type A', 'Type B', 'Type A', 'Type C'],
        'continuous': np.random.normal(100, 15, size=4)
    })
    
    data = {'dataframe': df}
    config = {'enable_learning': False, 'pattern_threshold': 0.6}
    
    result = await profiler.execute(data, config)
    
    print("Patterns:")
    for col, pat in result['data']['patterns'].items():
        print(f"{col}: {pat}")
    
    print("\nProfile dtypes:")
    for col, prof in result['data']['profile'].items():
        print(f"{col}: dtype={prof.get('dtype')}")

asyncio.run(test_patterns())