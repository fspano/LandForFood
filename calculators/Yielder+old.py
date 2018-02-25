#//=====================================================================-*-C++-*-
#Authors: Francesco Span\`o <francesco.spano@cern.ch>
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
#correlations or production with certain climate zones...yes
#     // iyt is worth making a class of objects 
#     //  nd eahc class also stores the name of the foot type
#     // then we make a map of these objects 


from ROOT import TRandom, TFile, TH1D, TH1F
from sys import exit


class Yielder:
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

#  // some initialization, I am probably better off with a poiinter
#  theAverageYieldAndLand.push_back(-1);

void Yielder::setYields(string yieldfile){

  // ---load  the file with  yields -------
  /* some checks
  // std::ifstream data("apples.csv");
  // std::ifstream data("pippo.txt");
  // string filename = "/Users/fspano/Action/WorkDeskAction/SustainabilityStudies/goodData/apples.csv";
  */

  std::ifstream data(yieldfile.c_str());
  std::string line;
  std::cout<<__FILE__<<__LINE__<<"I am reading file"<<yieldfile.c_str()<<std::endl;
  // ---row Counter counts the number of rows;TODO: we could even find it in advance with wc; not sure this is needed---
  Int_t rowCounter = 0;
  // --- cellCounter counts the elements in a row
  Int_t cellCounter = 0;

  /* goodColumns  and goodColumnNames are used  to stores the columns that need to be stored for each tables
     in our specific case: the country, the year, the yield
     TOIMPROVE: if we want we can save the  firct column to have the interpretation
  */
  vector<int> goodColumns;
  vector<string> goodColumnNames;
  goodColumnNames.push_back("AreaName");
  //--- additional colum that is not needed now 
  //  goodColumnNames.push_back("ItemName");
  goodColumnNames.push_back("Year");
  //--- additional column that is not needed now 
  // goodColumnNames.push_back("Unit");
  goodColumnNames.push_back("Value");
   /* 
     getline extracts character from the file until it encounters a delimiter or the newline sign
     in this case it only stops with the newline as no delimiter is mentioned
  */

  //  std::cout<<"standard two "<<std::endl;
  //  std::cout<<"standard twobis "<<std::endl;
  vector< vector< Double_t > > superVec;
  string nameState;
  string theState;

  //  std::cout<<"standard three "<<std::endl;
  // the vector of data that is generated outside the lines
  vector<Double_t> dataVec;	

  while(std::getline(data,line)){


    // to skip comments
    //line.erase(line.begin(), find_if(line.begin(), line.end(), not1(ptr_fun<int, int>(isspace)))); 
    //    if(line[0] == '#') continue;


    // increment the counter as the line is a good one
    rowCounter++;      
    std::cout<<__FILE__<<__LINE__<<"reading line "<<rowCounter<<std::endl;
    // this is one way of tokenizing
    // check
    //std::cout<<line.size()<<std::endl;
    //std::cout<<line.c_str()<<std::endl;
    
    /*
      the line is passed to the stringstream object that is then analyszed with getline again, this time the cell is derived by stopping at the 
      given delimiter as FAO files have all the same delimiter it is easy to build the cell
      a more complex tokenizing scheme would require the use of the references for tokenizing that are mentioned above like strtok
      this is good enough for now; it can be improved; I have examples.
      The problem is that with getline you have only one delimiter ; if you nee dmore dleimiters (as I will) you have to use tok or strtk
    */
    std::stringstream lineStream(line);
    std::string lineStreamX(line);
    std::string cell;
    Double_t theCellD;
    std::stringstream theCell;

    cellCounter=0;
    //=============== special treatment for the first row==========
    //in the first row find  the data you are interested in. TOIMPROVE: now hardcoded, but it can be passesd with another datacard file

    if (rowCounter == 1){
      while(std::getline(lineStream,cell,',') && cell.compare(",") !=0) {
	cellCounter++;
	/* check if the cell is one of the good names for columns
	   notice that the assumptoin is that all cells in the first row are different
	*/
	for(Int_t i = 0;i<goodColumnNames.size();i++) {
	  // compare cell with the given goodColum string. if it is the same keep the cell number
	  if (cell.compare(goodColumnNames.at(i)) ==0 ){
	    goodColumns.push_back(cellCounter);    // std::cout<<"I found a good column at cell"<<cellCounter<<endl;
	  }
	}// end loop of column names
      } // end of loop of cells of first line
    } // end requirement for it to be on first line

    // if we are beyond the first line
    //=============== treatment for  rows beyond the first one ==========
	//    std::cout<<"the line is "<<rowCounter<<std::endl;
    // this solution works as it gives the same result as above without the lines

    dataVec.clear();
	// clean the data vector so that it is ready to be filled in the following loop
    while(std::getline(lineStream,cell,'"') && cell.compare("\"") !=0 ){	
      if (cell.compare(",")!=0 && cell.size()>0 ){
	cellCounter++;
	//	std::cout<<"the cell size is "<<cell.size()<<endl;
	//std::cout<<"this is the cell number"<<cellCounter << "and it is "<<cell.c_str()<<std::endl;            // You have a cell!!!!
	// if the cell is one of the good ones save the first in a name and then the oter two in a vector

	for(Int_t i = 0;i<goodColumns.size();i++) {
	  std:: cout<<" the good Columns size is"<<goodColumns.size()<<std::endl;
	  if ( cellCounter == goodColumns.at(i)) {
	    if (i==0) {
	      // if it is the first line save the name of the country (Italy, France, etc..)
	      // save the name of the state to be changed if necessary
	      if (rowCounter == 2) theState = cell;
	      // save the name of the state for this line
	      nameState = cell;
	      // save neme of the state at the first row
	      //	      if (strcmp(cell,theState)!=0) theState=cell;
	    }
	    // fill in the year and the yield
	    if (i>0) {
	      std:: cout<< "the cell for year and yield"<<cell<<std::endl;
	      theCell.clear();
	      theCell.str(cell);
	      theCell>>theCellD;
	      std:: cout<< "the cellD is"<<theCellD<<std::endl;
              dataVec.push_back(theCellD);
	      std::cout<<"the size of datavec is"<<dataVec.size()<<std::endl;
	    }
	  }// 
	}// end of loop over columns to compare the value of the cell to what it is interesting
      }// end of checking the cell size and type (avoid , and ")
    }// end of loop over line elements for a given line one has the 2d vector and the name of the state   
    std::cout<<"the size of datavec outsid ethe line elemts loop is"<<dataVec.size()<<std::endl;
    //save the 2 vector that was generated in the loop above, if it is not empty it might weel be it si one 
    // of teh cases where nothing was found
    if (dataVec.size()>0) superVec.push_back(dataVec);
    // now if the name of the state is  different than the one of the previous line
    // it is time to 0) fill in the last step of the supervec 2) save the supervec and the name 	 
    // this one needs to be done 
    if (theState.compare(nameState)!=0){
      // put in the datavec
      //	      superVec.push_back(dataVec);
      // theMap[theState]=superVec;
      theYieldsMap->insert (std::pair<string,vector<vector<Double_t> > >(theState,superVec));
      // then
      // 1) change the name of the state
      theState=nameState;
      // 2)  clear the vector --> make it ready for the next step
      superVec.clear();
    }

  }// end of looping over lines

  // check that the Yield has done its job
  // what happens if the file is empty?
  // one should send a warning
  if (rowCounter==0) std::cout<<"warning: the number od lines that were read from the file named "<<yieldfile.c_str()<<" is zero!!!. Check the file content and Make sure the input list has the appropriate directory path"<<std::endl; 
  // if it has not dobne the Yield is empty


}

/*
// TO DO THIS IS NEED TO BREAK  calculateAverageYieldAndLand(Double_t healthyQuanPerDay) in two methods; not needed now
vector<Double_t> getAverageYield(){
  this->calculateAverageYieldAndLand();
  return theAverageYieldVec;  
}

vector<Double_t> getAverageLand(){
  this->calculateAverageLand();
  return theAverageLandVec;  
}

vector<Double_t> calculateAverageLand(){
  vector<Double_t> theLandVec;
  // if there is no average yield vector, fill one
  if (theAverageYieldVec.size()=0) this->calculateAverageYield();
  // now calulcate the average land
  for (Int_t i=0;i<theAverageYieldVec.size(); i++){
    theLandVec.push_back(healthyQuantityPerDay*DaysInAYear/theYield);
  }
  Double_t meanLand = TMath::Mean(theLandVec.begin(), theLandVec.end());
  Double_t RMSLand = TMath::RMS(theLandVec.begin(), theLandVec.end());
} 
*/

vector<Double_t> Yielder::getAverageYieldAndLand(){
  // this can be -1 or not
  this->calculateAverageYieldAndLand();
  return  theAverageYieldAndLand;
}


vector<Double_t>  Yielder::getAverageYieldAndLand(Double_t healthyQuantityPerDay){
  // this can be -1 or not
  this->calculateAverageYieldAndLand(healthyQuantityPerDay);
  return theAverageYieldAndLand;
}

void Yielder::calculateAverageYieldAndLand(){
  this->calculateAverageYieldAndLand(theHealthyQuantityPerDay);
}

void Yielder::calculateAverageYieldAndLand(Double_t healthyQuanPerDay){
  // 

  std::cout<<__FILE__<<__LINE__<<"healthyQuanPerDay is "<< healthyQuanPerDay<<std::endl;
  // local variables
  Double_t theYield=-1.;
  vector<Double_t> theYieldVec;
  vector<Double_t> theLandVec;

  map < string,vector< vector<Double_t> > >::iterator theMapIterator;
  for (theMapIterator=theYieldsMap->begin(); theMapIterator!=theYieldsMap->end(); ++theMapIterator){
    vector< vector<Double_t> > theVec = theMapIterator->second;
    std:: cout<< "the Vec size is"<<theVec.size()<<std::endl;
    vector<Double_t> oneVec;
    for (Int_t i=0; i< theVec.size();i++){
      oneVec= theVec.at(i);
      //std::cout<<"oneVec.size is"<<oneVec.size()<<std::endl; 
      //std::cout << "the country is "<< theMapIterator->first<< "and in year "<< (theVec.at(i)).at(0)<<" the yield was "<<(theVec.at(i)).at(1)<<std::endl;   
      //http://root.cern.ch/drupal/content/tmath    
      // including the yield for a given country
      theYield=scaleFromHgPerHaToGramsPerM2*(theVec.at(i)).at(1);
      theYieldVec.push_back(theYield);
      if (theYield>0)     theLandVec.push_back(theHealthyQuantityPerDay*DaysInAYear/theYield);
      else theLandVec.push_back(-1.);
    }
    // std::cout << "the country is "<< theMapIterator->first<<std::end;
  }

  std::cout << "the size of the yeiled vec is"<< theYieldVec.size()<<std::endl;
  Double_t meanYieldPerYear = 0;
  Double_t RMSYieldPerYear = 0;
  Double_t meanLand = 0;
  Double_t RMSLand = 0;

  if(theYieldVec.size()>0){
    meanYieldPerYear = TMath::Mean(theYieldVec.begin(), theYieldVec.end());
    RMSYieldPerYear = TMath::RMS(theYieldVec.begin(), theYieldVec.end());
    meanLand = TMath::Mean(theLandVec.begin(), theLandVec.end());
    RMSLand = TMath::RMS(theLandVec.begin(), theLandVec.end());
    std::cout<< "mean yieled per year = "<< meanYieldPerYear <<std::endl;
    std::cout<< "rms yeield per year = "<< RMSYieldPerYear <<std::endl;
    std::cout<< "mean required land = "<< meanLand<<std::endl;
    std::cout<< "rms required land = "<< RMSLand <<std::endl;
  }
  theAverageYieldAndLand.clear();
  theAverageYieldAndLand.push_back(meanYieldPerYear);
  theAverageYieldAndLand.push_back(RMSYieldPerYear);
  theAverageYieldAndLand.push_back(meanLand);
  theAverageYieldAndLand.push_back(RMSLand);
  
  //  theAverageYieldVec=theYieldVec;
  //  theAverageLandVec=theLandVec;
}




  // the vector without iteration
  //http://stackoverflow.com/questions/8351089/how-to-create-new-vector-in-each-iteration


//   map < string,vector< vector<Double_t> > >::iterator theMapIterator;
//   for (theMapIterator=theMap->begin(); theMapIterator!=theMap->end(); ++theMapIterator){
//     vector< vector<Double_t> > theVec = theMapIterator->second;
//     std:: cout<< "the Vec size is"<<theVec.size()<<std::endl;
//     vector<Double_t> oneVec;
//     for (Int_t i=0; i< theVec.size();i++){
//       oneVec= theVec.at(i);
//       std::cout<<"oneVec.size is"<<oneVec.size()<<std::endl; 
//       std::cout << "the country is "<< theMapIterator->first<< "and in year "<< (theVec.at(i)).at(0)<<" the yield was "<<(theVec.at(i)).at(1)<<std::end;
   
//     }
//     // std::cout << "the country is "<< theMapIterator->first<<std::end;
//   }

//   // save  name of countries  and the assocaited vector of numbers
//   //  std::map<string, vector<Double_t>)::iterator yieldsIterator;
//  for (yieldsIterator = yieldsPerYear->begin(); theScenariosCounter!= totalLandPerPerson->end();theScenariosCounter++){
//     // the key
//     //    theScenarioCounter->first()
//       std::cout <<"for the scenario"<< theScenarioCounter->first() << " the total land required per person is" theScenarioCounter->second()<< " in the interval ["<< bandOnTotalLandPerPerson.at(theScenarioCounter->first())[0]<<","<<bandOnTotalLandPerPerson.at(theScenarioCounter->first())[1]<<"]"<<endl;
//       // the value
//   }

//   yieldsPerYear* = new   map<string countryname, vector<Double_t>;


// }
