# faostat yields and crops
# http://faostat.fao.org/site/567/DesktopDefault.aspx?PageID=567#ancor
# download info in csv format and fill them in a vector of arrays to load the land calculator
# http://stackoverflow.com/questions/19720193/how-to-put-tokens-read-from-a-csv-file-into-an-array-of-objects
# New yeiled paghe : one gets there by the major page and one searches for yield
# http://faostat3.fao.org/download/Q/QL/E

from calculators.LandCalculator import LandCalculator
#import calculators.FoodType
#import FoodType
import numpy as np
import math
import sys
import getopt


#def landToFeed:

# if I am claling it from somehwer else i.e. if I do import LandFeed.py
#https://stackoverflow.com/questions/287204/python-program-start

def main(argv=None):
  if argv is None:
    argv = sys.argv
    #main program here
  #  print I am loading the library"<<std::endl
  
  #  gSystem->Load("libFinal.so")
  #  gStyle->SetPalette(1,0)
  
  # TODO: expand the LAND Calcuator to become a WaterCAlculator, shelterCalculator, heatCalculator,sewerCalculator
  # general point==> effectively one needs code that implement MUSIASIEM as that is the most complete tool
  # each yield is a function of (nations, year) i.e. (space,time)
  # in reality it is also a function other crucial variables like land quality
  # first step is to use average value from standard agriculture
  # add permaaculture values later on, assume they standard business is an estimate to start with
  # for some items we should see the difefrence they make with and without oil
  #so the yield  with non standard agriculture can be different
  
  print "I am defining the calculator "
  myLandCalculator = LandCalculator()
  print "after the defining the LandCalculator "  

  # read info about yields
  # load average yield for a given item
  # yield  in hectogram per hecter
  # so load (name_commodity, yield, max-min yield)
  # we can load it for a given item or for many items
  # this one defines the  diet 
  theDiet="data/filenames.csv"
  

  # TOIMPROVE: maybe separate QB?
  print "reading ingredients"
  #  myLandCalculator.ReadYieldsAndQBList(theListOfFiles)
  #  read the ingredients; this allows for more than one  list of files to be addded
  #  this is why it is separated from the next step
  myLandCalculator.ReadIngredients(theDiet) # it exists
  
  # Now that the reading of the ingredinets info is complete
  # load them all i.e. make a dictiornary of food types
  # each food type knows its properties and the diet info  
  myLandCalculator.LoadIngredients() # it exists
  
  # now calculate the total land given the diet assigned to the ingredients   
  #ReadYields(yield.csv)
  
  print "calculating land" 
  myLandCalculator.CalculateTotalLand()  
  theLandInfo = myLandCalculator.GetTotalLand()

  print "The  average total land in the scenario of interest is ", theLandInfo[0],"+/-",theLandInfo[1]," square metres and the associated spread is ", theLandInfo[2]






  
  # need to evalute the uncertainty
  #,"+/-",theLandInfo[1],'square metres'
#  print "The total land in the scenario of interest is ", theLandInfo[0],"+/-",theLandInfo[1]," square metres"

  
  ##################################### STILL TO BE REALIZED#######################################
  # read many yields
  #  MyLandCalculator->ReadYields(apples.csv, "apples")
  #  MyLandCalculator->ReadYields(vegetables.csv, "vegetables")
  # read info about QBs for each yield
  #  MyLandCalculator->ReadQBs(QBs.csv)
  
  #set different interesting scenario
  #
  # 1) no meat
  # 2) no fish
  # 3) no grain
  # no diary
  # no meat no diary no eggs
  # no meat no diary no eggs no grain
  ##  scenario
  # scenario = ["meat""fish","grain","diary",]
  #MyLandCalculator.SetScenarios(scenario)

  #--------------
  #  MyLandCalculator.GetRequiredLand(scenario)
  # find required quantity/yield = required land for each commodity +/- max min land
  # sum required land and get estimate of total land  with band

  #  MyLandCalculator.GetTotalRequiredLand()
  #  vector<Double_t> totalLandPerPerson = MyLandCalculator.GetTotalRequiredLandPerPerson()
  # vector<Double_t> bandOnTotalLandPerPerson = MyLandCalculator.GetBandOnTotalRequiredLandPerPerson()

  #=====================================THIS SHOULD COME LATER=========================================  

  #
  #map<string,Double_t> totalLandPerPerson = MyLandCalculator.GetTotalRequiredLandPerPerson()
  #map<string, Double_t[2]> bandOnTotalLandPerPerson = MyLandCalculator.GetBandOnTotalRequiredLandPerPerson()
  
  # get different components : absolute values per components per scenario
  # fraction of total land per component
  #=====Additional level of complexity to be coded 
  # map<string,Double_t> componentsOfTotalLandPerPerson = MyLandCalculator.GetComponentsOfTotalRequiredLandPerPerson()


  # derive results  for different scenarios with band and write them
  #std::map<string, Double_t>::iterator theScenariosCounter 
  #for (theScenariosCounter = totalLandPerPerson.begin() theScenariosCounter!= totalLandPerPerson.end()theScenariosCounter++){
  #  // the key
  #  //    theScenarioCounter.first()
  #    std::cout <<"for the scenario"<< theScenarioCounter.first() << " the total land required per person is" theScenarioCounter.second()<< " in the interval ["<< bandOnTotalLandPerPerson.at(theScenarioCounter.first())[0]<<","<<bandOnTotalLandPerPerson.at(theScenarioCounter.first())[1]<<"]"<<endl
 #     // the value
#  }
 # */
 # // what si the plan for using acquaponics and landless agriculture?

 # // plot it as a function of the year as a function of place  and so on
 # // use it as input for the city

 # //=====
#  //define city student
#  //  cityStudent *RomeStudent = new cityStudent
#  // get population of city
#  // RomeStudent.GetPopulation(population) 
#  // getRequired Land

#  // get land for full population support


if __name__ == "__main__":
    sys.exit(main())


#if __name__ == '__main__':
#    main()
