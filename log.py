
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# Creating a RotatingFileHandler handler
log_file = 'log/app.log'
max_bytes = 2000000  # Maximum size of each log file
backup_count = 100  # Number of retained old log files
file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)

# Set the log level of the handler
file_handler.setLevel(logging.INFO)
# Creating a Logger
logger = logging.getLogger()
logger.addHandler(file_handler)