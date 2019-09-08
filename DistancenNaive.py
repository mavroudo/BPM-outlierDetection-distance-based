
def calculateDiffernce(trace1,trace2,minmaxTimes):
   dif=0
   for i in range(int(len(trace1)/2)):
       dif+=abs(trace1[i]-trace2[i])
   for i in range(int(len(trace1)/2),len(trace1)):
       minmax=minmaxTimes[i-int(len(trace1)/2)]
       if trace1[i]==0 or trace2[i]==0: #what happens when one of them are 0? 0 or 1?
           dif+=0
       else:
           dif+=abs(trace1[i]-trace2[i])/(minmax[1]-minmax[0]) # follows uniform distribution
   return int(dif)

def findAllDistances(results,minmaxTimes):  
    #find all the distances in the upper corner
    distances=[[]for i in range(len(results))]
    for i in range(len(results)):
        print(i)
        for j in range(len(results)):
            if j<=i:
                distances[i].append(0)
            else:
                distances[i].append(calculateDiffernce(results[i],results[j],minmaxTimes))
    return distances
