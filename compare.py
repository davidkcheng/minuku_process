import urllib, json

Answer = []
Target = []
Recall = 0;
Precision = 0;

class Trans:
    starttime = 0;
    endtime= 0;
    activity = ""

def readAnswer(filename):
    
    global Answer
    
    input_file = open(filename, 'rU')
    line = input_file.readline()
    
    while line:
        trans = Trans()
        sub = line.split('\t')
    
        trans.starttime = int(sub[0])
        trans.endtime = int(sub[1])
        trans.activity = sub[2]
    
        Answer.append(trans)
        line = input_file.readline()
   
    input_file.close()

def readTarget(filename):
    
    global Target
    
    input_file = open(filename, 'rU')
    line = input_file.readline()
    
    while line:
        trans = Trans()
        sub = line.split('\t')
    
        trans.starttime = int(sub[0])
        trans.endtime = int(sub[1])
        trans.activity = sub[2]
    
        Target.append(trans)
        line = input_file.readline()
    input_file.close()


# def getRecall():
#     global Recall
#     
#     for trans in Answer:
#         
    
def getPrecision():
    global Precision
    
    error = 0;
    total = 0;
    
    for i in range(0, len(Answer)):

#         larger than 10 seconds
        if abs(Answer[i].starttime - Target[i].starttime) > 10000: 
            error = error + abs(Answer[i].starttime - Target[i].starttime)
        if abs(Answer[i].endtime - Target[i].endtime) > 10000:
            error = error + abs(Answer[i].endtime - Target[i].endtime)
    
        total = total + max(Answer[i].endtime - Answer[i].starttime, Target[i].endtime - Target[i].starttime)

def GoogPlac(lat,lng, key):
    #making the url
    AUTH_KEY = key
    LOCATION = str(lat) + "," + str(lng)
#     RADIUS = radius
#     TYPES = types
    MyUrl = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
         '?location=%s'
         '&sensor=false&key=%s') % (LOCATION, AUTH_KEY)
    #grabbing the JSON result
    response = urllib.urlopen(MyUrl)
    jsonRaw = response.read()
    jsonData = json.loads(jsonRaw)
    return jsonData


# https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=42.279532,-83.741024&radius=20&key=AIzaSyDkmJL928g4hLfqECzESks8XdbVNvSsv9Y

def main():
    readAnswer('Answer.txt')
    readTarget('output1.txt')
    getPrecision()
    GoogPlac(42, -85, 'AIzaSyDkmJL928g4hLfqECzESks8XdbVNvSsv9Y')
    
#     print Target[0].starttime


if __name__ == '__main__':
    main()  