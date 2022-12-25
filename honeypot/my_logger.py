import logging 
import time 
logger = logging.getLogger("L4wisdom") 
logger.setLevel(logging.INFO)
fh = logging.FileHandler("live1.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh) 