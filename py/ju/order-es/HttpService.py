import getopt
import sys
import EsConfig
import db
from flask import Flask, request
import  os
app = Flask(__name__)
#nohup python  HttpService.py -a prod   >> logs/nohup-httpservice.log 2>&1 &
@app.route("/syncOrder", methods=["GET"])
def syncOrder():
    cmd = "nohup python  -u HistoryDataSync.py -a prod -s %d -e %d  >nohup.log 2>&1 &"
    arg = request.args.get("orderId")
    if arg is None:
        return "orderId is not null"
    ids = db.getIdByOrderId(arg)
    os.system(cmd%(int(ids[0]["id"]),int(ids[0]["id"])))
    return "success"



if __name__ == '__main__':
    active = "test"
    opts, args = getopt.getopt(sys.argv[1:], "a:")
    for opt, arg in opts:
        if opt == "-a":
            active = arg
    # 初始化es db
    EsConfig.initEs(active)
    db.initDb(active)
    app.run(debug=True, port=10001, host="0.0.0.0")

