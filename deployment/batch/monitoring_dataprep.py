"""Entry script for Model Data Collector Data Window Component."""

import os
import argparse
import pandas as pd
from pyspark.sql import SparkSession, functions as f

import mltable
# import tempfile
# from azureml.fsspec import AzureMachineLearningFileSystem
# from datetime import datetime
# from dateutil import parser


def main(data_window_start, data_window_end, input_data_uri, output_data_uri):
    print("main")

    # Read batch predictions data
    input_preds_sdf = read_input_predictions(input_data_uri)
    print(f"Total rows processed: {input_preds_sdf.count()}")
    print("Schema:")
    print(input_preds_sdf, "\n")

    # Window start/end in ISO8601 format, example: '2023-10-03T13:12:52.037534Z'
    # Simulate like it's 2016 - same as use case data
    # Take date only bc predictions are scheduled daily - #TODO configure in monitor directly
    custom_window_start = f'2016-{data_window_start[5:10]} 00:00:00'
    custom_window_end = f'2016-{data_window_end[5:10]} 00:00:00'
    print(f'Window start: {data_window_start} => {custom_window_start}')
    print(f'Window end: {data_window_end} => {custom_window_end}')

    # Filter window
    output_sdf = (input_preds_sdf
        .filter(f.col('timestamp') >= custom_window_start)
        .filter(f.col('timestamp') <= custom_window_end)
        .select('prediction')
    )
    print(f"Rows after filtering: {output_sdf.count()}")
    print("Schema:")
    print(output_sdf, "\n")

    # output_sdf.write.option('output_format', 'parquet').option('overwrite', True).mltable(output_data_uri)
    output_sdf.write.format('parquet').option('overwrite', True).mltable(output_data_uri)

    print("Finished.")


def read_input_predictions(input_data_uri):

    preds_sdf = (spark
        .read.format('text')
        .load(f'{input_data_uri}/*/*/*/predictions.csv')
        .withColumn('value', f.from_json(f.col('value'), schema='array<string>'))
        .withColumn('filepath', f.input_file_name())
        .withColumn('dirpath', f.regexp_extract(f.col('filepath'), f'{input_data_uri}(.*)/predictions.csv', 1))
        .select(
            f.to_timestamp(f.col('dirpath'), format='yyyy/MM/dd').alias('timestamp'),
            f.col('value')[0].alias('inputfile'),
            f.col('value')[1].astype('float').alias('prediction')
        )
    )

    return preds_sdf


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

    import pyspark
    print(">>> pyspark version:")
    print(pyspark.__version__)

    spark = SparkSession.builder.appName("monitoringdataprep").getOrCreate()
    print(spark)

    main(
        data_window_start=args.data_window_start,
        data_window_end=args.data_window_end,
        input_data_uri=args.input_data_uri,
        output_data_uri=args.output_data_uri,
    )
