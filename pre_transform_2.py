from pypinyin import pinyin, Style
import pypinyin
import math
import Levenshtein as Lev
import ssc
import editdistance
from ssc_similarity.compute_ssc_similarity import computeSSCSimilaruty
import sys


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

WL = 2

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
	# return 1.0 / (lev+1)


# SIMILARITY_THRESHOLD = 0.5
SIMILARITY_THRESHOLD = 0.3
SSC_ENCODE_WAY = 'SOUND'#'ALL','SOUND','SHAPE'

ssc.getHanziStrokesDict()
ssc.getHanziStructureDict()
ssc.getHanziSSCDict()

def transform(ch_str):
	ch_str_out = ''
	for i in range(len(ch_str)):
		chi_word1_ssc = ssc.getSSC(ch_str[i], SSC_ENCODE_WAY)
		ind = -1
		max_sim = -1
		res = {}
		for x in range(10):
			str_ch = trans[str(x)]
			chi_word2_ssc = ssc.getSSC(str_ch, SSC_ENCODE_WAY)
			sim = computeSSCSimilaruty(chi_word1_ssc[0],chi_word2_ssc[0],SSC_ENCODE_WAY)
			if sim>max_sim:
			    ind = x
			    max_sim = sim
			if sim in res.keys():
			    res[sim].append(x)
			else:
			    res[sim] = []
			    res[sim].append(x)
		if max_sim>SIMILARITY_THRESHOLD:
		    ch_str_out += trans[str(ind)]
	return ch_str_out


def check_valid(chi_word,str_ch):
	for c in chi_word:
		if not (c in str_ch):
			return False
	return True

aviliable_predict_list = [
	'2315',
	'4742',
	'4752',
	'4754',
	'4758',
	'4760',
	'4762',
	'4764',
	'4766',
	'4768',
	'4777',
	'4781',
	'4786',
	'4788',
	'4792',
	'4793',
	'4794',
	'4806',
	'4808',
	'4810',
	'4818',
	'4821',
	'4823',
	'4825',
	'4832',
	'4838',
	'4843',
	'4845',
	'4849',
	'4857',
	'4863'
]


def predict(chi_word1):
	# if len(chi_word1)>4:
	# 	chi_word1 = chi_word1[:4]
	# max_similarity = -1
	# res = {}
	# for x in range(10000):
	# 	str_x = str(x)
	# 	for i in range(4-len(str_x)):
	# 	    str_x = '0' + str_x
	# 	str_ch = ""
	# 	for c in str_x:
	# 	    str_ch += trans[c]
	# 	assert(len(str_ch)==4)
	# 	if check_valid(chi_word1,str_ch):
	# 		similarity = ch_similarity(chi_word1,str_ch)
	# 		if similarity > max_similarity:
	# 		    max_similarity = similarity
	# 		if similarity in res.keys():
	# 		    res[similarity].append(str_ch)
	# 		else:
	# 		    res[similarity] = []
	# 		    res[similarity].append(str_ch)
	# if max_similarity==-1:
	# 	return [chi_word1]
	# return res[max_similarity]
	if len(chi_word1)>4:
		chi_word1 = chi_word1[:4]
	max_similarity = -1
	res = {}
	print(chi_word1)
	for str_ch in aviliable_predict_list:
		str_ch = translate(str_ch)
		assert(len(str_ch)==4)
		similarity = ch_similarity(chi_word1,str_ch)
		if similarity > max_similarity:
		    max_similarity = similarity
		if similarity in res.keys():
		    res[similarity].append(str_ch)
		else:
		    res[similarity] = []
		    res[similarity].append(str_ch)
	return res[max_similarity]





trans_rev = {}
trans_rev['零'] = '0'
trans_rev['一'] = '1'
trans_rev['二'] = '2'
trans_rev['三'] = '3'
trans_rev['四'] = '4'
trans_rev['五'] = '5'
trans_rev['六'] = '6'
trans_rev['七'] = '7'
trans_rev['八'] = '8'
trans_rev['九'] = '9'

def trans_to_number(ch_str):
	ch_str_out = ""
	for c in ch_str:
		ch_str_out += trans_rev[c]
	return ch_str_out

def predict2(ch_str):
	print(ch_str)
	str_trans = transform(ch_str)
	print(str_trans)
	key_ind = str_trans.find('六')
	assert(key_ind!=-1)
	print(str_trans[key_ind+1:])
	pred = predict(str_trans[key_ind+1:])
	return trans_to_number(translate("2016") + pred[0])

if __name__=="__main__":
	all_cnt = 0
	cor_cnt = 0
	with open("data.txt","r") as fr:
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
				
				# str_trans = transform(ch_str_1)
				# print("output: %s transform: %s" % (ch_str_1,str_trans))
				# key_ind = str_trans.find('六')
				# if not (key_ind==-1):
				# 	pred = predict(str_trans[key_ind+1:])
				# 	res = (ch_str_2[4:] in pred)
				# 	all_cnt += 1
				# 	cor_cnt += res
				# 	print("original: %s predict: %s result: %d" % (ch_str_2,pred,res))
				# 	print("")
	print("rate: %f" % (float(cor_cnt)/float(all_cnt)))
