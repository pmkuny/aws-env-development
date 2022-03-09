from email.mime import image
from constructs import Construct
from aws_cdk import (
    aws_ecr as ecr,
    Stack,
    CfnOutput,
)

class EcrStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id)

        self.repository = ecr.Repository(
            self,
            "PrivateRepository",
            image_scan_on_push=True,
        )

        CfnOutput(
            self,
            "EcrRepositoryUrl",
            value=self.repository.repository_uri,
        )