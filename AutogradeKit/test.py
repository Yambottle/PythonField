#!/usr/bin/env python 3.6
# -*- coding: utf-8 -*-
# @Time    : 2/23/18 12:22
# @Author  : Yam
# @Site    :
# @File    : test.py
# @Software: PyCharm

import autograde as ag

grader = ag.AutoGrader('0204', '2359', 36)
grader.file_read()
grader.pre_check()
print("------------")
grader.find_best()
grader.best_check()
print("------------")
grader.find_late()
#grader.late_check()


