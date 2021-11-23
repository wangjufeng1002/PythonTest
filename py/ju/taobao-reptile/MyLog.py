import datetime
import logging
import os


class Logger:
    def __init__(self, loggername):
        #目录
        log_path = '/dev/reptile/logs/'
        # 创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)

        time = datetime.datetime.now().strftime("%Y-%m-%d")

        exists = os.path.exists(log_path)
        if exists is False:
            os.makedirs(log_path)
        # 创建一个handler，用于写入日志文件
        #log_path = r'D:\\logs\\cmt\\file\\'  # 指定文件输出路径，注意logs是个文件夹，一定要加上/，不然会导致输出路径错误，把logs变成文件名的一部分了
        logname = log_path + time + '.log'  # 指定输出的日志文件名
        fh = logging.FileHandler(logname, encoding='utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        fh.setLevel(logging.DEBUG)

        # 创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger
