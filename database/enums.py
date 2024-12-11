from enum import IntEnum


class Role(IntEnum):
    UNDEFINED = 0
    MEMBER = 1
    TRAINER = 2
    ADMIN = 4


class Level(IntEnum):
    TRAINER = 1
    SWIMMING_POOL = 2
    DIETOLOG = 4
    MEALS = 8
    SPA = 16
    KIDS = 32


_l = {
    Level.TRAINER: "Тренер",
    Level.SWIMMING_POOL: "Бассейн",
    Level.KIDS: "Дети",
    Level.DIETOLOG: "Услуги диетолога",
    Level.SPA: "СПА",
    Level.MEALS: "Питание",
}


def get_included_string(level: int) -> str:
        included = []
        for l in Level:
            if level & l:
                included.append(_l[level & l])
        return ", ".join(included)
