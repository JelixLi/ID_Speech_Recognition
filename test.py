import ssc
import editdistance
from ssc_similarity.compute_ssc_similarity import computeSSCSimilaruty
import sys

SIMILARITY_THRESHOLD = 0.0
SSC_ENCODE_WAY = 'SOUND'#'ALL','SOUND','SHAPE'

ssc.getHanziStrokesDict()
ssc.getHanziStructureDict()
ssc.getHanziSSCDict()

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


def transform(ch_str):
    ch_str_out = ''
    for i in range(len(ch_str)):
        chi_word1_ssc = ssc.getSSC(ch_str[i], SSC_ENCODE_WAY)
        ind = -1
        max_sim = -1
        for x in range(10):
            str_ch = trans[str(x)]
            chi_word2_ssc = ssc.getSSC(str_ch, SSC_ENCODE_WAY)
            sim = computeSSCSimilaruty(chi_word1_ssc[0],chi_word2_ssc[0],SSC_ENCODE_WAY)
            if sim>max_sim:
                ind = x
                max_sim = sim
        if max_sim>SIMILARITY_THRESHOLD:
            ch_str_out += trans[str(ind)]
    return ch_str_out

print(transform('有'))
