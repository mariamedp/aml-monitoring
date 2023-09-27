import os
import argparse

import joblib
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import sklearn.metrics as skmetrics


def main(data_path, model_path):

    mlflow.sklearn.autolog()

    print("Reading training data...")
    data_file = os.path.join(data_path, 'energydemand_2012-2016.csv')
    data_raw = pd.read_csv(data_file)

    print("Data preparation...")
    data_clean = dataprep(data_raw)
    mlflow.log_metric('training_size', len(data_clean))

    # Direct training just to get a working model
    print("Training model...")
    model = RandomForestRegressor(
        n_estimators=500,
        criterion='friedman_mse',
        max_depth=50,
        min_samples_split=10,
        min_samples_leaf=2,
        random_state=2023
    )
    model.fit(data_clean.drop(columns='demand'), data_clean['demand'])

    print(f"Saving model in folder {model_path}...")
    model_file = os.path.join(model_path, 'model.pkl')
    with open(model_file, 'wb') as f:
        joblib.dump(model, f)

    print('Finished.')


def dataprep(raw_data):

    data = raw_data.rename(columns={'timeStamp': 'timestamp'})
    data['timestamp'] = pd.to_datetime(data.timestamp)

    # Additional features
    data['hour'] = data.timestamp.dt.hour
    data['dayofmonth'] = data.timestamp.dt.day
    data['dayofweek'] = data.timestamp.dt.dayofweek
    data['dayofyear'] = data.timestamp.dt.dayofyear
    data['weekofyear'] = data.timestamp.dt.isocalendar().week
    data['year'] = data.timestamp.dt.year

    data = data.set_index('timestamp')
    data = data[data.index < '2015-01-01']

    return data


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-path', type=str, required=True)
    parser.add_argument('--model-path', type=str, required=True)
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(
        data_path=args.data_path,
        model_path=args.model_path
    )
