import datetime
import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

class LoggerSingleton:
    _instance = None

    @staticmethod
    def get_instance(log_to_file=True, log_to_console=True):
        if LoggerSingleton._instance is None:
            LoggerSingleton(log_to_file, log_to_console)
        return LoggerSingleton._instance

    def __init__(self, log_to_file=True, log_to_console=True):
        if LoggerSingleton._instance is not None:
            raise RuntimeError("LoggerSingleton instance already exists.")
        LoggerSingleton._instance = self

        # 定义日志格式
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 获取 AppData\Local 目录路径
        self.appdata_local_path = os.path.join(os.getenv('LOCALAPPDATA'), 'llzgd', 'ETBSGT')

        # 创建所需目录
        os.makedirs(self.appdata_local_path, exist_ok=True)

        # 打印日志文件路径，以便确认
        print(f"Log directory: {self.appdata_local_path}")

        # 清理旧的日志文件
        self.clean_old_logs(self.appdata_local_path)

        # 生成包含时间戳的文件名
        current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.log_filename = f'{self.appdata_local_path}/ETBSGT [{current_time}].log'

        # 创建一个日志记录器
        self.logger = logging.getLogger('ETBSGT_logger')

        # 设置日志级别
        self.logger.setLevel(logging.DEBUG)

        try:
            if log_to_file:
                # 创建一个文件处理器，并设置每天轮换一次日志文件
                file_handler = TimedRotatingFileHandler(self.log_filename, when='midnight', interval=1, backupCount=7)
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(self.formatter)
                self.logger.addHandler(file_handler)
                print(f"File handler added: {self.log_filename}")
        except Exception as e:
            print(f"Failed to set up file handler: {e}")

        try:
            if log_to_console:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.DEBUG)
                console_handler.setFormatter(self.formatter)
                self.logger.addHandler(console_handler)
                print(f"Console handler added")
        except Exception as e:
            print(f"Failed to set up console handler: {e}")

    def clean_old_logs(self, log_dir, days=1):
        """
        删除指定目录下超过一定天数的日志文件。
        
        :param log_dir: 日志文件所在的目录
        :param days: 要删除的文件的天数
        """
        now = time.time()
        cutoff_time = now - (days * 24 * 60 * 60)  # 计算截止时间

        for filename in os.listdir(log_dir):
            filepath = os.path.join(log_dir, filename)
            if os.path.isfile(filepath):
                filemtime = os.path.getmtime(filepath)
                if filemtime < cutoff_time:
                    os.remove(filepath)
                    print(f"Deleted old log file: {filepath}")

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)