class RestroomModel:
    restroom = [0,0,0,0,0,0]
    place = {
        '0201':[10,30,50,70,90,110],
        '0301':[30,10,30,50,70,90]
    }

    people = [
        [0,'men','0210',0,50],
        [1,'men','0210',1,50],
        [2,'men','0210',2,50],
        [3,'men','0210',3,50],
        [4,'men','0210',4,50],
        [5,'men','0210',5,50],
        [6,'men','0210',6,50]
    ]

    t=0

    def start(self, duration):
        for i in range(duration):
            print(self.t)
            for j in self.people:
                if self.t - j[3] == 0:
                    
                    for k in range(len(self.restroom)):
                        if self.restroom[k] != 0:
                            if k == len(self.restroom)-1:
                                print('cannnot enter')
                        else:
                            self.restroom[k] = 1
                            print('enter')
                            break

                if self.t - (j[3] + j[4]) == 0:
                    for k in range(len(self.restroom)):
                        if self.restroom[k] == 1:
                            self.restroom[k] = 0
                            print('leave')
                            break
            print(self.restroom)
            self.t += 1

model = RestroomModel()
model.start(100)