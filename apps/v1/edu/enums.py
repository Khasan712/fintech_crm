from enum import Enum


class StudentInGroupStatus(Enum):
    studying = "studying"
    finished = "finished"

    @classmethod
    def choices(cls):
        return ((key.value, key.name) for key in cls)
