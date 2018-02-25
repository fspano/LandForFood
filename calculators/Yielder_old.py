#//=====================================================================-*-C++-*-
# Authors: Francesco Span\`o <francesco.spano@cern.ch>
# File and Version Information:
#
#
#// Description:class holding yields (gram/m^2) for a given food type
# as a function of time (year)  and space(country)
#
#Year of generation: 2104 - October/November
#==============================================================================
#     // this contains < the type of food , the object containing yields as a function of the year nd of teh country>
#     // the question is:" do we want to make a map 
#     // or do we want to make an object?
#     // if we have a class the clas for each given food dtype can be
#     // asked questions
#     // mean production, spread, production including certain zones 
#     // or not, certain years or not, plot of time evolution of yield
#     // for a given country or the opverall time evolution summing over the
#      correlations or production with certain climate zones...yes
#     // iyt is worth making a class of objects 
#     //  nd eahc class also stores the name of the foot type
#     // then we make a map of these objects 

from ROOT import TRandom, TFile, TH1D, TH1F
from sys import exit

class YielderMy:
    """Class that will calculate all the yields thata re necesssary for the land requirements"""
    def __init__(self):
        self.DayInAYear=365.
        # //    scale the y    ield from Hg/Ha to grams/m^2
        #       Hg=100g; 1he    ctar =10000m^2 > Hg/Ha= 100g/10000m^2= 1/100 g/m^2
        self.scaleFromHgPerHaToGramsPerM2=1/100.
        self.theFoodType = "noFood"
        self.TheYields={}
        self.theAverageYieldAndLand=[]
        self.theUsage="N"
        self.theVariableNames=[]
        self.theHealtyQuantityPerDay=[]
    def setHealthyQuantityPerdDay(self, healthyQuantityPerDay):
            self.theHealthyQuantityPerDay =  healthyQuantityPerDay
    def setFoodType(self,foodType):
            self.foodType = foodType
    # check if this is really what you want to do
    def setUsage(self,usage):
        self.theUsage=usage
    def setVariableNames(slef, variableNames):
        self.theVariableNames=theVariableNames
            

    def setYields(self, csvYieldsFile):
#        with  open(csvYieldsFile,"r") as yieldsFile:
#         theYields = csv.reader(csvfile, delimiter=' ', quotechar='|')
#           for row in spamreader:
#        print ', '.join(row)
#Spam, Spam, Spam, Spam, Spam, Baked Beans
#Spam, Lovely Spam, Wonderful Spam
