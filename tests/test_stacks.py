import aws_cdk as core
import aws_cdk.assertions as assertions

from stacks.infrastructure.ecr import *
from stacks.infrastructure.eks_cluster import *
from stacks.infrastructure.monitoring import *
from stacks.infrastructure.networking import *
from stacks.infrastructure.efs import *

from stacks.cdkpipelines.pipeline import *
from stacks.cdkpipelines.app_stage import *


def create_stack_test_functions():
    app = core.App()
    stack_list = [
        EcrStack(app, "EcrStack"),
        InfrastructureEksCluster(app, "InfrastructureEksClusterStack"),
        KubernetesNetworkingStack(app, "KubernetesNetworkingStack"),
        ClusterFileSystemStack(app, "ClusterFileSystemStack")
    ]
    for stack in stack_list:
        def common_stacks_tests(child_stack=stack):
            app = core.App()
            template = assertions.Template.from_stack(child_stack)

