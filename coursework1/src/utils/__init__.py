import pandas as pd
from pathlib import Path

def load_data():
    """加载和预处理数据"""
    try:
        current_dir = Path(__file__).parent.parent.parent
        data_path = current_dir / "data" / "newdata.csv"
        
        # 读取 CSV 文件
        df = pd.read_csv(data_path)
        
        # 数据类型转换
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df['Recycling_Rates'] = pd.to_numeric(df['Recycling_Rates'], errors='coerce')
        
        # 确保所有必要的列存在
        required_columns = ['Year', 'Area', 'Recycling_Rates', 'London_Status']
        if not all(col in df.columns for col in required_columns):
            missing_cols = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # 数据验证
        print(f"Loaded data shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")
        print(f"Number of unique areas: {df['Area'].nunique()}")
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
