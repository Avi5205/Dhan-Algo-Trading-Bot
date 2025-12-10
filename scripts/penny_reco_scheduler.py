import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Penny Recommendation Scheduler started")
    logger.info("This is a placeholder service")
    
    while True:
        time.sleep(60)
