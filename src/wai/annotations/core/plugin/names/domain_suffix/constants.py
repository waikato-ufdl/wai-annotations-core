import re

# Ensure domain-codes are 2 letters only
DOMAIN_CODE_MATCHER = re.compile(r'^[a-z]{2}$').fullmatch

# Matcher which checks if a source/sink plugin name might end in a domain-code suffix
# Matches anything ending in -dc where dc is a 2-letter domain code
SOURCE_SINK_DOMAIN_CODE_SUFFIX_MATCHER = re.compile(r'^.*(-[a-z]{2})$').fullmatch

# Matcher which checks if a processor plugin name might end in a domain-code suffix
# Matches anything ending in -dc-dc or -from-dc or -into-dc
# Also matches anything ending in -dc, which is equivalent to -dc-dc
PROCESSOR_DOMAIN_CODE_SUFFIX_MATCHER = re.compile(r'^.*?((-from|-into|-[a-z]{2})?-[a-z]{2})$').fullmatch
