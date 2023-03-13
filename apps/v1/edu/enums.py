from enum import Enum


class StudentInGroupStatus(Enum):
    studying = "studying"
    finished = "finished"

    @classmethod
    def choices(cls):
        return ((key.value, key.name) for key in cls)
    

class StudentProjectStatus(Enum):
    in_progress = "in_progress"
    accepted = "accepted"
    rejected = "rejected"

    @classmethod
    def choices(cls):
        return ((key.value, key.name) for key in cls)
