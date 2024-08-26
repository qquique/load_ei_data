from peewee import *


db = PostgresqlDatabase(ei_data,
                        user='postgres',
                        password='postgres',
                        host='localhost',
                        port=5432)
