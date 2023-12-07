from enum import IntEnum, auto

class Tags(IntEnum):
    rampe = auto()
    fauteuilRoulant = auto()
    # ...

# print(Tags.rampe.value,Tags.fauteuilRoulant.value)