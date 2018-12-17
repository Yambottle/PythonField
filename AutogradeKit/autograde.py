#!/usr/bin/env python 3.6
# -*- coding: utf-8 -*-
# @Time    : 2/23/18 12:22
# @Author  : Yam
# @Site    : 
# @File    : autograde.py
# @Software: PyCharm


class AutoGrader:

    ddate = 0
    dtime = 0
    lname = ''

    premap = []
    latepremap = []

    scoremap = []
    latescoremap = []

    def __init__(self,logname, date, time):
        self.lname = logname
        self.ddate = int(date)
        self.dtime = int(time)

    def file_read(self):
        # "syslog.txt"
        file = open(self.lname, "r")
        lines = file.read().split('\n')
        file.close()

        # find total score
        tscore = 0
        for line in lines:
            if line == '':
                continue
            newline = line.split(">")
            if tscore<len(newline[1]):
                tscore = len(newline[1])

        for line in lines:
            # for the empty line with '\n'
            if line == '':
                continue
            # info & score
            newline = line.split(">")
            # infos
            newline[0] = newline[0].split("_")
            # name contain underscore
            newline[0][1:-1] = [''.join(newline[0][1:-1])]
            # date & time
            newline[0][2] = newline[0][2].split(":")
            # datetime type conversion
            newline[0][2][0] = int(newline[0][2][0])
            newline[0][2][1] = int(newline[0][2][1])
            # score
            if newline[1] =='unknown':
                newline[1] = 0
            else:
                tempscore = newline[1].split('F')
                newline[1] = round(len(tempscore[0])/tscore*100*0.01, 2)*20
                # newline[1] = round(len(tempscore[0]) / tscore * 100, 2)
            # deadline filter
            # if int(newline[0][2][0]) > self.ddate or (int(newline[0][2][0]) == self.ddate and int(newline[0][2][1]) > self.dtime):
            #     self.latepremap.append(newline)
            # else:
            #     self.premap.append(newline)
            self.premap.append(newline)

        self.premap.sort()

    def pre_check(self):
        for line in self.premap:
            print(line)

    def late_punish(self):
        for line in self.premap:
            if line[0][2][0]-self.ddate == 1:
                line[1] = line[1]*0.9
            elif line[0][2][0]-self.ddate >= 2 & line[0][2][0]-self.ddate <= 3:
                line[1] = line[1]*0.85
            elif line[0][2][0]-self.ddate >= 4 & line[0][2][0]-self.ddate <= 7:
                line[1] = line[1]*0.8
            else:
                line[1] = line[1] * (0.8-((line[0][2][0] - self.ddate) % 7) * 0.1)

    def find_best(self):
        cur_stu = self.premap[0][0][0]
        max = float(self.premap[0][1])
        best_score = self.premap[0]

        for line in self.premap:
            if cur_stu == line[0][0]:
                if max < line[1]:
                    max = line[1]
                    best_score = line
            else:
                self.scoremap.append(best_score)
                cur_stu = line[0][0]
                max = line[1]
                best_score = line

    def best_check(self):
        for line in self.scoremap:
            print(line)
    #
    # def find_late(self):
    #     cur_stu = self.latepremap[0][0][0]
    #     max = self.latepremap[0][1]
    #     best_score = self.latepremap[0]
    #
    #     for line in self.latepremap:
    #         if cur_stu == line[0][0]:
    #             if max < line[1]:
    #                 max = line[1]
    #                 best_score = line
    #         else:
    #             self.latescoremap.append(best_score)
    #             cur_stu = line[0][0]
    #             best_score = line
    #
    # def late_check(self):
    #     for line in self.latescoremap:
    #         print(line)

