#!/usr/bin/env python3
#

"""The method makedirs() is recursive directory creation function. Like
mkdir(), but makes all intermediate-level directories needed to contain the
leaf directory.

The default mode is 0o777 (octal). On some systems, mode is ignored. Where it
is used, the current umask value is first masked out.

If exist_ok is False (the default), an OSError is raised if the target
directory already exists."""
