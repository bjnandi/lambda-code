import json
import urllib3

http = urllib3.PoolManager()

def lambda_handler(event, context):
    print("EVENT RECEIVED:", json.dumps(event))

    try:
        sns_message_str = event['Records'][0]['Sns']['Message']
        sns_message = json.loads(sns_message_str)  # convert string to dict
        detail = sns_message['detail']

        print("DETAIL DEBUG:", json.dumps(detail))

        user = detail.get('userIdentity', {}).get('arn', 'Unavailable')
        ip = detail.get('sourceIPAddress', 'Unavailable')
        time = detail.get('eventTime', 'Unavailable')

        print("Success: Login data extracted.")

    except KeyError as e:
        print(f"Missing key in event: {e}")
        user = ip = time = 'Unavailable'
    except Exception as e:
        print(f"Unexpected error: {e}")
        user = ip = time = 'Unavailable'

    slack_url = "https://hooks.slack.com/services/T08ULTB9"  # replace with your real Slack Webhook
    message = {
        "text": f":lock: *AWS Login Alert*\n*User:* {user}\n*IP:* {ip}\n*Time:* {time}"
    }
    encoded_msg = json.dumps(message).encode('utf-8')
    response = http.request('POST', slack_url, body=encoded_msg)

    return {
        'statusCode': 200,
        'body': response.data.decode('utf-8')
    }
