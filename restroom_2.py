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
    num_floor_list = {
        't2':0,
        't3':1,
        't4':2,
        't5':3,
        't6':4
    }

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

    # 化粧室に並んでいる人数の推移をcsvファイルで出力する関数
    def write_csv(self, filename, list):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(list)

    
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

    # 指定されたフロアのトイレに移動する関数
    def move_room(self,num_people,place_from,place_to):
        transfer_time = 0
        for room in self.place :
            if room[0] == place_from :
                num_place_to = self.num_floor_list[place_to] + 1
                transfer_time = int(room[num_place_to])
                break
        print(transfer_time)
        self.people[num_people][3] = str(int(self.people[num_people][3]) + transfer_time)
        self.people[num_people][5] = str(int(self.people[num_people][3]) + int(self.people[num_people][4]))
        self.people[num_people][2] = place_to

    # 現在地から最も近いフロアのトイレを返す関数
    def search_near(self,place_name):
        for i in range(len(self.place)):
            if place_name == self.place[i][0]:
                break
        near = 't{0}'.format(self.place[i].index(sorted(self.place[i][1:])[1])+1)
        return near

    # 満室でない最も近いフロアのトイレを返す関数
    def search_empty_floor(self):
        num_restroom_each = [sum(i[0]) for i in self.restroom]
        empty_floor = 't{0}'.format(num_restroom_each.index(min(num_restroom_each))+2)
        return empty_floor


model = RestroomModel()
model.read_csv('./people.csv', 'people')
model.read_csv('./place.csv', 'place')
model.make_restroom((6,6,6,6,6))
finish_time = 1200
model.make_time_model(0,finish_time)
wait_people = [[],[],[],[],[]]
for time in model.t:
    print(time)
    for num_people in range(1,len(model.people)):
        place_name = model.people[num_people][2]
        try :
            num_floor = model.num_floor_list[place_name]
        except:
            pass
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
        elif (time == int(model.people[num_people][3])) & (int(model.people[num_people][6] == 4)):
            ret = model.search_empty(num_floor)
            if ret :
                model.people[num_people][6] = 1
            else :
                model.people[num_people][6] = 5
                model.restroom[num_floor][1] += 1
                model.people[num_people][3] = str(int(model.people[num_people][3])+1)
                model.people[num_people][5] = str(int(model.people[num_people][3]) + int(model.people[num_people][4]))
                model.people[num_people][7] = str(int(model.people[num_people][7])+1)
        elif (int(model.people[num_people][6]) == 2) or (int(model.people[num_people][6]) == 5):
            ret = model.search_empty(num_floor)
            if ret :
                model.people[num_people][6] = 1
                model.restroom[num_floor][1] -= 1
            # elif (np.random.rand() >= 0.0) & (int(model.people[num_people][6]) == 2):
            #     near = model.search_near(place_name)
            #     for search_i in range(len(model.restroom)):
            #         print(near)
            #         if model.search_empty(model.num_floor_list[near]):
            #             print('空室あった！！！！！！！！！！')
            #             break
            #         else:
            #             near = model.search_near(near)
            #             print('空室なし！！！！！！！！！！！！！！！')
            #     model.move_room(num_people,place_name,near)
            #     model.people[num_people][6] = 4
            #     model.restroom[num_floor][1] -= 1
            else :
                model.people[num_people][3] = str(int(model.people[num_people][3])+1)
                model.people[num_people][5] = str(int(model.people[num_people][3]) + int(model.people[num_people][4]))
                model.people[num_people][7] = str(int(model.people[num_people][7])+1)

        elif time == int(model.people[num_people][5]):
            model.leave_room(num_floor)
            model.people[num_people][6] = 3
    for i in range(len(model.restroom)):
        wait_people[i].append(model.restroom[i][1])
    print(*model.restroom, sep='\n')
    print(model.search_empty_floor())
    print('\n')
x = range(0,finish_time)
wait_time = []
for i in model.people[1:]:
    wait_time.append(int(i[7]))
print(*model.people, sep='\n')
print(np.mean(np.array(wait_time)))
list = [list(x)]
for i in range(len(wait_people)):
    pyplot.plot(x,wait_people[i])
    list.append(wait_people[i])
pyplot.show()
model.write_csv('./result_1.csv',list)