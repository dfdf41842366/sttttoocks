import logging
from pathlib import Path

def setup_logger(module_name, log_dir=None):
    log_dir = log_dir or (Path(__file__).parent)
    log_dir = Path(log_dir)
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"{module_name}.log"
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file, mode="a")
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    return logger
