import aws_cdk as core
import aws_cdk.assertions as assertions

from stacks.cdkpipelines.pipeline import *

def test_cdk_pipelines():
    # We pass a GITHUB_CONNECTION_ARN context in order to allow Stack creation to happen, since it's a required value.
    app = core.App(context={"GITHUB_CONNECTION_ARN": "1"})
    stack = CdkPipelineStack(app, "CdkPipelineStack")
    template = assertions.Template.from_stack(stack)

    # Test: Make sure a CodePipeline resource is being created
    template.resource_count_is(type="AWS::CodePipeline::Pipeline",count=1)

    