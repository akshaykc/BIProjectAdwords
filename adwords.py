import csv
import math
import sys
import random
i=0

def assignBestBidder(algType,bidderDictBudget,bidders,budgetInitial):
    global i
    def mssvValue(x,bidderDictBudget,budgetInitial):
        xu = 1 - bidderDictBudget[x[0]]/budgetInitial[x[0]]
        chi = 1 - math.exp(xu-1)
        return chi
    if algType == "greedy":
        bidders.sort(key=lambda x: float(x[2]),reverse=True)
    elif algType == "balance":
        for bids in bidders:
            bids[3]=bidderDictBudget[bids[0]]
        bidders.sort(key=lambda x: float(x[3]),reverse=True)
    elif algType == "mssv":
        bidders.sort(key=lambda x: float(x[2])*mssvValue(x,bidderDictBudget,budgetInitial),reverse=True)
    
    
    for highBidder in bidders:
        if (bidderDictBudget[highBidder[0]]-float(highBidder[2])) >= 0:
            bidderDictBudget[highBidder[0]] = float(bidderDictBudget[highBidder[0]] - float(highBidder[2]))
            return float(highBidder[2])
    return 0
    
def main():
    #Import all data
    typeAlg = str(sys.argv[1])
    random.seed(0)
    queryFilePath = "queries.txt"
    queriesFile = open(queryFilePath,"r")
    query=[]
    for line in queriesFile:
        query.append(line.strip("\n"))
    queriesFile.close()
    bidderFilePath="bidder_dataset.csv"
    bidderData = list(csv.reader(open(bidderFilePath)))
    
    for elem in bidderData:
        if elem[0]!="Advertiser" and elem[3]!="":
            elem[2]=float(elem[2])
            elem[3]=float(elem[3])
        
    #Make dictionary of bidder budgets from bidder dataset 
    totalBudgetSum = 0
    bidderBudget={}
    initialBudget={}
    for bidder in bidderData:
        if bidder[3]!="" and bidder[0]!="Advertiser":
            bidderBudget[bidder[0]]=float(bidder[3])
            initialBudget[bidder[0]]=float(bidder[3])
            totalBudgetSum = totalBudgetSum + float(bidder[3])
    #Revenue gereration
    revenue = 0
    average = 0
    withoutShuffleRevenue = 0
    #Without any shuffle
    bidderBudget=initialBudget.copy()
    for element in query:
        validBidders=[]
        for bidder in bidderData:
            if element==bidder[1]:
                validBidders.append(bidder)
        temp = assignBestBidder(typeAlg,bidderBudget,validBidders,initialBudget)
        withoutShuffleRevenue = withoutShuffleRevenue + temp    
    #Algorithm
    temp=0
    for j in range(0,100):
        random.shuffle(query)
        revenue = 0
        bidderBudget=initialBudget.copy()
        for element in query:
            validBidders=[]
            for bidder in bidderData:
                if element==bidder[1]:
                    validBidders.append(bidder)
            temp = assignBestBidder(typeAlg,bidderBudget,validBidders,initialBudget)
            revenue = revenue + temp
        average = revenue/100 + average
    print "Revenue %.2f"%withoutShuffleRevenue
    print "Competitive ratio %.2f"%(average/totalBudgetSum)
        
            
if __name__ == '__main__':
    main()
