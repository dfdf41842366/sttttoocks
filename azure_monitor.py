from loguru import logger

def emit_event(event_type, message, details=None):
    logger.info(f"[AZURE-MONITOR] {event_type}: {message} | {details or ''}")
