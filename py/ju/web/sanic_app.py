from sanic import Sanic, json
from functions import get_datetime, sum_x_y

app = Sanic("CodeToAPI")
HOST = "localhost"
PORT = 8000


@app.route("/getdatetime")
async def getdatetime(request):
    return json({"now": get_datetime()})


@app.get('/sumxy')
async def sumxy(request):
    parameters = request.args
    result = sum_x_y(int(parameters['x'][0]), int(parameters['y'][0]))
    return json({'result': result})


@app.post('/sumxy')
async def sumxy(request):
    parameters = request.json
    print(parameters)
    result = sum_x_y(int(parameters['x']), int(parameters['y']))
    return json({'result': result})



if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=False)
