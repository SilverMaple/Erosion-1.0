# -*- coding=utf-8 -*-
from unittest import TestCase


class TestBagSwitch(TestCase):

    def setUp(self):
        self.p = Player()
        self.p.name = 'playername'
        self.bag = Bag(self.p)

    def tearDown(self):
        del self.p

    def test_switchItemBack(self):
        # self.fail()
        self.switchItemBack_1()
        self.switchItemBack_2()
        self.switchItemBack_3()
        self.switchItemBack_4()
        print self.p.name

    '''
    1.    current_item == -1 and gameState == ‘pause’
    2.    current_item != -1 and gameState == ‘pause’
    3.    current_item == -1 and gameState != ‘pause’
    4.    current_item != -1 and gameState != ‘pause’
    5.    current_item == 0
    6.    current_item != 0
    '''

    # 1, 6
    def switchItemBack_1(self):
        self.bag.current_item = -1
        self.bag.item_num = 3
        self.p.game.gameState = 'pause'
        self.bag.switchItemFor()
        self.assertEqual(self.bag.items[self.current_item].goods.picture, None, 'assert_1')

    # 2, 5
    def switchItemBack_2(self):
        self.bag.current_item = 0
        self.bag.item_num = 3
        self.p.game.gameState = 'pause'
        self.bag.switchItemFor()
        self.assertEqual(self.bag.items[self.current_item].goods.picture, None, 'assert_2')

    # 3, 6
    def switchItemBack_3(self):
        self.bag.current_item = -1
        self.bag.item_num = 3
        self.p.game.gameState = ''
        self.bag.switchItemFor()
        self.assertEqual(self.bag.items[self.current_item].goods.picture, None, 'assert_3')

    # 4, 5
    def switchItemBack_4(self):
        self.bag.current_item = 0
        self.bag.item_num = 3
        self.p.game.gameState = ''
        self.bag.switchItemFor()
        self.assertEqual(self.bag.items[self.current_item].goods.picture, 'imageSrc', 'assert_4')

    '''
    1. current_item == -1 and gameState == ‘pause’
    2. current_item != -1 and gameState == ‘pause’
    3. current_item == -1 and gameState != ‘pause’
    4. current_item != -1 and gameState != ‘pause’
    5. current_item == item_num - 1
    6. current_item != item_num – 1
    '''

    def test_switchItemFor(self):
        # self.fail()
        self.switchItemFor_1()
        self.switchItemFor_2()
        self.switchItemFor_3()
        self.switchItemFor_4()
        print self.p.name

    # 1, 5
    def switchItemFor_1(self):
        self.bag.current_item = -1
        self.bag.item_num = 0
        self.p.game.gameState = 'pause'
        self.bag.switchItemFor()
        self.assertEqual(self.bag.items[self.current_item].goods.picture, None, 'assert_1')

    # 2, 6
    def switchItemFor_2(self):
        self.bag.current_item = 0
        self.bag.item_num = 3
        self.p.game.gameState = 'pause'
        self.bag.switchItemFor()
        self.assertEqual(self.bag.items[self.current_item].goods.picture, None, 'assert_2')

    # 3, 5
    def switchItemFor_3(self):
        self.bag.current_item = -1
        self.bag.item_num = 0
        self.p.game.gameState = ''
        self.bag.switchItemFor()
        self.assertEqual(self.bag.items[self.current_item].goods.picture, None, 'assert_3')

    # 4, 5
    def switchItemFor_4(self):
        self.bag.current_item = 0
        self.bag.item_num = 3
        self.p.game.gameState = ''
        self.bag.switchItemFor()
        self.assertEqual(self.bag.items[self.current_item].goods.picture, 'imageSrc', 'assert_4')




class Player:
    def __init__(self):
        self.name = ''