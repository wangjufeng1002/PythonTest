import re
import io
import sys, getopt
#import pandas as pd
#import  logdb

input = None
out = None
opts, args = getopt.getopt(sys.argv[1:], "i:o:")
for opt, arg in opts:
    if opt == "-i":
        input = arg
    if opt == "-o":
        out = arg

f = io.open(input)
w = io.open(out, "w", encoding='utf-8')

lines = f.readlines()
results = []
for line in lines:
    try:
        result = [None, None, None, None, None]
        replace = re.match(".*?(rest\\?.*&).*", line, re.S).group(1).split("&")
        for k in replace:
            if "v=" in k:
                v = k.replace("rest?", "").replace("v","")
                result[2] = v
            if "app_key=" in k:
                result[1] = k.replace("rest?", "").replace("app_key=","")
            if "method=" in k and "sign_method" not in k:
                result[0] = k.replace("rest?", "").replace("method=","")
            if "session=" in k:
                result[3] = k.replace("rest?", "").replace("session=","")
        split = line.split(" ")
        result[4] = split[len(split) - 1].replace("\n", "")
        results.append(",".join(result))
        w.write(",".join(result)+"\n")
        w.flush()
    except Exception as e:
        print(e)
# df_etllog = pd.DataFrame({'message':results})
# df_etllog1 = df_etllog['message'].str.split(',',expand = True)
# df_etllog1.columns=['method','app_key','v','session','dev']
# df_etllog2 = df_etllog1.join(df_etllog)
# df_etllog2.to_excel("C:\\Users\\wangjufeng\\Desktop\\test.xlsx")
# df_etllog2.head()

