
def calculateDiffernce(trace1,trace2,minmaxTimes):
   dif=0
   for i in range(int(len(trace1)/2)):
       dif+=abs(trace1[i]-trace2[i])
   for i in range(int(len(trace1)/2),len(trace1)):
       minmax=minmaxTimes[i-int(len(trace1)/2)]
       if trace1[i]==0 or trace2[i]==0:
           dif+=1
       else:
           dif+=abs(trace1[i]-trace2[i])/(minmax[1]-minmax[0]) # follows uniform distribution
   return int(dif)
