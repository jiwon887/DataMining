import csv
from collections import defaultdict  # 키 없이 사용 가능한 dictionary
from itertools import combinations # 조합 사용하기 위한 라이브러리
import matplotlib.pyplot as plt

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
            self.threshold -= 15
            extend = self.ExtendSet(itemset, length)
            if not extend:
                break
            itemset.update(extend)
            length += 1

        self.frequentItemSet = itemset
        return itemset
    
    # 연관 규칙 생성
    def GenerateRules(self):
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
                            interest = abs(confidence - (support_consequent / self.numTransactions))

                            if confidence >= self.confidence:
                                rules.append({
                                    'antecedent': antecedent,
                                    'consequent': consequent,
                                    'support': support_itemset / self.numTransactions,
                                    'confidence': confidence,
                                    'interest': interest
                                })

        return rules
    
    def PrintRules(self):
        rules = self.GenerateRules()

        if not rules:
            print("No rules found")
            return

        supports = []
        confidences = []
        interests = []

        for rule in rules:
            supports.append(rule['support'])
            confidences.append(rule['confidence'])
            interests.append(rule['interest'])

        
        plt.figure(figsize=(12, 6))

        # support , interest
        plt.subplot(1, 2, 1)
        plt.scatter(supports, interests, c='r', marker='o')
        plt.xlabel('Support')
        plt.ylabel('Interest')
        plt.title('Support vs Interest')

        # confidence , interest
        plt.subplot(1, 2, 2)
        plt.scatter(confidences, interests, c='b', marker='o')
        plt.xlabel('Confidence')
        plt.ylabel('Interest')
        plt.title('Confidence vs Interest')

        plt.tight_layout()  
        plt.show()


a = Aprior('market.csv', threshold=150, confidence=0.2)
b = Aprior('market.csv', threshold=150, confidence=0.4)
c = Aprior('market.csv', threshold=150, confidence=0.6)


a.FindItemSet()
a.PrintRules()

b.FindItemSet()
b.PrintRules()

c.FindItemSet()
c.PrintRules()
