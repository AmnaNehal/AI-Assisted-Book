import time
from typing import Dict, Optional
from collections import defaultdict
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple rate limiter to respect free-tier API limits
    """
    
    def __init__(self):
        self.requests = defaultdict(list)  # Store request timestamps by key
        self.limit = settings.MAX_CONCURRENT_REQUESTS
        self.window = 60  # Time window in seconds (1 minute)
    
    def is_allowed(self, key: str = "default") -> bool:
        """
        Check if a request is allowed based on rate limits
        """
        now = time.time()
        # Remove requests older than the time window
        self.requests[key] = [req_time for req_time in self.requests[key] if now - req_time < self.window]
        
        # Check if we're under the limit
        if len(self.requests[key]) < self.limit:
            self.requests[key].append(now)
            return True
        
        logger.warning(f"Rate limit exceeded for key: {key}")
        return False
    
    def get_wait_time(self, key: str = "default") -> float:
        """
        Get the time to wait before the next request is allowed
        """
        if self.is_allowed(key):
            return 0.0
        
        # Calculate when the oldest request will expire
        oldest_request = min(self.requests[key])
        wait_time = self.window - (time.time() - oldest_request)
        return max(0.0, wait_time)


# Global rate limiter instance
rate_limiter = RateLimiter()


def check_rate_limit(identifier: str) -> bool:
    """
    Check if a request from a specific identifier is allowed
    """
    return rate_limiter.is_allowed(identifier)


def get_rate_limit_wait_time(identifier: str) -> float:
    """
    Get the wait time before a request from a specific identifier is allowed
    """
    return rate_limiter.get_wait_time(identifier)