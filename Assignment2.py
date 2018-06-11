import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index)
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero()

def answer_one():
    return df['Gold'].argmax()

#print(answer_one())

def answer_two():
    country=(abs(df['Gold']-df['Gold.1'])).argmax()
    return country

#print(answer_two())

def answer_three():
    df_sub=df[df['Gold']>=1  ]
    df_sub=df_sub[df['Gold.1']>=1]
    df_sub2=df_sub['Gold']/df_sub['Gold.2'] - df_sub['Gold.1']/df_sub['Gold.2']
    print(df_sub2)
    country=(df_sub2).argmax()
    return country

print(answer_three())

def answer_four():
    points=3*df['Gold.2']+2*df['Silver.2']+1*df['Bronze.2']
    return points

#print(answer_four())

census_df = pd.read_csv('census.csv')
#census_df = census_df.set_index(['STATE', 'COUNTY'])


def answer_five():
    gr=census_df.groupby(by='STNAME').count()

    return gr['COUNTY'].argmax()

#print(answer_five())
#print(census_df.head(150))

def answer_six():
    census_df2 = census_df[census_df['SUMLEV'] != 40]
    df_sorted = census_df2.sort_values(by=['STNAME', 'CENSUS2010POP'], ascending=False)
    gr = df_sorted.groupby(by='STNAME')

    state = gr.head(3).groupby(by='STNAME')['CENSUS2010POP'].sum()
    state_sorted = state.sort_values(ascending=False)
    l=[state_sorted.index[0], state_sorted.index[1], state_sorted.index[2]]
    return [state_sorted.index[0], state_sorted.index[1], state_sorted.index[2]]

#print(answer_six())


def answer_seven():
    census_df = pd.read_csv('census.csv')
    census_df2 = census_df[census_df['SUMLEV']!=40]
    populations=['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']

    census_df2['diff']=census_df2[populations].max(axis=1)-census_df2[populations].min(axis=1)
    #print(census_df2['max'])
    county=census_df2['diff'].argmax()

    return census_df2['CTYNAME'].loc[county]

#print(answer_seven())


def answer_eight():
    region=census_df[(census_df['REGION']==1) | (census_df['REGION']==2) ]
    l=len('Washington')
    region=region[region['CTYNAME'].str.match('Washington County')]
    region=region[region['POPESTIMATE2015']>=region['POPESTIMATE2014']]
    #print(region)
    return region[['STNAME', 'CTYNAME']]

print(answer_eight())