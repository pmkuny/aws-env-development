from multiprocessing import connection
import aws_cdk as cdk
import os
import logging
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

from stacks.cdkpipelines.app_stage import AppStage

class CdkPipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Make sure our connection ARN is set before trying to execute the Pipeline
        self.connection_arn = f'arn:aws:codestar-connections:us-west-2:{os.environ.get("CDK_DEFAULT_ACCOUNT")}:connection/dec5cc18-a17b-496d-a4ef-363e509fae51'

        self.pipeline =  CodePipeline(self, "Pipeline", 
                        synth=ShellStep("Synth", 
                            input=CodePipelineSource.connection(
                                repo_string="pmkuny/aws-env-development", 
                                branch="develop", 
                                connection_arn=self.connection_arn,
                                trigger_on_push=True),
                            commands=[
                                "cd development/infra/cdk/",
                                "npm install -g aws-cdk", 
                                "python -m pip install -r requirements.txt", 
                                "cdk synth",
                                "mv cdk.out/ $CODEBUILD_SRC_DIR"
                            ]
                        )
                    )
        
        self.pipeline.add_stage(
            AppStage(
                self,
                "AppStage"
            )
        )