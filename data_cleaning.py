

class DataCleaning():
    '''
    '''
    def __init__(self) -> None:
        pass

    @staticmethod    
    def add_zero(value):
        if value.startswith('£'):
            return value
        else: 
            return '0.' + value
    
    def ocado_morrisons_cleaning(self, df):
        '''
        '''
        for var in ['product_names', 'weights']:
            df[var] = df[var].str.upper()
        df['product_names'] = df['product_names'] + ' ' + df['weights']
        df.drop(['weights','Unnamed: 0'], axis=1, inplace=True)
        df['delivered_prices'] = df['delivered_prices'].apply(self.add_zero)
        df['delivered_prices'] = df['delivered_prices'].replace('[^0-9.]','',regex=True)
        df['delivered_prices'] = df['delivered_prices'].astype(float)
        return df
