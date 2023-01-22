#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import numpy as np
import csv
from matplotlib import pyplot

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
            self.restroom.append([restroom_floor,0])

    # 時間軸を生成する関数
    def make_time_model(self,start,stop):
        self.t = np.arange(start,stop)

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

    def make_line_graph(self,x,y):
        pyplot.plot(x,y)
        pyplot.show()


model = RestroomModel()
model.read_csv('./people.csv', 'people')
model.read_csv('./place.csv', 'place')
model.make_restroom((6,6,6,6,6))
model.make_time_model(0,5400)
wait_people = []
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
                model.restroom[num_floor][1] += 1
                model.people[num_people][3] = str(int(model.people[num_people][3])+1)
                model.people[num_people][5] = str(int(model.people[num_people][3]) + int(model.people[num_people][4]))
                model.people[num_people][7] = str(int(model.people[num_people][7])+1)
        elif int(model.people[num_people][6]) == 2:
            ret = model.search_empty(num_floor)
            if ret :
                model.people[num_people][6] = 1
                model.restroom[num_floor][1] -= 1
            else :
                model.people[num_people][3] = str(int(model.people[num_people][3])+1)
                model.people[num_people][5] = str(int(model.people[num_people][3]) + int(model.people[num_people][4]))
                model.people[num_people][7] = str(int(model.people[num_people][7])+1)

        elif time == int(model.people[num_people][5]):
            model.leave_room(num_floor)
    wait_people.append(model.restroom[num_floor][1])

    print(*model.restroom, sep='\n')
    print('\n')
x = range(0,5400)
y = wait_people
model.make_line_graph(x,y)
wait_time = []
for i in model.people[1:]:
    wait_time.append(int(i[7]))
print(np.mean(np.array(wait_time)))