import numpy as np
import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = pd.read_json('data.json')

    # 扁平化嵌套的 JSON 数据
    df_normalized = pd.json_normalize(df['users'])

    # 使用 numpy 统计每个国家的用户数量
    country_counts = np.unique(df_normalized['address.country'], return_counts=True)

    print(country_counts)
