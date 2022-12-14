"""tasks:
1.write udf to get dtdiff convert to 3 yrs,4mnt,9days
2.every month 15th what day u ll get?
"""

import calendar as c
from pyspark.sql import *
from pyspark.sql.functions import *

def function(str):
    year=str//365
    i=1
    while i<=year:
        str=str-365
        i+=1
    month=str//30
    str=str%30
    if str != 0:
        return f"{year}years{month}months{str}"
    else:
        return f"{year}years{month}months"

spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()
sc = spark.sparkContext

uf=udf(function)
df=spark.read.format('csv').option('header','true').option('inferSchema','true').load("C:\\Users\\chinm\\OneDrive\\Documents\\record1.csv")
nd=df.withColumn("OD",to_date(col('Order Date'),'d-M-yyyy'))\
    .withColumn("Newdate",last_day(col('OD'))).withColumn("new1",date_sub(last_day(col('OD')),30)).withColumn("new",date_add(col('new1'),15))\
    .withColumn("15thday",date_format(col('new'),'EEE')).withColumn("Daysofdatediff",datediff(current_date(),col('OD')))\
    .withColumn("converttoyrmntday",uf(col('Daysofdatediff')))
nd.show()

