import enum


class Preamplifier(enum.Enum):
    UNKNOWN = 0
    NONE = 1
    TERRA_AB010 = 2
    TERRA_AB011 = 3
    SELF_BUILT_WITHOUT_FILTER = 4
    SELF_BUILT_WITH_FILTER = 5

    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)
