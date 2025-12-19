import os
import json
from groq import Groq
from cerebras.cloud.sdk import Cerebras

def handler(event, context):
    # Anahtarları Netlify Panelinden çekeceğiz (Buraya anahtar yazma!)
    c_key = os.getenv("CEREBRAS_API_KEY")
    g_key = os.getenv("GROQ_API_KEY")

    body = json.loads(event['body'])
    question = body.get('question', '')

    try:
        client = Cerebras(api_key=c_key)
        response = client.chat.completion.create(
            model="llama-3.3-70b",
            messages=[{"role": "system", "content": "Sen Aizonai AI'sın."}, {"role": "user", "content": question}]
        )
        reply = response.choices[0].message.content
    except:
        client = Groq(api_key=g_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": question}]
        )
        reply = response.choices[0].message.content

    return {
        'statusCode': 200,
        'body': json.dumps({'reply': reply})

    }
