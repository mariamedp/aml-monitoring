"""Entry script for Model Data Collector Data Window Component."""

import os
import argparse
import pandas as pd
from pyspark.sql import SparkSession

# import mltable
# import tempfile
# from azureml.fsspec import AzureMachineLearningFileSystem
# from datetime import datetime
# from dateutil import parser


def main(data_window_start, data_window_end, input_data_uri, output_data_uri):
    print("main")

    spark = SparkSession.builder.appName("AccessParquetFiles").getOrCreate()
    print(spark)

    try:
        df = spark.read.mltable(input_data_uri)
    except Exception as ex:
        print("mltable - no")
        print(ex)

    print("++++++++")

    try:
        df = spark.read.json(input_data_uri)
        print(df)
    except Exception as ex:
        print("json - no")
        print(ex)

    print("++++++++")

    try:
        df = mltable.from_json_lines_files(input_data_uri, invalid_lines='error', include_path_column=True)
        print(df)
    except Exception as ex:
        print("mltable json - no")
        print(ex)

    print("++++++++")

    try:
        df = mltable.from_json_lines_files(paths=[{"pattern": f"{input_data_uri}**/*.csv"}], invalid_lines='error', include_path_column=True)
        print(df)
    except Exception as ex:
        print("mltable json vpattern - no")
        print(ex)

    print("++++++++")

    try:
        df = mltable.from_paths(input_data_uri, invalid_lines='error', include_path_column=True)
        print(df)
    except:
        print("mltable paths - no")
        print(ex)

    print("++++++++")

    try:
        df = mltable.from_paths(paths=[{"pattern": f"{input_data_uri}**/*.csv"}], invalid_lines='error', include_path_column=True)
        print(df)
    except:
        print("mltable paths - no")
        print(ex)

    print("++++++++")

    output_df = spark.createDataFrame(pd.DataFrame([], index=[0], columns=["prediction"]))
    output_df.write.option("output_format", "parquet").option("overwrite", True).mltable(output_data_uri)

    print("++++OUT++++")
    print(output_df)
    print("++++++++")

    print("Finished.")


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-window-start", type=str, help="Data window start-time in ISO8601 format")
    parser.add_argument("--data-window-end", type=str, help="Data window end-time in ISO8601 format")
    parser.add_argument("--input-data-uri", type=str, help="Production inference data registered as data asset")
    parser.add_argument("--output-data-uri", type=str, help="Tabular dataset, which matches a subset of baseline data schema.")
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':

    import sys
    print(sys.argv)
    print("----------")
    args = parse_args()
    print(args)
    print("----------")
    print(os.listdir())
    print("----------")

    main(
        data_window_start=args.data_window_start,
        data_window_end=args.data_window_end,
        input_data_uri=args.input_data_uri,
        output_data_uri=args.output_data_uri,
    )
