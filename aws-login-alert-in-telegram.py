import json
import urllib3

http = urllib3.PoolManager()

def lambda_handler(event, context):
    try:
        sns_msg = json.loads(event['Records'][0]['Sns']['Message'])
        detail = sns_msg['detail']
        user = detail['userIdentity']['arn']
        ip = detail['sourceIPAddress']
        time = detail['eventTime']
    except Exception as e:
        print(f"Error parsing event: {e}")
        user = ip = time = 'Unavailable'

    message = f"🔐 *AWS Login Alert*\n👤 *User:* {user}\n🌐 *IP:* {ip}\n🕒 *Time:* {time}"
    telegram_token = "7560083477:ABCD" # replace with your telegram token
    chat_id = "12345" # replace with your telegram chat id
    
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = http.request("POST", url, body=json.dumps(data), headers={"Content-Type": "application/json"})
    print("Telegram response:", response.data)

    return {
        'statusCode': 200,
        'body': 'Alert sent to Telegram'
    }
