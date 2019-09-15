from pypinyin import pinyin, Style
import pypinyin
import math

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

WL = 4

def I(ch1,ch2):
	return (ch1==ch2)

def F(d):
	return 1.0 / (d+1)

# def F(d):
# 	return 1.0 / math.sqrt(d+1)

# def F(d):
# 	return 1.0 / pow(2,d+1)

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

def get_shengdiao(pinyin_str):
	res = []
	for x in pinyin_str:
		s = x[0]
		res.append(s[-1])
	return res

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

def SLT(ch_str_1,ch_str_2):
	l1 = float(len(ch_str_1))
	l2 = float(len(ch_str_2))
	return -1*2.0/math.pi*math.atan(abs(math.log(l2/l1)))

def ch_similarity(ch_str_1,ch_str_2):
	sch = SCH(ch_str_1,ch_str_2)
	spy = SPY(ch_str_1,ch_str_2)
	ssm = SSM(ch_str_1,ch_str_2)
	sym = SYM(ch_str_1,ch_str_2)
	stm = STM(ch_str_1,ch_str_2)
	slt = SLT(ch_str_1,ch_str_2)
	# return 1.0*sch + 0.8*spy + 0.5*ssm + 0.5*sym + 0.3*stm + 1.0*slt
	return 0.3*spy + ssm + 0.8*sym + stm
	# return max(ssm,max(sym,stm))


# ch_str_1 = translate("20164462")
# print(ch_str_1)
# ch_str_2 = translate("20164762")
# print(ch_str_2)
# print(ch_similarity(ch_str_1,ch_str_2))


chi_word1 = '二零一六二四六华'
# chi_word1 = '二零一一六三九八五五'
# chi_word1 = '二女一六七五一其'

max_similarity = -1
res = {}

key_ind = chi_word1.find('六')
if key_ind==-1:
	print("failed")
	exit(0)
chi_word1 = chi_word1[key_ind+1:]
print(chi_word1)
for x in range(10000):
    str_x = str(x)
    for i in range(4-len(str_x)):
        str_x = '0' + str_x
    str_ch = ""
    for c in str_x:
        str_ch += trans[c]
    assert(len(str_ch)==4)
    similarity = ch_similarity(chi_word1,str_ch)
    if similarity > max_similarity:
        max_similarity = similarity
    if similarity in res.keys():
        res[similarity].append(str_ch)
    else:
        res[similarity] = []
        res[similarity].append(str_ch)

print(res[max_similarity])
print(len(res[max_similarity]))


# ans = [
# 	"SCH",
# 	"SPY",
# 	"SSM",
# 	"SYM",
# 	"STM",
# 	"SLT"
# ]

# cnt = [0,0,0,0,0,0]

# with open("data_1.txt","r") as fr:
# 	for line in fr:
# 		ch_str_2 = line[10:18]
# 		ch_str_1 = line[29:]
# 		res = []
# 		res.append(SCH(ch_str_1,ch_str_2))
# 		res.append(SPY(ch_str_1,ch_str_2))
# 		res.append(SSM(ch_str_1,ch_str_2))
# 		res.append(SYM(ch_str_1,ch_str_2))
# 		res.append(STM(ch_str_1,ch_str_2))
# 		res.append(SLT(ch_str_1,ch_str_2))
# 		ind = res.index(max(res))
# 		cnt[ind] = cnt[ind] + 1

# for i in range(6):
# 	print(ans[i]+":")
# 	print(cnt[i])
