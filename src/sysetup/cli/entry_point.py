from package_utils.context.entry_point import create_entry_point

from sysetup.context import context
from sysetup.main.main import main

entry_point = create_entry_point(main, context)
