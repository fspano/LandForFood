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
import csv
import numpy as np
import math
from common import utilities as ut

class FoodType:
    """Class that will calculate all the yields thata are necesssary for the land requirements"""
    def __init__(self):
      self.theIngredients={}
      self.theYields={}
      #        self.theName = "noFood"
      #        self.theUsage="N"
      #        self.theHealtyQuantityPerDay=[]        

    
      self.theAverageYieldAndLand=[]
      self.theVariableNames=[]            
      #  constants to calculate averages
      #     scale the yield from Hg/Ha to grams/m^2
      #       Hg=100g; 1he    ctar =10000m^2 > Hg/Ha= 100g/10000m^2= 1/100 g/m^2  
      self.scaleFromHgPerHaToGramsPerM2=1./100.
      # number of days in a year
      self.DayInAYear=365.
      self.theAverageLand=-1.
      self.dTheAverageLand=-1.
      self.theRMSLand=-1.
      self.dTheRMSLand=-1.        
      self.infoLandUpdated=False
      # setting the name of the food type        
      #        def setName(self,theName):
      #            self.theName = theName
      # check if this is really what you want to do
      
      #      def setHealthyQuantityPerdDay(self, healthyQuantityPerDay):
      #            self.theHealthyQuantityPerDay = healthyQuantityPerDay
      #        def setUsage(self,usage):
      #            self.theUsage = usage
      #        def getHealthyQuantityPerdDay(self)
      #            return self.ingredients["QB"]        
      #        def getName(self):
      #            return self.ingredients["foodType"]
       
    def isToBeUsed(self):
        if self.ingredients["usage"]=="Y":
            usageFlag=True
        else:
            usageFlag=False
        return usageFlag
    
    
#        def setVariableNames(self, variableNames):
#            self.theVariableNames=theVariableNames

    def loadIngredients(self,foodtype,ingredients):
      # get the yields
      # save the ingredients  in the appropriate dictionary 
      self.theIngredients=ingredients            
      # fil the yields in the appropriate dictionary
      self.getYields(ingredients["filename"])
      #        ingredients ingredients["filename"]
      #        ingredients["foodType"]
      #        ingredients["usage"]
      #        ingredients["QB"]
      #        theYields=self.getYields(ingredients["filename"])
      #        self.theIngredients[foodType]=theYields
      
    def getYields(self,csvYieldsFile):
    # TODO THIS FUNCTION NEEDS IMPROVEMENT : 
    # make it a ditionarty of dictionaries using ideas from https://stackoverflow.com/questions/8550912/python-dictionary-of-dictionaries
# and from https://www.python-course.eu/dictionaries.php abourt the use of zip  i.e. dictinarty from lists
    # mnake so that I realize what I want to have in calculateAverageLand for the line where I have  elif (theYear != None && theCountry != None):
    # the rest willl follow
    
    
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

      positionOfCountryName=-1
      positionOfUnitsforYield=-1
      positionOfUnitsforYield=-1
      positionOfYield=-1
      positionOfYear=-1
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
        #theYields={}
        
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
              # copy the list into the dictionary with a key corresponding to the
              #contry name
              # technical detail: to copy the list to another one, notice that
              #                   one uses a=list(b) to generate a new list
              #                   in fact a=b betwen two lists is just assigning
              #                   the reference
              #                   to the same list to two different names
              #                   see https://stackoverflow.com/questions/2612802/how-to-clone-or-copy-a-list
              self.theYields[CountryForList]=list(infoList)
              # I could have made it anbother dictionary i.e. something like suggested
              #  in https://stackoverflow.com/questions/8550912/python-dictionary-of-dictionaries                
              # empty the list
              del infoList[:]
              # assign a new name to the country
              CountryForList=row[positionOfCountryName]
                
              # extract the Unit, the year and the Yield from the current row,
              # make a dictionary associated to them and save the dictionary in a list
              Unit=row[positionOfUnitsforYield]
              Year=row[positionOfYear]
              Yield=row[positionOfYield]
              # it is alist of dictionaries
              infoList.append({"Year":Year,"Unit":Unit,"Yield":Yield})
              # set the dictionary
              #self.theYields=theYields
              
              #TODO as maybe an improvement
              # an alternative is to generate a dictionary where the key is a tuple (CountryForList,Year,X....)
              # and the result is the Yield  or in generat a list with more results
              # the tuple is immutable
              # and the the value is the Yield
              # the dictonary wil then contain 
              
              
              # TODO
              # 1 add uncertainties ONLY AFTER THE rest is calculated and working
              # given a certain type of food and the necessary quantity per day
              # one calculates the average Yield and the associated land
              # 2 add  calculateAverageYieldAndLand(self):
        
        #def calculateOverallAverageLand(self,healthyQuanPerDay):      
    def getLand(self,year=None,country=None):
        # one needs to check if the status of the calculation is set and updated
        if self.infoLandUpdated == False:
          self.calculateAverageLand(year,country)
        return self.theAverageLand
      
    def getLandUnc(self,year=None,country=None):    
        if self.infoLandUpdated == False:
          self.calculateAverageLand(year,country)
        return self.dTheAverageLand

    def getLandRMS(self,year=None,country=None):
        # one needs to check if the status of the calculation is set and updated
        if self.infoLandUpdated == False:
          self.calculateAverageLand(year,country)
        return self.theRMSLand
      
    def getLandRMSUnc(self,year=None,country=None):    
        if self.infoLandUpdated == False:
          self.calculateAverageLand(year,country)
        return self.dTheRMSLand


      
    
    def calculateAverageLand(self,theYear=None,theCountry=None):
      #TODO IMPROVE THIS HWNE YOU IMPROVEGET YIELDS and you have ditionary of dictionaries
      # now
      # for country, infoList in self.theYields.iteritems()
      
      # this that this can also be done with list comprehension
      # ---------------1---------------------------------------
      
      
      if (theYear != None and theCountry == None):
          ## first way to do it
          #--------------------------
          #theYearYieldsList=[]
          # loop over the list of dictionaries associated countries: each dictionary carries info for one country i.e. years and yields
          #for yieldInfo in self.theYields.values():
          ##loop over the dictionaries : each dictionary carries a year and a yield 
          #    for yieldVal in yieldInfo.values():
          ## check the year and save only on that case
          #        if theYear in yieldVal["Year"]:
          #            theYearYieldsList.append(float(yieldVal["Yield"]))
          #theListOfYields=np.array(theYearYieldsList)
          ## second way to do it
          theYields=np.array([float(yieldVal["Yield"]) for yieldInfo in self.theYields.values() for yieldVal in yieldInfo if theYear in yieldVal["Year"]])
      elif (theYear == None and theCountry != None):
          ## first way to do it
          #--------------------------
          #theCountryYieldsList=[]
          # if the country of interest in amongst those that are in the list of keys
          #loop over the list of dictionaries associated countries: each dictionary carries info for one country i.e. years and yields
          #if theCountry in self.theYields.keys():
          #    # select the country and the associated list of dictionaries
          #    yieldInfo=theYields[theCountry]
          #    # loop over all the dictionaries , each associated to a year and a yield save all the yileds fro all the years assocaited to the given country
          #    for yieldVal in yieldInfo:
          #         theCountryYieldList.append(float(yieldVal["Yield"]))
          #theListOfYields=np.array(theCountryYieldsList)
          
          ## second way to do it
          if theCountry in self.theYields.keys():
              theYields=np.array([float(yieldVal["Yield"])  for yieldVal in theYields[theCountry]])
              
      elif (theYear != None and theCountry != None):
          # make it simple
          # TODO:CHECK THIS 
          # when I improve this I want  to get it like
          # 1) three dictionaries  in cascade
          #  theYields.np.array(float(theYields[theCountry][theYear]["Yield"]))
          # or
          # 2) two dictionaries followed by a list of which the zero element is the yield
          # theYields.np.array(float(theYields[theCountry][theYear][0]))
          # the
          # transform quantities to float, to be on teh safe side when you do ratios 
          theYields=np.array([float(yieldVal["Yield"])  for yieldVal in theYields[theCountry] if theYear in yieldVal["Year"]  ])                             
      else:
         # this include salso the case where both are different from zero which is not an average  so it is replace by the global average 
         #               if (theYear == None && theState == None):
         # first way to do it
         #--------------------------
         #                theYieldsList=[]
         #                # this gives ingredients to derive the average yield and land over the years for a given country
         #                for yieldInfo in self.theYields.values():
         #                    #  yieldInfo is a list of dictionaries
         #                    # if I loop over it I get dictionaries 
         #                    for yieldVal in yieldInfo:
         #                      theYieldsList.append(yieldVal["Yield"])
         #                theListOfYields=np.array(theCountryYieldsList)
         # second way to do it
         # transform quantities to float, to be on teh safe side when you do ratios 
          theYields=np.array([float(yieldVal["Yield"]) for yieldInfo in self.theYields.values()  for yieldVal in yieldInfo])
    #                theYields=np.array([yieldInfo["Yield"] for yieldInfo in self.theYields[theState]])
    
    # The yields is dQ/dAdT; quantity of grams per year so I need the quantity DeltaQ to be for a year
    # the QB is daily so we need the QB per year
    # TODO: have a list of QB values depending on the diet and perosnw e nee dto feed: QB changes if you are an adult and in changes depending on your weight, in principle, QB has an uncertainty!! it need to e factored in
    # deltaQ=QB*DayInAYear
    #  A     Int (dA/dQ) dQ= A ~ 1/(dQ/dA) *DeltaQ= QB*DayInAYear/Yield= Area  
    # scale the yields to g/m^2
    # use broadcasting https://docs.scipy.org/doc/numpy-1.10.0/user/basics.broadcasting.html
      scaledYields=self.scaleFromHgPerHaToGramsPerM2*theYields
    # calculate the inverse of  the yields : the input is a float (https://docs.scipy.org/doc/numpy/reference/generated/numpy.reciprocal.html)
    # TODO: check there are no zeros in scaled Yield: use suggestions from https://stackoverflow.com/questions/26248654/numpy-return-0-with-divide-by-zero
      inverseYield=np.reciprocal(scaledYields)
    # calculate the quantity that is required for this food in a year
      scale=self.theIngredients["QB"]*self.DayInAYear
    # divide the quantity one needs  in a year by the yield per             
      theLands=scale*inverseYield
    # this is only the "statistical" unceratinty form the average
    #  TODO : include  uncertainty on the QB so add QB uncertainty as an info in the  initial ingredients file, important to give a mdoel
    #         for that uncertainty it need sto be the parameter for the model i.e. it can be a log normal and so teh accosiated parameter, a Gaussian,
    #         the vaue can be in percentage. one need sto check if there are unceratinties that are due to other sources
    #         it is possible that adiferent average function is needed so as  to contain info about the PDF one chooses
      theAverageLand,dTheAverageLand=ut.average(theLands)
      theRMSLand,dTheRMSLand=ut.rms(theLands)
      self.theAverageLand=theAverageLand
      self.dTheAverageLand=dTheAverageLand
      self.theRMSLand=theRMSLand
      self.dTheRMSLand=dTheRMSLand
      self.infoLandUpdated=True
    
