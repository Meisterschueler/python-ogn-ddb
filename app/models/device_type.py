import enum


class DeviceType(enum.Enum):
    FLARM = 0
    ICAO = 1
    OGN = 2

    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)
