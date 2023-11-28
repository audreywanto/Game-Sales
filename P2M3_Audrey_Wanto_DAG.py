########################################
## Milestone 3                        ##
##                                    ##
## Name: Audrey Wanto                 ##
## Batch: BSD 002                     ##
## Objective: Create DAG to fetch     ##
##            data from Postgresql,   ##
##            data cleaning, and      ##
##            post to Elasticsearch.  ##
##                                    ##
########################################


# Import Libraries
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import psycopg2 as db
import json
import csv
import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def FetchPostgresql():
    '''
    Fetch data from Postgresql
    
    '''
    db_name = 'airflow'
    db_user = 'airflow'
    db_password = 'airflow'
    db_host = 'localhost'
    db_port = '5433'
    connection = db.connect(
        database = db_name,
        user = db_user,
        password = db_password,
        host = db_host,
        port = db_port
    )
    df=pd.read_sql("select * from table_m3", connection)
    df.to_csv('P2M3_Audrey_Wanto_data_raw.csv')
    print("-------Data Saved------")
    
    
def DataCleaning():
    '''
    Data cleaning and saving it into a new csv file
    '''
    df = pd.read_csv('/opt/airflow/dags/P2M3_Audrey_Wanto_data_raw.csv')
    df = df.drop_duplicates() # Drop duplicates
    df = df.dropna() # Drop missing values
    df['Year'] = df['Year'].astype('int') # Change datatype of 'Year' to numeric from string
    df.columns = df.columns.str.lower() # Change column names to lower case
    df.to_csv('/opt/airflow/dags/P2M3_Audrey_Wanto_data_clean.csv') # Export data to csv


def PostElasticSearch():
    '''
    Post cleaned data to Elasticsearch
    '''
    es = Elasticsearch('http://localhost:9200')
    print('Connection status: ', es.ping())
    df = pd.read_csv('/opt/airflow/dags/P2M3_Audrey_Wanto_data_clean.csv')
    json_str = df.to_json(orient='records')
    json_records = json.loads(json_str)
    index_name = 'data_records'
    doctype = 'data_record'
    es.indices.delete(index=index_name, ignore=[400, 404])
    es.indices.create(index=index_name, ignore=400)
    action_list = []
    for row in json_records:
        record ={
            '_op_type': 'index',
            '_index': index_name,
            '_type': doctype,
            '_source': row
        }
        action_list.append(record)
    helpers.bulk(es, action_list)
    
    
default_args = {
    'owner': 'Audrey',
    'start_date': dt.datetime(2023, 11, 22, 23, 30), # 06:30 WIB = 23:30 UTC
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=15),
}


with DAG('M3CleanData',
         default_args=default_args,
         schedule_interval=timedelta(minutes=60),      
         ) as dag:

    fetchData = PythonOperator(task_id='fetch',
                                 python_callable=FetchPostgresql)
    
    cleanData = PythonOperator(task_id='clean',
                                 python_callable=DataCleaning)

    postFile = PythonOperator(task_id='post',
                                 python_callable=PostElasticSearch)


fetchData >> cleanData >> postFile