#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import numpy as np
import csv
from matplotlib import pyplot
import cv2
import os
import time
import sys

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
    height = 0
    width = 0
    img_count = 0
    probability = 0.0

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
        self.size = size
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
        if near == 't7':
            near = 't6'
        return near

    # 満室でない最も近いフロアのトイレを返す関数
    def search_empty_floor(self):
        num_restroom_each = [sum(i[0]) for i in self.restroom]
        empty_floor = 't{0}'.format(num_restroom_each.index(min(num_restroom_each))+2)
        return empty_floor

    # シミュレーション映像のフレーム作成
    def make_img(self, size):
        self.height = size[0]
        self.width = size[1]
        self.frame = np.zeros((self.height,self.width,3))
        self.margin = int(10*self.width/640)
        # 縦の線を描画
        for i in range(max(self.size)+1):
            cv2.line(
                self.frame,
                (int(i*(self.width/2-self.margin)/max(self.size))+self.margin,self.margin),
                (int(i*(self.width/2-self.margin)/max(self.size))+self.margin,self.height-self.margin),
                (255,255,255),
                1
            )
        cv2.line(
            self.frame,
            (self.width-self.margin,self.margin),
            (self.width-self.margin,self.height-self.margin),
            (255,255,255),
            1
        )
        # 横の線を描画
        for i in range(len(self.size)+1):
            cv2.line(
                self.frame,
                (self.margin,int(i*(self.height-self.margin*2)/len(self.size))+self.margin),
                (self.width-self.margin,int(i*(self.height-self.margin*2)/len(self.size))+self.margin),
                (255,255,255),
                1
            )
            cv2.putText(
                self.frame,
                '{0}F'.format(i+2),
                (self.width-(self.margin+int(50*self.width/640)),int((i+1)*(self.height-self.margin*2)/len(self.size))),
                cv2.FONT_HERSHEY_PLAIN,
                int(2*self.width/640),
                (127*(i%3),127*((i+1)%3),127*((i+2)%3)),
                3,
                cv2.LINE_AA
            )

        for i in range(len(self.restroom)):
            for j in range(len(self.restroom[i][0])):
                if self.restroom[i][0][j] == 1:
                    cv2.circle(
                        self.frame,
                        (int((j+0.5)*(self.width/2-self.margin)/max(self.size))+self.margin,int((i+0.5)*(self.height-self.margin*2)/len(self.size))+self.margin),
                        int(20*self.width/640),
                        (127*(i%3),127*((i+1)%3),127*((i+2)%3)),
                        -1
                    )
            for j in range(self.restroom[i][1]):
                cv2.circle(
                    self.frame,
                    (int(self.width/2+self.margin)+j*int(12*self.width/640),int((i+0.5)*(self.height-self.margin*2)/len(self.size))+self.margin),
                    int(3*self.width/640),
                    (127*(i%3),127*((i+1)%3),127*((i+2)%3)),
                    -1
                )
        cv2.imwrite('./img/{0}.png'.format(self.img_count),self.frame)
        self.img_count += 1

    # フレームをつなぎ合わせて動画を作成する関数
    def make_video(self,size):
        ts = time.time()
        fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
        video = cv2.VideoWriter('User_{0}.mp4'.format(1-self.probability), fourcc, 30.0, (size[1],size[0]))
        print('動画エンコード中')
        for img_file in os.listdir('./img'):
            img = cv2.imread('./img/{0}'.format(img_file))
            video.write(img)
            os.remove('./img/{0}'.format(img_file))
        video.release()
        print('エンコード時間：{0}秒'.format(time.time()-ts))


model = RestroomModel()
model.read_csv('./people.csv', 'people')
model.read_csv('./place.csv', 'place')
model.make_restroom((6,6,6,6,6))
model.probability = 1 - int(sys.argv[1])/100
print(model.probability)
finish_time = 1500
model.make_time_model(0,finish_time)
wait_people = [[],[],[],[],[]]
img_size = (720,1280)
for model_time in model.t:
    print(model_time)
    for num_people in range(1,len(model.people)):
        place_name = model.people[num_people][2]
        try :
            num_floor = model.num_floor_list[place_name]
        except:
            pass
        if (model_time == int(model.people[num_people][3])) & (int(model.people[num_people][6]) == 0):
            ret = model.search_empty(num_floor)
            if ret :
                model.people[num_people][6] = 1
            else :
                model.people[num_people][6] = 2
                model.restroom[num_floor][1] += 1
                model.people[num_people][3] = str(int(model.people[num_people][3])+1)
                model.people[num_people][5] = str(int(model.people[num_people][3]) + int(model.people[num_people][4]))
                model.people[num_people][7] = str(int(model.people[num_people][7])+1)
        elif (model_time == int(model.people[num_people][3])) & (int(model.people[num_people][6] == 4)):
            ret = model.search_empty(num_floor)
            if ret :
                model.people[num_people][6] = 1
            else :
                model.people[num_people][6] = 5
                model.restroom[num_floor][1] += 1
                model.people[num_people][3] = str(int(model.people[num_people][3])+1)
                model.people[num_people][5] = str(int(model.people[num_people][3]) + int(model.people[num_people][4]))
                model.people[num_people][7] = str(int(model.people[num_people][7])+1)
        elif (int(model.people[num_people][6]) == 2) or (int(model.people[num_people][6]) == 5) or (int(model.people[num_people][6]) == 6):
            ret = model.search_empty(num_floor)
            temp_probability = np.random.rand()
            if ret :
                model.people[num_people][6] = 1
                model.restroom[num_floor][1] -= 1
            elif (np.random.rand() > model.probability) & (int(model.people[num_people][6]) == 2):
                near = model.search_near(place_name)
                for search_i in range(len(model.restroom)):
                    print(near)
                    if model.search_empty(model.num_floor_list[near]):
                        print('空室あった！！！！！！！！！！')
                        model.move_room(num_people,place_name,near)
                        break
                    else:
                        near = model.search_near(near)
                        print('空室なし！！！！！！！！！！！！！！！')
                model.people[num_people][6] = 4
                model.restroom[num_floor][1] -= 1
            elif (temp_probability <= model.probability) & (int(model.people[num_people][6]) == 2):
                model.people[num_people][6] = 6
            else :
                model.people[num_people][3] = str(int(model.people[num_people][3])+1)
                model.people[num_people][5] = str(int(model.people[num_people][3]) + int(model.people[num_people][4]))
                model.people[num_people][7] = str(int(model.people[num_people][7])+1)

        elif model_time == int(model.people[num_people][5]):
            model.leave_room(num_floor)
            model.people[num_people][6] = 3
    for i in range(len(model.restroom)):
        wait_people[i].append(model.restroom[i][1])
    print(*model.restroom, sep='\n')
    print(model.search_empty_floor())
    print('\n')
    model.make_img(img_size)
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
model.write_csv('./User_{0}.csv'.format(1-model.probability),list)
model.make_video(img_size)