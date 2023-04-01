from enum import Enum


class StudentInGroupStatus(Enum):
    studying = "studying"
    finished = "finished"
    gone = 'gone'

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


class GroupStatus(Enum):
    active = 'active'
    finished = 'finished'
    canceled = 'canceled'
    
    @classmethod
    def choices(cls):
        return ((key.value, key.name) for key in cls)
    
class GroupType(Enum):
    online = 'online'
    offline = 'offline'
    hibrid = 'hibrid'

    @classmethod
    def choices(cls):
        return ((key.value, key.name) for key in cls)