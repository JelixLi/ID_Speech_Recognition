from pypinyin import pinyin, Style
import pypinyin
import math
import Levenshtein as Lev

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

def translate(num_str):
	s2 =''	
	for x in num_str:
		s2 += trans[x]
	return s2

def get_shengdiao(pinyin_str):
	res = []
	for x in pinyin_str:
		s = x[0]
		res += s[-1]
	return res

WL = 3

def I(ch1,ch2):
	return (ch1==ch2)

# def F(d):
# 	return 1.0 / (d+1)

# def F(d):
# 	return 1.0 / math.sqrt(d+1)

def F(d):
	return 1.0 / pow(2,d+1)

# def F(d):
# 	return 1.0 / pow(d+1,2)

def ch_similarity_sub(ch_str_1,ch_str_2):
	n = len(ch_str_1)
	m = len(ch_str_2)
	e1 = 0.0
	for i in range(n):
		for j in range(m):
			d = abs(i-j)
			if d<=WL:
				e1 += F(d)*I(ch_str_1[i],ch_str_2[j])
	return e1 / n

def SCH(ch_str_1,ch_str_2):
	return ch_similarity_sub(ch_str_1,ch_str_2)

def SPY(ch_str_1,ch_str_2):
	pinyin_1 = pinyin(ch_str_1,style=Style.NORMAL)
	pinyin_2 = pinyin(ch_str_2,style=Style.NORMAL)
	return ch_similarity_sub(pinyin_1,pinyin_2)

def SSM(ch_str_1,ch_str_2):
	shengmu_1 = pinyin(ch_str_1,style=Style.INITIALS)
	shengmu_2 = pinyin(ch_str_2,style=Style.INITIALS)
	return ch_similarity_sub(shengmu_1,shengmu_2)

def SYM(ch_str_1,ch_str_2):
	yunmu_1 = pinyin(ch_str_1,style=Style.FINALS)
	yunmu_2 = pinyin(ch_str_2,style=Style.FINALS)
	return ch_similarity_sub(yunmu_1,yunmu_2)

def STM(ch_str_1,ch_str_2):
	shengdiao_1 = get_shengdiao(pinyin(ch_str_1,style=Style.TONE3))
	shengdiao_2 = get_shengdiao(pinyin(ch_str_2,style=Style.TONE3))
	return ch_similarity_sub(shengdiao_1,shengdiao_2)

def ch_similarity(ch_str_1,ch_str_2):
	sch = SCH(ch_str_1,ch_str_2)
	spy = SPY(ch_str_1,ch_str_2)
	ssm = SSM(ch_str_1,ch_str_2)
	sym = SYM(ch_str_1,ch_str_2)
	stm = STM(ch_str_1,ch_str_2)
	lev = Lev.distance(ch_str_1,ch_str_2)
	return sch + 0.8*spy + 0.5*ssm + 0.5*sym + 0.3*stm + 1.0 / (lev+1)
	# return sch + 1.0 / (lev+1)

# def gen_dict(lis):
# 	dic = {}
# 	for i in range(len(lis)):
# 		x = lis[i][0][0]
# 		if not x=='':
# 			if x in dic.keys():
# 				dic[x] += trans[str(i)]
# 			else:
# 				dic[x] = []
# 				dic[x] += trans[str(i)]
# 	return dic

# 零一二三四五六七八九
# [['ling'], ['yi'], ['er'], ['san'], ['si'], ['wu'], ['liu'], ['qi'], ['ba'], ['jiu']]

# shengmu_list = [['l'], [''], [''], ['s'], ['s'], [''], ['l'], ['q'], ['b'], ['j']]
# yunmu_list = [['ing'], ['i'], ['er'], ['an'], ['i'], ['u'], ['iou'], ['i'], ['a'], ['iou']]
# shengdiao_list = ['2', '1', '4', '1', '4', '3', '4', '1', '1', '3']

# shengmu_dict = gen_dict(shengmu_list)
# yunmu_dict = gen_dict(yunmu_list)
# shengdiao_dict = gen_dict(shengdiao_list)

# print(shengmu_dict)
# print(yunmu_dict)
# print(shengdiao_dict)

# shengmu
# {
# 	'l': ['零', '六'], 's': ['三', '四'], 'q': ['七'], 
# 	'b': ['八'], 'j': ['九']
# }
# yunmu
# {
# 	'ing': ['零'], 'i': ['一', '四', '七'], 'er': ['二'], 
# 	'an': ['三'], 'u': ['五'], 'iou': ['六', '九'], 'a': ['八']
# }
# shengdiao
# {
# 	'2': ['零'], '1': ['一', '三', '七', '八'],'4': ['二', '四', '六'], 
# 	'3': ['五', '九']
# }

pinyin_list = [['ling'], ['yi'], ['er'], ['san'], ['si'], ['wu'], ['liu'], ['qi'], ['ba'], ['jiu']]
def parse_pinyin(ind,piny):
	c = piny[ind][0]
	for i in range(len(pinyin_list)):
		if c==pinyin_list[i][0]:
			return trans[str(i)]
	return None

def parse_left(i,piny,shengmu,yunmu):
	if shengmu[i][0]=='q':
		return trans['7']
	elif shengmu[i][0]=='b':
		return trans['8']
	elif shengmu[i][0]=='j':
		return trans['9']
	elif piny[i][0][0]=='w': #ling shengmu
		return trans['5']
	# elif piny[i][0][0]=='y': #ling shengmu
	# 	return trans['1']
	elif yunmu[i][0]=='ing':
		return trans['0']
	# elif yunmu[i][0]=='an':
	# 	return trans['3']
	# elif yunmu[i][0]=='u':
	# 	return trans['5']
	elif yunmu[i][0]=='er':
		return trans['2']
	elif yunmu[i][0]=='a':
		return trans['8']
	elif piny[i][0]=='ao':
		return trans['2']
	# elif piny[i][0]=='lei':
	# 	return trans['0']
	# elif piny[i][0]=='nei':
	# 	return trans['6']
	return None


def parse_others(i,shengmu,yunmu,shengdiao):
	if shengdiao[i][0]=='2':
		if yunmu[i][0]=='ing':
			return trans['0']
	elif shengdiao[i][0]=='1':
		if yunmu[i][0]=='an':
			return trans['3']
		elif yunmu[i][0]=='a':
			return trans['8']
		elif shengmu[i][0]=='q':
			return trans['7']
		elif yunmu[i][0]=='i':
			return trans['1']
	elif shengdiao[i][0]=='3':
		if yunmu[i][0]=='u':
			return trans['5']
		elif shengmu[i][0]=='j':
			return trans['9']
	elif shengdiao[i][0]=='4':
		if yunmu[i][0]=='er':
			return trans['2']
		elif yunmu[i][0]=='i':
			return trans['4']
		elif yunmu[i][0]=='iou':
			return trans['6']
	return None

def transform(ch_str):
	ch_str_out = ''
	piny = pinyin(ch_str,style=Style.NORMAL)
	shengmu = pinyin(ch_str,style=Style.INITIALS)
	yunmu = pinyin(ch_str,style=Style.FINALS)
	shengdiao = get_shengdiao(pinyin(ch_str,style=Style.TONE3))
	for i in range(len(ch_str)):
		o = parse_pinyin(i,piny)
		if o==None:
			o = parse_others(i,shengmu,yunmu,shengdiao)
		if o==None:
			o = parse_left(i,piny,shengmu,yunmu)
		if not (o==None):
			ch_str_out += o
	return ch_str_out


def check_valid(chi_word,str_ch):
	for c in chi_word:
		if not (c in str_ch):
			return False
	return True

def predict(chi_word1):
	max_similarity = -1
	res = {}
	for x in range(10000):
		str_x = str(x)
		for i in range(4-len(str_x)):
		    str_x = '0' + str_x
		# str_ch = translate("2016")
		str_ch = ""
		for c in str_x:
		    str_ch += trans[c]
		# assert(len(str_ch)==8)
		assert(len(str_ch)==4)
		if check_valid(chi_word1,str_ch):
			similarity = ch_similarity(chi_word1,str_ch)
			if similarity > max_similarity:
			    max_similarity = similarity
			if similarity in res.keys():
			    res[similarity].append(str_ch)
			else:
			    res[similarity] = []
			    res[similarity].append(str_ch)
	if max_similarity==-1:
		return chi_word1
	return res[max_similarity]

all_cnt = 0
cor_cnt = 0
with open("data_1.txt","r") as fr:
	for line in fr:
		ch_str_2 = line[10:18]
		ch_str_1 = line[29:]
		ch_str_1 = ch_str_1.replace("\n","")
		if ch_str_2[:4]==translate("2016"):
			key_ind = ch_str_1.find('六')
			if not (key_ind==-1):
				str_trans = transform(ch_str_1[key_ind+1:])
				print("output: %s transform: %s" % (ch_str_1,str_trans))
				pred = predict(str_trans)
				res = (ch_str_2[4:] in pred)
				all_cnt += 1
				cor_cnt += res
				print("original: %s predict: %s result: %d" % (ch_str_2,pred,res))
				print("")
print("rate: %f" % (float(cor_cnt)/float(all_cnt)))
