from mlops.release.Release import ReleaseCandidate


class MLFLowCandidate(ReleaseCandidate):

    def __init__(self, run_id):
        super(MLFLowCandidate, self).__init__()
        self.mlflow_id = run_id

    def run(self):
        pass

    def get_artifacts(self):
        pass
