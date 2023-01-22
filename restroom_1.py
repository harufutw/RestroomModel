#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import numpy as np
import csv

class RestroomModel:
    restroom = []
    place = []
    people = []
    t = np.arange(0)

    def __init__(self):
        pass

    # 場所や人のデータを格納したcsvファイルを読み取る関数
    def read_csv(self, filename, datatype):
        with open(filename, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            # 場所のデータのとき
            if datatype == 'place':
                self.place = [row for row in reader]
            # 人のデータのとき
            elif datatype == 'people':
                self.people = [row for row in reader]
            else :
                pass
    
    # 化粧室の各個室の利用状況を格納した配列を生成する関数
    def make_restroom(self,size):
        for num_element in size:
            restroom_floor = []
            for i in range(num_element):
                restroom_floor.append(0)
            self.restroom.append([restroom_floor,[]])

    # 時間軸を生成する関数
    def make_time_model(self,start,stop,step):
        self.t = np.arange(start,stop,step)

    # 空室を探す関数
    def search_empty(self,num_floor):
        flag = 0
        for i in range(len(self.restroom[num_floor][0])):
            if self.restroom[num_floor][0][i] == 0:
                self.restroom[num_floor][0][i] = 1
                flag = 1
                break
        return flag == 1

    # 個室から退出する関数
    def leave_room(self,num_floor):
        flag = 0
        for i in range(len(self.restroom[num_floor][0])):
            if self.restroom[num_floor][0][i] == 1:
                self.restroom[num_floor][0][i] = 0
                flag = 1
                break
        return flag == 1


model = RestroomModel()
model.read_csv('./people.csv', 'people')
model.read_csv('./place.csv', 'place')
model.make_restroom((6,6,6,6,6))
print(model.restroom)
model.make_time_model(1,100,1)
for time in model.t:
    print(time)
    num_floor = 2
    for num_people in range(1,len(model.people)):
        if (time == int(model.people[num_people][3])) & (int(model.people[num_people][6]) == 0):
            ret = model.search_empty(num_floor)
            if ret :
                model.people[num_people][6] = 1
            else :
                model.people[num_people][6] = 2
                model.restroom[num_floor][1].append(1)
        elif (time == int(model.people[num_people][5])):
            model.leave_room(num_floor)

    print(model.restroom)