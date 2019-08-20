import enum


class RxFilter(enum.Enum):
    UNKNOWN = 0
    NONE = 1
    SAW = 2
    CBP840 = 3
    CAVITY = 4

    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)
