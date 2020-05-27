import sys
from datetime import datetime
from pathlib import Path
LOG_PATH = Path('./logs/')
LOG_PATH.mkdir(exist_ok=True)

import logging
run_start_time = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
#FIXME: make a task name "Matching entities" dynamic
logfile = str(LOG_PATH/'log-{}-{}.txt'.format(run_start_time, "Matching entities"))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    handlers=[
        logging.FileHandler(logfile),
        logging.StreamHandler(sys.stdout)
    ])

logger = logging.getLogger()
log=logger.info


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

