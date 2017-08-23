"""Tests for slackmentions."""
import unittest
from slackperson import SlackPerson
from slackperson import SlackDataError
import slackmentions


USERLIST = {"members": [
    {
        "color": "ffffff",
        "id": "U00000001",
        "name": "jbiden",
        "profile": {
            "email": "jbiden@whitehouse.gov",
            "first_name": "Joe",
            "last_name": "Biden",
            "real_name": "Joe Biden",
            "real_name_normalized": "Joe Biden",
            "team": "T00000001",
            "title": ""
        },
        "real_name": "Joe Biden",
        "team_id": "T00000001",
        "tz": "America/New_York",
        "tz_label": "Eastern Daylight Time",
        "tz_offset": -14400,
    },
    {
        "color": "000000",
        "id": "U00000002",
        "name": "bobama",
        "profile": {
            "email": "bobama@whitehouse.gov",
            "first_name": "Barack",
            "last_name": "Obama",
            "real_name": "Barack Obama",
            "real_name_normalized": "Barack Obama",
            "team": "T00000001"
        },
        "real_name": "Barack Obama",
        "team_id": "T00000001",
        "tz": "America/New_York",
        "tz_label": "Eastern Daylight Time",
        "tz_offset": -14400,
    },
],
}

TESTTEXT1 = 'hey @jbiden, give me a call'
TESTTEXT2 = 'tell @jbiden and @bobama that I have a cool idea'
TESTTEXT3 = "tell @dtrump that he's not in our team."


class TestSlackMentions(unittest.TestCase):
    """Tests slackmentions."""
    def setUp(self):
        """Set up some SlackPerson objects to use in tests."""
        self.biden = SlackPerson('jbiden', USERLIST)
        self.obama = SlackPerson('bobama', USERLIST)

    def test_findperson(self):
        """Tests the findperson method."""
        # test fine one person
        test_people = slackmentions.findpeople(TESTTEXT1, USERLIST)
        assert len(test_people) == 1
        assert test_people[0].userid == 'U00000001'

        # test find two people
        test_people2 = slackmentions.findpeople(TESTTEXT2, USERLIST)
        assert len(test_people2) == 2
        assert test_people2[1].userid == 'U00000002'

        # test error raised
        self.assertRaises(
            SlackDataError,
            slackmentions.findpeople,
            TESTTEXT3,
            USERLIST
        )

        # test error swallowed
        self.assertListEqual(
            slackmentions.findpeople(TESTTEXT3, USERLIST, silent=True),
            []
        )

    def test_mention_text(self):
        """Tests mention_text."""
        # test with people
        self.assertEqual(
            slackmentions.mention_text(TESTTEXT2,
                                       people=[self.obama, self.biden]),
            'tell <@U00000001> and <@U00000002> that I have a cool idea')

        # test with userlist
        self.assertEqual(
            slackmentions.mention_text(TESTTEXT2,
                                       userlist=USERLIST),
            'tell <@U00000001> and <@U00000002> that I have a cool idea')

        # raises an error
        self.assertRaises(
            SlackDataError,
            slackmentions.mention_text,
            TESTTEXT3,
            userlist=USERLIST
        )

        # swallows the error
        self.assertEqual(
            slackmentions.mention_text(
                TESTTEXT3,
                userlist=USERLIST,
                silent=True),
            TESTTEXT3
        )

        # Illegal Arguments
        self.assertRaises(
            ValueError,
            slackmentions.mention_text,
            TESTTEXT1
        )

    def test_clean_text(self):
        """Test cleaning the text of mentions."""
        # working correctly
        self.assertEqual(
            slackmentions.clean_text(TESTTEXT1, userlist=USERLIST),
            'hey, give me a call')

        self.assertEqual(
            slackmentions.clean_text(TESTTEXT1, people=[self.obama,
                                                        self.biden]),
            'hey, give me a call')

        self.assertEqual(
            slackmentions.clean_text(TESTTEXT2, people=[self.obama,
                                                        self.biden]),
            'tell and that I have a cool idea')

        self.assertEqual(
            slackmentions.clean_text('@bobama hi', people=[self.obama]),
            'hi')

        # raise a SlackDataError
        self.assertRaises(
            SlackDataError,
            slackmentions.clean_text,
            TESTTEXT3,
            userlist=USERLIST
        )

        # swallow the error
        self.assertEqual(
            slackmentions.clean_text(TESTTEXT3, userlist=USERLIST,
                                     silent=True),
            "tell @dtrump that he's not in our team."
        )

        # nuke everything
        self.assertEqual(
            slackmentions.clean_text(TESTTEXT3, clean_all=True),
            "tell that he's not in our team."
        )

        # Illegal argument combination
        self.assertRaises(
            ValueError,
            slackmentions.clean_text,
            TESTTEXT1
        )
