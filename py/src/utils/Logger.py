import sys
from pathlib import Path
import logging

class Logger:
    """
    线程安全的Agent日志记录模块
    """
    _logger = None
    _initialized = False

    @classmethod
    def setup(cls, level=logging.INFO, log_file=None, log_dir="./logs"):
        """
        Logger模块初始化配置，在程序入口调用一次
        """
        if cls._initialized:    # 已经初始化则跳过
            return

        cls._logger = logging.getLogger('agentLogger')
        cls._logger.setLevel(level)

        # 清空可能存在的默认 handler
        cls._logger.handlers.clear()

        # 控制台 handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # 文件 handler
        handlers = [console_handler]
        if log_file:
            Path(log_dir).mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(
                Path(log_dir) / log_file,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            handlers.append(file_handler)

        # 统一格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        for handler in handlers:
            handler.setFormatter(formatter)
            cls._logger.addHandler(handler)

        cls._initialized = True

    @classmethod
    def get_instance(cls):
        """
        获取内部logger实例
        """
        if cls._logger is None:
            cls.setup()  # 自动初始化
        return cls._logger

    # 代理所有日志方法为类方法
    @classmethod
    def debug(cls, msg, *args, **kwargs):
        cls.get_instance().debug(msg, *args, **kwargs)

    @classmethod
    def info(cls, msg, *args, **kwargs):
        cls.get_instance().info(msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        cls.get_instance().warning(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        cls.get_instance().error(msg, *args, **kwargs)

    @classmethod
    def critical(cls, msg, *args, **kwargs):
        cls.get_instance().critical(msg, *args, **kwargs)

    @classmethod
    def exception(cls, msg, *args, **kwargs):
        cls.get_instance().exception(msg, *args, **kwargs)

    @classmethod
    def log(cls, level, msg, *args, **kwargs):
        cls.get_instance().log(level, msg, *args, **kwargs)