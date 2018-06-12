import pandas as pd
import numpy as np
from scipy import stats


def get_list_of_university_towns():
    with open('university_towns.txt', 'r') as myfile:
        data = myfile.read()
    listOfUniverityTowns = pd.DataFrame(columns=["State", "RegionName"])

    data = data.split('[edit]')
    state = data[0]
    for stateUniversities in data[1:]:
        unis = pd.DataFrame(columns=["State", "RegionName"])
        unis['RegionName'] = stateUniversities.split("\n")[1:-1]
        unis['State'] = state
        listOfUniverityTowns = listOfUniverityTowns.append(unis, ignore_index=True)
        state = stateUniversities.split("\n")[-1]
    listOfUniverityTowns = listOfUniverityTowns.replace(['\s*\(.*'], [''], regex=True)
    listOfUniverityTowns = listOfUniverityTowns.replace(['\[.*\]'], [''], regex=True)
    return listOfUniverityTowns


def get_recession_start():

    gpd = pd.read_excel('gdplev.xls', skiprows=5, header=0, usecols=[4, 5, 6])
    gpd.rename(columns={'Unnamed: 0': 'Quarter'}, inplace=True)
    gpd = gpd.iloc[212:]
    quarter = -1

    for i in gpd.index[0:-2]:
        if gpd.at[i, 'GDP in billions of current dollars'] > gpd.at[i + 1, 'GDP in billions of current dollars'] and \
                        gpd.at[i+1, 'GDP in billions of current dollars'] > gpd.at[
                            i +2, 'GDP in billions of current dollars']:
            quarter = gpd.ix[i]['Quarter']
            break

    return quarter


def get_recession_end():
    recessionStart=get_recession_start()

    gpd = pd.read_excel('gdplev.xls', skiprows=5, header=0, usecols=[4, 5, 6])
    gpd.rename(columns={'Unnamed: 0': 'Quarter'}, inplace=True)
    gpd = gpd[gpd['Quarter'] >= '2000']
    quarter = -1

    index = gpd.index[gpd['Quarter']==recessionStart].tolist()[0]

    for i in range(index,gpd.index[-3]):
        if gpd.at[i+1, 'GDP in billions of current dollars'] > gpd.at[i, 'GDP in billions of current dollars'] and \
                        gpd.at[i+2, 'GDP in billions of current dollars'] > gpd.at[
                            i+1, 'GDP in billions of current dollars']:
            quarter = gpd.ix[i+2]['Quarter']
            break

    return quarter


def get_recession_bottom():
    recessionStart=get_recession_start()
    recessionEnd=get_recession_end()
    gpd = pd.read_excel('gdplev.xls', skiprows=5, header=0, usecols=[4, 5, 6])
    gpd.rename(columns={'Unnamed: 0': 'Quarter'}, inplace=True)
    gpd = gpd[gpd['Quarter'] >= '2000']
    gpdRecession=gpd[((gpd['Quarter']>=recessionStart) & (gpd['Quarter']<=recessionEnd)) ]


    bottom=gpdRecession['GDP in billions of current dollars'].idxmin()

    return gpd.at[bottom,'Quarter']


def convert_housing_data_to_quarters():

    homes = pd.read_csv('City_Zhvi_AllHomes.csv', header=0)
    columnsYear = [year for year in homes.columns if year[0] == '2']
    columnsState = ["State", "RegionName"]
    columns = [col for col in homes.columns if col in columnsYear or col in columnsState]
    homes.fillna(0,inplace=True)
    # homes=homes[columns]
    quarters = []
    # calcl all quartes we want to use
    for i in range(int(np.ceil(len(columnsYear) / 3))):
        q = i % 4 + 1
        year = int(i / 4)
        quarter = 2000 + year
        quarter = str(quarter) + 'q' + str(q)
        quarters.append(quarter)
    quartersDict = {}
    for q in quarters:
        year = q[0:4]
        quarter = int(q[5:6])
        list = [str(year) + '-' + ("%02d" % (i + (quarter - 1) * 3)) for i in range(1, 4)]

        quartersDict[q] = list
    for q, v in quartersDict.items():
        vcopy = [e for e in v if e <= '2016-08']

        homes[q] = homes[vcopy].mean(axis=1)
    columnsState.extend(quarters)
    homes = homes[columnsState]
    homes['State']=homes['State'].map( {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'})
    homes.set_index(['State', 'RegionName'], inplace=True)
    return homes


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''


    recessionStart=get_recession_start()
    recessionBottom=get_recession_bottom()
    housePrices=convert_housing_data_to_quarters()
    housePricesRecession=housePrices[recessionStart]-housePrices[recessionBottom]


    univerityTowns=get_list_of_university_towns()
    print(housePricesRecession)
    universityTownsCopy=univerityTowns.set_index(['State', 'RegionName'])
    a=housePricesRecession.loc[universityTownsCopy.index]
    b=housePricesRecession.loc[housePricesRecession.index.difference(universityTownsCopy.index)]
    a=a.dropna()

    test=stats.ttest_ind(a, b,equal_var = False)

    return (True,test.pvalue,'university town')

# convert_housing_data_to_quarters()
print(run_ttest())