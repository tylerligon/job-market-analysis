import pandas as pd
#load into dataframe from excel
def load_dataset(path):
    df = pd.read_excel(path)
    return df

