import enum


class SdrDongle(enum.Enum):
    UNKNOWN = 0
    BLUE_PLASTIC = 1
    BLACK_PLASTIC = 2
    RTLSDR_COM = 3
    NOELEC = 4
    OTHER = 5

    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)
