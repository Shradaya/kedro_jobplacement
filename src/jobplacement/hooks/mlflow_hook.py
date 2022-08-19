from pluggy import HookspecMarker, HookimplMarker
import mlflow
from mlflow.tracking import MlflowClient

hook_spec = HookspecMarker("kedro")
hook_impl = HookimplMarker("kedro")


class MlflowHook:
    def __init__(self, experiment_name, artifact_repository):
        self.experiment_name = experiment_name
        self.artifact_repository = artifact_repository

    def create_experiment(self):
        experiment_name = self.experiment_name
        artifact_repository = self.artifact_repository
        client = MlflowClient()
        try:
            experiment_id = client.create_experiment(
                experiment_name, artifact_location=artifact_repository
            )
        except:
            experiment_id = client.get_experiment_by_name(experiment_name).experiment_id
        return experiment_id

    @hook_impl
    def before_pipeline_run(self) -> None:
        print("This is the start of the pipeline")
        experiment_id = self.create_experiment()
        mlflow.start_run(experiment_id=experiment_id)

    @hook_impl
    def after_pipeline_run(self):
        print("The pipeline run has ended.")
        mlflow.end_run()
