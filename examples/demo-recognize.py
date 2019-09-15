import _init_path
from models.conv import GatedConv
import pre_transform_2 as pt2
import enhance_speach as es
# import beamdecode

model = GatedConv.load("pretrained/gated-conv.pth")
# model = GatedConv.load("pretrained/model_110.pth")


# with open("train_index","w") as f:
# 	for filename in os.listdir('data/'):
# 		# print(filename)
# 		s1 = filename[:8]
# 		s2 = ""
# 		for x in s1:
# 			s2 += trans[x]
# 		s1 = "data/" + s1 +".wav"
# 		f.write(s1+","+s2+"\n")

# text = model.predict("test.wav")
# text = model.predict("12345_man.wav")
# text = model.predict("678910_man.wav")
# text = model.predict("862409_in.wav")
# text = model.predict("20164239_kuai.wav")
# text = model.predict("20164762_kuai.wav")
# text = model.predict("20164762_man.wav")
# text = model.predict("data/20166565.wav")
# text = model.predict("20164786.wav")
input_file_src = "record.wav"
# output_file_src = "record_out.wav"
# es.denoise(input_file_src,output_file_src)
# text = model.predict(output_file_src)
text = model.predict(input_file_src)
text = pt2.predict2(text)

# text = beamdecode.predict(output_file_src)
print("")
print("识别结果:")
print(text)

