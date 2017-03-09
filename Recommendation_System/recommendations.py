from math import *
movie = {'mohini':{'sholey':2.5,'rustam':3.5,'dangal':3.0,'jolly llb 2':3.5,'ishq':2.5,'sumperman':3.0},
          'vinod':{'sholey':3.0,'rustam':3.5,'dangal':1.5,'jolly llb 2':5.0,'ishq':3.5,'sumperman':3.0},
          'sparsh':{'sholey':2.5,'rustam':3.5,'jolly llb 2':3.5}}


'''def sim_pearson(prefs,p1,p2):
    #Get the list of mutually rated items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:si[item]=1
    #Find the number of elements
    n = len(si)
    #if there are no ratings in common, return 0
    if n==0:return 0
    #Add up all the preferences
    sum1=sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    #sum up the square
    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])
    #sum up the products
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])
    #cal pearson score
    num = pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den == 0:return 0
    r= num/den
    return r'''
def sim_pearson(prefs,p1,p2):
    si={}
    for items in prefs[p1]:
        if items in prefs[p2]: si[items] = 1
    n = len(si)
    if n == 0 : return 0
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    sum1sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2sq = sum([pow(prefs[p2][it],2) for it in si])

    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])

    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1sq- pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
    if den==0: return 0
    r= num/den
    return r


def recommend(movies,person,similarity = sim_pearson):
    totals = {}
    simSums = {}
    for others in movies:
        #don't compare me to myself
        if others == person:
            continue
        sim = similarity(movies,person,others)
        #ignore score of zero or lower
        if sim<=0:continue
        for item in movies[others]:
            #only score movie i haven't seen
            if item not in movies[person] or movies[person][item]==0:
                #similarityb * score
                totals.setdefault(item,0)
                totals[item]+=movies[others][item]*sim
                #sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
    #create the normalized list
    ranking = [(totals/simSums[item],item) for item,totals in totals.items()]
    #return the sorted list
    ranking.sort()
    print ranking
    ranking.reverse()
    return ranking