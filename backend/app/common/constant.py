from enum import Enum


class BaseEnum(str, Enum):
    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    @classmethod
    def list(cls):
        return [c.value for c in cls]
