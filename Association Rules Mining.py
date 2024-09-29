import csv
from collections import defaultdict # 키 없이 사용 가능한 dictionary
from itertools import combinations # 조합 사용하기 위한 라이브러리



class Aprior:

    def __init__(self, filename, threshold, confidence):
        self.filename = filename
        self.threshold = threshold
        self.frequentItemSet = {}
        self.confidence = confidence

    # 첫 dataset 만들기
    def GenInitialSet(self):
        itemset = defaultdict(int)
        numTranscation = 0 # support계산에 이용
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader: 
                numTranscation+=1
                transaction = set(row)
                for item in transaction:
                    itemset[frozenset([item])] +=1 # 해시 가능한 set 사용

        # frequent를 세서 dic 만들기
        frequentItemSet = {itemset:count for itemset, count in itemset.items() if count >= self.threshold}
            
        return frequentItemSet, transaction
    
    def ExtendSet(self, prevItemSet, length):
        
        # 새로 연산해줄 집합
        candidates = set()

        prevItemSets = list(prevItemSet.keys())


        for i in range(len(prevItemSets)):
            for j in range(i+1, len(prevItemSets)):
                extendItemSet = prevItemSets[i].union(prevItemSets[j])
                if len(extendItemSet) == length:
                    candidates.add(extendItemSet)
                    if all(frozenset(subset) in prevItemSet for subset in combinations(extendItemSet, length - 1)):
                        candidates.add(extendItemSet)

        # 후보 집합에서 threshold 넘는 경우를 담을 집합
        new_itemsets = defaultdict(int)

        with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    transaction = set(row)
                    for candidate in candidates:
                        if candidate.issubset(transaction):
                            new_itemsets[frozenset(candidate)] += 1
        

        return  {itemset: count for itemset, count in new_itemsets.items() if count >= self.threshold}
    
    def FindItemSet(self):
        itemset, numTranscation = self.GenInitialSet()
        length = 2

        while True:
            extend = self.ExtendSet(itemset, length)
            if not extend:
                break
            itemset.update(extend)
            length +=1

        self.frequentItemSet = itemset

        return itemset

# 테스트
a = Aprior('market.csv', threshold=100, confidence=0.5)


initdataset, numTranscation = a.GenInitialSet()

kk = a.FindItemSet()

for itemset, count in kk.items():
    print(f"{set(itemset)}: {count}\n")