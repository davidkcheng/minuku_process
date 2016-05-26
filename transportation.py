import time
from datetime import datetime, timedelta
from SettingClass import *
from __builtin__ import True
from scipy.stats.mstats_basic import threshold
from logging import thread
import urllib
import json
import pytz
import calendar
    
Alldata = []
suspectedStartActivityType = ActivityType.NOACTIVITYTYPE
suspectedStopActivityType = ActivityType.NOACTIVITYTYPE
confirmedActivityType = ActivityType.NOACTIVITYTYPE
suspectTime = 0
currentState = StateType.STATE_STATIC


class Record:
    date = ""
    timestamp = 0
    probableActivity = []
    lat = 0
    long = 0
    rawstring = ""
    
def contains_digits(s):
    return any(char.isdigit() for char in s)

def readData(filename):
    
    global Alldata
    
    input_file = open(filename, 'rU')
    line = input_file.readline()
    while line:
        record = Record()
        sub = line.split('\t')
        if sub[0] != "AR": 
#             print sub[0]
            line = input_file.readline()
            continue
            
        if not contains_digits(sub[3]):
            line = input_file.readline()
            continue
        
        record.date = sub[1]
        record.timestamp = int(sub[2])/1e3
        record.rawstring = sub[3].rstrip('\n')
        
        latlong = sub[4].strip().split(',')
#         latlong = sub[4].split(',')
        record.lat = latlong[0][1:]
        record.long = latlong[1][:-1]
#         print record.lat + " " + record.long
        
        sub1 = sub[3].split(';;')
        
    
        probableactivity = []
        for e in sub1:
            activity = e.split(':')[0]
            probability = e.split(':')[1]
            if activity == 'on_bicycle':
                probableactivity.append([ActivityType.ONBICYCLE, probability])
            elif activity == 'in_vehicle':
                probableactivity.append([ActivityType.INVEHICLE, probability])
            elif activity == 'walking':
                probableactivity.append([ActivityType.WALKING, probability])
            elif activity == 'on_foot':
                probableactivity.append([ActivityType.ONFOOT, probability])
            elif activity == 'unknown':
                probableactivity.append([ActivityType.UNKNOWN, probability])
            elif activity == 'still':
                probableactivity.append([ActivityType.STILL, probability])
            elif activity == 'tilting':
                probableactivity.append([ActivityType.TILTING, probability])
            elif activity == 'running':
                probableactivity.append([ActivityType.RUNNING, probability])

        record.probableActivity = probableactivity
        Alldata.append(record)
        line = input_file.readline()
     
    input_file.close()
    
def transportationMode(record):
    
    global Alldata
    global suspectedStartActivityType
    global suspectedStopActivityType
    global confirmedActivityType
    global suspectTime
    global currentState    
    
#     print 'currentstate '+str(currentState)
#     print 'confirmedActivityType '+ Code2Type(confirmedActivityType)
    
#     print 'suspectedStartActivityType '+str(suspectedStartActivityType)
#     print 'suspectedStopActivityType '+str(suspectedStopActivityType)
#     print '\n'
    timestamp = record.timestamp
    probableActivity = record.probableActivity
#     if len(probableActivity) == 0:
#         return  
    if currentState == StateType.STATE_STATIC: #0
#         print 'first statement'
        if probableActivity[0][0] == ActivityType.ONFOOT or probableActivity[0][0] == ActivityType.INVEHICLE or probableActivity[0][0] == ActivityType.ONBICYCLE:
            currentState = StateType.STATE_SUSPECTING_START #1
            suspectedStartActivityType = probableActivity[0][0] 
            suspectTime = timestamp
              
    elif currentState == StateType.STATE_SUSPECTING_START: #1
#         print 'second statement'
        istime2check = checkIsTime2Confirm(timestamp, suspectTime, getWindowLength(suspectedStartActivityType, currentState))
        
        if istime2check:
#             print 'istime2check'
            starttime = (timestamp - getWindowLength(suspectedStartActivityType, currentState))
            endtime = timestamp
            isNewTransportationModeConfirmed = confirmStartPossibleTransportation(suspectedStartActivityType, getWindowData(starttime, endtime))
            
            if isNewTransportationModeConfirmed:
#                 print 'isNewTransportationModeConfirmed!!!!'
                currentState = StateType.STATE_CONFIRMED
                confirmedActivityType = suspectedStartActivityType
                suspectedStartActivityType = ActivityType.NOACTIVITYTYPE
                suspectTime = starttime
                return confirmedActivityType
            else:
#                 print 'NOT isNewTransportationModeConfirmed!!!!'
                currentState = StateType.STATE_STATIC
                confirmedActivityType = ActivityType.NOACTIVITYTYPE
                suspectTime = 0
                return confirmedActivityType
                
    elif currentState == StateType.STATE_CONFIRMED:
#         print 'third statement'
        if probableActivity[0][0] != confirmedActivityType and probableActivity[0][0] != ActivityType.TILTING and probableActivity[0][0] != ActivityType.UNKNOWN:
            currentState = StateType.STATE_SUSPECTING_STOP
            suspectedStopActivityType = confirmedActivityType
            suspectTime = timestamp
            
    elif currentState == StateType.STATE_SUSPECTING_STOP:
#         print 'fourth statement'
        istime2confirm = checkIsTime2Confirm(timestamp, suspectTime, getWindowLength(suspectedStopActivityType, currentState))
        if istime2confirm:
            starttime = (timestamp - getWindowLength(suspectedStartActivityType, currentState))
            endtime = timestamp
            isExitingTransportationMode = confirmStopPossibleTransportation(suspectedStopActivityType, getWindowData(starttime, endtime))
            
            if isExitingTransportationMode:
                currentState = StateType.STATE_STATIC
                confirmedActivityType = ActivityType.NOACTIVITYTYPE
                suspectedStopActivityType = ActivityType.NOACTIVITYTYPE
                suspectTime = starttime
            else:
                currentState = StateType.STATE_CONFIRMED
                suspectedStopActivityType = ActivityType.NOACTIVITYTYPE
            
            suspectTime = 0
        
        if probableActivity[0][0] != suspectedStopActivityType and probableActivity[0][0] != ActivityType.TILTING and probableActivity[0][0] != ActivityType.STILL and probableActivity[0][0] != ActivityType.UNKNOWN:
            istime2confirm = checkIsTime2Confirm(timestamp, suspectTime, getWindowLength(suspectedStartActivityType, StateType.STATE_SUSPECTING_START))
            if istime2confirm:
#                 print 'istime2confirm!!'
                starttime = (timestamp - getWindowLength(probableActivity[0][0], StateType.STATE_SUSPECTING_START))
                endtime = timestamp 
                isActuallyStartingAnotherActivity = changeSuspectingTransportation(probableActivity[0][0], getWindowData(starttime, endtime))
                if isActuallyStartingAnotherActivity:
                    currentState = StateType.STATE_SUSPECTING_START
                    suspectedStartActivityType = probableActivity[0][0]
                    suspectedStopActivityType = ActivityType.NOACTIVITYTYPE
                    suspectTime = timestamp
                        
    
    return confirmedActivityType
    


def checkIsTime2Confirm(timestamp, suspectime, windowlength):
        
    if timestamp - suspectime > windowlength:
        return True
    else:
        return False
    
def getWindowLength(activitytype, statetype):
    

    if statetype == StateType.STATE_SUSPECTING_START:
        
        if activitytype == ActivityType.INVEHICLE:
            return WindowLength.START_ACTIVITY_IN_VEHICLE
        elif activitytype == ActivityType.ONFOOT:
            return WindowLength.START_ACTIVITY_ON_FOOT
        elif activitytype == ActivityType.ONBICYCLE:
            return WindowLength.START_ACTIVITY_ON_BICYCLE
        else:
            return WindowLength.START_ACTIVITY_DEFAULT
        
    elif statetype == StateType.STATE_SUSPECTING_STOP:
        
        if activitytype == ActivityType.INVEHICLE:
            return WindowLength.STOP_ACTIVITY_IN_VEHICLE
        elif activitytype == ActivityType.ONFOOT:
            return WindowLength.STOP_ACTIVITY_ON_FOOT
        elif activitytype == ActivityType.ONBICYCLE:
            return WindowLength.STOP_ACTIVITY_ON_BICYCLE
        else:
            return WindowLength.STOP_ACTIVITY_DEFAULT

def getWindowData(starttime, endtime):
    
    global Alldata
    
    windowdata = []
#     print len(Alldata)
#     print starttime
#     print endtime
    for i in range(0, len(Alldata)):
        if Alldata[i].timestamp >= starttime and Alldata[i].timestamp <= endtime:
            
            windowdata.append(Alldata[i])
#     print len(windowdata)
    return windowdata
 
def confirmStopPossibleTransportation(activitytype, windowdata):
    
    global Alldata
    global suspectedStartActivityType
    global suspectedStopActivityType
    global confirmedActivityType
    global suspectTime
    global currentState    
    
    threshold = getConfirmStopThreshold(activitytype)
    count = 0
    inRecentCount = 0
    
    for i in range(0, len(windowdata)):
        detectedActivities = windowdata[i].probableActivity
        
        if i >= len(windowdata)-5:
            if detectedActivities[0][0] == activitytype:
                inRecentCount += 1 
        
        
        for activityIndex in range(0, len(detectedActivities)):
            if detectedActivities[0][0] == activitytype:
                count += 1
                break
        
        
    percentage = count/len(windowdata)
    
    if len(windowdata) !=0:
        
        if threshold >= percentage and inRecentCount <= 2:
            return True
        else:
            return False
    else:
        return False 
    
    return True
    
    
def confirmStartPossibleTransportation(activitytype, windowdata):
    
    global Alldata
    global suspectedStartActivityType
    global suspectedStopActivityType
    global confirmedActivityType
    global suspectTime
    global currentState    
    
    threshold = getConfirmStartThreshold(activitytype)
    count = 0
    inRecentCount = 0
    for i in range(0, len(windowdata)):
        detectedActivities = windowdata[i].probableActivity
#         print detectedActivities
        if i >= len(windowdata)-5:
            if detectedActivities[0][0] == activitytype:
                inRecentCount += 1
        
        if detectedActivities[0][0] == activitytype:
            count += 1
    
    if len(windowdata) !=0:
        percentage = count/len(windowdata)
        if threshold <= percentage or inRecentCount >= 2:
            return True
        else:
            return False
    else:
        return False 
    
    return True

def changeSuspectingTransportation(activitytype, windowdata):
        
#     threshold = getConfirmStartThreshold(activitytype)
    inRecentCount = 0
#     print len(windowdata)
    for i in range(len(windowdata)-1, -1, -1):
#         print i
        detectedActivities = windowdata[i].probableActivity
        if i >= len(windowdata)-3:
            if detectedActivities[0][0] == activitytype:
                inRecentCount += 1
    
    if len(windowdata) != 0:
        if inRecentCount >= 2:
            return False
        else:
            return True
    else:
        return False

        
        

def getConfirmStopThreshold(activitytype):
    if activitytype == ActivityType.INVEHICLE:
        return ConfirmStopActivityThreshold.INVEHICLE
    elif activitytype == ActivityType.ONFOOT:
        return ConfirmStopActivityThreshold.ONFOOT
    elif activitytype == ActivityType.ONBICYCLE:
        return ConfirmStopActivityThreshold.ONBICYCLE
    else:
        return 0.5;    

def getConfirmStartThreshold(activitytype):
    if activitytype == ActivityType.INVEHICLE:
        return ConfirmStartActivityThreshold.INVEHICLE
    elif activitytype == ActivityType.ONFOOT:
        return ConfirmStartActivityThreshold.ONFOOT
    elif activitytype == ActivityType.ONBICYCLE:
        return ConfirmStartActivityThreshold.ONBICYCLE
    else:
        return 0.5;
    
         
def main():

    utc_dt = datetime.utcfromtimestamp((1457413203165-18000000)/1000)

    readData('logfiles/AR.txt')
    writeFile = open("output.txt", 'wb')
    writeFile2 = open("output1.txt", 'wb')
     
    currentActivity = ""
    starttime = ""
    endtime = ""
   
    for record in Alldata:
 
        activity = Code2Type(transportationMode(record))
        time = str(int(record.timestamp*1000))
        lat = record.lat
        longi = record.long
         
        if not currentActivity:
            currentActivity = activity
            starttime = time
            endtime = time
#             print activity
        else:
            if currentActivity is not activity:
#                 print activity
                endtime = time
                if currentActivity is "NOACTIVITYTYPE":
#                     print starttime
                    newline2 = starttime + '\t' + endtime + '\t' + datetime.utcfromtimestamp((int(starttime)-18000000)/1000).strftime('%Y-%m-%d %H:%M:%S') + '\t' + datetime.utcfromtimestamp((int(endtime)-18000000)/1000).strftime('%Y-%m-%d %H:%M:%s')  + '\t' + getPlace(lat + "," + longi)
                else:
                    newline2 = starttime + '\t' + endtime + '\t' + datetime.utcfromtimestamp((int(starttime)-18000000)/1000).strftime('%Y-%m-%d %H:%M:%s')  + '\t' + datetime.utcfromtimestamp((int(endtime)-18000000)/1000).strftime('%Y-%m-%d %H:%M:%s')  + '\t' + currentActivity
                writeFile2.write(newline2)
                writeFile2.write("\n")
                 
                starttime = time
                currentActivity = activity
            else:
                endtime = time
                currentActivity = activity
#         print time
#         print datetime.utcfromtimestamp((int(time)-18000000)/1000).strftime('%Y-%m-%d %H:%M:%S')
        newline = time + '\t' + datetime.utcfromtimestamp((int(time)-18000000)/1000).strftime('%Y-%m-%d %H:%M:%S')  + '\t' + record.rawstring + '\t' + activity
        writeFile.write(newline)
        writeFile.write("\n")
     
    if currentActivity is "NOACTIVITYTYPE":
        newline2 = starttime + '\t' + endtime + '\t' + datetime.utcfromtimestamp((int(starttime)-18000000)/1000).strftime('%Y-%m-%d %H:%M:%s')  + '\t' + datetime.utcfromtimestamp((int(endtime)-18000000)/1000).strftime('%Y-%m-%d %H:%M:%s')  + '\t' + getPlace(lat + "," + longi)
    else:
        newline2 = starttime + '\t'  + endtime + '\t' + datetime.utcfromtimestamp((int(starttime)-18000000)/1000).strftime('%Y-%m-%d %H:%M:%s')  + '\t' + datetime.utcfromtimestamp((int(endtime)-18000000)/1000).strftime('%Y-%m-%d %H:%M:%s')  + '\t' + currentActivity
    writeFile2.write(newline2)
    writeFile2.write("\n")
     
    writeFile.close()
    writeFile2.close()
#     getPlace("42.279532,-83.741024")

def getPlace(location):
        #making the url
    ret = ""    
    
    AUTH_KEY = 'AIzaSyDkmJL928g4hLfqECzESks8XdbVNvSsv9Y'

    MyUrl = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
         '?location=%s'
         '&radius=20&key=%s') % (location, AUTH_KEY)
    print MyUrl
    #grabbing the JSON result
    response = urllib.urlopen(MyUrl)
    jsonRaw = response.read()
    jsonData = json.loads(jsonRaw)
    result = jsonData['results']
    for loc in result:
        ret = ret + loc['name'] + ':'
        ret = ret + loc['types'][0]

        if loc['types'][0].strip() == "point_of_interest":
            ret = ret + ';'
            continue
        
        for i in range(1, len(loc['types'])):   
            ret = ret + ',' + loc['types'][i]
            if loc['types'][i].strip() == 'point_of_interest':
                break
        ret = ret + ';'
    print ret
    return ret

if __name__ == '__main__':
    main()  