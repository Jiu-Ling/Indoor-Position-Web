import pandas as pd
from io import BytesIO


def create_excel(df):
    # 写入到内存中并返回
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()
    return output
