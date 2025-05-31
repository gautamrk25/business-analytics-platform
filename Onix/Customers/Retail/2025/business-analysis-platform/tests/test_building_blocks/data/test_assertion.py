import pandas as pd
import numpy as np
from src.building_blocks.data.smart_data_profiler import SmartDataProfiler
import asyncio

async def test_assertions():
    profiler = SmartDataProfiler()
    
    df = pd.DataFrame({
        'email': ['user1@example.com', 'user2@example.com', 'invalid', None],
    })
    
    data = {'dataframe': df}
    config = {'enable_learning': False, 'pattern_threshold': 0.6}
    
    result = await profiler.execute(data, config)
    patterns = result['data']['patterns']
    
    print(f"Type of patterns['email']['is_email']: {type(patterns['email']['is_email'])}")
    print(f"Value: {patterns['email']['is_email']}")
    print(f"Simple equality: {patterns['email']['is_email'] == True}")
    print(f"Identity check: {patterns['email']['is_email'] is True}")
    
    # Try with various assertions
    if patterns['email']['is_email'] == True:
        print("Equality check passes")
    
    try:
        assert patterns['email']['is_email'] is True
        print("Identity assertion passes")
    except AssertionError as e:
        print(f"Identity assertion fails: {e}")
        print(f"Actual value: {patterns['email']['is_email']!r}")
        print(f"Type: {type(patterns['email']['is_email'])}")

asyncio.run(test_assertions())