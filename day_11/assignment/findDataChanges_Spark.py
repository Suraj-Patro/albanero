spark

df = spark.read.option("header", True).csv( "data.csv" )
df_c = spark.read.option("header", True).csv( "upload.csv" )


diff_1 = df.subtract(df_c)
diff_2 = df_c.subtract(df)

cols = diff_1.columns

diff_1 = diff_1.withColumn("index", concat(lit("ngjuesgrv"), col("phone")))
diff_2 = diff_2.withColumn("index", concat(lit("ngjuesgrv"), col("phone")))

joined = diff_1.join(diff_2, on='index', how='inner')

joined = rename_duplicate_columns(joined)

joined = create_columns_compare(joined, cols)

joined.show()
