from reviewer.git_client import GH

from unittest import TestCase



class TestAIClient(TestCase):
    def setUp(self):
        return super().setUp()

    def test_collect_pr_patches(self):
        # Here we need to mock the GH.repo attribute
        pass

    def test_create_comment(self):
        # Here we need to mock the same GH.repo as the test above
        # perhaps different subattributes though
        pass