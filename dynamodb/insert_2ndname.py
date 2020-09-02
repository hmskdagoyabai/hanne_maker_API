import boto3
from boto3.session import Session
import json
from boto3.dynamodb.conditions import Key, Attr

profile = 'hama'
session = Session(profile_name=profile)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('second_name')

with open("../json/katakana_fixed.json", 'r') as f:
    katakanas = json.load(f)

    with table.batch_writer(overwrite_by_pkeys=['id', 'second_name', "second_name_original", "caption"]) as batch:
        for (i, katakana) in enumerate(katakanas):
            insert_item = {
                "id": i,
                "second_name": katakana["2nd_name"],
                "second_name_original": katakana["2nd_name_original"],
                "caption": katakana["caption"]
            }

            batch.put_item(Item=insert_item)
