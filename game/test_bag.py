from unittest import TestCase


class TestBag(TestCase):
    def setUp(self):
        self.p = Player()
        self.p.name = 'playername'
        self.bag = Bag(self.p)

    def tearDown(self):
        del self.p

    def test_interact(self):
        # self.fail()
        self.test_interact_1()
        print self.p.name

    def test_interact_1(self):
        self.assertEqual('a', 'a', 'same2')


class Player:
    def __init__(self):
        self.name = ''