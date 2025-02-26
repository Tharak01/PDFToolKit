"""
Logging utilities for the PDFToolkit package.
"""

import logging
from typing import Optional, Union
from discrd_logger import DiscordLogger

def setup_logger(name: str = "PDFToolkit", 
                level: str = "INFO", 
                discord_webhook: Optional[str] = None) -> Union[logging.Logger, DiscordLogger]:
    """
    Set up and return a logger instance.
    
    Args:
        name: Logger name
        level: Logging level
        discord_webhook: Optional Discord webhook URL
        
    Returns:
        Logger instance (either standard Logger or DiscordLogger)
    """
    if discord_webhook:
        return DiscordLogger(
            webhook_url=discord_webhook, 
            app_name=name, 
            min_level=level
        )
    
    logger = logging.getLogger(name)
    level_num = getattr(logging, level, logging.INFO)
    logger.setLevel(level_num)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger