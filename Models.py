import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,JSON, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def safe_div(x,y):
    if y > 0:
        return (float(x)/float(y)) * 100
    else:
        return float(0.00)

Base = declarative_base()
class Poll(Base):
    __tablename__ = 'polls'
    id = Column(Integer,primary_key=True)
    poll_message = Column(String(1000),nullable=True)
    choices = Column(JSON)
    voters = Column(JSON)
    server = Column(String(255))
    message_obj = Column(String(255))
    one = Column(Integer,default=0)
    one_voters = Column(JSON)
    two = Column(Integer,default=0)
    two_voters = Column(JSON)
    three = Column(Integer,default=0)
    three_voters = Column(JSON)
    four = Column(Integer,default=0)
    four_voters = Column(JSON)
    author = Column(String(100),nullable=True)
    closed = Column(Boolean,default=False)

    def generate_text(self):
        if self.closed:
            closed_text = " CLOSED"
        else:
            closed_text = ""
        choice_text = "`%.3d%% (%s)` 1⃣: %s\n`%.3d%% (%s)` 2⃣: %s\n" % (safe_div(self.one,len(self.voters)),
                                                                                self.one,
                                                                                self.choices[0],
                                                                                safe_div(self.two,len(self.voters)),
                                                                                self.two,
                                                                                self.choices[1])
        if self.choices[2]:
            choice_text += "`%.3d%% (%s)` 3⃣: %s" % (safe_div(self.three,len(self.voters)),
                                self.three,
                                self.choices[2])
        if self.choices[3]:
            choice_text += "\n`%.3d%% (%s)` 4⃣: %s" % (safe_div(self.four,len(self.voters)),
                                self.four,
                                self.choices[3])
        full_msg = "`Poll p" + str(self.id) + closed_text + "`\n" + self.poll_message + "\n" + choice_text + "\n\n`Created by " + self.author + "`"
        return full_msg
