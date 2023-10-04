import os
import argparse

from pyspark.sql import SparkSession, functions as f


def main(data_window_start, data_window_end, input_data_uri, output_data_uri):
    print("main")

    # Read training data
    input_train_sdf = read_input_trainingdata(input_data_uri)
    print(f"Total rows processed: {input_train_sdf.count()}")
    print("Schema:")
    print(input_train_sdf, "\n")

    # No filtering if data is training data - whole period should be used for comparing.
    # Filter window
    output_sdf = input_train_sdf
    print(f"Rows after (no) filtering: {output_sdf.count()}")
    print("Schema:")
    print(output_sdf, "\n")

    output_sdf.write.format('parquet').option('overwrite', True).mltable(output_data_uri)

    print("Finished.")


def read_input_trainingdata(input_data_uri):

    train_sdf = (spark
        .read.format('csv')
        .option('header', 'true')
        .load(f'{input_data_uri}/*.csv')
    )

    return train_sdf


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-window-start", type=str, help="Data window start-time in ISO8601 format")
    parser.add_argument("--data-window-end", type=str, help="Data window end-time in ISO8601 format")
    parser.add_argument("--input-data-uri", type=str, help="Production inference data registered as data asset")
    parser.add_argument("--output-data-uri", type=str, help="Tabular dataset, which matches a subset of baseline data schema.")
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':

    args = parse_args()

    spark = SparkSession.builder.appName("monitoringdataprep").getOrCreate()

    main(
        data_window_start=args.data_window_start,
        data_window_end=args.data_window_end,
        input_data_uri=args.input_data_uri,
        output_data_uri=args.output_data_uri,
    )
