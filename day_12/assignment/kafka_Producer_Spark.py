

df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .write \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host1:port1,host2:port2") \
    .option("kafka.security.protocol", "SSL") \
    .option("failOnDataLoss", "false") \
    .option("topic", "topic2") \
    .save()


