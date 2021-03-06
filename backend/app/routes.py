from flask import render_template, request
import json
from app import app
from app.exporter import *

@app.route('/')
@app.route('/index')
def index():
    initial_filters = getInitialFilters()
    initial_countries = initCountries().items()
    initial_countries = [curr_item[1] for curr_item in initial_countries]

    return render_template('index.html', years=initial_filters.get('years'), countries=initial_countries)

@app.route('/get_map_data')
def get_map_data():
    country = request.args.get('country')
    year = request.args.get('year')
    
    df_list = getFilteredDataframe(country, year)
    print(json.dumps(df_list))
    return render_template('main.html', years=year, country=country)

@app.route('/get_filter_data')
def get_filter_data():
    country = request.args.get('country')
    year = request.args.get('year')
    initial = request.args.get('initial')

    df = getLSDataframe()

    if(initial):
        initial_dict = {}

        initial_dict["years"] = df.year.unique().tolist()
        initial_dict["countries"] = df.country_name.unique().tolist()
        return initial_dict

    if(country is not None):
        df = df[df.country_name == country]
        curr_df_series = df.year
    else:
        df = df[df.year == int(year)]
        curr_df_series = df.country_name

    curr_df_series = json.dumps(curr_df_series.values.tolist())
    return curr_df_series


    