import logging,time
from Common import ReadConfig

class FrameLog():
    def __init__(self,logger=None):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        self.log_time = time.strftime("%Y-%m-%d")
        self.log_path = ReadConfig.log_path
        self.log_name = self.log_path + self.log_time + '.log'
        # print(self.log_name)
        # logging.basicConfig(level=logging.INFO,
        #                 format="%(asctime)s - %(levelname)s - %(message)s",
        #                 filename=self.log_name,
        #                 filemode='a')
        console = logging.FileHandler(self.log_name,'a',encoding='utf-8')
        # fh = logging.FileHandler(self.log_name,'a',encoding='utf-8')
        console.setLevel(logging.INFO)

        ##定义handler的输出格式
        formatter = logging.Formatter('[%(asctime)s] %(filename)s ->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        # self.logger.removeHandler(console)
        console.close()

    def log(self):
        return self.logger

if __name__ == '__main__':
    lo = FrameLog()
    log = lo.log()
    log.error("error")
    log.debug("Debug")
    log.info("info")
    log.critical("严重")

