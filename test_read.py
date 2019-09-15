import os

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


with open("train_index","w") as f:
	for filename in os.listdir('data/'):
		# print(filename)
		s1 = filename[:8]
		s2 = ""
		for x in s1:
			s2 += trans[x]
		s1 = "data/" + s1 +".wav"
		f.write(s1+","+s2+"\n")