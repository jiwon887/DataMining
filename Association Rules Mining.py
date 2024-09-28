import csv



class Aprior:


    def __init__(self, filename, threshold):
        self.threshold = threshold
        self.dataset = self.ReadData(filename)

    def ReadData():