# Mock entry point
import mlflow
import torch
import os


def test():

    print('test entry point')

    mlflow.pytorch.autolog(log_models=False)
    with mlflow.start_run() as run:

        model = torch.nn.Linear(3, 2)
        x = torch.rand(1, 3)
        y = model(x)
        model = mlflow.pytorch.log_model(model, 'test_model', registered_model_name="test-model",)
        print(f'model logged at {model.model_uri}')


if __name__ == '__main__':
    test()
