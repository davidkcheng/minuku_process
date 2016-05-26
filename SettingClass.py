millisecondpersecond = 1


def Code2Type(num):
    if num == 0:
        return 'ONBICYCLE'
    elif num == 1:
        return 'INVEHICLE'
    elif num == 2:
        return 'WALKING'
    elif num == 3:
        return 'ONFOOT'
    elif num == 4:
        return 'NOACTIVITYTYPE'
    elif num == 5:
        return 'STILL'
    elif num == 6:
        return 'UNKNOWN'
    elif num == 7:
        return 'TILTING'
    elif num == 8:
        return 'RUNNING'

class ActivityType:
    ONBICYCLE = 0
    INVEHICLE = 1
    WALKING = 2
    ONFOOT = 3
    NOACTIVITYTYPE = 4
    STILL = 5
    UNKNOWN = 6
    TILTING = 7
    RUNNING = 8       
    
class StateType:
    STATE_STATIC = 0
    STATE_SUSPECTING_START = 1
    STATE_CONFIRMED = 2
    STATE_SUSPECTING_STOP = 3
    
class WindowLength:
    START_ACTIVITY_DEFAULT = 20 * millisecondpersecond
    START_ACTIVITY_IN_VEHICLE = 20 * millisecondpersecond
    START_ACTIVITY_ON_FOOT = 20 * millisecondpersecond
    START_ACTIVITY_ON_BICYCLE = 20 * millisecondpersecond
    
    STOP_ACTIVITY_DEFAULT = 20 * millisecondpersecond
    STOP_ACTIVITY_IN_VEHICLE = 150 * millisecondpersecond
    STOP_ACTIVITY_ON_FOOT = 60 * millisecondpersecond
    STOP_ACTIVITY_ON_BICYCLE = 90 * millisecondpersecond

class ConfirmStartActivityThreshold:
    INVEHICLE = 0.6;
    ONFOOT = 0.6
    ONBICYCLE = 0.6
    
class ConfirmStopActivityThreshold:
    INVEHICLE = 0.2
    ONFOOT = 0.2
    ONBICYCLE = 0.2
    
