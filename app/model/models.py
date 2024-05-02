from sqlalchemy import Column, Integer, String, Text, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, unique=False, index=True)

    def to_json_object(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }

    def __str__(self):
        return ("{" +
                "id: " + str(self.id) +
                ", username: " + self.username +
                ", password: " + self.password +
                "}")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    user_name = Column(String(50))
    created_at = Column(Time)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(
        "User",
        backref=backref("messages", uselist=False),
        uselist=False
    )

    def to_json_object(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'user_name': self.user_name,
            'created_at': self.created_at.strftime("%H:%M") if self.created_at else None
        }

    def __str__(self):
        return ("{" +
                "id: " + str(self.id) +
                ", user_id: " + str(self.id) +
                ", content: " + self.content +
                ", user_name: " + self.user_name +
                ", created_at: " + str(self.created_at) +
                "}")
