"""
Utility decorators for the HIT137 Assignment 3 project.

This module provides reusable decorators for logging, caching, and retry logic.
Demonstrates the use of multiple decorators as per assignment requirements.
"""

import time
import functools
from typing import Callable, Any, Dict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def api_call_logger(func: Callable) -> Callable:
    """
    Decorator that logs API calls with timing information.
    
    Logs:
        - Function name and arguments
        - Execution time
        - Success or failure status
    
    Example:
        @api_call_logger
        def fetch_data(model_id):
            return api.get(model_id)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.info(f"🔵 Starting API call: {func_name}")
        logger.debug(f"   Args: {args}, Kwargs: {kwargs}")
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"✅ API call {func_name} completed in {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"❌ API call {func_name} failed after {elapsed:.2f}s: {str(e)}")
            raise
    
    return wrapper


def simple_cache(max_size: int = 128) -> Callable:
    """
    Simple LRU-style cache decorator for function results.
    
    Args:
        max_size: Maximum number of cached results (default: 128)
    
    Example:
        @simple_cache(max_size=50)
        def expensive_computation(x, y):
            return x ** y
    
    Note:
        Only works with hashable arguments (strings, numbers, tuples).
    """
    def decorator(func: Callable) -> Callable:
        cache: Dict[tuple, Any] = {}
        cache_order = []
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from args and kwargs
            cache_key = (args, tuple(sorted(kwargs.items())))
            
            # Check if result is cached
            if cache_key in cache:
                logger.debug(f"💾 Cache hit for {func.__name__}")
                return cache[cache_key]
            
            # Compute result
            logger.debug(f"🔄 Cache miss for {func.__name__}, computing...")
            result = func(*args, **kwargs)
            
            # Store in cache with LRU eviction
            cache[cache_key] = result
            cache_order.append(cache_key)
            
            # Evict oldest if cache is full
            if len(cache) > max_size:
                oldest_key = cache_order.pop(0)
                del cache[oldest_key]
                logger.debug(f"🗑️ Evicted oldest cache entry for {func.__name__}")
            
            return result
        
        # Add cache management methods
        wrapper.cache_clear = lambda: cache.clear() or cache_order.clear()
        wrapper.cache_info = lambda: {
            'size': len(cache),
            'max_size': max_size,
            'hits': len([k for k in cache_order if k in cache])
        }
        
        return wrapper
    
    return decorator


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0) -> Callable:
    """
    Retry decorator with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1.0)
        backoff: Multiplier for delay after each retry (default: 2.0)
    
    Example:
        @retry(max_attempts=5, delay=2.0)
        def unstable_api_call():
            return requests.get("https://api.example.com")
    
    Returns:
        The successful result or raises the last exception encountered.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.debug(f"🔄 Attempt {attempt}/{max_attempts} for {func.__name__}")
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"⚠️ Attempt {attempt} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {current_delay:.1f}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"❌ All {max_attempts} attempts failed for {func.__name__}"
                        )
            
            # Raise the last exception after all retries exhausted
            raise last_exception
        
        return wrapper
    
    return decorator


def timing_decorator(func: Callable) -> Callable:
    """
    Simple timing decorator to measure function execution time.
    
    Example:
        @timing_decorator
        def slow_function():
            time.sleep(2)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"⏱️ {func.__name__} took {elapsed:.4f}s")
        return result
    
    return wrapper


# Example usage demonstrating multiple decorators
@api_call_logger
@retry(max_attempts=3, delay=0.5)
@simple_cache(max_size=100)
def example_api_function(model_id: str, input_text: str) -> dict:
    """
    Example function showing how to stack multiple decorators.
    
    Decorators are applied bottom-up:
    1. simple_cache - caches results
    2. retry - retries on failure
    3. api_call_logger - logs all calls
    """
    # Simulated API call
    return {
        "model": model_id,
        "input": input_text,
        "output": f"Processed: {input_text}"
    }