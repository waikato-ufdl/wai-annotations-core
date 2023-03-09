import re

# Ensures other plugins have normalised names
# (runs of lowercase letters separated by dashes)
PLUGIN_NAME_MATCHER = re.compile(r'^[a-z]+(-[a-z]+)*$').fullmatch
