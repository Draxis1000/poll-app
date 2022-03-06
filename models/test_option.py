from typing import List
from connection_pool import get_connection
import Finaldatabase


class OptionTest:
    def __init__(self, text: str, poll_id: int, _id: int = None):
        self.text = text
        self.poll_id = poll_id
        self.id = _id

    def __repr__(self):
        return f'{self.text!r}, {self.poll_id!r}, {self.id!r}'

    def save(self):
        with get_connection() as connection:
            new_option_id = Finaldatabase.add_option(connection, self.text, self.poll_id)
            self.id = new_option_id

    @classmethod
    def get(cls, option_id: int) -> 'OptionTest':
        with get_connection() as connection:
            option = Finaldatabase.get_option(connection, option_id)
            return cls(option[1], option[2], option[0])

    def vote(self, username: str):
        with get_connection() as connection:
            Finaldatabase.add_poll_vote(connection, username, self.id)

    @property
    def votes(self) -> List[Finaldatabase.Vote]:
        with get_connection() as connection:
            votes = Finaldatabase.get_votes_for_option(connection, self.id)
            return votes
