from package_utils.context.entry_point import create_entry_point

from .context import context
from .main import main

entry_point = create_entry_point(main, context)
