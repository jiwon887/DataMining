import csv
from collections import defaultdict # 키 없이 사용 가능한 dictionary



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
    

# 테스트 실행
a = Aprior('market.csv', threshold=30, confidence=0.5)

# 초기 빈번한 아이템셋 생성
initdataset, numTranscation = a.GenInitialSet()

# 2-아이템셋 확장
extended_itemset = a.ExtendSet(initdataset, 2)

# 결과 출력
for itemset, count in extended_itemset.items():
    print(f"{set(itemset)}: {count}\n")