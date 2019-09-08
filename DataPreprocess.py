#!/usr/bin/env python3

import datetime 
from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter
def dataPreprocess(log):
    activities_all = log_attributes_filter.get_attribute_values(log, "concept:name")
    org_all=log_attributes_filter.get_attribute_values(log,"org:resource")
    activities=list(activities_all.keys())
    org=list(org_all.keys())
    results=[]
    times=[[] for i in range(len(activities))]
    for trace in log:
        k=[0 for i in range(len(activities))]
        l=[0 for i in range(len(org))]
        timesSpend=[datetime.timedelta(0) for i in range(len(activities))]
        previousTime=trace.attributes["REG_DATE"]
        for index,event in enumerate(trace):
            indexActivity=activities.index(event["concept:name"])
            k[indexActivity]+=1
            timesSpend[indexActivity]+=event["time:timestamp"]-previousTime
            times[indexActivity].append(event["time:timestamp"]-previousTime)
            previousTime=event["time:timestamp"]
            try:
                l[org.index(event["org:resource"])]+=1
            except:
                pass
        timesSpend=[timesSpend[i]/k[i] if k[i]!=0 else 0 for i in range(len(activities))] #this is where the int comes from
        results.append(k+timesSpend) #removed org
    times=[sorted(times[i]) for i in range(len(activities))]
    return results,times

# up untill here we have the logs loaded as dataframe0



#get the dfg and print it
#from pm4py.algo.discovery.dfg import factory as dfg_factory
#dfg = dfg_factory.apply(log)
#from pm4py.visualization.dfg import factory as dfg_vis_factory
#gviz = dfg_vis_factory.apply(dfg, log=log, variant="frequency")
#dfg_vis_factory.view(gviz)



#from pm4py.algo.filtering.log.variants import variants_filter
#variants = variants_filter.get_variants(log)