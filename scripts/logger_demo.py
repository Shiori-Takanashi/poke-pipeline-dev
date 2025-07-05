# loggers.py
import logging
from logging import StreamHandler, FileHandler, Formatter
from pathlib import Path
from config.dirpath import LOGS_DIR_PATH


def setup_demo_logger(name: str, level=logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logger.handlers:
        return logger

    # ログディレクトリはinitで生成するので存在確認から入っておく
    if not LOGS_DIR_PATH.exists():
        LOGS_DIR_PATH.mkdir(exist_ok=True)

    # ログファイル名：呼び出し元ファイル名 or ロガー名ベース（__main__問題を避けるなら name でよい）
    logfile_name = name.replace(".", "_") + ".log"
    logfile_path = LOGS_DIR_PATH / logfile_name

    fmt = Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    sh = StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)

    fh = FileHandler(logfile_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger
