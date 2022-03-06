# Create Poll model (python class)
# to make it easier for different parts of our app to communicate

# At the moment our code deals in:
# Polls
# Options
# Votes
# Users
# And in this case, we create model class for Poll & Option
# Now votes -> already quite simple / Users -> just attached to votes

from typing import List
from connection_pool import get_connection
from models.test_option import OptionTest
import Finaldatabase


class PollTest:
    def __init__(self, title: str, owner: str, _id: int = None):
        self.id = _id  # set to None : auto-created <-- SERIAL
        self.title = title
        self.owner = owner

    def __repr__(self):
        return f'Poll({self.title!r}, {self.owner!r}, {self.id!r})'

    def save(self):
        with get_connection() as connection:
            new_poll_id = Finaldatabase.create_poll(connection, self.title, self.owner)
            self.id = new_poll_id

    def add_option(self, option_text: str):
        OptionTest(option_text, self.id).save()

    @property
    def options(self) -> List[OptionTest]:
        with get_connection() as connection:
            options = Finaldatabase.get_poll_options(connection, self.id)
            return [OptionTest(option[1], option[2], option[0]) for option in options]

    @classmethod
    def get(cls, poll_id: int) -> 'PollTest':
        with get_connection() as connection:
            poll = Finaldatabase.get_poll(connection, poll_id)
            return cls(poll[1], poll[2], poll[0])

    @classmethod
    def all(cls) -> List['PollTest']:
        with get_connection() as connection:
            polls = Finaldatabase.get_polls(connection)
            return [cls(poll[1], poll[2], poll[0]) for poll in polls]

    @classmethod
    def latest(cls) -> 'PollTest':
        with get_connection() as connection:
            latest_poll = Finaldatabase.get_latest_poll(connection)
            return cls(latest_poll[1], latest_poll[2], latest_poll[0])


# poll_example = Poll('Python vs JavaScript', 'devjson')
# print(poll_example)
