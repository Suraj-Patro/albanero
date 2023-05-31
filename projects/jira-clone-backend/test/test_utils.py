import unittest


class UtilsTestCase(unittest.TestCase):
    def test_mail(self):
        """
        GIVEN a email utility
        WHEN a recipient email, subject and content are given
        THEN send an email using SMTP via gmail
        """
        from util import mail
        pass
