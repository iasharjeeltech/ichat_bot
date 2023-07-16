#This example requires the 'message_content' intent.
#App id: 1126615946149240923
#PUBLIC KEY: 6aef1f887901d543d71db2922fd2cf1d2bc4c08bce52eaf56ba7ea39c94ff8e2

import discord
import os
import openai

file = "1"
match file:
    case "1":
        file = "chat1.txt"
    case "2":
        file = "chat2.txt"
    case "3":
        file = "chat3.txt"
    case _:
        print("Invalid choice.")
        exit()

with open(file, "r") as f:
    chat = f.read()
openai.api_key = os.getenv("OPENAI_API_KEY")

token = os.getenv("SECRET_KEY")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        global chat
        try:
            chat += f"{message.author}: {message.content}\n"
            print(f"Message from {message.author}: {message.content}")
            if self.user != message.author:
                if self.user in message.mentions:
                    response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=f"{chat}\nI_Chat: ",
                        temperature=1,
                        max_tokens=256,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )
                    channel = message.channel
                    messageToSend = response.choices[0].text
                    await channel.send(messageToSend)
        except Exception as e:
            print(e)
            chat = ""

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
