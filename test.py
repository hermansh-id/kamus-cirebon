from main import translate
import pandas as pd
import time
data = pd.read_csv('test.csv')

def trans(txt):
    start_time = time.time()
    translate_result, kosong = translate(txt, "cerbon")
    end_time = time.time()
    total_time = end_time - start_time
    return translate_result, total_time, kosong
res = []
kosong_list = []
for i, d in enumerate(data['text']):
    result, timetaken, kosong = trans(d)
    res.append({"text": d, "result": result, "time": timetaken})
    kosong_list.extend(kosong)

result = pd.DataFrame(res)
result.to_csv('result.csv')

kosong_list = pd.DataFrame(kosong_list)
kosong_list.to_csv('kosong.csv')

