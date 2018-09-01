from pkg_resources import load_entry_point
from .settings import CONF_DIR

print(load_entry_point)
load_entry_point('pywal==3.1.0', 'console_scripts', 'wal')()
