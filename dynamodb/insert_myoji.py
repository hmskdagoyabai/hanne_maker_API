import boto3
from boto3.session import Session
import json
from boto3.dynamodb.conditions import Key, Attr

profile = 'hama'
session = Session(profile_name=profile)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('myoji')

with open("../json/myoji.json", 'r') as f:
    myojis = json.load(f)

    for (i, myoji) in enumerate(myojis):
        insert_item = {
            "id": i,
            "name": myoji["name"],
            "name_read": myoji["name_read"],
            "rank": myoji["rank"]
        }

        table.put_item(Item=insert_item)
