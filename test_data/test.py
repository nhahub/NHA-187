import pandas as pd 

df = pd.read_csv('/home/medhat-mohamed/tst/complaints_dataset.csv')

df['categories'] = (
    df['categories']
    .str.replace('[', '', regex=False)
    .str.replace(']', '', regex=False)
)

# df['categories'] = df['categories'].str.split(",").str[0]

df = df.loc[df['categories'].str.strip() != ""]

print(df.head())

df2 = df[['text', 'categories']]


df2['categories'] = df2['categories'].str.replace("'", "")

# print(df2.head())

rep = df2.groupby(['text', 'categories']).size().reset_index(name='count')

print(rep.head())
rep_sorted = rep.sort_values('count', ascending=False)
rep_sorted.reset_index(inplace=True)
rep_sorted.drop('index', axis=1, inplace=True)
rep_sorted.index = range(1, len(rep_sorted) + 1)
print(rep_sorted.head())
rep_sorted.to_excel('report22.xlsx')
# df2.to_csv('short.csv')



# df2['concat'] = df2['text'] + " " + df2['categories']

# print(df2['concat'].value_counts())

# (df2['concat'].value_counts()).to_csv('final_report.csv')

