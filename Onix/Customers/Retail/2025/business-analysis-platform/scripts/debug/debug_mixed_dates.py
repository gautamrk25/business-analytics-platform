import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pandas as pd
from datetime import datetime
from src.building_blocks.data.smart_data_profiler import SmartDataProfiler
import asyncio

async def test_mixed_dates():
    df = pd.DataFrame({
        'mixed_dates': [
            '2024-01-01',
            datetime(2024, 1, 2),
            pd.Timestamp('2024-01-03'),
            'not a date',
            None
        ]
    })
    
    profiler = SmartDataProfiler()
    
    # Check types
    types = set(type(x) for x in df['mixed_dates'] if x is not None)
    print(f"Types in mixed_dates: {types}")
    
    # Check dropna
    non_null = df['mixed_dates'].dropna()
    types_non_null = set(type(x) for x in non_null)
    print(f"Types in non-null: {types_non_null}")
    
    # Check conversion
    try:
        parsed = pd.to_datetime(non_null, errors='coerce', format='mixed')
        valid_dates = parsed.notna().sum()
        print(f"Valid dates: {valid_dates} out of {len(non_null)}")
        print(f"Ratio: {valid_dates / len(non_null)}")
    except Exception as e:
        print(f"Error parsing: {e}")
    
    data = {'dataframe': df}
    config = {'enable_learning': False}
    
    result = await profiler.execute(data, config)
    
    profile = result['data']['profile']['mixed_dates']
    print(f"Detected dtype: {profile['dtype']}")

asyncio.run(test_mixed_dates())