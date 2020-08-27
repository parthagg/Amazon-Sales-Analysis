import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 100)

pd.set_option('display.width', 1000)
#Parsing all files
files=glob.glob('*.txt')

df_list=[]
for filename in files:
    df_list.append(pd.read_csv(filename,sep='\t'))
#Inputting all the order details into our dataframe.
df=pd.concat(df_list)
print('Now we have parsed all the dataframes and created our final dataframe.'
      'Let us take a look at it.')
print(df.head())
#print(df.columns)
print('\n Let us start our analysis by calculating the number of times each city occurs in the df.'
      'We use the value_counts function.')
city_df=df['ship-city'].value_counts().reset_index()
city_df.columns=['ship-city','quantity']
print(city_df)
print('As expected, this data has a lot of rows with value=1.'
      'Let us view its distribution')
print(city_df.describe())
print('Now here, even the 75 percentile mark is at 2. Let us start by only looking at data over 50 qty.')

#plt.figure(figsize=[8,5])
#plt.subplot()
#plt.bar(city_df['index'],city_df['ship-city'])
#plt.show()
df=df.drop(['last-updated-date','fulfillment-channel', 'sales-channel', 'order-channel', 'url', 'ship-service-level', 'product-name','asin', 'item-status','shipping-price', 'shipping-tax', 'gift-wrap-price', 'gift-wrap-tax', 'item-promotion-discount', 'ship-promotion-discount','ship-country', 'promotion-ids', 'is-business-order', 'purchase-order-number', 'price-designation', 'fulfilled-by', 'is-sold-by-ab ','merchant-order-id','currency','ship-postal-code','item-tax','order-status'],axis=1)

print(df.head())
split_date=df['purchase-date'].str.split('T')
df['date']=split_date.str.get(0)
df['time']=split_date.str.get(1)
df.drop(['purchase-date'],axis=1,inplace=True)
print(df.head())

print(df.dtypes)
df['date']=pd.to_datetime(df['date'])
df['time']=pd.to_datetime(df['time'])

print(df.dtypes)

#print(df.sort_values(by=['date']))
#print(df.time.to)
df['hourwise']=df['time'].dt.hour
print(df.head())
print(df.dtypes)
#plt.hist(df['hourwise'])
#plt.show()
print(df.groupby('hourwise')['item-price'].sum())
total_value_by_city=df.groupby('ship-city')['item-price'].sum().reset_index()
total_value_by_city.columns=['city','value']
print(total_value_by_city.sort_values(by='value'))
avg_value_by_city=df.groupby('ship-city')['item-price'].mean().reset_index()
print(avg_value_by_city.dtypes)
print(city_df.dtypes)
#avg_value_by_city=avg_value_by_city.merge(city_df,on='ship-city')
print(avg_value_by_city)
#print(avg_value_by_city.sort_values(by='item-price',ascending=False).head(70))

merged_df=pd.merge(avg_value_by_city, city_df, how='left', on='ship-city')

merged_df=merged_df[merged_df['quantity']>40].reset_index()
print(merged_df)
merged_df.drop(columns='index',inplace=True)
merged_df.drop(index=5,inplace=True)
city_df=city_df[city_df['quantity']>40]
print(merged_df)
figure,axes = plt.subplots(nrows=2, ncols=2,figsize=[14,8])

#Graph of cities vs average value per order
axes[0,0].set_xticks(np.arange(len(merged_df['ship-city'])))
axes[0,0].set_xticklabels(merged_df['ship-city'],fontsize=6)
axes[0,0].set_xlabel('Cities')
axes[0,0].set_ylabel('Average value per order')
axes[0,0].bar(merged_df['ship-city'],merged_df['item-price'])

#Graph of hours of the day vs order quantity
axes[0,1].hist(df['hourwise'],bins=24)
axes[0,1].set_xlabel('Time of the day')
axes[0,1].set_ylabel('Number of Orders')

#Graph of Cities and their respective order quantities
axes[1,0].bar(city_df['ship-city'],city_df['quantity'])
axes[1,0].set_xticks(np.arange(len(city_df['ship-city'])))
axes[1,0].set_xticklabels(city_df['ship-city'],fontsize=6)
axes[1,0].set_xlabel('Cities')
axes[1,0].set_ylabel('Number of orders')
plt.show()

#print(df.loc[df['ship-city'].str.match(r'(^LUDHIANA)')==True].head(50))
#S.str.match(r'(^P.*)')==True