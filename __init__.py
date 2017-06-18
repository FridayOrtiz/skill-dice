from os.path import dirname
import os

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import read_stripped_lines
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
        dice = message.data.get("Dice")
        if "sided" not in dice and "d" in dice:
            feedback = self.feedback[randrange(len(self.feedback))]
            dice = dice.split("d")
            dice_phrase = dice[0] + " " + dice[1] + " sided dice"
            dice_array = []
            for i in range(int(dice[0])):
                dice_array.append(randint(1, int(dice[1])))
            dice_string = ''
            for i in dice_array:
                dice_string = dice_string + " " + str(i)
            dice_string += " for a total of " + str(sum(dice_array))
            sentence = feedback.replace('<dice>', dice_phrase)\
                .replace('<results>', dice_string)
            self.speak(sentence)
        elif "sided" in dice:
            feedback = self.feedback[randrange(len(self.feedback))]
            dice = dice.split("sided")
            dice = dice[0].split(" ")
            dice_phrase = dice[0] + " " + dice[1] + " sided dice"
            dice_array = []
            for i in range(int(dice[0])):
                dice_array.append(randint(1, int(dice[1])))
            dice_string = ''
            for i in dice_array:
                dice_string = dice_string + " " + str(i)
            dice_string += " for a total of " + str(sum(dice_array))
            sentence = feedback.replace('<dice>', dice_phrase)\
                .replace('<results>', dice_string)
            self.speak(sentence)
        else:
            self.speak("Please use RPG dice notation.")

    def stop(self):
        pass


def create_skill():
    return RollSkill()
