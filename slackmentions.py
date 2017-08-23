"""Defines functions for dealing with mentions in slack messages."""
import re
from slackperson import SlackPerson
from slackperson import SlackDataError


def findpeople(text, userlist, silent=False):
    """Finds username mentions in slack text and creates SlackPerson objects
    for those people. Returns a list of those SlackPerson objects.

    Arguments:
    text: text to find @ mentions in.
    userlist: output of slack api users.list
    silent: By default is users are not in the userlist,
    slackperson.SlackDataError will be raised. Set silent to True to swallow
    this error and ignore the bad mention.

    Returns: List of SlackPerson objects or empty list.
    """
    usernames = re.findall('@([a-zA-Z0-9-._]*)', text)
    person_list = []
    for user in usernames:
        try:
            person_list.append(SlackPerson(user, userlist))
        except SlackDataError:
            if not silent:
                raise
    return person_list


def mention_text(text, people=None, userlist=None, silent=False):
    """Replaces username mentions in text with user id mentions for tagging by
    slack api message sending.

    Arguments:
    text: The text containing @ mentions
    people: A list of SlackPerson objects for people found in the text. If not
    specified, one will be generated by passing text and userlist to
    findpeople. Required if userlist is not provided.
    userlist: The json from slack api users.list. Required if people is not
    provided.
    silent: If a user is found in the text and not in userlist,
    slackperson.SlackDataError will be raise. Set silent to True to suppress
    these errors. Does not apply is people is provided instead of userlist.
    """
    if people is None:
        if userlist is None:
            raise ValueError("Either people or userlist is required.")
        people = findpeople(text, userlist, silent=silent)
    for person in people:
        text = text.replace('@' + person.username,
                            '<@{}>'.format(person.userid, person.email))

    return text


def clean_text(text, people=None, userlist=None, silent=False,
               clean_all=False):
    """Deletes username mentions from a slack message.

    Arguments:
    text: The text containing @ mentions
    people: A list of SlackPerson objects for people found in the text. If not
    specified, one will be generated by passing text and userlist to
    findpeople. Required if userlist is not provided.
    userlist: The json from slack api users.list. Required if people is not
    provided.
    silent: If a user is found in the text and not in userlist,
    slackperson.SlackDataError will be raise. Set silent to True to suppress
    these errors. Does not apply is people is provided instead of userlist.
    clean_all: Clean all the mentions regardless of whether they are valid or
    not.
    """
    if clean_all:
        # if we just want to nuke them all, we don't care about the userlist or
        # people or anything
        text = re.sub('\s?@([a-zA-Z0-9-._])*', '', text)
        return text

    if people is None:
        if userlist is None:
            raise ValueError(
                "One of clean_all, people, and userlist is required.")
        people = findpeople(text, userlist, silent=silent)
    for person in people:
        text = re.sub('\s?@{}'.format(person.username), '', text).strip()

    return text
