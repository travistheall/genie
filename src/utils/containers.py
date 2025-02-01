from enum import Enum
from typing import TypeVar
from collections.abc import KeysView, ValuesView, ItemsView
from collections import UserDict


K = TypeVar("K")
V = TypeVar("V")


class MyUserDict(UserDict[K, V]):
    def keys(self) -> KeysView[K]:
        return self.data.keys()

    def values(self) -> ValuesView[V]:
        return self.data.values()

    def items(self) -> ItemsView[K, V]:
        return self.data.items()


class EnumKeyDict(MyUserDict[str, V]):

    def _clean_key(fn):
        def wrapped(self, key: Enum | str, *args, **kwargs):
            if isinstance(key, Enum):
                key_s = key.value
            else:
                key_s = str(key)
            return fn(self, key_s, *args, **kwargs)

        return wrapped

    @_clean_key
    def __contains__(self, key: Enum | str) -> bool:
        return super().__contains__(key)

    @_clean_key
    def get(self, key: Enum | str, default=None) -> V:
        return super().get(key, default)

    @_clean_key
    def __getitem__(self, key: Enum | str) -> V:
        return super().__getitem__(key)

    @_clean_key
    def __setitem__(self, key: Enum | str, item: V) -> None:
        self.data[key] = item

    @_clean_key
    def __delitem__(self, key: Enum | str) -> None:
        del self.data[key]
