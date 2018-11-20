# rfm.py: Recency, Fequency & Monetary (RFM) Analytics in Python.
import pandas as pd

def rfm(df_raw, today, user_id='member_id', date='date', checkout_id='checkout_id', price='price'):
    """
    Recency, Frequency & Monetary Analytics.

    Args:
      df_raw: pandas DataFrame with columns: user_id, date, checkout_id, price.
      today: E.g. '2016/04/01'.
      user_id: string. Column name of user id for group-by aggregation.
      date: string. Column name of date for calculating recency.
      checkout_id: string. Column name of checkout is for calculating frequency.
      price: string. Column name checkout price for calculating monetary.
    
    Returns:
      rfm_df: DataFrame with columns user_id, recency, frequency and monetary.
    """
    
    data_df = df.loc[:, [user_id, date, checkout_id, price]]
    data_df.columns = ['user_id', 'date', 'checkout_id', 'price']
    
    today = pd.to_datetime(today)
    
    recency_df = (data_df[data_df.user_id.notnull()]
                  .groupby('user_id')['date']
                  .agg([('recency', lambda x: (today - pd.to_datetime(x).max()).days)])
                  .reset_index())
    
    frequency_df = (data_df[data_df.user_id.notnull()]
                    .groupby('user_id')['checkout_id']
                    .agg([('frequency', 'nunique')])
                    .reset_index())

    monetary_df = (data_df[data_df.user_id.notnull()]
                   .groupby('user_id')['price']
                   .agg([('monetary', lambda x: x.sum())])
                   .reset_index())
    
    rf_df = pd.merge(recency_df, frequency_df, on='user_id')
    rfm_df = pd.merge(rf_df, monetary_df, on='user_id')
    
    return(rfm_df)
