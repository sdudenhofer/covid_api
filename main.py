import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

pg_user = os.getenv('POSTGRES_USER')
pg_pass = os.getenv('POSTGRES_PASSWORD')

engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@127.0.0.1:5432/covid_data')

def get_data(url):
    response = requests.get(url=url)
    data = response.json()
    return data

def write_to_db(data):
    df = pd.DataFrame(data, index=['active_cases', 'country', 'last_update', 'new_cases', 'new_deaths', 'total_cases', 'deaths', 'recovered'])
    df.to_sql('covid_data', engine, if_exists='replace', index=False)
    print('Data written to database')

def main():
    url = 'https://covid-19.dataflowkit.com/v1/USA'
    get_initial_data = get_data(url)
    write_to_db(get_initial_data)


if __name__ == "__main__":
    main()