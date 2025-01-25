import sqlite3
import pandas as pd
from pathlib import Path

def get_area_options():
    """获取所有区域选项"""
    db_path = Path(__file__).parent.parent.parent / "data" / "paralympics.db"
    connection = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM paralympics_data", connection)  # 从数据库读取数据
    # 其余代码保持不变 