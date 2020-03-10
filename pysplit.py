from tkinter import *
import time
import re

class SplitGUI:
    def __init__(self, app):

        self.root = Tk()
        self.root.title("PySplit 0.4")
        self.root.geometry("400x800")
        self.root.configure(bg = "black")
        self.root.resizable(False, False)

        self.hf = None
        self.app = app

        self.loadSetup()
        self.root.mainloop()


    def mainGUI(self):

            self.started = 0
            self.dispText = "00:00"
            self.timePassed = 0
            self.hide = False

            self.ahead = True
            self.behind = False
            self.near = False
            self.lastSplit = False

            self.runSplits = []

            lblLists = self.createLblLists()
            self.labelRunTimeList = lblLists[0]
            self.labelNameList = lblLists[1]
            self.labelTimeList = lblLists[2]

            self.nbrOfSplits = len(self.hf.splitObjList)
            self.currentSplit = 0
            self.finalSplitInfo = self.hf.splitObjList[-1].name + ": " + self.hf.splitObjList[-1].time

            self.currTimeDiff = ""
            self.currTimeDiffText = ""


            self.hrOne = Frame(self.root, height = 1, width = self.root.winfo_width(), bg = "gray")
            self.hrOne.place(relx = 0.5, rely = 0.18, anchor = N)
            self.hrTwo  = Frame(self.root, height = 1, width = self.root.winfo_width(), bg = "gray")
            self.hrTwo.place(relx = 0.5, rely = 0.27, anchor = N)

            self.timeLbl = Label(self.root, text = self.dispText, bg = "black", fg = "white")
            self.timeLbl.config(font=("Courier 40 bold"))

            self.timeDiffLbl =  Label(self.root, text = self.currTimeDiffText, bg = "black", fg = "white")
            self.timeDiffLbl.config(font=("Courier 12 bold"))

            self.currentSplitInfo = self.getCurrSplitInfo()
            self.currentSplitName = self.currentSplitInfo[0]
            self.currentSplitTime = self.currentSplitInfo[1]

            self.currSplitNameLbl = Label(self.root, text = self.currentSplitName, bg = "black", fg = "white")
            self.currSplitNameLbl.config(font=("Courier 12 bold"))

            self.currSplitTimeLbl = Label(self.root, text = self.currentSplitTime, bg = "black", fg = "white")
            self.currSplitTimeLbl.config(font=("Courier 12 bold"))

            self.finalSplitLbl = Label(self.root, text = self.finalSplitInfo, bg = "black", fg = "orange")
            self.finalSplitLbl.config(font=("Courier 12"))

            self.startBtn = Button(self.root, text = "Start", command = self.start, highlightbackground="Black", fg="Black")
            self.stopBtn = Button(self.root, text = "Stop", command = self.stop, highlightbackground="Black", fg="Black")
            self.resetBtn = Button(self.root, text = "Reset", command = self.reset, highlightbackground="Black", fg="Black")

            self.timeLbl.place(relx=0.5, rely=0.06, anchor=CENTER)

            self.currSplitNameLbl.place(relx = 0.22, rely = 0.2, anchor = CENTER)
            self.currSplitTimeLbl.place(relx = 0.5, rely = 0.2, anchor = CENTER)
            self.timeDiffLbl.place(relx = 0.7, rely = 0.2, anchor = CENTER)
            self.finalSplitLbl.place(relx = 0.025, rely = 0.27, anchor = W)


            self.startBtn.place(relx=0.35, rely=0.13, anchor=CENTER)
            self.stopBtn.place(relx=0.5, rely=0.13, anchor=CENTER)
            self.resetBtn.place(relx=0.65, rely=0.13, anchor=CENTER)

            self.hideID = self.root.bind("<h>", lambda e:self.hideBtns(not self.hide))
            self.root.bind("r", lambda e:self.reset())
            if(self.started == 0):
                self.bindSpaceID = self.root.bind("<space>", lambda e:self.start())


    def start(self):
        self.started = 1
        self.startBtn.configure(text = "Split", command = self.split)
        if(self.currentSplit < self.nbrOfSplits):
            self.bindSpaceID = self.root.bind("<space>", lambda e:self.split())
        self.timeStart = time.time()
        self.count()

    def count(self):
        if(self.started == 1):
            self.afterID = self.root.after(50, self.count)

        self.timePassed = time.time() - self.timeStart

        self.currTimeDiff = self.timePassed - self.app.toTotalSec(self.hf.splitObjList[self.currentSplit].time)
        if(abs(self.currTimeDiff) <= 20):
            self.near = True
        else:
            self.near = False

        if(self.currTimeDiff < 0):
            self.ahead = True
            self.behind = False
            self.currTimeDiff = self.app.toTime(abs(self.currTimeDiff))
        else:
            self.ahead = False
            self.behind = True
            self.currTimeDiff = self.app.toTime(self.currTimeDiff)

        self.dispText = self.app.toTime(self.timePassed)
        self.update()

    def update(self):
        self.timeLbl.configure(text = self.dispText)

        currSplitInfo = self.getCurrSplitInfo()
        currSplitName = currSplitInfo[0]
        currSplitTime = currSplitInfo[1]
        self.currSplitNameLbl.configure(text = currSplitName)

        if(self.lastSplit == False):
            self.currSplitTimeLbl.configure(text = currSplitTime)
        else:
            self.currSplitTimeLbl.configure(text = self.runSplits[-1])

        if(self.ahead == True and self.near == True):
            self.currTimeDiffText = "-" + self.currTimeDiff
            self.timeDiffLbl.configure(text = self.currTimeDiffText)
        elif(self.behind == True):
            self.currTimeDiffText = "+" + self.currTimeDiff
            self.timeDiffLbl.configure(text = self.currTimeDiffText)
        else:
            self.timeDiffLbl.configure(text = "")
            self.currTimeDiffText = "-" + self.currTimeDiff

    def getCurrSplitInfo(self):
        return([self.hf.splitObjList[self.currentSplit].name,
               self.hf.splitObjList[self.currentSplit].time])

    def stop(self):
        if(self.started==0):
            try:
                self.startBtn.destroy()
                self.stopBtn.destroy()
            except:
                pass
            return
        self.root.unbind("<space>", self.bindSpaceID)
        self.startBtn.destroy()
        self.stopBtn.destroy()

        pb = (self.timePassed < self.app.toTotalSec(self.hf.splitObjList[-1].time))
        stopEarly = (self.currentSplit + 1 < self.nbrOfSplits)
        if(pb and not stopEarly):
            self.timeLbl.config(fg = "yellow")

            self.saveSplitTextLbl = Label(self.root,
                                          text = "Save new splits? (Enter filename)",
                                          bg = "black", fg = "white")
            self.saveSplitTextLbl.config(font=("Courier 10"))

            self.saveSplitTextLbl.place(relx = 0.5, rely = 0.85, anchor = S)

            self.saveSplitEntry = Entry(self.root)
            self.saveSplitEntry.place(relx = 0.5, rely = 0.90, anchor = S)

            self.saveSplitBtn = Button(self.root, text = "Save",
                                       command = self.save,
                                       highlightbackground="Black", fg="Black")
            self.saveSplitBtn.place(relx = 0.8, rely = 0.90, anchor = S)
            self.bindID = self.root.bind("<Return>", lambda e:self.save())


        elif(not stopEarly):
            self.timeLbl.config(fg = "red")
        else:
            self.timeLbl.config(fg = "white")
        self.started = 0

    def save(self):
        self.root.unbind("<Return>", self.bindID)
        fileName = str(self.saveSplitEntry.get())
        self.hf.save(fileName, self.runSplits, self.hf.splitObjList)
        self.saveSplitBtn.destroy()
        self.saveSplitEntry.destroy()
        self.saveSplitTextLbl.destroy()

    def loadSetup(self):
        self.loadSplitTextLbl = Label(self.root,
                                      text = "Load split (Enter filename)",
                                      bg = "black", fg = "white")
        self.loadSplitTextLbl.config(font=("Courier 10"))
        self.loadSplitTextLbl.place(relx = 0.5, rely = 0.1, anchor = N)

        self.loadSplitEntry = Entry(self.root)
        self.loadSplitEntry.place(relx = 0.5, rely = 0.125, anchor = N)

        self.loadSplitBtn = Button(self.root, text = "Load",
                                   command = self.load,
                                   highlightbackground="Black", fg="Black")
        self.loadSplitBtn.place(relx = 0.8, rely = 0.125, anchor = N)
        self.bindID = self.root.bind("<Return>", lambda e:self.load())

    def load(self):
        self.root.unbind("<Return>", self.bindID)
        fileName = str(self.loadSplitEntry.get())
        self.hf = HandleFile(fileName = fileName, app = self.app)
        self.loadSplitBtn.destroy()
        self.loadSplitEntry.destroy()
        self.loadSplitTextLbl.destroy()
        self.mainGUI()

    def reset(self):
        try:
            self.saveSplitBtn.destroy()
            self.saveSplitEntry.destroy()
            self.saveSplitTextLbl.destroy()
        except:
            pass

        if hasattr(self, 'afterID'):
            self.root.after_cancel(self.afterID)
        self.timeLbl.config(fg = "white")
        self.runSplits = []

        self.started = 0
        self.timePassed = 0
        self.hide = False

        self.ahead = True
        self.behind = False
        self.near = False
        self.lastSplit = False

        self.currentSplit = 0
        self.finalSplitInfo = self.hf.splitObjList[-1].name + ": " + self.hf.splitObjList[-1].time

        self.currentSplitInfo = self.getCurrSplitInfo()
        self.currentSplitName = self.currentSplitInfo[0]
        self.currentSplitTime = self.currentSplitInfo[1]

        self.currSplitNameLbl.configure(text = self.currentSplitName)
        self.currSplitTimeLbl.configure(text = self.currentSplitTime)
        self.timeDiffLbl.configure(text = "")
        self.timeLbl.configure(text = "00:00")

        try:
            self.startBtn.destroy()
            self.stopBtn.destroy()
        except:
            pass
        self.startBtn = Button(self.root, text = "Start", command = self.start,
                               highlightbackground="Black", fg="Black")
        self.stopBtn = Button(self.root, text = "Stop", command = self.stop,
                              highlightbackground="Black", fg="Black")
        self.startBtn.place(relx=0.35, rely=0.13, anchor=CENTER)
        self.stopBtn.place(relx=0.5, rely=0.13, anchor=CENTER)

        self.hrTwo.place(relx = 0.5, rely = 0.27, anchor = N)

        for lbl in self.labelRunTimeList:
            lbl.destroy()
        for lbl in self.labelNameList:
            lbl.destroy()
        for lbl in self.labelTimeList:
            lbl.destroy()
        lblLists = self.createLblLists()
        self.labelRunTimeList = lblLists[0]
        self.labelNameList = lblLists[1]
        self.labelTimeList = lblLists[2]

        self.currSplitNameLbl.place(relx = 0.22, rely = 0.2, anchor = CENTER)
        self.currSplitTimeLbl.place(relx = 0.5, rely = 0.2, anchor = CENTER)
        self.timeDiffLbl.place(relx = 0.7, rely = 0.2, anchor = CENTER)
        self.finalSplitLbl.place(relx = 0.025, rely = 0.27, anchor = W)

        self.bindSpaceID = self.root.bind("<space>", lambda e:self.start())

    def hideBtns(self, hide):
        if(hide == True):
            try:
                self.startBtn.place_forget()
                self.stopBtn.place_forget()
                self.resetBtn.place_forget()
            except:
                pass
        else:
            try:
                self.startBtn.place(relx=0.35, rely=0.13, anchor=CENTER)
                self.stopBtn.place(relx=0.5, rely=0.13, anchor=CENTER)
                self.resetBtn.place(relx=0.65, rely=0.13, anchor=CENTER)
            except:
                pass
        self.hide = not self.hide



    def split(self):
        if(self.started == 0):
            return
        self.runSplits.append(self.app.toTime(self.timePassed))
        if(self.currentSplit >= self.nbrOfSplits - 1):
            self.lastSplit = True
            self.startBtn.destroy()
            self.stopBtn.destroy()
            currX = float(self.currSplitTimeLbl.place_info()["relx"])
            currY = float(self.currSplitTimeLbl.place_info()["rely"])
            if(self.ahead == True):
                colVar = "yellow"
            else:
                colVar = "red"
            self.labelRunTimeList.append(Label(self.root,
                                            text = self.currTimeDiffText,
                                            bg = "black", fg = colVar,
                                            font = ("Courier 12 bold") ))
            self.labelRunTimeList[-1].place(relx = 0.7, rely = currY, anchor = CENTER)
            self.stop()
        else:
            self.currentSplit += 1
            offset = 0.02
            currX = float(self.currSplitNameLbl.place_info()["relx"])
            currY = float(self.currSplitNameLbl.place_info()["rely"])

            self.currSplitNameLbl.place(relx = 0.22, rely = currY + offset)
            self.labelNameList[self.currentSplit - 1].place(relx = currX, rely = currY, anchor = CENTER)
            self.labelNameList[self.currentSplit - 1].config(fg = "gray")


            currX = float(self.currSplitTimeLbl.place_info()["relx"])
            currY = float(self.currSplitTimeLbl.place_info()["rely"])
            self.currSplitTimeLbl.place(relx = 0.5, rely = currY + offset, anchor = CENTER)

            self.timeDiffLbl.place(relx = 0.7, rely = currY + offset, anchor = CENTER)
            self.labelRunTimeList[self.currentSplit - 1].configure(text = self.currTimeDiffText)
            self.labelRunTimeList[self.currentSplit - 1].place(relx = 0.7, rely = currY, anchor = CENTER)
            if(self.ahead):
                self.labelRunTimeList[self.currentSplit -1].configure(fg = "yellow")
            if(self.behind):
                self.labelRunTimeList[self.currentSplit -1].configure(fg = "red")

            self.labelTimeList[self.currentSplit - 1].place(relx = 0.5, rely = currY, anchor = CENTER)
            self.labelTimeList[self.currentSplit - 1].config(fg = "gray", text = self.runSplits[-1])

            currX = float(self.finalSplitLbl.place_info()["relx"])
            currY = float(self.finalSplitLbl.place_info()["rely"])
            self.finalSplitLbl.place(relx = currX, rely = currY + offset, anchor = W)

            self.hrTwo.place(relx = 0.5, rely = currY + offset, anchor = N)

    def createLblLists(self):
        runTimeList = []
        splitNameList = []
        splitTimeList = []
        for split in self.hf.splitObjList:
            name = split.name
            time = split.time
            runTimeList.append(Label(self.root, text = "",
                                        bg = "black", fg = "white",
                                        font = ("Courier 12 bold")))
            splitNameList.append(Label(self.root, text = name,
                                        bg = "black", fg = "white",
                                        font = ("Courier 12 bold")))
            splitTimeList.append(Label(self.root, text = time,
                                        bg = "black", fg = "white",
                                        font = ("Courier 12 bold")))
        return([runTimeList, splitNameList, splitTimeList])

class SplitApp:
    def __init__(self):
        pass

    def toTime(self, totalSec):
        m = int(totalSec/60)
        h = int(m/60)
        if(h > 0):
            m = m - 60*h
            s = int(totalSec - 3600*h - 60*m )
        elif(m > 0):
            s = int(totalSec - 60*m)
        else:
            s = int(totalSec)

        if(h >= 10):
            hText = str(h) + ":"
        else:
            hText = "0" + str(h) + ":"

        if(m >= 10):
            mText = str(m) + ":"
        else:
            mText = "0" + str(m) + ":"

        if(s >= 10):
            sText = str(s)
        else:
            sText = "0" + str(s)

        if(hText == "00:"):
            return(mText + sText)
        else:
            return(hText + mText + sText)

    def toSegmentTime(self, time):
        times = re.split("-", time)
        currTime = times[0]
        prevTime = times[1]
        self.timeDiff = self.toTotalSec(currTime) - self.toTotalSec(prevTime)
        return(self.timeDiff)

    def toTotalSec(self, time):
        if(len(time) == 5):
            time = "00:" + time
        hms = re.split(":", time)
        h = hms[0]
        m = hms[1]
        s = hms[2]
        if(h != "00"):  #Will not work if h>=10
            h = int(h[1])
        else:
            h = 0
        if(m != "00"):
            if(m[0] == "0"):
                m = int(m[1])
            else:
                m = int(m)
        else:
            m = 0
        if(s != "00"):
            if(s[0]=="0"):
                s = int(s[1])
            else:
                s = int(s)
        else:
            s = 0

        s = s + m*60 + h*3600
        return(s)



class HandleFile:
    def __init__(self, fileName, app):
        self.fileName = fileName
        self.app = app
        self.splitObjList = []
        self.segmentObjList = []
        self.splitDict = {}
        self.createSplits()
        self.createSegments()

    def createSplits(self):

        fh = open(self.fileName,"r")
        fileContents = fh.read()
        runInfo = re.findall(r'\[(.*?)\]', fileContents)

        splitList = runInfo[1].split(",")
        timeList = runInfo[2].split(",")

        index = 0
        for split in splitList:
            self.splitDict[split] = timeList[index]
            index+=1

        order = 0
        for key in self.splitDict:
            run = runInfo[0]
            name = key
            time = self.splitDict[key]

            splitObj = Split(run = run, name = name,
                             time = time, order = order)
            self.splitObjList.append(splitObj)
            order+=1


    def createSegments(self):
        order = 0
        for split in self.splitObjList:
            curr=split.time
            if(order == 0):
                previous = "00:00:00"
            else:
                previous = self.splitObjList[order - 1].time

            timeDiff = curr + "-" + previous
            timeDiff = self.app.toSegmentTime(timeDiff)
            newSegment = Segment(run = split.run, best = 0,
                                 timeDiff=timeDiff, order=order)
            self.segmentObjList.append(newSegment)
            order += 1

    def save(self, fileName, runSplits, splitNames):
        fh = open(fileName, "w")

        run = splitNames[0].run.lstrip()
        runString = "<Run>[" + run + "]"

        splitNameString = ""
        for split in splitNames:
            splitNameString = splitNameString + split.name + ", "
        splitNameString = splitNameString[:-2]
        splitNameString = "<Splits>[" + splitNameString + "]"

        splitTimeString = ""
        for time in runSplits:
            splitTimeString = splitTimeString + time + ", "
        splitTimeString = splitTimeString[:-2]
        splitTimeString = "<Times>[" + splitTimeString + "]"

        fh.write(runString + "\n")
        fh.write(splitNameString + "\n")
        fh.write(splitTimeString)


class Segment:
    def __init__(self, run, best, timeDiff, order):
        self.run = run
        self.best = "0"
        self.timeDiff = timeDiff
        self.order = order + 1
    def __str__(self):
        return("Run: " + self.run + "\n" +
               "Time: " + str(self.timeDiff))

class Split:
    def __init__(self, run, name, time, order):
        self.run = run.lstrip()
        self.name = name.lstrip()
        self.time = time.lstrip()
        self.time = SplitApp.toTotalSec(self, self.time)
        self.time = SplitApp.toTime(self, self.time)
        self.order = order + 1

    def __str__(self):
        return("Run: " + self.run + "\n" +
               "Name: " + self.name + "\n" +
               "Time: " + self.time + "\n" +
               "Order: " + str(self.order) + "\n")




app = SplitApp()
gui = SplitGUI(app = app)


## TODO:
## Segment and gold segments
