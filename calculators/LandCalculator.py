#=====================================================================-
# Authors: Francesco Span\`o <francesco.spano@cern.ch>
# File and Version Information:
#
#
#Description:Calculation of land extension necessary for a given diet
#  given a yield of food types yield of certain food types
#
#Year of generation: 2104 - October/November==> Fill rewriting in python on 7th jan 2017
#==============================================================================
# complete redefinition in python
# not necessarily to be used
from ROOT import TRandom, TFile, TH1D,TH1F
from sys import exit
from FoodType import FoodType
import numpy as np
import math

#if !defined(__CINT__) || defined(__MAKECINT__)
#include <iostream>
#using std::cout;
#using std::endl;

#include "TRandom.h"
#include "TFile.h"
#include "TH1D.h"
#include "TH1F.h"
#endif
#include "LandCalculator.h"



class LandCalculator:
# features of the class 
  """Class that will calculate the land requirementf for  a given diet"""
    
    # tyhis is teh alternative definition
    #def __init__(self,theListOfInputFiles):

  def __init__(self,noOverWrite=True):
      self.noOverWrite=noOverWrite  
      self.fileNamesList = ""
      #self.fileNamesList = theListOfInputFiles
      self.fileNames = []    
      self.foodTypes= []
      self.usage=[]
      self.healthyQuantitiesPerDay=[]
      self.theIngredients={}
      self.theYieldContainer={}
      self.theLandInfo=[]
      
      #self.ReadYieldsAndQBList(self, thelistOfInputFiles)
    
    #def __init__(self,theListOfInputFiles):
    #self.fileNamesList = theListOfInputFiles
    #    self.fileNames = []    
    #    self.foodTypeNames = []
    #    self.usage=[]
    #    self.healthQuantitiesPerDay=[]
    #    self.theYieldsMapVector=[]
    #    self.theAvYieldAndLandMapVector={}
    #self.ReadYieldsAndQBList(self, thelistOfInputFiles)
    
    
    # this method is used to inialize the class
    # the list of each food info is read in the  file 
    # it reads info from the outside and fills all the self objects==> so it needs self.
    #@classmethod


    
 #def ReadYieldsAndQBList(self, thelistOfInputFiles):
  def ReadIngredients(self, thelistOfInputFiles):
      # open the file for reading
      listOfFiles = open(thelistOfInputFiles,"r")    
      
      # this works if the file is not a csv file
      # it is possible to have it also with a 
      for line in listOfFiles:
        print 'the line is',line   
        # skip comments in the 
        if line[0] == "#" or not line:
            pass
        else:
            # this one uses only space separator
            infod=line.split(",")
            # necessary to clean up
            info = [w.strip("\"").strip("\n").strip("\"") for w in infod]
            print 'info is',info
            self.fileNames.append(info[0])
            self.foodTypes.append(info[1])
            self.usage.append(info[2])
            print 'line 3 is',info[3]
            self.healthyQuantitiesPerDay.append(float(info[3]))
            print  self.healthyQuantitiesPerDay
            # save the first 3 elements of the line
            # make it more robust
            fileName=info[0]
            foodType=info[1]
            usage=info[2]
            QB=float(info[3])
            # in this way if the positions change or if I need to add something I can do it
            # by just redefining ingredients
            ingredients={"filename":fileName,"foodType":foodType,"usage":usage,"QB":QB}
            # skip the info of the first line that only carries the definitions
            if ingredients["filename"]=="fileName":
                pass
            else:
                # add the element to the dictionary of the ingredients
                # one expects the fuleName to be unique
                # TODO chech that the filename is unique
                # for the moment do NOT overwrite past info
                # one can change it
                if (fileName in self.theIngredients.keys() and noOverWrite == True):
                    pass
                else:
                    self.theIngredients[fileName]=ingredients
            
      # one way of filling the ingredients            
      #    self.theIgredients={"fileNames":self.fileNames,"foodType":self.foodTypes,"usage":self.usage,"QB":self.healthyQuantitiesPerDay]
  
      # if one nees to add someting to this one can used
      #theFileInfo.append(something);
      # close the ingredients info
      listOfFiles.close()
#      loading all the info is a separate step
#      self.ReadYields()

# method to load all the ingredties that have been added
# TODO: add another version of  the method (overload it ) with a list as object i.e. it will call read first and then load everything
# for the moment this assumes all the info is loaded already 
       
  def LoadIngredients(self):
      #https://stackoverflow.com/questions/19747371/python-exit-commands-why-so-many-and-when-should-each-be-used
      #https://stackoverflow.com/questions/1187970/how-to-exit-from-python-without-traceback
      #https://docs.python.org/2/tutorial/errors.html: here  section 8,4  specifies how to raise execptions
      
      # check if list are filled
      try:
        listsAreFilled = ( len(self.fileNames)>0 or len(self.foodTypes)>0 or len(self.usage)>0 or len(self.healthyQuantitiesPerDay))
        listsAreNotEqual = (len(self.fileNames) !=  len(self.foodTypes) or  len(self.fileNames) != len(self.usage)
                                or  len(self.fileNames) != len(self.healthyQuantitiesPerDay)
                                or  len(self.foodTypes) != len(self.usage)
                                or  len(self.foodTypes) != len(self.healthyQuantitiesPerDay)
                                or  len(self.usage)     != len(self.healthyQuantitiesPerDay))
    
        if listsAreFilled == False or listsAreNotEqual == True :
            if listsAreFilled == True:
                raise ValueError ("lists are filled, but they are not equal")
            else:
                raise ValueError ("lists are not filled")
    # notice that if the first exception is raised it is the only one that is seen     
      except ValueError:      
        # rtaise raises the exception and then sys.exit exits the program
        raise 
        sys.exit(0)
        #this was in the past nwo I want to move to a lost of Food objects that I will use to calculate
        # averages in here : I keep the ffod objects in here and from each food objects I obtain information
        # theYieldContainer = Yielder()
    #  self.theYieldContainer = {}
           
# now fill in the yields  thanks to the ingredients
# this means that for each ingredient one fills in the yielder
      for fileName,ingredients in self.theIngredients.iteritems():
        # if one ingredient is mentioned as usable,
        if ingredients["usage"] == "Y":
# every time I call FoodType I am generating a new instance of the class and this is what I need: I new foodType
            myFoodType=FoodType()   
#            theYieldContainer.LoadIngredients(theIngredients["foodType"],ingredients)
# now  load the food type and the file that contains all the info associated with that foodtype
            myFoodType.loadIngredients(ingredients["foodType"],ingredients)
# it asks the food type to Calculate all the associated info
# and make it ready and avaialble--> do not use it yet
#            myFoodType.fillInfo()
# now save the food type in the dictionary that contains it so it is retrieved quickly
            self.theYieldContainer["foodType"]=myFoodType

# once that info is availabel to the yield container it needs to open that file and read al the yields            
            
# this needs to be a dictionarty that has the food type  as key and the average LandYeild
# for the for type          
#            self.theAverageYieldAndLand = theYieldContainer.GetAverageYieldAndLand()

#    def getYieldInfo(self,foodtype)
#    def

            
  def CalculateTotalLand(self):
      
        # loop over all food Types and ask each food type to give you the
        # associated land 
        # loop over the values only
        # TODO: consider if it is neceesary to loop on both
        #http://dev-notes.eu/2017/09/iterating-over-dictionary-in-python/
        # recover the list of land values 
        #theLands=[theFoodType.getLand() for theFoodType in theYieldContainer.values()]
        #theLandRMSs= [theFoodType.getLandRMS() for theFoodType in theYieldContainer.values()]
        #np.array(theLandRMSs)
        # this is looping over each food type
        # each food type produces a land that is averaged over space and time
        # and it contain information about the appropriate quantities  of food that are necessary
        # for a human being
        # TODO: add parameters to modify the foodType calculation of the land
        # if no parameter is specified tha land is averaged over space and time
        # averages over space and time and associated spreads
        # I put them in arrays in case one wanted  to perform more complex info
        theLands=np.array([theFoodType.getLand() for theFoodType in self.theYieldContainer.values()])
        theLandsUnc=np.array([theFoodType.getLandUnc() for theFoodType in self.theYieldContainer.values()])
        theLandsRMS=np.array([theFoodType.getLandRMS() for theFoodType in self.theYieldContainer.values()])
        theLandsRMSUnc=np.array([theFoodType.getLandRMSUnc() for theFoodType in self.theYieldContainer.values()])
 
        
        
        moreAv=False
        # TODO: the country and the year to be set from above
        # so this code is temporary
         # averages over space, but not time and associated spreads
        if (moreAv == True):
            theYear=2008
            theLandsAvSpace=np.array([theFoodType.getLand(year=theYear) for theFoodType in self.theYieldContainer.values() if theFoodType.isToBeUsed()])
            theLandsUncAvSpace=np.array([theFoodType.getDLand(yea=theYear) for theFoodType in self.theYieldContainer.values() if theFoodType.isToBeUsed()])
            
            # averages over time, but not time and associated spreads
            theCountry="Italy"
            theLandsAvTime=np.array([theFoodType.getLand(country=theCountry) for theFoodType in self.theYieldContainer.values()])
            theLandsUncAvTime=np.array([theFoodType.getDLand(country=theCountry) for theFoodType in self.theYieldContainer.values()])

        
        # sum the land info from each food type
        totalLand=sum(theLands)
#        dTotalLand=sum(sum(error*error for error in theLandsUnc))
# this is expecte dto work
#        dTotalLand=sum(sum(error*error for error in np.nditer(theLandsUnc)))
        print "theLands",theLands
        print "theLandsUnc",theLandsUnc
        dTotalLand=math.sqrt((theLandsUnc**2).sum())

        totalLandRMS=math.sqrt((theLandsRMS**2).sum())
#        totalLand=sum(theLandsRMS)
#        dTotalLand=math.sqrt((theLandsUnc**2).sum())

        
        if (moreAv == True):
            totalLandAvTime=sum(theLandsAvTime)
            dTotalLandAvTime=sum(sum(error*error for error in theLandsUncAvTime))
            totalLandAvSpace=sum(theLandsAvSpace)
            dTotalLandAvSpace=sum(sum(error*error for error in theLandsUncAvSpace))
            
            # save total land total landInfo
        # we can meke it dynmic later on accoridng to needs
        if (moreAv == True):
            self.theLandInfo=[totalLand,dTotalLand,totalLandAvSpace,dTotalLandAvSpace,totalLandAvTime,dTotalLandAvTime]
        else:
            self.theLandInfo=[totalLand,dTotalLand,totalLandRMS]


  def GetTotalLand(self):
#        totalLandAndUnc=[]
#        totalLandAndUnc.append(self.totalLand)
#        totalLandAndUnc.append(self.RMStotalLand)
# TODO: consider making a dictionary
    return self.theLandInfo
  #totalLandAndUNc
     
         
#void LandCalculator::calculateTotalLand(){
# // Now loop over the LandMapVector and sum the various land Contributions
  
#  std::cout<<__FILE__<<__LINE__<<"calculating total land"<<std::endl;
#  this->ReadYields();
  
#  std::cout<<__FILE__<<__LINE__<<"after reading yields"<<std::endl;
#  map< string, vector< Double_t > >::iterator theLandMapVectorIterator;
#  Double_t totalLand=0.;
#  Double_t RMS2TotalLand=0;
#  Double_t RMSTotalLand=0;
  
#  vector<Double_t> theAverages;
#  for (theLandMapVectorIterator=theAvYieldAndLandMapVector->begin(); theLandMapVectorIterator!=theAvYieldAndLandMapVector->end(); ++theLandMapVectorIterator){
    
#    theAverages=  theLandMapVectorIterator->second;
#    totalLand+=theAverages.at(2);
#    RMS2TotalLand+= pow(theAverages.at(3),2);
#  }
  
#  RMSTotalLand=pow(RMS2TotalLand,0.5);
#  
#  theTotalLand=totalLand;
#  theRMSTotalLand=RMSTotalLand;
#}
#
#vector<Double_t> LandCalculator::getTotalLand(){
#  theTotalLandVector.push_back( theTotalLand);
#  theTotalLandVector.push_back(theRMSTotalLand);
#  return theTotalLandVector;
#}
#
