from unittest.mock import DEFAULT
import aws_cdk.aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct


class KubernetesNetworkingStack(Stack):
   def __init__(self, scope: Construct, id: str, my_cidr, **kwargs) -> None:
       super().__init__(scope, id)

       # K8s Subnet / VPC Configuration:
       # VPC: 10.40.0.0/16
       # Control-00: 10.40.10.0/28
       # Control-01: 10.40.20.0/28
       # Worker-00: 10.40.30.0/24
       # Worker-01: 10.40.40.0/24
       # Public-00: 10.40.98.0/27
       # Public-01: 10.40.99.0/27

       # Setup Subnet Configuration Groups - important to remember that this creates a SubnetGroup, with a subnet in each AZ
       self.control_subnets = ec2.SubnetConfiguration(
           name = 'Control',
           cidr_mask=28,
           subnet_type= ec2.SubnetType.PRIVATE_WITH_EGRESS,
           reserved= False
       )

       self.worker_subnets = ec2.SubnetConfiguration(
               name = 'Worker',
               cidr_mask=24,
               subnet_type = ec2.SubnetType.PRIVATE_WITH_EGRESS,
               reserved = False
           )

       self.public_subnets = ec2.SubnetConfiguration(
           name = 'Public',
           cidr_mask=27,
           map_public_ip_on_launch=True,
           subnet_type= ec2.SubnetType.PUBLIC,
           reserved = False
       )

       self.kubernetes_vpc = ec2.Vpc(self, 
       "Infrastructure-Kubernetes-KubernetesVpc", 
       #cidr=my_cidr,
       default_instance_tenancy=ec2.DefaultInstanceTenancy.DEFAULT,
       enable_dns_hostnames=True,
       enable_dns_support=True,
       flow_logs=None,
       gateway_endpoints=None,
       ip_addresses=ec2.IpAddresses.cidr(my_cidr),
       max_azs=2,
       nat_gateway_provider=ec2.NatProvider.gateway(),
       nat_gateways=1, # this is 1 PER AZ
       subnet_configuration=[self.public_subnets,self.control_subnets,self.worker_subnets],
       vpn_connections=None
       )
       

       self.controlplane_security_group = ec2.SecurityGroup(self, "ControlPlaneSecurityGroup", vpc=self.kubernetes_vpc)
       self.workerplane_security_group = ec2.SecurityGroup(self, "WorkerPlaneSecurityGroup", vpc=self.kubernetes_vpc) 
       self.public_security_group = ec2.SecurityGroup(self, "PublicPlaneSecurityGroup", vpc=self.kubernetes_vpc)





