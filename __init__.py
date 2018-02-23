from os.path import dirname, join
import os
import re

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import read_stripped_lines
from mycroft.util import play_mp3
from random import randrange
from random import randint
__author__ = "Friday811"

LOGGER = getLogger(__name__)


class RollSkill(MycroftSkill):
    def __init__(self):
        super(RollSkill, self).__init__(name="RollSkill")
        self.feedback = read_stripped_lines(dirname(__file__) +
                                            '/dialog/' + self.lang + '/roll.dialog')

    def initialize(self):
        self.load_data_files(dirname(__file__))

        roll_intent = IntentBuilder("RollIntent").\
            require("DiceKeyword").require("Dice").build()
        self.register_intent(roll_intent, self.handle_roll_intent)

    def handle_roll_intent(self, message):
        feedback = self.feedback[randrange(len(self.feedback))]
        dice = message.data.get("Dice")
        dice = re.findall(r'\d+', dice)
        if len(dice) >= 2:
            num = dice[0]
            sides = dice[1]
            if num == '40':
                num = '4'
        elif len(dice) == 1:
            sides = '6'
            num = dice[0]
            if num == '46':
                num = '4'
        else:
            num = '1'
            sides = '6'
        dice_phrase = num + " " + sides + " sided dice"
        dice_array = []
        for i in range(int(num)):
            dice_array.append(randint(1, int(sides)))
        dice_string = ''
        for i in dice_array:
            dice_string = dice_string + " " + str(i)
        dice_string += ", the total is " + str(sum(dice_array))
        sentence = feedback.replace('<dice>', dice_phrase)\
            .replace('<results>', dice_string)
        self.process = play_mp3(join(dirname(__file__), "mp3", "dice.mp3"))
        self.process.wait()
        self.speak(sentence)

    def stop(self):
        pass

def create_skill():
    return RollSkill()
