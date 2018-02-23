import os
import re
import discord
import asyncio
import urllib.request
import aiohttp
import json
import datetime
import time
import random
import aiofiles
import psycopg2

def safe_div(x,y):
    if y > 0:
        return (float(x)/float(y)) * 100
    else:
        return float(0.00)



class TestPoll(object):
    def __init__(self,server,message_obj,poll_msg,choice1,choice2,choice3,choice4):
        self.poll_message = poll_msg
        self.choices = [choice1,choice2,choice3,choice4]
        self.voters = []
        self.choice_text = "1⃣: %s\n2⃣: %s\n3⃣: %s\n4⃣: %s" % tuple(self.choices)
        self.server = server
        self.message_obj = message_obj
        self.one = 0
        self.one_voters = []
        self.two = 0
        self.two_voters = []
        self.three = 0
        self.three_voters = []
        self.four = 0
        self.four_voters = []

    def generate_text(self):
        self.choice_text = "`%.3d%%` 1⃣: %s\n`%.3d%%` 2⃣: %s\n`%.3d%%` 3⃣: %s\n`%.3d%%` 4⃣: %s" % (safe_div(self.one,len(self.voters)),
                                                                                self.choices[0],
                                                                                safe_div(self.two,len(self.voters)),
                                                                                self.choices[1],
                                                                                safe_div(self.three,len(self.voters)),
                                                                                self.choices[2],
                                                                                safe_div(self.four,len(self.voters)),
                                                                                self.choices[3])
        full_msg = self.poll_message + "\n" + self.choice_text + "\n"
        #full_msg += str(self.one) + " - " + str(self.two) + " - " + str(self.three) + " - " + str(self.four)
        return full_msg

    def __str__(self):
        return self.generate_text()

class PollBot(discord.Client):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.poll_messages = []
        self.published_messages = []

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        for channel in self.get_all_channels():
            async for msg in self.logs_from(channel,limit=1000):
                if msg.author == self.user:
                    self.published_messages.append(msg)

    async def on_reaction_add(self,reaction,user):
        if reaction.message.author == self.user and user != self.user:
            test_poll = None
            for m in self.poll_messages:
                if m.message_obj == reaction.message.id:
                    test_poll = m
            if reaction.emoji == "1⃣" and test_poll:
                if not user in test_poll.voters:
                    test_poll.voters.append(user)
                    test_poll.one_voters.append(user)
                    test_poll.one += 1
            elif reaction.emoji == "2⃣" and test_poll:
                if not user in test_poll.voters:
                    test_poll.voters.append(user)
                    test_poll.two_voters.append(user)
                    test_poll.two += 1
            elif reaction.emoji == "3⃣" and test_poll:
                if not user in test_poll.voters:
                    test_poll.voters.append(user)
                    test_poll.three_voters.append(user)
                    test_poll.three += 1
            elif reaction.emoji == "4⃣" and test_poll:
                if not user in test_poll.voters:
                    test_poll.voters.append(user)
                    test_poll.four_voters.append(user)
                    test_poll.four += 1
            if test_poll:
                await self.edit_message(reaction.message,test_poll.generate_text())


    async def on_reaction_remove(self,reaction,user):
        if reaction.message.author == self.user and user != self.user:
            test_poll = None
            for m in self.poll_messages:
                if m.message_obj == reaction.message.id:
                    test_poll = m

            if reaction.emoji == "1⃣" and test_poll:
                if user in test_poll.voters and user in test_poll.one_voters:
                    test_poll.voters.remove(user)
                    test_poll.one_voters.remove(user)
                    test_poll.one -= 1
            elif reaction.emoji == "2⃣" and test_poll:
                if user in test_poll.voters and user in test_poll.two_voters:
                    test_poll.voters.remove(user)
                    test_poll.two_voters.remove(user)
                    test_poll.two -= 1
            elif reaction.emoji == "3⃣" and test_poll:
                if user in test_poll.voters and user in test_poll.three_voters:
                    test_poll.voters.remove(user)
                    test_poll.three_voters.remove(user)
                    test_poll.three -= 1
            elif reaction.emoji == "4⃣" and test_poll:
                if user in test_poll.voters and user in test_poll.four_voters:
                    test_poll.voters.remove(user)
                    test_poll.four_voters.remove(user)
                    test_poll.four -= 1
            if test_poll:
                await self.edit_message(reaction.message,test_poll.generate_text())

    async def on_message(self,message):
        if self.user in message.mentions:
            reg = re.match(r'.*?"(.+?)"\s*?"(.+?)"\s*?"(.*?)"\s*?"(.*?)"\s*?"(.+?)"',message.content)
            poll_msg = "`POLL`\n"
            choice1 = ""
            choice2 = ""
            choice3 = ""
            choice4 = ""
            if reg:
                if reg.group(1):
                    poll_msg += "%s\n" % reg.group(1)
                else:
                    print("no group 1")
                if reg.group(2):
                    choice1 = reg.group(2)
                if reg.group(3):
                    choice2 = reg.group(3)
                if reg.group(4):
                    choice3 = reg.group(4)
                if reg.group(5):
                    choice4 = reg.group(5)
                self.poll_messages.append(TestPoll(message.server,None,poll_msg,choice1,choice2,choice3,choice4))
                msg = await self.send_message(message.channel,self.poll_messages[-1].generate_text()+"\n")
                self.poll_messages[-1].message_obj = msg.id
                await self.add_reaction(msg,"1⃣")
                await self.add_reaction(msg,"2⃣")
                await self.add_reaction(msg,"3⃣")
                await self.add_reaction(msg,"4⃣")
            else:
                msg = await self.send_message(message.channel,'Usage:```"<Question>"\n"<answer 1>"\n"<answer 2>"\n"<answer 3>"\n"<answer 4>"')



if __name__=="__main__":
    client = PollBot()
    client.run('MzgyNjc1NDk2OTg4ODM1ODQx.DPZJ1w.BA2yE4df3q5Vn5tJ6GjHNyUcoZw')
