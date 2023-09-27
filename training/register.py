import os
import argparse

import joblib
import mlflow
from azureml.core import Run


def main(model_path, model_name):

    print("Registering model...")

    model_file = os.path.join(model_path, 'model.pkl')
    model = joblib.load(model_file)

    mlflow_model_path = 'mlflow-model'
    mlflow.sklearn.log_model(model, mlflow_model_path)
    # mlflow.register_model(f'file://{os.path.abspath(mlflow_model_path)}', model_name)  # Fails
    current_run_id = Run.get_context().get_details()['runId']
    mlflow.register_model(f'runs:/{current_run_id}/{mlflow_model_path}', model_name)

    print('Finished.')


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-path', type=str, required=True)
    parser.add_argument('--model-name', type=str, required=True)
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(
        model_path=args.model_path,
        model_name=args.model_name
    )
