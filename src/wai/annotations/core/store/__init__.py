"""
Stores are a generalised way of representing data-stores as file-system-like structures.
This abstracts the local file-system and allows for other data-storage-systems to be
used as sources/sinks of data at either end of a conversion pipeline.

Each type of store specifies a type of store-key, which is used to address files in the
store. A store-key is "path-key-like", meaning they can be manipulated as paths to e.g.
find related files by modifying the filename/extension/etc. Their path representation is
also used to generate labels for dataset items in a conversion pipeline.

Stores can be readable, writable, or both, but should not be neither. Readable stores can be
addressed by a specific instance of their key-type, or queried using a string, which is
interpreted as some type of pattern, according to the store. For example, queries to the
local-file-store are interpreted as glob syntax, while the dict-store uses regular expressions.
Writable stores require an exact key at which to write the file-data.

New store types can be added to wai.annotations via the plugin system, by creating a store-specifier
and adding it to setup.py as an entry-point.
"""
from ._DictStore import DictStore, DictStoreMapping
from ._LocalFileStore import LocalFileStore
from ._ReadableStore import ReadableStore
from ._Store import Store
from ._WritableStore import WritableStore
