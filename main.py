import pandas as pd
import numpy as np

order_df = pd.read_csv('data/order_log.csv')
order_df['created_at'] = pd.to_datetime(
    order_df['created_at'],
    format='%Y-%m-%d'
)

revenue_for_month = order_df.resample('M', on='created_at')['amount'].sum()

min_dates = order_df.groupby(['customer_id'])['created_at'].min()
order_df['first_order_date'] = order_df.apply(
    lambda row: min_dates.loc[row['customer_id']], axis=1
)
order_df['new_customer'] = order_df['created_at'] <= \
                           order_df['first_order_date']
order_df['new_customer_total'] = np.where(order_df['new_customer'],
                                          order_df['amount'], 0)
order_df['previous_customer'] = order_df['created_at'] > \
                                order_df['first_order_date']

table = order_df.resample(
    'M', on='created_at')['amount', 'new_customer_total'].sum()
table['new_customer_percentage'] = round(table['new_customer_total'] /
                                         table['amount'] * 100, 2)
print("Answers for the 1 and 2 questions:")
print(table)

total_revenue_new_customers = table['new_customer_total'].sum()
print("Extra credit:", total_revenue_new_customers)
