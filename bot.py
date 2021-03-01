import os
import discord
# from dotenv import load_dotenv

# load_dotenv()
# TOKEN = os.getenv('ODE2MDA1NjI5NzEzODQyMTg3.YD0qdg.js0Z1_F9eDVd1W8clw3f74pHXsU')
TOKEN = "ODE2MDA1NjI5NzEzODQyMTg3.YD0qdg.js0Z1_F9eDVd1W8clw3f74pHXsU"

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)