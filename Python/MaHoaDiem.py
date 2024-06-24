#%%
import pandas as pd

# Đọc dữ liệu từ file Excel

df = pd.read_excel('../BangDiem/SinhVienNam2_clean.xlsx')

def convert_number_to_char(data:pd.DataFrame):
    # Thay đổi điểm trong khoảng từ 1 đến 10 thành điểm hệ chữ
    df = data.copy()
    for index, row in df.iterrows():
        for col in df.columns:
            cell_value = row[col]
            if isinstance(cell_value, (int, float)) and 1 <= cell_value < 4:
                df.at[index, col] = 'F'
            if isinstance(cell_value, (int, float)) and 4 <= cell_value < 5.5:
                df.at[index, col] = 'D'
            if isinstance(cell_value, (int, float)) and  5.5<= cell_value < 7:
                df.at[index, col] = 'C'
            if isinstance(cell_value, (int, float)) and 7 <= cell_value < 8.5:
                df.at[index, col] = 'B'
            if isinstance(cell_value, (int, float)) and 8.5 <= cell_value <= 10:
                df.at[index, col] = 'A'
    return df
df = convert_number_to_char(df)
# Lưu dữ liệu vào file Excel mới
df.to_excel('../BangDiem/SinhVienNam2_HeChu_clean.xlsx', index=False)