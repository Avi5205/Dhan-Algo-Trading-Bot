import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Dhan Swing Bot main service started")
    logger.info("This container provides base environment for other services")
    
    import time
    while True:
        time.sleep(60)
