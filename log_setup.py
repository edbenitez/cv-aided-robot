import logging

logFormatter = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(format=logFormatter, level=logging.DEBUG)

logger = logging.getLogger('top')

