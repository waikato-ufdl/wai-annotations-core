from typing import TypeVar, MutableMapping, Iterator, Generic
from weakref import WeakValueDictionary, WeakKeyDictionary

KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


class ID(Generic[KeyType]):
    """
    Helper class for the WeakIdentityKeyDictionary class, which references
    the ID of an object.
    """
    def __init__(self, key: KeyType):
        self._identity: int = id(key)

    def __hash__(self):
        return self._identity

    def __eq__(self, other):
        if isinstance(other, ID):
            other = other._identity
        return isinstance(other, int) and other == self._identity


class WeakIdentityKeyDictionary(MutableMapping[KeyType, ValueType]):
    """
    Dictionary which weakly references keys by their identity.
    """
    def __init__(self):
        # If a strong reference to the key exists, self._keys will keep a strong
        # reference to the ID object, which will keep the value in self._values. Once the
        # key is dropped, self._keys will also drop the ID object, which will in turn
        # drop the value. IDs are internal so other strong reference can't exist.
        self._keys: MutableMapping[ID, KeyType] = WeakValueDictionary()
        self._values: MutableMapping[ID, ValueType] = WeakKeyDictionary()

    def __setitem__(self, k: KeyType, v: ValueType):
        identity = ID(k)
        self._keys[identity] = k
        self._values[identity] = v
        
    def __delitem__(self, v: KeyType):
        identity = ID(v)
        del self._keys[identity]

        # Race condition: deleting self._keys[identity] may cause self._values[identity] to be collected
        #                 (its only strong key reference is removed) so the delete may fail
        try:
            del self._values[identity]
        except KeyError:
            pass

    def __getitem__(self, k: KeyType) -> ValueType:
        identity = ID(k)
        return self._values[identity]

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[KeyType]:
        return iter(self._keys.values())

    def __contains__(self, item: KeyType) -> bool:
        return id(item) in self._keys
