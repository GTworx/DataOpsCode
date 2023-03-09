from pyspark.sql import SparkSession, functions as F
from pyspark.sql import DataFrame


class MyHelpers:

    def get_spark_session(self, session_params: dict) -> SparkSession:
        # Create spark session and return it.

        if session_params["hive_support"] == True:

            SparkS = SparkSession.builder \
                .master(session_params["master"]) \
                .appName(session_params["appName"]) \
                .enableHiveSupport() \
                .config("spark.jars.packages", "org.apache.spark:spark-avro_2.12:3.1.1") \
                .config("spark.executor.memory", session_params["executor_memory"]) \
                .config("spark.executor.cores", session_params["executor_cores"]) \
                .config("spark.executor.instances", session_params["executor_instances"]) \
                .getOrCreate()
        else:
            SparkS = SparkSession.builder \
                .master(session_params["master"]) \
                .appName(session_params["appName"]) \
                .config("spark.jars.packages", "org.apache.spark:spark-avro_2.12:3.1.1") \
                .config("spark.executor.memory", session_params["executor_memory"]) \
                .config("spark.executor.cores", session_params["executor_cores"]) \
                .config("spark.executor.instances", session_params["executor_instances"]) \
                .getOrCreate()

        #SparkS = SparkSession.builder.master("local[2]").appName(session_params["appName"]).getOrCreate()

        return SparkS

    def get_data(self, spark_session: SparkSession, read_params: dict) -> DataFrame:

        df = spark_session.read.format(read_params["format"]) \
            .option("header", read_params["header"]) \
            .option("sep", read_params["sep"]) \
            .option("inferSchema", read_params["inferSchema"]) \
            .load(read_params["path"])

        return df

    def format_dates(self, date_cols: list, input_df: DataFrame) -> DataFrame:

        for cols in date_cols:
            input_df = input_df.withColumn(cols, F.to_date(F.col(cols), 'yyyy-MM-dd HH:mm:ss.SSSSSS+00'))

        return input_df


    def make_nulls_to_unknown(self, input_df: DataFrame) -> DataFrame:

        return input_df.na.fill("unknown")

    def trim_str_cols(self, input_df) -> DataFrame:
        ## trim all string cols
        for cols in input_df.columns:
            if(input_df.schema[cols].dataType == "string"):
                input_df = input_df.withColumn(cols, F.trim(cols))

        return input_df

    def write_to_hive(self, input_df: DataFrame):
        # write to hive test1 database cars_cleaned table in avro format
        input_df.write.format("avro") \
            .mode("overwrite") \
            .saveAsTable("test1.cars_cleaned")
        pass
