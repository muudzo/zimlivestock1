# AUTO-GENERATED FROM TypeScript
# SOURCE: src/lib/utils.ts
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

import re
import math
import time
import random
import string
from typing import List, Union, Optional, Any, Callable, Dict, TypeVar
from datetime import datetime, timedelta
import threading

# Placeholder for external libraries
# import { type ClassValue, clsx } from 'clsx'
# import { twMerge } from 'tailwind-merge'
# import { format, formatDistanceToNow, isAfter, isBefore } from 'date-fns'

# Helper implementations to match logic
def clsx(*inputs: Any) -> str:
    # Basic implementation of clsx for string joining
    # This is a placeholder for the actual library behavior
    classes = []
    for inp in inputs:
        if isinstance(inp, str) and inp:
            classes.append(inp)
        elif isinstance(inp, list):
            classes.append(clsx(*inp))
        # Handle dicts if needed
    return " ".join(classes)

def twMerge(class_string: str) -> str:
    # Placeholder for tailwind-merge
    return class_string

def date_fns_format(date: Union[datetime, str], format_str: str) -> str:
    # format(dateObj, formatStr)
    # TS formatStr: 'MMM dd, yyyy' -> Python '%b %d, %Y'
    # This mapping is incomplete but covers the example.
    dt = date if isinstance(date, datetime) else datetime.fromisoformat(date.replace('Z', '+00:00'))
    
    mapping = {
        'MMM': '%b',
        'dd': '%d',
        'yyyy': '%Y'
    }
    py_format = format_str
    for k, v in mapping.items():
        py_format = py_format.replace(k, v)
    return dt.strftime(py_format)

def date_fns_distance_to_now(date: datetime, add_suffix: bool = False) -> str:
    now = datetime.now()
    diff = now - date if now > date else date - now
    # Very basic approximation
    seconds = diff.total_seconds()
    if seconds < 60:
        return "less than a minute"
    minutes = int(seconds / 60)
    if minutes < 60:
        val = f"{minutes} minutes"
        return f"{val} ago" if add_suffix else val
    hours = int(minutes / 60)
    if hours < 24:
        val = f"{hours} hours"
        return f"{val} ago" if add_suffix else val
    days = int(hours / 24)
    val = f"{days} days"
    return f"{val} ago" if add_suffix else val

def is_before(date1: datetime, date2: datetime) -> bool:
    return date1 < date2

# --- Translated Functions ---

def cn(*inputs: Any):
    return twMerge(clsx(inputs))

def formatCurrency(amount: float, currency: str = 'USD') -> str:
    # return new Intl.NumberFormat(...).format(amount)
    # Python equivalent layout
    # minimumFractionDigits: 0, maximumFractionDigits: 0
    try:
        # Simple formatting respecting currency symbol (manual map)
        symbol = '$' if currency == 'USD' else currency
        return f"{symbol}{amount:,.0f}"
    except Exception:
        return str(amount)

def formatCurrencyCompact(amount: float, currency: str = 'USD') -> str:
    # notation: 'compact', maximumFractionDigits: 1
    # 1.2k, 1M etc.
    symbol = '$' if currency == 'USD' else currency
    
    n = float(amount)
    if n < 1000:
        return f"{symbol}{n:,.0f}" # usually compact keeps decimals? max 1
    
    suffixes = ['', 'K', 'M', 'B', 'T']
    suffix_index = 0
    while n >= 1000 and suffix_index < len(suffixes) - 1:
        n /= 1000.0
        suffix_index += 1
    
    # maxFractionDigits: 1
    formatted_num = f"{n:.1f}".rstrip('0').rstrip('.')
    return f"{symbol}{formatted_num}{suffixes[suffix_index]}"

def formatDate(date: Union[datetime, str], formatStr: str = 'MMM dd, yyyy') -> str:
    # const dateObj = typeof date === 'string' ? new Date(date) : date
    # return format(dateObj, formatStr)
    dateObj = date if isinstance(date, datetime) else datetime.fromisoformat(str(date).replace('Z', '+00:00'))
    return date_fns_format(dateObj, formatStr)

def formatTimeAgo(date: Union[datetime, str]) -> str:
    # const dateObj = typeof date === 'string' ? new Date(date) : date
    # return formatDistanceToNow(dateObj, { addSuffix: true })
    dateObj = date if isinstance(date, datetime) else datetime.fromisoformat(str(date).replace('Z', '+00:00'))
    return date_fns_distance_to_now(dateObj, add_suffix=True)

def formatTimeLeft(endDate: Union[datetime, str]) -> str:
    # const end = typeof endDate === 'string' ? new Date(endDate) : endDate
    end = endDate if isinstance(endDate, datetime) else datetime.fromisoformat(str(endDate).replace('Z', '+00:00'))
    # const now = new Date()
    now = datetime.now()
    
    # if (isBefore(end, now)) {
    if is_before(end, now):
        # return 'Ended'
        return 'Ended'
    
    # const diff = end.getTime() - now.getTime()
    # Python: total_seconds() * 1000 for milliseconds, or just use seconds logic
    diff_ms = (end - now).total_seconds() * 1000
    
    # const days = Math.floor(diff / (1000 * 60 * 60 * 24))
    days = math.floor(diff_ms / (1000 * 60 * 60 * 24))
    # const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
    hours = math.floor((diff_ms % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
    # const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
    minutes = math.floor((diff_ms % (1000 * 60 * 60)) / (1000 * 60))
    
    # if (days > 0) {
    if days > 0:
        # return `${days}d ${hours}h`
        return f"{days}d {hours}h"
    # } else if (hours > 0) {
    elif hours > 0:
        # return `${hours}h ${minutes}m`
        return f"{hours}h {minutes}m"
    # } else {
    else:
        # return `${minutes}m`
        return f"{minutes}m"

def isAuctionEnding(endDate: Union[datetime, str], hours: float = 24) -> bool:
    # const end = typeof endDate === 'string' ? new Date(endDate) : endDate
    end = endDate if isinstance(endDate, datetime) else datetime.fromisoformat(str(endDate).replace('Z', '+00:00'))
    # const now = new Date()
    now = datetime.now()
    # const diff = end.getTime() - now.getTime()
    diff_ms = (end - now).total_seconds() * 1000
    # const diffHours = diff / (1000 * 60 * 60)
    diffHours = diff_ms / (1000 * 60 * 60)
    
    # return diffHours <= hours && diffHours > 0
    return diffHours <= hours and diffHours > 0

def isAuctionEnded(endDate: Union[datetime, str]) -> bool:
    # const end = typeof endDate === 'string' ? new Date(endDate) : endDate
    end = endDate if isinstance(endDate, datetime) else datetime.fromisoformat(str(endDate).replace('Z', '+00:00'))
    # return isBefore(end, new Date())
    return is_before(end, datetime.now())

def generateId() -> str:
    # return Math.random().toString(36).substr(2, 9)
    # Replicating base36 approximation of random
    # In JS: Math.random() is 0-1 float.
    # toString(36) converts to base 36 string (0-9a-z).
    # substr(2, 9) takes 9 chars after '0.'
    
    # Python doesn't have native float->base36.
    # We can just generate a random string of 9 chars [0-9a-z]
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=9))

T = TypeVar('T', bound=Callable[..., Any])

def debounce(func: T, wait: float):
    # wait is in ms in TS? usually yes.
    # TS: wait (number).
    wait_sec = wait / 1000.0
    
    timer: Optional[threading.Timer] = None
    
    def debounced(*args, **kwargs):
        nonlocal timer
        if timer is not None:
            timer.cancel()
        
        timer = threading.Timer(wait_sec, func, args=args, kwargs=kwargs)
        timer.start()
        
    return debounced

def throttle(func: T, limit: float):
    limit_sec = limit / 1000.0
    inThrottle = False
    
    def wrapper(*args, **kwargs):
        nonlocal inThrottle
        if not inThrottle:
            func(*args, **kwargs)
            inThrottle = True
            
            def reset():
                nonlocal inThrottle
                inThrottle = False
            
            threading.Timer(limit_sec, reset).start()
            
    return wrapper

def validateEmail(email: str) -> bool:
    # const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    # return emailRegex.test(email)
    emailRegex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return bool(re.match(emailRegex, email))

def validatePhone(phone: str) -> bool:
    # const phoneRegex = /^(\+263|0)7[7-8][0-9]{7}$/
    # return phoneRegex.test(phone)
    phoneRegex = r"^(\+263|0)7[7-8][0-9]{7}$"
    return bool(re.match(phoneRegex, phone))

def sanitizeInput(input_str: str) -> str:
    # return input.trim().replace(/[<>]/g, '')
    return re.sub(r'[<>]', '', input_str.strip())

def truncateText(text: str, maxLength: int) -> str:
    # if (text.length <= maxLength) return text
    if len(text) <= maxLength:
        return text
    # return text.slice(0, maxLength) + '...'
    return text[:maxLength] + '...'

def getCategoryIcon(category: str) -> str:
    icons = {
        'cattle': '🐄',
        'goats': '🐐',
        'sheep': '🐑',
        'pigs': '🐷',
        'chickens': '🐔',
        'horses': '🐎',
        'donkeys': '🦙',
    }
    return icons.get(category, '🐄')

def getCategoryColor(category: str) -> str:
    colors = {
        'cattle': 'bg-blue-100 text-blue-800',
        'goats': 'bg-green-100 text-green-800',
        'sheep': 'bg-gray-100 text-gray-800',
        'pigs': 'bg-pink-100 text-pink-800',
        'chickens': 'bg-yellow-100 text-yellow-800',
        'horses': 'bg-purple-100 text-purple-800',
        'donkeys': 'bg-orange-100 text-orange-800',
    }
    return colors.get(category, 'bg-gray-100 text-gray-800')

def calculateBidIncrement(currentBid: float) -> float:
    # if (currentBid < 100) return 10
    if currentBid < 100:
        return 10
    # if (currentBid < 500) return 25
    if currentBid < 500:
        return 25
    # if (currentBid < 1000) return 50
    if currentBid < 1000:
        return 50
    # if (currentBid < 5000) return 100
    if currentBid < 5000:
        return 100
    # return Math.ceil(currentBid * 0.05)
    return math.ceil(currentBid * 0.05)

def getMinimumBid(currentBid: float) -> float:
    return currentBid + calculateBidIncrement(currentBid)

def formatFileSize(bytes_val: float) -> str:
    # if (bytes === 0) return '0 Bytes'
    if bytes_val == 0:
        return '0 Bytes'
    
    # const k = 1024
    k = 1024
    # const sizes = ['Bytes', 'KB', 'MB', 'GB']
    sizes = ['Bytes', 'KB', 'MB', 'GB']
    # const i = Math.floor(Math.log(bytes) / Math.log(k))
    i = math.floor(math.log(bytes_val) / math.log(k))
    
    # return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    # In JS parseFloat("2.00") is 2.
    val = bytes_val / math.pow(k, i)
    val_fixed = f"{val:.2f}"
    val_float = float(val_fixed) # removes trailing zeros if integer? JS `parseFloat` preserves integer but removes `.00`? 
    # `(2.00).toFixed(2)` is "2.00". `parseFloat("2.00")` is 2.
    # Python `float(2.00)` is `2.0`.
    # I'll just use str(val_float) which might be `2.0`.
    # To match JS `parseFloat`, if it ends in `.0` or `.00`, remove it?
    # Actually standard float str in python is fine.
    
    # Wait, `val_fixed` is str. `float()` makes it float.
    # `str(val_float)` might have `.0`.
    res = f"{val_float:g}" # g removes insignificant zeros?
    
    return f"{res} {sizes[i]}"

def copyToClipboard(text: str):
    # if (navigator.clipboard) ...
    # Browser specific.
    raise NotImplementedError("Browser-specific functionality (navigator.clipboard) not available in Python")
    
def getErrorMessage(error: Any) -> str:
    # if (error instanceof Error) return error.message
    if isinstance(error, Exception):
        return str(error)
    # if (typeof error === 'string') return error
    if isinstance(error, str):
        return error
    # return 'An unknown error occurred'
    return 'An unknown error occurred'
