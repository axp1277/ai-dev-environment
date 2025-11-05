# Backward compatibility wrapper - use modularized structure
from .client import SchwabClient
from .auth import SchwabAuth  
from .models import *

# Alias for backward compatibility
SchwabApi = SchwabClient