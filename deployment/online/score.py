import os
import logging
import json

import joblib
import pandas as pd
from azureml.ai.monitoring import Collector


def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global model
    global inputs_collector, outputs_collector

    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    # Please provide your model's folder name if there is one
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "mlflow-model/model.pkl")
    model = joblib.load(model_path)

    inputs_collector = Collector(name='model_inputs')
    outputs_collector = Collector(name='model_outputs')

    logging.info("Init complete")


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    logging.info("Request received")

    input_df = process_raw_data(raw_data)
    context = inputs_collector.collect(input_df)

    result = model.predict(input_df)
    output_df = pd.DataFrame(result, index=input_df.index, columns=["prediction"])
    outputs_collector.collect(output_df, context)  # Context allows inputs and outputs to be correlated later

    logging.info("Request processed")
    return result.tolist()


def process_raw_data(raw_data):

    try:
        input_data = json.loads(raw_data)["input_data"]
        data_pd = pd.DataFrame(
            data=input_data["data"],
            index=input_data["index"],
            columns=input_data["columns"]
        )
    except KeyError as ex:
        raise ValueError(f"Keyword missing in input data: {ex}") from ex

    return data_pd
