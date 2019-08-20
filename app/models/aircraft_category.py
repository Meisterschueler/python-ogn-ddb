import enum


class AircraftCategory(enum.Enum):
    SAILPLANE = 0
    PLANE = 1
    ULTRALIGHT = 2
    HELICOPTER = 3
    DRONE = 4
    OTHER = 5
    WTF = 6

    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)
