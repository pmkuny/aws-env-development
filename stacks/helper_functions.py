
# Retrieve current workspace IP and and return as /32 CIDR value
from aws_cdk import aws_ssm as ssm
def get_ip(calling_stack):
    my_ip = ssm.StringParameter

    return f'{my_ip.value_for_string_parameter(calling_stack, parameter_name="/cdk/global/ip")}/32'