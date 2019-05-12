import pkg_resources
import netdev.vendors
from netdev.dispatcher import create, platforms
from netdev.logger import logger

__version__ = pkg_resources.get_distribution("netdev").version

__all__ = ("create", "platforms", "logger", "vendors", "__version__")
