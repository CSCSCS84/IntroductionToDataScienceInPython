import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2] == '01':
        df.rename(columns={col: 'Gold' + col[4:]}, inplace=True)
    if col[:2] == '02':
        df.rename(columns={col: 'Silver' + col[4:]}, inplace=True)
    if col[:2] == '03':
        df.rename(columns={col: 'Bronze' + col[4:]}, inplace=True)
    if col[:1] == '№':
        df.rename(columns={col: '#' + col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(')  # split the index by '('

df.index = names_ids.str[0]  # the [0] element is the country name (new index)
df['ID'] = names_ids.str[1].str[:3]  # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')


def answer_zero():
    return df.iloc[0]


def answer_one():
    return df['Gold'].argmax()


def answer_two():
    country = (abs(df['Gold'] - df['Gold.1'])).argmax()
    return country


def answer_three():
    df_sub = df[df['Gold'] >= 1]
    df_sub = df_sub[df['Gold.1'] >= 1]
    df_sub2 = df_sub['Gold'] / df_sub['Gold.2'] - df_sub['Gold.1'] / df_sub['Gold.2']
    country = df_sub2.argmax()
    return country


def answer_four():
    points = 3 * df['Gold.2'] + 2 * df['Silver.2'] + 1 * df['Bronze.2']
    return points


census_df = pd.read_csv('census.csv')


def answer_five():
    group = census_df.groupby(by='STNAME').count()
    return group['COUNTY'].argmax()


def answer_six():
    census_df2 = census_df[census_df['SUMLEV'] != 40]
    df_sorted = census_df2.sort_values(by=['STNAME', 'CENSUS2010POP'], ascending=False)
    group = df_sorted.groupby(by='STNAME')

    state = group.head(3).groupby(by='STNAME')['CENSUS2010POP'].sum()
    state_sorted = state.sort_values(ascending=False)
    return [state_sorted.index[0], state_sorted.index[1], state_sorted.index[2]]


def answer_seven():
    census_df = pd.read_csv('census.csv')
    census_df2 = census_df[census_df['SUMLEV'] != 40]
    populations = ['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014',
                   'POPESTIMATE2015']
    census_df2['diff'] = census_df2[populations].max(axis=1) - census_df2[populations].min(axis=1)
    county = census_df2['diff'].argmax()
    return census_df2['CTYNAME'].loc[county]


def answer_eight():
    region = census_df[(census_df['REGION'] == 1) | (census_df['REGION'] == 2)]
    region = region[region['CTYNAME'].str.match('Washington County')]
    region = region[region['POPESTIMATE2015'] >= region['POPESTIMATE2014']]
    return region[['STNAME', 'CTYNAME']]
