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

def write_to_db():
    df = pd.read_csv("https://raw.githubusercontent.com/erkansirin78/datasets/master/Mall_Customers.csv")
    print(df.head())

    class MallCustomers(BaseModel):
        CustomerID: int = Field(default=999999, gt=0, lt=1000000)
        Gender: str = Field(default=None, max_length=6, min_length=4)
        Age: int = Field(default=1, gt=0, lt=130)
        AnnualIncome: float = Field(default=1.0, gt=0.0, lt=1000000.0)
        SpendingScore: int = Field(default=1, gt=0, lt=100)

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

# df.to_sql('customers_pandas', con=engine, if_exists='replace')