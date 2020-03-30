import enum


class AircraftCategory(enum.Enum):
    SAILPLANE = 1
    PLANE = 2
    ULTRALIGHT = 3
    HELICOPTER = 4
    DRONE = 5
    OTHER = 6

    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)
