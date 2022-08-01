import pandas as pd

def update_csv(file_name, df):
    df.to_csv(file_name,header=False)

def add_row_to_csv(file_name, row):
    df = read_csv(file_name)
    df.append(row)
    update_csv(file_name, df)




def read_csv(file_name):
    return pd.read_csv(file_name)

def read_csv_row(filename, row):
    data = read_csv(filename)
    return data[row]

df_final = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'), index=['x', 'y'])
update_csv("data.csv", df_final)
df_add = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'), index=['x', 'y'])
add_row_to_csv("data.csv", df_add)
z = read_csv("data.csv")
print(z)