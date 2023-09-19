import datetime


def get_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sum_x_y(x, y):
    return x + y