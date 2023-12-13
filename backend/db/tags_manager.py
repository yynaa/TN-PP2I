from enum import IntEnum, auto

class Tags(IntEnum):
    entrance_fauteuilRoulant = auto()
    toilets_fauteuilRoulant = auto()
    seat_fauteuilRoulant = auto()
    # ...

if __name__ == "__main__":
    print(Tags.entrance_fauteuilRoulant.value,Tags.toilets_fauteuilRoulant.value,Tags.seat_fauteuilRoulant.value)