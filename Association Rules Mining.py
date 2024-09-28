import csv
from collections import defaultdict # 키 없이 사용 가능한 dictionary



class Aprior:

    def __init__(self, filename, threshold):
        self.filename = filename
        self.threshold = threshold
        self.frequentItemSet = {}

    # 첫 dataset 만들기
    def GenInitialSet(self):
        itemset = defaultdict(int)
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader: 
                transaction = set(row)
                for item in transaction:
                    itemset[frozenset([item])] +=1

        # frequent를 세서 dic 만들기
        frequentItemSet = {itemset:count for itemset, count in itemset.items() if count >= self.threshold}
            
        return frequentItemSet
    

a = Aprior('market.csv',threshold=3 )
f = a.GenInitialSet()
print(f)