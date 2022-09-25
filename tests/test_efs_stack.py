
import aws_cdk as core
import aws_cdk.assertions as assertions

from stacks.infrastructure.efs import *
from stacks.infrastructure.networking import *
from stacks.infrastructure.eks_cluster import *

def test_efs_stack():
    app = core.App()
    
    # Dependency Stacks created here
    network_stack = KubernetesNetworkingStack(app, "KubernetesNetworkStack", my_cidr="10.40.0.0/16")
    cluster_stack = InfrastructureEksCluster(app, "InfrastructureEksClusterStack", my_network_stack=network_stack)
    
    # Stack to be tested
    stack = ClusterFileSystemStack(app, "ClusterFileSystemStack", my_cluster_stack=cluster_stack, my_network_stack=network_stack)
    template = assertions.Template.from_stack(stack)
    
    