import duckdb
from pyspark.sql import SparkSession

print("--- DUCKDB 1.5.5 - 14% ---")
duckdb.sql("SELECT 'EDGE 50 VIVO EM CAJURU' as status").show()

print("\n--- SPARK 3.5.1 ---")
spark = SparkSession.builder.master("local[1]") \
.config("spark.driver.memory","512m") \
.config("spark.ui.enabled","false").getOrCreate()

dados = [("A",120),("B",95),("A",130),("B",110)]
spark.createDataFrame(dados, ["turno","prod"]).groupBy("turno").avg("prod").show()
spark.stop()
print("FINALIZADO - FUNDADOR ITUPEVA")
