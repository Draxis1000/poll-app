from typing import List
import psycopg2
from psycopg2.errors import DivisionByZero
from connection_pool import get_connection
import Finaldatabase
from models.test_poll import PollTest
from models.test_option import OptionTest
import random

MENU_PROMPT = """-- Menu --

1) Create new poll
2) List open polls
3) Vote on a poll
4) Show poll votes
5) Select a random winner from a poll option
6) Exit

Enter your choice: """
NEW_OPTION_PROMPT = "Enter new option text (or leave empty to stop adding options): "


def prompt_create_poll():
    poll_title = input("Enter poll title: ")
    poll_owner = input("Enter poll owner: ")
    poll = PollTest(poll_title, poll_owner)
    poll.save()

    # Add options to poll
    while new_option := input(NEW_OPTION_PROMPT):
        poll.add_option(new_option)


def list_open_polls():
    for poll in PollTest.all():
        print(f"{poll.id}: {poll.title} (created by {poll.owner})")


def prompt_vote_poll():
    poll_id = int(input("Enter poll would you like to vote on: "))
    poll_options = PollTest.get(poll_id).options
    _print_poll_options(poll_options)

    option_id = int(input("Enter option you'd like to vote for: "))
    username = input("Enter the username you'd like to vote as: ")

    OptionTest.get(option_id).vote(username)


def _print_poll_options(options: List[OptionTest]):
    for option in options:
        print(f"{option.id}: {option.text}")


def show_poll_votes(connection):
    poll_id = int(input("Enter poll you would like to see votes for: "))
    poll = PollTest.get(poll_id)
    options = poll.options
    votes_per_option = [len(option.votes) for option in options]
    total_votes = sum(votes_per_option)

    try:
        for option, votes in zip(options, votes_per_option):
            percentage = votes / total_votes * 100
            print(f"{option.text} for {votes} ({percentage:.2f}% of total)")
    except ZeroDivisionError:
        print("No votes yet cast for this poll.")


def randomize_poll_winner(connection):
    poll_id = int(input("Enter poll you'd like to pick a winner for: "))
    poll = PollTest.get(poll_id)
    _print_poll_options(poll.options)

    option_id = int(input("Enter which is the winning option, we'll pick a random winner from voters: "))
    votes = OptionTest.get(option_id).votes
    winner = random.choice(votes)
    print(f"The randomly selected winner is {winner[0]}.")


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_votes,
    "5": randomize_poll_winner
}


def menu():
    with get_connection() as connection:
        Finaldatabase.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "6":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again.")


menu()
