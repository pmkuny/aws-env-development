import os
import logging
from aws_cdk import aws_aps as aps
from aws_cdk import Stack
from constructs import Construct

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)


class AmpStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id , **kwargs)
        
        development_workspace = aps.CfnWorkspace(
            self,
            "DevelopmentWorkspace",
            )