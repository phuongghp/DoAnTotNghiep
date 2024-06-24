# %%
# %pip install xlrd
# %pip install openpyxl


# %%
import pandas as pd
from unidecode import unidecode
import os
import csv
import json


# %%
files_K60_61 = {
    'CTDT':'../K60_61/KhungChuongTrinh-CNTT_K60_61.xlsx',
    'TN': '../K60_61/DaTNK60.xls', 
    'TH':'../K60_61/DiemTongHopToanKhoaK60.xls'}

files_K59 = {
    'CTDT':'../K59/KhungChuongTrinh-CNTT_K59.xlsx',
    'TN': '../K59/DaTNK59.xls', 
    'TH':'../K59/DiemTongHopToanKhoaK59.xls'}


hoc_phan_tuong_duong = {
    'Triết học Mác- Lênin':'Triết học Mác- Lê Nin F1',
    'An toàn bảo mật thông tin':'An toàn và bảo mật thông tin',
    'Chuyên đề về công nghệ phần mềm':'Chuyên đề công nghệ phần mềm',
    'Những nguyên lý cơ bản của chủ nghĩa MLN F1':'Những nguyên lý cơ bản của chủ nghĩa Mác- Lê Nin F1',
    'Những nguyên lý cơ bản của chủ nghĩa MLN F2':'Những nguyên lý cơ bản của chủ nghĩa Mác- Lê Nin F2',
    'Đường lối cách mạng của Đảng CSVN':'Đường lối cách mạng Đảng Cộng sản Việt Nam',
}

hoc_ky_loai_bo = [7,8]
# %%
# def convert_excel_to_csv(files):
#     folder = "./csv/"
#     current_dir = os.getcwd()
#     csv_dir = os.path.join(current_dir, "csv")
#     if not os.path.isdir(csv_dir):
#         # Tạo thư mục "csv"
#         os.makedirs(csv_dir)

#     for file in files:
#         df = pd.read_excel(file)
#         df.to_csv(folder + file+".csv")

# %%
def convert_personal_points(personal_points):# lay dtb va drl cua sv da tot nghiep
    for i in range(personal_points.shape[0]):
        row = personal_points.iloc[i]
        if "STT" in row.values:#các thao tác trích xuất điểm nếu có stt
            mask = personal_points.index > i+1
            data_points = personal_points[mask]
            columns = row.tolist()
            columns[columns.index("Bằng chữ") - 1] = "Lần 2"
            columns = [str(_) for _ in columns]
            data_points = data_points.set_axis(columns, axis='columns')
            break
            
    columns = [i for i in columns if i != 'nan']

    data_points = data_points.loc[:, columns]
    data_points = data_points.fillna(-1)
    data_points.iloc[42]

    for i in range(data_points.shape[0]):
        if type(data_points.iloc[i][-1]) == type(-1):
            if sum(data_points.iloc[i].values) == -len(data_points.columns):
                break_line = i
                dtb = data_points.iloc[break_line+1]
                drl = data_points.iloc[break_line+2]
                data_points = data_points.iloc[:break_line]
                break
    print(data_points)
    print(dtb.values)
    print(drl.values)
    data_points = data_points.reset_index(drop=True)
    data_points.to_csv('../TestCv/diem.csv', index=False)

    return data_points, dtb, drl

# %%
def read_ctdt(path_file):
    global hoc_ky_loai_bo
    ctdt = pd.read_excel(path_file)

    for i in range(ctdt.shape[0]):
        row = ctdt.iloc[i]
        if "TT" in row.values:
            mask = ctdt.index > i+3
            next_columns = ctdt.iloc[i+2].tolist()
            data_ctdt = ctdt[mask]
            columns = row.tolist()
            columns = [str(_) for _ in columns]
            next_columns = [str(_) for _ in next_columns]
            for i in range(len(columns)):
                if next_columns[i] != 'nan':
                    columns[i] = next_columns[i]
            data_ctdt.set_axis(columns, axis='columns')
            break

    data_ctdt = data_ctdt[data_ctdt.iloc[:, 1] != 'Cộng']
    data_ctdt = data_ctdt.iloc[:, :4]
    data_ctdt = data_ctdt.reset_index(drop=True)
    data_ctdt.to_csv("../TestCv/ctdt.csv", index=False)

    dict_ctdt = []
    option = {'hp': '', 'option': False}
    number_option=0
    for row in data_ctdt.values:
        stt, ten_hp, ma_hp, so_tc = [str(value) for value in row]
        tu_chon = 0
        
        if "HỌC KỲ" in ten_hp:
            hk = ten_hp.split()[-1]
            continue
        if "GDT" in ma_hp or "GQP" in ma_hp:
            continue

        if str(ma_hp) == 'nan':
            option = {'hp': ten_hp, 'option': True}
            number_option += 1
            continue
        elif str(stt) != 'nan':
            option = {'hp': '', 'option': False}
        
        if option['option'] == True:
            pos_ = ten_hp.index("-")
            ten_hp = ten_hp[pos_+2:]
            tu_chon = number_option
            if 'chuyên ngành' in option['hp'].lower():
                ten_hp += ' chuyên ngành'
        if int(hk) in hoc_ky_loai_bo:
            continue
        dict_ctdt.append({'ten_hp':ten_hp, 'ma_hp': ma_hp,'tu_chon':tu_chon, 'so_tc': so_tc, 'hoc_ky': hk})
    print(dict_ctdt)
    return dict_ctdt


dict_ctdt_K59 = read_ctdt(files_K59['CTDT'])
dict_ctdt_K60_61 = read_ctdt(files_K60_61['CTDT'])
# %%
def merge_ctdt(dict_ctdt_K60_61:list, dict_ctdt_K59:list):
    result = dict_ctdt_K60_61.copy()
    hp_K60_61 = [_['ten_hp'] for _ in dict_ctdt_K60_61]
    for hoc_phan in dict_ctdt_K59:
        if hoc_phan['ten_hp'] not in hp_K60_61:
            for (ind, hp) in enumerate(result):
                if int(hp['hoc_ky']) > int(hoc_phan['hoc_ky']): 
                    result.insert(ind, hoc_phan)
                    break

    return result

dict_ctdt = merge_ctdt(dict_ctdt_K60_61, dict_ctdt_K59)

# %%
def write_csv(dict_data:list[dict], filename = 'data.csv'):
    # Open the file in write mode
    with open(filename, 'w', newline='') as csvfile:
        # Create a csv writer object
        writer = csv.DictWriter(csvfile, fieldnames=dict_data[0].keys())

        # Write the header row (assuming all dictionaries have the same keys)
        writer.writeheader()

        # Write each dictionary as a row in the CSV file
        for data in dict_data:
            writer.writerow(data)

    print(f"Data exported successfully to '{filename}'.")

# write_csv(dict_ctdt)
# %%
list_hp = []
header = []
tc_hp = {}
hk_hp = {}
dict_tu_chon = {}

def map_points(dict_ctdt:list[dict], data_points):
    global list_hp, header, tc_hp, hk_hp, dict_tu_chon
    list_hp = [unidecode(i['ten_hp'].lower().replace(" ", '')) for i in dict_ctdt]
    header = [i['ten_hp'] for i in dict_ctdt]
    tc_hp = {unidecode(i['ten_hp'].lower().replace(" ", '')):i['so_tc'] for i in dict_ctdt}
    hk_hp = {unidecode(i['ten_hp'].lower().replace(" ", '')):i['hoc_ky'] for i in dict_ctdt}

    for i in dict_ctdt:
        number_option = i['tu_chon']
        if int(number_option) != 0:
            option = dict_tu_chon.get(f'{number_option}')
            if option == None:
                option = {}
            option[unidecode(i['ten_hp'].lower().replace(" ", ''))] = i['ten_hp']
            dict_tu_chon[f'{number_option}'] = option

    diem_sv = {}
    for ind_row in range(data_points.shape[0]):
        # print(data_points.iloc[ind_row].values)
        stt, hp, so_tc, lan_1, lan_2, bang_chu = data_points.iloc[ind_row].values

        unidecode_hp_tuong_duong={unidecode(key.lower().replace(" ", '')):unidecode(hoc_phan_tuong_duong[key]).lower().replace(" ", '') for key in hoc_phan_tuong_duong.keys()}

        hp = unidecode(hp.lower()).replace(" ", "")

        if hp not in list_hp:
            if hp in unidecode_hp_tuong_duong.keys():
                hp = unidecode_hp_tuong_duong[hp]
            

            if hp not in list_hp:
                print(f'_{hp}_')
                continue
        
        diem_sv[hp] = f"{lan_1}, {lan_2}".replace(", -1", "").replace("-1 ,", "")

    # print(diem_sv)
    return diem_sv


# %%
def read_diem_tot_nghiep(file_path):
    # Read all sheets into a dictionary
    data = pd.read_excel(file_path, sheet_name=None)

    # Get sheet names from the dictionary keys
    sheet_names = list(data.keys())

    bang_diem = []
    # Print sheet names
    print("Sheet names:", sheet_names)
    for sheet_name in sheet_names:
        personal_points = data[sheet_name]
        mssv = personal_points.iloc[5, 8]
        ngay_sinh = personal_points.iloc[6].values
        # print("MSSV:", personal_points.iloc[5, 8])
        data_points, dtb, drl = convert_personal_points(personal_points)
        # data_points = data_points.iloc[15:]
        diem_ca_nhan = map_points(dict_ctdt, data_points)

        if mssv.lower().count('v') > 0:
            continue

        diem_ca_nhan['mssv'] = f"{mssv}"
        diem_ca_nhan['ngay_sinh'] = f"{ngay_sinh[3]}"
        dtb = str(dtb.values).replace(" -1", "").split(":")

        diem_ca_nhan['tc_tich_luy'] = dtb[1].split()[0]
        diem_ca_nhan['tbc_hoc_tap'] = dtb[2].split()[0].split("/")[0]
        diem_ca_nhan['tbc_tich_luy'] = dtb[3].split()[0].split("/")[0]
        diem_ca_nhan['xep_loai_hoc_tap'] = dtb[4].split()[0][:-1]
        if diem_ca_nhan['xep_loai_hoc_tap'][0] == "X":
            diem_ca_nhan['xep_loai_hoc_tap'] = "Xuất sắc"
        elif diem_ca_nhan['xep_loai_hoc_tap'][0] == "T":
            diem_ca_nhan['xep_loai_hoc_tap'] = "Trung bình"

        diem_ca_nhan['drl'] = str(drl.values).replace(" -1", "").split(":")[1].split()[0]
        bang_diem.append(diem_ca_nhan)
    return bang_diem
    
# %%
# CSV file name
diem_tot_nghiep_K59 = read_diem_tot_nghiep(files_K59['TN'])
diem_tot_nghiep_K60_61 = read_diem_tot_nghiep(files_K60_61['TN'])

bang_diem = [hk_hp] + [tc_hp] + diem_tot_nghiep_K59 + diem_tot_nghiep_K60_61

# %%  
def read_diem_chua_tot_nghiep(path_file):
    data = pd.read_excel(path_file, sheet_name=None)

    # Get sheet names from the dictionary keys
    sheet_names = list(data.keys())

    bang_diem = []
    # Print sheet names
    # print("Sheet names:", sheet_names)
    for sheet_name in sheet_names:
        personal_points = data[sheet_name]
        # print(personal_points)
        columns = personal_points.iloc[5, :]

        index = [i for i in range(1, len(columns.values)) if str(columns.values[i]) != 'nan']

        tc_ = personal_points.iloc[7, :]

        for i in range(9, len(personal_points)):
            diem_ca_nhan = {}
            row = personal_points.iloc[i, :]
            if not row[1]:
                continue
            for ind in index:
                key = columns.values[ind].replace("\n", " ")
                key_map={'masinhvien':'mssv',
                          'hovaten':'', 
                          'antoanbaomatthongtin':'antoanvabaomatthongtin', 
                          'hethongthongtindialy':'hethongtindialy',
                          'chuyendevecongnghephanmem':'chuyendecongnghephanmem',
                          'triethocmac-lenin':'triethocmac-leninf1',
                          'chuyendevehethongthongtin':'chuyendehethongthongtin'}
                key = unidecode(key.lower().replace(" ", ''))
                if key in key_map.keys():
                    key = key_map[key]
                if not key:
                    continue 
                if ind > 1:
                    value = ', '.join(str(x) for x in row[ind:ind+2].values)
                else:
                    value = str(row[ind])
                    
                value = value.lower().replace('nan', '')
                if value.endswith(", "):
                    value = value[:-2]
                diem_ca_nhan[key] = value
            if diem_ca_nhan['mssv'].lower().count('v') > 0:
                continue
            diem_ca_nhan['xep_loai_hoc_tap'] = 'Chưa Xếp Loại'
            bang_diem.append(diem_ca_nhan)
        
    # # Open the file in write mode ('w')
    # with open('data.json', 'w', encoding='utf-8') as outfile:
    #     # Use json.dump to write the list of dictionaries to the file
    #     json.dump(bang_diem, outfile, ensure_ascii=False)

    return bang_diem

# %%
chua_tot_nghiep_K59 = read_diem_chua_tot_nghiep(files_K59['TH'])
chua_tot_nghiep_K60_61 = read_diem_chua_tot_nghiep(files_K60_61['TH'])

chua_tot_nghiep = chua_tot_nghiep_K59 + chua_tot_nghiep_K60_61

# %%
def merge_data(data_tot_nghiep:list[dict], data_chua_tot_nghiep:list[dict]):
    keys = set()
    # for data in [data_tot_nghiep, data_chua_tot_nghiep]:
    for data in [data_tot_nghiep, []]:
        for row in data:
            keys.update(row.keys())
    
    result = []
    for data in [data_tot_nghiep, data_chua_tot_nghiep]:
        for row in data:
            # Tạo một bản sao của row
            row_moi = {}

            # Gán value cho các key chung
            for key in keys:
                row_moi[key] = row.get(key, '')

            for key in ['diemtbclan1','diemtbccaonhat', 'tongsomonconno', 'tongsohoctrinhconno' ]:
                row_moi[key] = row.get(key, '')

            # Thêm bản ghi mới vào result
            result.append(row_moi)
    return result

# %%
#chua_tot_nghiep=[]
bang_diem_tong_hop = merge_data(bang_diem, chua_tot_nghiep)
#bang_diem_tong_hop=bang_diem

# %%
def convert_tuchon(bang_diem_tong_hop):
    global list_hp
    for i in range(len(bang_diem_tong_hop)):
        row = bang_diem_tong_hop[i]
        for key in dict_tu_chon.keys():
            diem = []
            for hoc_phan in dict_tu_chon[key].keys(): 
                value = row.get(hoc_phan, "").split(", ")
                for _ in value:
                    if _ :
                        diem.append(_)
                del bang_diem_tong_hop[i][hoc_phan]
                try:
                    ind_hp = list_hp.index(hoc_phan)

                    if f'Môn tự chọn {key}' not in header:
                        header.insert(ind_hp, f'Môn tự chọn {key}')
                    if f'montuchon{key}' not in list_hp:
                        list_hp.insert(ind_hp, f'montuchon{key}')
                    list_hp.remove(hoc_phan)
                    header.remove(dict_tu_chon[key][hoc_phan])
                except:
                    print('No map data')

            print(diem)
            bang_diem_tong_hop[i][f'montuchon{key}'] = ', '.join(diem)
            

# %%
def diem_he_so_tin(bang_diem_tong_hop):
    for row in bang_diem_tong_hop[2:]:
        for cell_key in row.keys():
            if tc_hp.get(cell_key, 0):
                value = row[cell_key]
                if value:
                    value = value.split(",")
                    diem = ""
                    print(f'{value}_{tc_hp.get(cell_key, 0)}')
                    for v in value:
                        if v:
                            diem += '%.1f'%(float(v)*int(tc_hp.get(cell_key, 0))) 
                        diem += ", "
                    row[cell_key] = diem[:-2]


#diem_he_so_tin(bang_diem_tong_hop)

# %%
convert_tuchon(bang_diem_tong_hop)


#write_csv(bang_diem_tong_hop, 'diem_tong_hop_v3.csv')

# %%


list_hp = ['mssv', 'ngay_sinh'] + list_hp + ['tc_tich_luy', 'tbc_hoc_tap', 'tbc_tich_luy', 'xep_loai_hoc_tap', 'drl']
header = ['MSSV', 'Ngày Sinh'] + header + ['Số tín chỉ tích lũy', "Trung bình cộng học tập", 'Trung bình cộng tích lũy', 'Xếp loại học tập', 'Điểm rèn luyện']

header = {i:j for (i, j) in zip(list_hp, header) }

print(header)

for key in bang_diem_tong_hop[0].keys():
    if key not in list_hp:
        list_hp.append(key)

for key in list_hp:
    if key not in header.keys():
        header[key] = key

# %%

# Create a pandas DataFrame
df = pd.DataFrame(bang_diem_tong_hop, columns=list_hp)
df = df.rename(columns=header)

file_excel = "../BangDiem/SinhVienNam3.xlsx"
# Export to Excel with UTF-8 encoding
df.to_excel(file_excel, index=False)

print(f"Data exported successfully to '{file_excel}'.")

# %%



# %%
df.head(5)
# %%

print(header)
# %%
