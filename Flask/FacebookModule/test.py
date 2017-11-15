class tahi():

    dict = {2:["dsada"]}


    def getDict(self):
        print self.dict

    def callDict(self):
        self.dict[0] = ["sad","sdd"]
        self.dict[1] = ["hikta"]

    def addDict(self):
        self.dict[0].append("takjtak")


if __name__ == "__main__":
    x= tahi()
    x.getDict()
    x.callDict()
    x.getDict()
    x.addDict()
    x.getDict()