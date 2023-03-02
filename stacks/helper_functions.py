
# Retrieve current workspace IP and and return as /32 CIDR value
from aws_cdk import aws_ssm as ssm
from aws_cdk import aws_iam as iam

def get_ip(calling_stack):
    my_ip = ssm.StringParameter

    return f'{my_ip.value_for_string_parameter(calling_stack, parameter_name="/cdk/global/ip")}/32'
    
def get_user_arn_from_ssm(calling_stack):
    my_arn = ssm.StringParameter
    
    return f'{my_arn.value_for_string_parameter(calling_stack, parameter_name="/cdk/global/assumed_arn")}'

def get_user_arn_from_iam(calling_stack):
    my_iam_role = iam.Role.from_role_name(calling_stack, "SSOReservedRole", role_name="AWSReservedSSO_AWSAdministratorAccess_03b9350052ec1191")
    print(my_iam_role.role_arn)
    return my_iam_role.role_arn