import json
import boto3
from time import gmtime, strftime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CloudResourceTable')
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

def lambda_handler(event, context):
    users = int(event['users'])
    
    vm_count = users // 10
    storage = Decimal(users * 0.5)
    
    response = table.put_item(
        Item={
            'ID': str(users),
            'VMCount': vm_count,
            'StorageGB': storage,
            'Timestamp': now
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'resources': f'{vm_count} VMs, {storage} GB Storage'})
    }
