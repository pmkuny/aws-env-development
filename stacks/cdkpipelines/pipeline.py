from multiprocessing import connection
import aws_cdk as cdk
import os
import logging
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

from stacks.cdkpipelines.stages import Cloud9EnvironmentStage, InfraStage

class CdkPipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Make sure our connection ARN is set before trying to execute the Pipeline
        self.connection_arn = f'arn:aws:codestar-connections:us-west-2:{os.environ.get("CDK_DEFAULT_ACCOUNT")}:connection/3141d1db-68ad-41a9-a9b1-7c454498a6a2'

        self.pipeline =  CodePipeline(self, "Pipeline", 
                        synth=ShellStep("Synth", 
                            input=CodePipelineSource.connection(
                                repo_string="pmkuny/aws-env-development", 
                                branch="develop", 
                                connection_arn=self.connection_arn,
                                trigger_on_push=True),
                            commands=[
                                "npm install -g aws-cdk", 
                                "python -m pip install -r requirements.txt", 
                                "cdk synth"
                            ]
                        )
                    )
        
        self.infra_stage = self.pipeline.add_stage(
            InfraStage(
                self,
                "InfraStage"
            )
        )
        
        # TODO: Figure out sourcing from CodePipeline raw source (not synth'd assets)
#        self.infra_stage.add_post(
#            ShellStep(
#                "IntegrationTests",
#                input=CodePipelineSource.connection(
#                    repo_string="pmkuny/aws-env-development", 
#                    branch="develop", 
#                    connection_arn=self.connection_arn,
#                    trigger_on_push=True),
#                commands=["python3 tests/integration/teamcity_reachability/main.py"]
#                )
#            )
        
# Deploy our Cloud9 Environment for Developmnet
        self.pipeline.add_stage(
            Cloud9EnvironmentStage(
                self,
                "Cloud9EnvironmentStage"
            )
        )
        
