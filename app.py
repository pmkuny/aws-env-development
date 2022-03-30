#!/usr/bin/env python3

## NOTE:
# Since we're using CDK Pipelines, there shouldn't be much reaason to deploy this app manually.

import os
import subprocess
import logging
import aws_cdk as cdk
import aws_cdk.aws_ssm as ssm
from stacks.cdkpipelines.pipeline import CdkPipelineStack

# Infrastructure Components
from stacks.infrastructure.eks_cluster import *
from stacks.infrastructure.networking import *
from stacks.infrastructure.ecr import *
from stacks.infrastructure.efs import *

# CDK Pipelines Components
from stacks.cdkpipelines import *

# Set our Logging Level
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)



app = cdk.App()
stage = app.node.try_get_context('stage')

cdkpipeline_stack = CdkPipelineStack(
    app, 
    "CdkPipelineStack",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"]
    )
)


app.synth()
