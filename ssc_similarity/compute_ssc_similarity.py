#coding=utf-8

strokesDictReverse = {'1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'A':10,
               'B':11, 'C':12, 'D':13, 'E':14, 'F':15, 'G':16, 'H':17, 'I':18, 'J':19, 'K':20,
               'L':21, 'M':22, 'N':23, 'O':24, 'P':25, 'Q':26, 'R':27, 'S':28, 'T':29, 'U':30,
               'V':31, 'W':32, 'X':33, 'Y':34, 'Z':35, '0':0}

# shengmuDict = {'b':'1', 'p':'2', 'm':'3', 'f':'4', 
#              'd':'5', 't':'6', 'n':'7', 'l':'7', 
#              'g':'8', 'k':'9', 'h':'A', 'j':'B',
#              'q':'C', 'x':'D', 'zh':'E', 'ch':'F',
#              'sh':'G', 'r':'H', 'z':'E', 'c':'F', 
#              's':'G', 'y':'I', 'w':'J', '0':'0'}

shengmu_weak_pattern = ['1234','567','89A','BCD','EFGH']
def shengmu_weak_match(c1,c2):
    for p in shengmu_weak_pattern:
        if (c1 in p) and (c2 in p):
            return True
    return False

# yunmuDict = {'a':'1', 'o':'2', 'e':'3', 'i':'4', 
#              'u':'5', 'v':'6', 'ai':'7', 'ei':'7', 
#              'ui':'8', 'ao':'9', 'ou':'A', 'iou':'B',#有：you->yiou->iou->iu
#              'ie':'C', 've':'D', 'er':'E', 'an':'F', 
#              'en':'G', 'in':'H', 'un':'I', 'vn':'J',#晕：yun->yvn->vn->ven
#              'ang':'F', 'eng':'G', 'ing':'H', 'ong':'K'}

yunmu_weak_pattern = ['34','E9']
def yunmu_weak_match(c1,c2):
    for p in yunmu_weak_pattern:
        if (c1 in p) and (c2 in p):
            return True
    return False

soundWeight=0.9
shapeWeight=0.1
def computeSoundCodeSimilarity(soundCode1, soundCode2):#soundCode=['2', '8', '5', '2']
    featureSize=len(soundCode1)
    # wights=[0.4,0.4,0.1,0.1]
    wights=[0.4,0.4,0.0,0.2]
    multiplier=[]
    for i in range(featureSize):
        if soundCode1[i]==soundCode2[i]:
            multiplier.append(1)
        elif (i==1) and shengmu_weak_match(soundCode1[i],soundCode2[i]):
            multiplier.append(0.5)
        elif (i==0) and yunmu_weak_match(soundCode1[i],soundCode2[i]):
            multiplier.append(0.25)
        else:
            multiplier.append(0)
    soundSimilarity=0
    for i in range(featureSize):
        soundSimilarity += wights[i]*multiplier[i]
    return soundSimilarity
    
def computeShapeCodeSimilarity(shapeCode1, shapeCode2):#shapeCode=['5', '6', '0', '1', '0', '3', '8']
    featureSize=len(shapeCode1)
    wights=[0.25,0.1,0.1,0.1,0.1,0.1,0.25]
    multiplier=[]
    for i in range(featureSize-1):
        if shapeCode1[i]==shapeCode2[i]:
            multiplier.append(1)
        else:
            multiplier.append(0)
    multiplier.append(1- abs(strokesDictReverse[shapeCode1[-1]]-strokesDictReverse[shapeCode2[-1]])*1.0 / max(strokesDictReverse[shapeCode1[-1]],strokesDictReverse[shapeCode2[-1]]) )
    shapeSimilarity=0
    for i in range(featureSize):
        shapeSimilarity += wights[i]*multiplier[i]
    return shapeSimilarity

def computeSSCSimilaruty(ssc1, ssc2, ssc_encode_way):
    #return 0.5*computeSoundCodeSimilarity(ssc1[:4], ssc2[:4])+0.5*computeShapeCodeSimilarity(ssc1[4:], ssc2[4:])
    if ssc_encode_way=="SOUND":
        return computeSoundCodeSimilarity(ssc1, ssc2)
    elif ssc_encode_way=="SHAPE":
        return computeShapeCodeSimilarity(ssc1, ssc2)
    else:
        soundSimi=computeSoundCodeSimilarity(ssc1[:4], ssc2[:4])
        shapeSimi=computeShapeCodeSimilarity(ssc1[4:], ssc2[4:])
        return soundWeight*soundSimi+shapeWeight*shapeSimi
