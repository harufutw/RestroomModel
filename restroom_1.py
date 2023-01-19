#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import numpy as np
import csv

class RestroomModel:
    restroom = np.zeros(0,0)
    place = []
    people = []
    t = np.arange(0)

    def __init__(self):
        with open('./people.csv', newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            self.people = [row for row in reader]

    def read_csv(self, filename, datatype):
        with open(filename, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            if datatype == 'place':
                self.place = [row for row in reader]
            elif datatype == 'people':
                self.people = [row for row in reader]
            else :
                raise 

model = RestroomModel()
print(model.place)