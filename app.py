from flask import Flask, Response, request
import discord

app = Flask(__name__)
ssl_context=('/etc/letsencrypt/live/www.jamesearl.co.uk/fullchain.pem', '/etc/letsencrypt/live/www.jamesearl.co.uk/privkey.pem')

bot = discord

@app.route('/discord/valheim/webhook', methods=['POST'])
def hello():
    print(request.json)
    return Response(status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, ssl_context=ssl_context)