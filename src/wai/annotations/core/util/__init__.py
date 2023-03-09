"""
Package for general utility functions.
"""
from ._chain_map import chain_map
from ._describe_value import describe_value
from ._first import first, first_lazy_default
from ._gcd import gcd
from ._get_files_from_directory import get_files_from_directory
from ._InstanceState import InstanceState
from ._is_subtype import is_subtype
from ._OptionalContextManager import OptionalContextManager
from ._polygon_to_poly_array import polygon_to_poly_array
from ._polygons import UNION, INTERSECT, COMBINATIONS, to_polygon, to_polygons, intersect_over_union
from ._raise_expression import raise_expression
from ._read_file_list import read_file_list
from ._recursive_iglob import recursive_iglob
from ._ReentrantContextManager import ReentrantContextManager
from ._type_name import type_name
from ._unique import unique
from ._WeakIdentityKeyDictionary import WeakIdentityKeyDictionary
