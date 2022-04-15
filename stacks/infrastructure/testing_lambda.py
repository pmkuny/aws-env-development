import aws_cdk.aws_lambda as lambda_
from aws_cdk import Stack

from constructs import Construct

class TestingLambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id , **kwargs)
        
#        teamcity_reachability_lambda = lambda_.Function(
#            self,
#            "TestingFunction",
#            runtime=lambda_.Runtime.PYTHON_3_9,
#            )