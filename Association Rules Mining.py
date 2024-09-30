import csv
from collections import defaultdict  # 키 없이 사용 가능한 dictionary
from itertools import combinations # 조합 사용하기 위한 라이브러리

class Aprior:

    def __init__(self, filename, threshold, confidence):
        self.filename = filename
        self.threshold = threshold
        self.frequentItemSet = {}
        self.confidence = confidence
        self.numTransactions = 0  # 트랜잭션 수

    # 첫 dataset 만들기
    def GenInitialSet(self):
        itemset = defaultdict(int)
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader: 
                self.numTransactions += 1  # 트랜잭션 수 증가
                transaction = set(row)
                for item in transaction:
                    itemset[frozenset([item])] += 1 

        
        frequentItemSet = {itemset: count for itemset, count in itemset.items() if count > self.threshold}
        return frequentItemSet
    
    
    def ExtendSet(self, prevItemSet, length):
        candidates = set()
        prevItemSets = list(prevItemSet.keys())

        for i in range(len(prevItemSets)):
            for j in range(i+1, len(prevItemSets)):
                extendItemSet = prevItemSets[i].union(prevItemSets[j])
                if len(extendItemSet) == length:
                    if all(frozenset(subset) in prevItemSet for subset in combinations(extendItemSet, length - 1)):
                        candidates.add(extendItemSet)

        # 새로 생성된 후보 집합에서 threshold 넘는 경우 저장
        new_itemsets = defaultdict(int)

        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                transaction = set(row)
                for candidate in candidates:
                    if candidate.issubset(transaction):
                        new_itemsets[frozenset(candidate)] += 1

        return {itemset: count for itemset, count in new_itemsets.items() if count > self.threshold}
    
    # 자주 등장하는 항목집합 찾기
    def FindItemSet(self):
        itemset = self.GenInitialSet()
        length = 2

        while True:
            extend = self.ExtendSet(itemset, length)
            if not extend:
                break
            itemset.update(extend)
            length += 1

        self.frequentItemSet = itemset
        return itemset
    
    # 연관 규칙 생성
    def generate_rules(self):
        rules = []
        for itemset, count in self.frequentItemSet.items():
            if len(itemset) > 1:
                for consequent_length in range(1, len(itemset)):
                    for consequent in combinations(itemset, consequent_length):
                        antecedent = itemset.difference(consequent)
                        consequent = frozenset(consequent)

                        support_antecedent = self.frequentItemSet.get(antecedent, 0)
                        support_consequent = self.frequentItemSet.get(consequent, 0)
                        support_itemset = count

                        if support_antecedent > 0:
                            confidence = support_itemset / support_antecedent
                            interest = confidence - (support_consequent / self.numTransactions)

                            if confidence >= self.confidence:
                                rules.append({
                                    'antecedent': antecedent,
                                    'consequent': consequent,
                                    'support': support_itemset / self.numTransactions,
                                    'confidence': confidence,
                                    'interest': interest
                                })

        return rules

    # 규칙 출력
    def print_rules(self):
        rules = self.generate_rules()

        if not rules:
            print("fail")
            return

        for rule in rules:
            print(f"{set(rule['antecedent'])} -> {set(rule['consequent'])}")
            print(f"  Support: {rule['support']:.3f}, Confidence: {rule['confidence']:.3f}, Interest: {rule['interest']:.3f}\n")

# 테스트
a = Aprior('market.csv', threshold=50, confidence=0.5)

a.FindItemSet()
a.print_rules()
