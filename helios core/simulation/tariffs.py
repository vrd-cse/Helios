"""
Tariff Module
==============
Provides time-of-use electricity pricing.

Note: This module is deprecated - use config.get_tariff() instead.
Kept for backward compatibility.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_tariff

# Re-export for backward compatibility
__all__ = ['get_tariff']
