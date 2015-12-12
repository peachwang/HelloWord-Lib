# -*- coding: utf-8 -*-  
import sys, os; sys.path.extend([os.path.abspath(_[0]) for _ in os.walk(os.path.join(os.getcwd(), '../'))]);
from util import *

# class Morphy
# 
# @property 
# 
# @method dict getInfo(str wordForm)
# @method list getBaseForms(str wordForm)
# @method list getMorphyForms(str wordForm, str morphyType = None)
class Morphy :

    def __init__(self) :
        # load data from local files or MongoDB
        pass

    # Gets info of a word.
    # @param str wordForm
    # @return dict
    def getInfo(self, wordForm) :
        pass

    # Gets base forms of a word.
    # @param str wordForm
    # @return list
    #   <baseForm str>
    def getBaseForms(self, wordForm) :
        pass

    # Gets morphy forms of a word
    # @param str wordForm
    # @param str morphyType
    # @return dict
    #   <morphyTypes str> []
    #       <morphyForm str>
    def getMorphyForms(self, wordForm, morphyType = None) :
        pass

