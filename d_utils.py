import pandas as pd

class Utils():
    '''
    ''' 
    def __init__(self):
        pass

    def generic_csv_to_df(self, filename: str, sheetname: str = None):
        df = pd.read_excel(filename, sheetname)
        df.columns = ['label', 'generic_product', 'quantity']
        df['generic_product'] = df['generic_product'].str.replace(' ','%20')
        return df
