
# Create database connection and tables
## Check needed packages available in venvairflow virtualenv
- SQLAlchemy
```commandline
(venvairflow) [train@trainvm ~]$ pip freeze | grep SQLAlchemy
Flask-SQLAlchemy==2.5.1
SQLAlchemy==1.3.24
SQLAlchemy-JSONField==1.0.0
SQLAlchemy-Utils==0.37.8
```
- psycopg2-binary
```commandline
(venvairflow) [train@trainvm ~]$ pip freeze | grep psycopg2-binary
psycopg2-binary==2.9.1
```

## Install pydantic
```commandline
pip install pydantic==1.10.2
```

## Create pydantic_example.py
```commandline
import json
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float
import pandas as pd
from pydantic import BaseModel, ValidationError, Field
from typing import List
from enum import Enum

df = pd.read_csv("https://raw.githubusercontent.com/erkansirin78/datasets/master/Mall_Customers.csv")
print(df.head())


class Classes(str, Enum):
    PHYS101 = "Physics I"
    PHYS125 = "Calculational Methods In Physics"
    PHYS150 = "Information and Entropy"


class MallCustomers(BaseModel):
    CustomerID: int = Field(default=999999, gt=0, lt=1000000)
    Gender: str = Field(default=None, max_length=6, min_length=4)
    Age: int = Field(default=1, gt=0, lt=130)
    AnnualIncome: float = Field(default=1.0, gt=0.0, lt=1000000.0)
    SpendingScore: int = Field(default=1, gt=0, lt=100)


# 1,Male,19,15000,39
customer1_data = {
    'CustomerID': 1,
    'Gender': "Male",
    'Age': 19,
    'AnnualIncome': 15000,
    'SpendingScore': 39
}

try:
    customer1 = MallCustomers(**customer1_data)
    schema = customer1.schema()
    pprint(json.dumps(schema))
except ValidationError as e:
    pprint(e.json())

# an Engine, which the Session will use for connection
# Connection
engine = create_engine('postgresql://train:Ankara06@localhost:5432/traindb')


Base = declarative_base()
# Create database table
class Customer(Base):
    __tablename__ = "customers"

    CustomerID = Column(Integer, primary_key=True)
    Gender = Column(String)
    Age = Column(Integer)
    AnnualIncome = Column(Float)
    SpendingScore = Column(Integer)


Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()

# Write table
for _, row in df.iterrows():
    customer_x = Customer(
        CustomerID=row['CustomerID'],
        Gender=row['Gender'],
        Age=row['Age'],
        AnnualIncome=row['AnnualIncome'],
        SpendingScore=row['SpendingScore']
    )
    session.add(customer_x)
session.commit()

df.to_sql('customers_pandas', con=engine, if_exists='replace')
```

## Describe paydantic table on psql
```commandline
traindb=> \d customers
                                          Table "public.customers"
    Column     |       Type        | Collation | Nullable |                     Default                     
---------------+-------------------+-----------+----------+-------------------------------------------------
 CustomerID    | integer           |           | not null | nextval('"customers_CustomerID_seq"'::regclass)
 Gender        | character varying |           |          | 
 Age           | integer           |           |          | 
 AnnualIncome  | double precision  |           |          | 
 SpendingScore | integer           |           |          | 
Indexes:
    "customers_pkey" PRIMARY KEY, btree ("CustomerID")
```

## Describe pandas table on psql
```commandline
traindb=> \d customers_pandas
             Table "public.customers_pandas"
    Column     |  Type  | Collation | Nullable | Default 
---------------+--------+-----------+----------+---------
 index         | bigint |           |          | 
 CustomerID    | bigint |           |          | 
 Gender        | text   |           |          | 
 Age           | bigint |           |          | 
 AnnualIncome  | bigint |           |          | 
 SpendingScore | bigint |           |          | 
Indexes:
    "ix_customers_pandas_index" btree (index)
```