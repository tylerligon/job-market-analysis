import pandas as pd
#load into SQL
def load_dataset(path):
    df = pd.read_excel(path)
    return df

