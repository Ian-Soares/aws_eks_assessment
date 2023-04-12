import boto3
import os
import textwrap
#from kubernetes import client, config

client = boto3.client('eks')
directory_path = f'{os.getcwd()}/markdown'

def check_if_exists(directory_path, file_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    if not os.path.exists(file_path):
        return False
    
    return True

def describe_cluster(cluster):
    response = client.describe_cluster(
        name = f'{cluster}'
    )

    file_path=f'{directory_path}/{cluster}.md'
    
    with open(file_path, 'a') as f:
        f.write(textwrap.dedent(f"""
        # {response['cluster']['name']}
        ## Cluster informations:
        - Cluster Version: {response['cluster']['version']}
        - Cluster ARN: {response['cluster']['arn']}
        - Cluster VPC: {response['cluster']['resourcesVpcConfig']['vpcId']}
        - Cluster Subnet IDs: {response['cluster']['resourcesVpcConfig']['subnetIds']}
        - Cluster Security Group IDs: {response['cluster']['resourcesVpcConfig']['securityGroupIds']}, {response['cluster']['resourcesVpcConfig']['clusterSecurityGroupId']}
        - Cluster Identity OIDC issuer: {response['cluster']['identity']['oidc']['issuer']}
        - Service Ipv4 CIDR: {response['cluster']['kubernetesNetworkConfig']['serviceIpv4Cidr']}
        """))
    return 

def get_nodes(cluster):
    nodegroups = client.list_nodegroups(clusterName=cluster)
    response = []
    for ng in nodegroups['nodegroups']:
        response.append(client.describe_nodegroup(clusterName=cluster, nodegroupName=ng)['nodegroup'])
    
    file_path=f'{directory_path}/{cluster}.md'
    
    for ng in response:
        with open(file_path, 'a') as f:
            f.write(textwrap.dedent(f"""
            ## NodeGroup "{ng['nodegroupName']}"
            - Version: {ng['version']} ({ng['releaseVersion']})
            - NodeGroup ARN: {ng['nodegroupArn']}
            - Instance Types: {ng['instanceTypes']}
            - AMI Type: {ng['amiType']}
            - Subnets: {ng['subnets']}
            - Capacity Type: {ng['capacityType']}
            Scaling Config:
                - Minimum: {ng['scalingConfig']['minSize']}
                - Maximum: {ng['scalingConfig']['maxSize']}
                - Desired: {ng['scalingConfig']['desiredSize']}
            """))

    return response

def get_namespaces():
    return

def get_deployments():
    return

def get_ingress():
    return

def get_ports():
    return

def generate_markdown():
    return

