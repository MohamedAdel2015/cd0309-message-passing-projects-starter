import os
import json

from kafka import KafkaConsumer

from sqlalchemy import create_engine  
from sqlalchemy import Table, Column, String, MetaData, DateTime
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Point

from datetime import datetime
import os

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db = create_engine(DB_URL)
meta = MetaData(db)  

location_table = Table('location', meta,  
                       Column('person_id', String),
                       Column('coordinate', Geometry("POINT",  srid=4326)),
                       Column('creation_time', DateTime))

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER])

with db.connect() as conn:
    for message in consumer:
        print(f"Received message: {message}")
        msg_str = message.value.decode('utf-8')
        msg_data = json.loads(msg_str)

        person_id = msg_data['person_id']
        longitude = msg_data['longitude']
        latitude = msg_data['latitude']

        # Create
        insert_statement = location_table.insert().values(person_id=person_id, coordinate=ST_Point(latitude, longitude), creation_time=datetime.now())
        conn.execute(insert_statement)