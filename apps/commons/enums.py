from enum import Enum


class LessonStatus(Enum):
    started = 'started'
    finished = 'finished'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
