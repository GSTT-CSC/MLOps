import logging.config

LOG_FILE = "mlops_log_file.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("mlops_log_file.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.propagate = True

from . import Experiment
from . import ProjectFile
