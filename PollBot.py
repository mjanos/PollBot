import os
import re
import discord
import asyncio
import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,JSON
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import Base, Poll
from Settings import POLLBOT_KEY


class PollBot(discord.Client):
    def __init__(self,*args,**kwargs):
        db_user = "postgres"
        db_pass = "#4#si8imp"
        db_name = "pollsdb"
        engine = create_engine("postgresql+psycopg2://%s:%s@localhost/%s" % (db_user,db_pass,db_name))
        Base.metadata.create_all(engine)

        Base.metadata.bind = engine

        self.DBSession = sessionmaker(bind=engine)
        self.session = self.DBSession()

        super().__init__(*args,**kwargs)

    async def on_ready(self):
        print('Logged in as %s' % self.user.name)
        print(self.user.id)
        print('------')
        for channel in self.get_all_channels():
            async for msg in self.logs_from(channel,limit=1000):
                if msg.author == self.user:
                    self.messages.append(msg)

    async def on_reaction_add(self,reaction,user):
        print("got reaction")
        print(reaction.message.author)
        print(self.user)
        if reaction.message.author == self.user and user != self.user:
            test_poll = test_poll = self.session.query(Poll).filter_by(message_obj=str(reaction.message.id)).one()
            if reaction.emoji == "1⃣" and test_poll:
                if str(user) in test_poll.voters:
                    if str(user) in test_poll.two_voters:
                        test_poll.two_voters = [u for u in test_poll.two_voters if u != str(user)]
                        test_poll.two -= 1
                    if str(user) in test_poll.three_voters:
                        test_poll.three_voters = [u for u in test_poll.three_voters if u != str(user)]
                        test_poll.three -= 1
                    if str(user) in test_poll.four_voters:
                        test_poll.four_voters = [u for u in test_poll.four_voters if u != str(user)]
                        test_poll.four -= 1
                    if not str(user) in test_poll.one_voters:
                        test_poll.one_voters = test_poll.one_voters + [str(user)]
                        test_poll.one += 1
                else:
                    test_poll.voters = test_poll.voters + [str(user)]
                    test_poll.one_voters = test_poll.one_voters + [str(user)]
                    test_poll.one += 1
            elif reaction.emoji == "2⃣" and test_poll:
                if str(user) in test_poll.voters:
                    if str(user) in test_poll.one_voters:
                        test_poll.one_voters = [u for u in test_poll.one_voters if u != str(user)]
                        test_poll.one -= 1
                    if str(user) in test_poll.three_voters:
                        test_poll.three_voters = [u for u in test_poll.three_voters if u != str(user)]
                        test_poll.three -= 1
                    if str(user) in test_poll.four_voters:
                        test_poll.four_voters = [u for u in test_poll.four_voters if u != str(user)]
                        test_poll.four -= 1
                    if not str(user) in test_poll.two_voters:
                        test_poll.two_voters = test_poll.two_voters + [str(user)]
                        test_poll.two += 1
                else:
                    test_poll.voters = test_poll.voters + [str(user)]
                    test_poll.two_voters = test_poll.two_voters + [str(user)]
                    test_poll.two += 1
            elif reaction.emoji == "3⃣" and test_poll:
                if str(user) in test_poll.voters:
                    if str(user) in test_poll.one_voters:
                        test_poll.one_voters = [u for u in test_poll.one_voters if u != str(user)]
                        test_poll.one -= 1
                    if str(user) in test_poll.two_voters:
                        test_poll.two_voters = [u for u in test_poll.two_voters if u != str(user)]
                        test_poll.two -= 1
                    if str(user) in test_poll.four_voters:
                        test_poll.four_voters = [u for u in test_poll.four_voters if u != str(user)]
                        test_poll.four -= 1
                    if not str(user) in test_poll.three_voters:
                        test_poll.three_voters = test_poll.three_voters + [str(user)]
                        test_poll.three += 1
                else:
                    test_poll.voters = test_poll.voters + [str(user)]
                    test_poll.three_voters = test_poll.three_voters + [str(user)]
                    test_poll.three += 1
            elif reaction.emoji == "4⃣" and test_poll:
                if str(user) in test_poll.voters:
                    if str(user) in test_poll.one_voters:
                        test_poll.one_voters = [u for u in test_poll.one_voters if u != str(user)]
                        test_poll.one -= 1
                    if str(user) in test_poll.two_voters:
                        test_poll.two_voters = [u for u in test_poll.two_voters if u != str(user)]
                        test_poll.two -= 1
                    if str(user) in test_poll.three_voters:
                        test_poll.three_voters = [u for u in test_poll.three_voters if u != str(user)]
                        test_poll.three -= 1
                    if not str(user) in test_poll.four_voters:
                        test_poll.four_voters = test_poll.four_voters + [str(user)]
                        test_poll.four += 1
                else:
                    test_poll.voters = test_poll.voters + [str(user)]
                    test_poll.four_voters = test_poll.four_voters + [str(user)]
                    test_poll.four += 1
            if test_poll:
                print("poll found")
                self.session.commit()
                await self.edit_message(reaction.message,test_poll.generate_text())
            else:
                print("poll NOT found")


    async def on_reaction_remove(self,reaction,user):
        if reaction.message.author == self.user and user != self.user:
            test_poll = self.session.query(Poll).filter_by(message_obj=str(reaction.message.id)).one()
            if reaction.emoji == "1⃣" and test_poll:
                if str(user) in test_poll.voters and str(user) in test_poll.one_voters:
                    test_poll.voters = [u for u in test_poll.voters if u != str(user)]
                    test_poll.one_voters = [u for u in test_poll.one_voters if u != str(user)]
                    test_poll.one -= 1
            elif reaction.emoji == "2⃣" and test_poll:
                if str(user) in test_poll.voters and str(user) in test_poll.two_voters:
                    test_poll.voters = [u for u in test_poll.voters if u != str(user)]
                    test_poll.two_voters = [u for u in test_poll.two_voters if u != str(user)]
                    test_poll.two -= 1
            elif reaction.emoji == "3⃣" and test_poll:
                if str(user) in test_poll.voters and str(user) in test_poll.three_voters:
                    test_poll.voters = [u for u in test_poll.voters if u != str(user)]
                    test_poll.three_voters = [u for u in test_poll.three_voters if u != str(user)]
                    test_poll.three -= 1
            elif reaction.emoji == "4⃣" and test_poll:
                if str(user) in test_poll.voters and str(user) in test_poll.four_voters:
                    test_poll.voters = [u for u in test_poll.voters if u != str(user)]
                    test_poll.four_voters = [u for u in test_poll.four_voters if u != str(user)]
                    test_poll.four -= 1
            if test_poll:
                self.session.commit()
                await self.edit_message(reaction.message,test_poll.generate_text())

    async def on_message(self,message):
        if self.user in message.mentions:
            reg = re.match(r'.*?"(.+?)"\s*?"(.+?)"\s*?"(.*?)"\s*?"(.*?)"\s*?"(.+?)"',message.content)
            poll_msg = ""
            choice1 = ""
            choice2 = ""
            choice3 = ""
            choice4 = ""
            if reg:
                if reg.group(1):
                    poll_msg += "%s\n" % reg.group(1)
                if reg.group(2):
                    choice1 = reg.group(2)
                if reg.group(3):
                    choice2 = reg.group(3)
                if reg.group(4):
                    choice3 = reg.group(4)
                if reg.group(5):
                    choice4 = reg.group(5)

                new_test_poll = Poll(server=str(message.server),
                                    poll_message=poll_msg,
                                    choices=[choice1,choice2,choice3,choice4],
                                    voters=[],
                                    one_voters=[],
                                    two_voters=[],
                                    three_voters=[],
                                    four_voters=[]
                                    )
                self.session.add(new_test_poll)
                self.session.commit()
                msg = await self.send_message(message.channel,new_test_poll.generate_text()+"\n")
                new_test_poll.message_obj = msg.id
                self.session.commit()

                await self.add_reaction(msg,"1⃣")
                await self.add_reaction(msg,"2⃣")
                await self.add_reaction(msg,"3⃣")
                await self.add_reaction(msg,"4⃣")
            else:
                reg = None
                reg = re.match(r'.*?\sp([0-9]+)$',message.content)
                if reg:
                    if not reg.group(1) is None:
                        #poll_msg += "%s\n" % reg.group(1)
                        print("Input %s" % (reg.group(1)))
                        msg = await self.send_message(message.channel,'Not Implemented yet but you will be able to close the poll this way.')

                else:
                    msg = await self.send_message(message.channel,'Usage:```"<Question>"\n"<answer 1>"\n"<answer 2>"\n"<answer 3>"\n"<answer 4>"```')



if __name__=="__main__":


    client = PollBot()
    client.run(POLLBOT_KEY)
