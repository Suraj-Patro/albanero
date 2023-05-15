# main.py

import os
import time
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from pyspark.sql import SparkSession

import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from fuzzywuzzy import fuzz
from pyspark.sql.functions import row_number,lit, when, col
from pyspark.sql.window import Window
from pyspark.sql import Window as window




app = FastAPI()
spark = SparkSession.builder.getOrCreate()
input_dir = "input"
ouput_dir = "output"


class Item(BaseModel):
    file_path: str
    columns: List[str] = []


@app.get("/")
async def root():
    return {"message": "Hello World"}



def rename_duplicate_columns(dataframe):
    columns = dataframe.columns
    duplicate_column_indices = list(set([columns.index(col) for col in columns if columns.count(col) == 2]))
    for index in duplicate_column_indices:
        columns[index] = columns[index]+'_2'
    dataframe = dataframe.toDF(*columns)
    return dataframe


def calculate_fuzz_ratio( sel_col, val1, val2 ):
    columns = [
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "address",
        "city",
        "state",
        "country",
        "email",
        "phone"
    ]

    columns_selection = [ [i, 1] if i in set(sel_col) else [i, 0] for i in columns ]

    sel_val1 = []
    sel_val2 = []

    for i in range( len(columns_selection) ):
        if columns_selection[i][1] == 1:
            sel_val1.append( val1[i] )

    for i in range( len(columns_selection) ):
        if columns_selection[i][1] == 1:
            sel_val2.append( val2[i] )

    return fuzz.ratio(sel_val1, sel_val2)



async def check(file_path, columns):
    df = spark.read.option("header", True).csv( os.path.join( input_dir, file_path ) )

    # Logic to group similar rows on basis of the fuzzy ratio
    ###################################################################################################

    w = Window().orderBy(lit('row_num'))
    df = df.withColumn("row_num", row_number().over(w))


    joined = df.crossJoin(df)
    joined = rename_duplicate_columns(joined)

    sch = ['group_no', 'row_no', 'match_%']
    joined = joined.rdd.map(lambda x: (x.row_num, x.row_num_2,
    calculate_fuzz_ratio(columns, [ x.first_name, x.last_name, x.gender, x.date_of_birth, x.address, x.city, x.state, x.country, x.email, x.phone ], \
                    [ x.first_name_2, x.last_name_2, x.gender_2, x.date_of_birth_2, x.address_2, x.city_2, x.state_2, x.country_2, x.email_2, x.phone_2 ] ))).toDF(sch)


    joined = joined.where(joined['match_%'] >= 80)


    w = window.partitionBy('group_no')
    joined = joined.select('group_no', 'row_no', 'match_%', F.count('group_no').over(w).alias('count')).sort('group_no', 'match_%')


    windowDept = Window.partitionBy("row_no").orderBy(col("count").desc())
    joined = joined.withColumn("row",row_number().over(windowDept)).filter(col("row") == 1).drop("row")


    df = joined.join(df, joined.row_no == df.row_num, "inner")

    # df = df.select( F.row_number().over( Window.partitionBy( df['group_no'] ).orderBy( df['row_no'] ) ).alias( "row_num" ), \
    #                "match_%", \
    #                 "first_name", "last_name", "gender", "address", "city", "state", "country", "email", "phone")

    df = df.select( "group_no", "first_name", "last_name", "gender", "address", "city", "state", "country", "email", "phone")

    ###################################################################################################

    df.coalesce(1).write.option("header", True).csv( os.path.join( ouput_dir, f"{ int( time.time() ) }_{file_path}" ) )
    return {"status": "success"}


@app.post("/chk_dup")
async def create_item(item: Item):
    item_dict = item.dict()
    output = await check( item_dict[ "file_path" ], item_dict[ "columns" ] )
    return output
