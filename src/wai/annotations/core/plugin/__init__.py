"""
wai-annotations can extend its functionality by adding plugins. Currently there
are 5 types of plugins:
 - Domains
 - Stores
 - Source, Processor, and Sink Stages

Plugins are added by creating a specifier class which extends the appropriate
base-class for the type of plugin being added. This class describes the functionality
of the plugin to wai-annotations, and allows it to instantiate that functionality.
To expose a plugin, in setup.py, under the entry_points dict, add a key "wai.annotations.plugins",
whose value should be a list of strings. Each string should be of the form:

"[name]=[my.package.path.to]:[SpecifierClassName]"

where name is a unique name (see below) for the plugin, and the path and class-name point
to the specifier class describing the plugin.

Plugin names for each type of plugin have different requirements:
 - Domains: Must be two lowercase English letters [a-z].
 - Stores: Must be words consisting of lowercase English letters separated by dashes [-].
 - Source and Sink Stages:
    Must be words consisting of lowercase English letters separated by dashes [-].
    Additionally, if the name ends in a dash followed by a two-letter domain name (as above),
    must be a source/sink stage capable of producing/consuming instances in that domain.
 - Processor Stages:
    Must be words consisting of lowercase English letters separated by dashes [-].
    Additionally, given [dc(1/2)] is a two-letter domain name (as above):
     - ending in -dc means the processor consumes and produces instances in that domain,
     - ending in -dc1-dc2 means that the processor consumes dc1 instances and produces
       dc2 instances,
     - ending in -from-dc means that the processor consumes instances in that domain,
     - ending in -into-dc means that the processor produces instances in that domain.
"""
from ._get_all_plugin_names import get_all_plugin_names
from ._get_all_plugins_by_type import get_all_plugins_by_type, AllPluginsByType
