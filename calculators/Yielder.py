## Authors: Francesco Span\`o <francesco.spano@cern.ch>
# File and Version Information:#
#
# Description:class holding yields (gram/m^2) for a given food type
# as a function of time (year)  and space(country)
#
#Year of first generation: 2104 - October/November in C++,
#                          rewriting in python Jan 2017
#==============================================================================

from ROOT import TRandom, TFile, TH1D, TH1F
from sys import exit

class Yielder:
    """Class that will calculate all the yields thata are necesssary for the land requirements"""
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
        self.theIngredients={} 

        
    def setHealthyQuantityPerdDay(self, healthyQuantityPerDay):
            self.theHealthyQuantityPerDay =  healthyQuantityPerDay
    def setFoodType(self,foodType):
            self.foodType = foodType
    # check if this is really what you want to do
    def setUsage(self,usage):
        self.theUsage=usage
        
    def setVariableNames(self, variableNames):
        self.theVariableNames=theVariableNames


    def loadYields(self,foodtype,ingredients):
        # get the yields corresponding to a certain foof type
        # put them in the corresponding dictionary
        theYields=self.getYields(ingredients["filename"])
        self.theIngredients[foodType]=theYields
                
    #     
    def setYields(self,csvYieldsFile):
        csvfile=open(csvYieldsFile)
        yieldfile = csv.reader(csvfile, delimiter=',', quotechar='"')

        # get the rows
        listOfRows  = [row for row in yieldfile]
        firstrow=listOfRows[0]

        
        # find the position of the four quantities we are interested in:
        # 'Area' for the name of the country where the food is produced
        # 'Unit' for the units in qhich the yileds are expressed (usually hg/ha)
        # 'Value' for the numerical value of the yield
        # 'Year' for the year the production refers to
        #  THese 4 words are hard coded as one uses the structure
        # of the csv files  that one downloads from http://www.fao.org/faostat/en/#data/QC
        #
        # observation: strange that the other way of doing this dowes ont seem to be working i.e. 
        # positionOfCountryName = [idx for idx, word in enumerate(firstrow) if word == 'Area']
        
        for idx, word in enumerate(firstrow):
        #    print idx,word
        if word == 'Area':
            positionOfCountryName=idx
        if word == 'Unit':
            positionOfUnitsforYield=idx
        if word == 'Value':
            positionOfYield=idx
        if word == 'Year':
            positionOfYear=idx
            
        # define the dictionary that will hold all the yields info
        theYields={}

        # two stringes used to svae the name of the country in the loop         
        CountryForList=""
        
        # the list that contains the dictionary of 4 quantities shown above
        # once 
        infoList=[]
        # loop over the rows of the csv reader :each row contains
        # the info about the productionin one year in a given country
        for row in listOfRows:
            # skip the first row  where the definitions are 
            if row[0]=="Domain Code":
                continue
            #if the country name that was saved is the same as the name found in the incoming row
            #go on beyond the if,else construct
            if CountryForList == row[positionOfCountryName] :
                pass
             else:
            #if the country name that was saved is diferent from the name found in the incoming row
            # the list of rowas corresponding to a given country is over so
            # copy the list into the dictionary with a key corresponding to the contry name
            # technical detail: to copy the list to another one, notice that
            #                   one uses a=list(b) to generate a new list
            #                   in fact a=b betwen two lists is just assigning the reference
            #                   to the same list to two different names
            #                   see https://stackoverflow.com/questions/2612802/how-to-clone-or-copy-a-list
                theYields[CountryForList]=list(infoList)
                # empty the list
                del infoList[:]
                # assign a new name to the country
                CountryForList=row[positionOfCountryName]
            
            # extract the Unit, the year and the Yield from the current row,
            # make a dictionary associated to them and save the dictionary in a list
            Unit=row[positionOfUnitsforYield]
            Year=row[positionOfYear]
            Yield=row[positionOfYield]
            infoList.append({"Year":Year,"Unit":Unit,"Yield":Yield})
            
        # set the dictionary
        self.theYields=theYields

 # TODO add uncertaintie sONLY AFTER THE rest is calculated and working
 # given a certain type of food and the necessary quantity per day
 # one calculates the average Yield and the associated land
    def calculateAverageYieldAndLand(self,healthyQuanPerDay):



          
        
    def getAverageYieldAndLand(self):
        
    return
