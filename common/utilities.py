import numpy as np
import math
#https://stackoverflow.com/questions/37127201/better-place-to-put-common-functions

def average(theArray):
    print 'theArray',theArray
    average=np.average(theArray)
    print 'average is ',average
    RMS=np.std(theArray,ddof=1)
    print 'rms is ',RMS
    print 'size ',theArray.shape[0]
    # hsape gives a tuple and the tuple is a list of immutable objects
    dAverage=RMS/math.sqrt(theArray.shape[0])  
    return average,dAverage

def rms(theArray):
    print 'theArray',theArray
    #average=np.average(theArray)
    RMS=np.std(theArray,ddof=1)
    print 'rms is ',RMS
    print 'size ',theArray.shape[0]
    # hsape gives a tuple and the tuple is a list of immutable objects
    dRMS=RMS/math.sqrt(2*theArray.shape[0])  
    return RMS,dRMS

# useifl code for averages
# theLands theLands
         
#        RMSLand=np.std(theLands,ddof=theLands.shape())
#        # calculate the total land and its uncertainty
#        # temporary uncertanty will need additional uncertainty propagation for syst uncertainties
#        averageLandUncertainty=RMSLand/math.sqrt(theLands.shape())   
#        theSize=len( theLands)    
#        self.totalLand=sum(theLands)
#        self.RMSTotalLand
#        theLandsRMSAvTime=np.array([theFoodType.getLandRMS(country=theCountry) for theFoodType in theYieldContainer.values()])

