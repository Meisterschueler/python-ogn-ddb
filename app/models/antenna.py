import enum


class Antenna(enum.Enum):
    UNKNOWN = 0
    CHINESE_9DB_JPOLE = 1
    JETVISION_ACTIVE = 2
    WIMO_SPERRTOPF = 3
    GROUND_PLANE = 4
    SELF_BUILT = 5

    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)
