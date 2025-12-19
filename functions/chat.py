import os
import json
from groq import Groq
from cerebras.cloud.sdk import Cerebras

def handler(event, context):
    # API Anahtarlarını kontrol et
    c_key = os.getenv("CEREBRAS_API_KEY")
    g_key = os.getenv("GROQ_API_KEY")

    if event['httpMethod'] == 'OPTIONS':
        return {'statusCode': 200, 'body': 'ok'}

    try:
        body = json.loads(event.get('body', '{}'))
        question = body.get('question', '')

        try:
            # Önce Cerebras dene
            client = Cerebras(api_key=c_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b",
                messages=[{"role": "system", "content": "Sen Aizonai AI'sın."}, {"role": "user", "content": question}]
            )
            reply = response.choices[0].message.content
        except:
            # Hata olursa Groq dene
            client = Groq(api_key=g_key)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": question}]
            )
            reply = response.choices[0].message.content

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'reply': reply})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
