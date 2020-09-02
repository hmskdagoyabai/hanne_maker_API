import boto3
import random

dynamodb = boto3.resource('dynamodb')
myoji_table = dynamodb.Table('myoji')
secondname_table = dynamodb.Table('second_name')


def get_myoji_by_id(id):
    response = myoji_table.get_item(
        Key={
            'id': id
        }
    )

    try:
        return response['Item']
    except KeyError:
        return get_myoji_random()


def get_secondname_by_id(id):
    response = secondname_table.get_item(
        Key={
            'id': id
        }
    )
    try:
        return response['Item']
    except KeyError:
        return get_secondname_random()


def get_myoji_count():
    response = myoji_table.scan(Select='COUNT')
    return response['Count']


def get_secondname_count():
    response = secondname_table.scan(Select='COUNT')
    return response['Count']


def get_myoji_random():
    count = get_myoji_count()
    random_id = random.randrange(count)
    response = myoji_table.get_item(
        Key={
            'id': random_id
        }
    )
    return response['Item']


def get_secondname_random():
    count = get_secondname_count()
    random_id = random.randrange(count)
    response = secondname_table.get_item(
        Key={
            'id': random_id
        }
    )
    return response['Item']


def lambda_handler(event, context):
    if event['name_id'] != "":
        name = get_myoji_by_id(int(event['name_id']))
    elif event['name'] != "":
        name = {
            "name_read": "",
            "id": 99999,
            "name": event["name"],
            "rank": ""
        }
    else:
        name = get_myoji_random()

    if event['second_id'] != "":
        secondname = get_secondname_by_id(int(event['second_id']))
    else:
        secondname = get_secondname_random()

    result = {
        "name": name,
        "second_name": secondname,

    }

    return result
