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


def main(data_window_start, data_window_end, input_data_path, output_data):
    print("main")

    spark = SparkSession.builder.appName("AccessParquetFiles").getOrCreate()
    print(spark)

    print("++++++++")
    print(os.listdir(input_data_path))
    print("++++++++")

    print("++++++++")
    print(os.listdir(output_data))
    print("++++++++")

    print("Finished.")


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-window-start", type=str, help="Data window start-time in ISO8601 format")
    parser.add_argument("--data-window-end", type=str, help="Data window end-time in ISO8601 format")
    parser.add_argument("--input-data-path", type=str, help="Production inference data registered as data asset")
    parser.add_argument("--output-data", type=str, help="Tabular dataset, which matches a subset of baseline data schema.")
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
        input_data_path=args.input_data_path,
        output_data=args.output_data,
    )
