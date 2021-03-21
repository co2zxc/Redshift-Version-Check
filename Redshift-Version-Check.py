import boto3
import os
import json
import time
from datetime import date
today = str(date.today().isoformat())
DBInstanceIdentifier_environ = str(os.environ['DBInstanceIdentifier'])
redshiftClusterIdentifier_environ = str(os.environ['redshiftClusterIdentifier'])
snsarn_environ = str(os.environ['snsarn'])
rdsclient = boto3.client('rds')
redshiftclient = boto3.client('redshift')
snsclient = boto3.client('sns')

def lambda_handler(event, context):
    
    response = rdsclient.describe_db_instances(
    DBInstanceIdentifier=DBInstanceIdentifier_environ
)
    DBInstance_EngineVersion = str(response['DBInstances'][0]['EngineVersion'])
    
    response2 = redshiftclient.describe_clusters(
        ClusterIdentifier=redshiftClusterIdentifier_environ
    )
    
    redshiftCluster_ClusterVersion = str(response2['Clusters'][0]['ClusterVersion'])
    redshiftCluster_ClusterRevisionNumber = str(response2['Clusters'][0]['ClusterRevisionNumber'])
    redshiftCluster_Currentclusterversion = redshiftCluster_ClusterVersion + "."+ redshiftCluster_ClusterRevisionNumber
    
    sns_message = json.dumps({'Check-date':today,'DBInstance_EngineVersion' : DBInstance_EngineVersion , 'redshiftCluster_Currentclusterversion': redshiftCluster_Currentclusterversion})
    
    response3 = snsclient.publish(
        TopicArn=snsarn_environ,
        Message=json.dumps({"default": sns_message}),
        Subject='RDS and Redshift Engine version check',
        MessageStructure='json'
    )
    
    return {
        'statusCode': 200,
        'body': sns_message
    }
