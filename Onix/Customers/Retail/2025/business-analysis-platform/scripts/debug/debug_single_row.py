import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pandas as pd
from datetime import datetime
from src.building_blocks.data.smart_data_profiler import SmartDataProfiler
import asyncio

async def test_single_row():
    df = pd.DataFrame({'a': [1], 'b': ['test'], 'c': [datetime.now()]})
    
    profiler = SmartDataProfiler()
    
    data = {'dataframe': df}
    config = {'enable_learning': False}
    
    result = await profiler.execute(data, config)
    
    print("Profile for column 'a':")
    print(result['data']['profile']['a'])

asyncio.run(test_single_row())