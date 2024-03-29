# Mock entry point
import mlflow
import torch
import os


def test():
    # Very basic ML project - creates and saves a pytroch model to mlflow

    print('test entry point')
    mlflow.set_tracking_uri('http://0.0.0.0:85')
    with mlflow.start_run() as run:

        model = torch.nn.Linear(3, 2)
        x = torch.rand(1, 3)
        y = model(x)
        model = mlflow.pytorch.log_model(model, 'test_model', registered_model_name="test-model",)
        print(f'model logged at {model.model_uri}')


if __name__ == '__main__':
    test()
