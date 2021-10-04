from app import app
from pandas import read_csv, DataFrame, DatetimeIndex, merge
import numpy

def cleanData(df):
    new_df = df[df.country_name != ""]
    new_df = new_df[new_df.event_date.notnull()]
    new_df = new_df[new_df.latitude != ""]
    new_df = new_df[new_df.longitude != ""]

    return new_df

def transformData(df):
    new_df = df

    new_df['year'] = DatetimeIndex(new_df['event_date']).year
    new_df['month'] = DatetimeIndex(new_df['event_date']).month

    return new_df

def initDF(): #initializes pandas dataframe
    df_landslides = read_csv(app.config['LS_CSV_PATH'], delimiter=',', parse_dates=[0], usecols=getCsvColumns(False))
    df_landslides = transformData(cleanData(df_landslides)) # removing rows where year and location components are null
    df_landslides = df_landslides.groupby(["year", "country_name", "country_code"]).aggregate(list).reset_index()

    return df_landslides

def initCountries():
    df_countries = read_csv(app.config['COUNTRY_CSV_PATH'], delimiter=',', usecols=[0,2,3], header=0, names=['country_code', 'country_latitude', 'country_longitude'])
    
    df_countries = merge(df_countries, getLSDataframe(), on="country_code", how="inner")
    df_countries = df_countries.drop_duplicates(subset=["country_code"])[["country_code", "country_latitude", "country_longitude", "country_name"]].copy()

    return df_countries.T.to_dict()


def getLSDataframe():
    return df

def getCsvColumns(initial=True):
    if(not initial):
        return ['event_date', 'event_title', 'event_description','location_description',  'landslide_category', 'landslide_trigger', 'landslide_size', 'fatality_count', 'injury_count', 'latitude', 'longitude', 'country_name', 'country_code']
    return ['event_date', 'event_title', 'event_description','location_description',  'landslide_category', 'landslide_trigger', 'landslide_size', 'fatality_count', 'injury_count', 'latitude', 'longitude', 'country_name']

def getFilteredDataframe(country, year):
    df = getLSDataframe()
    df = df.drop('country_code', 1)

    if(country is not None):
        df = df[df.country_name == country]
    if(year is not None):
        df = df[df.year == int(year)]

    print(df)

    df = df.to_dict('r')[0]
    df["event_date"] = [time_unit.to_pydatetime().timestamp() for time_unit in df["event_date"]]

    list_of_lists = []
    for column_name in getCsvColumns():
        if(column_name != 'country_name'):
            list_of_lists.append(df[column_name])

    numpy_array = numpy.array(list_of_lists)
    transpose = numpy_array.T
    transpose_list = transpose.tolist()
    print(transpose_list)
    transpose_list = [([year, country] + list) for list in transpose_list]

    return transpose_list

def getInitialFilters():
    df = getLSDataframe()

    initial_dict = {}

    initial_dict["years"] = df.year.unique().tolist()
    initial_dict["countries"] = df.country_name.unique().tolist()
    return initial_dict

df = initDF()
countries = initCountries()