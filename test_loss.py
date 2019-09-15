import torch
import torch.nn as nn
import sys

chi_word1 = '二零一六户'


trans = {}
trans['0'] = "零"
trans['1'] = "一"
trans['2'] = "二"
trans['3'] = "三"
trans['4'] = "四"
trans['5'] = "五"
trans['6'] = "六"
trans['7'] = "七"
trans['8'] = "八"
trans['9'] = "九"

min_distance = sys.maxsize
res = {}

ctcloss = torch.nn.CTCLoss()

for x in range(10000):
    str_x = str(x)
    for i in range(4-len(str_x)):
        str_x = '0' + str_x
    str_ch = "二零一六"
    for c in str_x:
        str_ch += trans[c]
    assert(len(str_ch)==8)
    distance = ctcloss(chi_word1,len(chi_word1),str_ch,len(str_ch))
    # print(distance)
    if distance < min_distance:
        min_distance = distance
    if distance in res.keys():
        res[distance].append(str_ch)
    else:
        res[distance] = []
        res[distance].append(str_ch)

print(res[min_distance])