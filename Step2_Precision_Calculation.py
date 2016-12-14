Answer = []
Output = []
Recall = 0
Precision = 0
framesize = 20

class Trans:
    starttime = 0
    endtime= 0
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
        trans.activity = sub[4].strip()
    
        Answer.append(trans)
        line = input_file.readline()
   
    input_file.close()

def readOutput(filename):
    
    global Output
    
    input_file = open(filename, 'rU')
    line = input_file.readline()
    
    while line:
        trans = Trans()
        sub = line.split('\t')
    
        trans.starttime = int(sub[0])
        trans.endtime = int(sub[1])
        trans.activity = sub[4].strip()
    
        Output.append(trans)
        line = input_file.readline()
    input_file.close()

# get number of correct in Answer divided by total frame in Answer
def getRecall():
    global Recall
    
    correct = 0
    total = 0

    for i in range(0, len(Answer)):
        
        if Answer[i].activity == Output[i].activity:
            currentframe = Answer[i].starttime + framesize*1000
            
            while currentframe < Answer[i].endtime:
                if currentframe > Output[i].starttime and currentframe < Output[i].endtime:
                    correct += 1
                currentframe = currentframe + framesize*1000
                total += 1
#     print correct
#     print total                
    Recall = round((float(correct)/float(total))*100, 2)
#     return Recall
         
    
# get number of correct in Output divided by total frame in Output
def getPrecision(): 
    global Precision
    
    correct = 0
    total = 0

    for i in range(0, len(Output)):
#         print i
        if Output[i].activity == Answer[i].activity:
            currentframe = Output[i].starttime + framesize*1000
            while currentframe < Output[i].endtime:
                if currentframe > Answer[i].starttime and currentframe < Answer[i].endtime:
                    correct += 1
                currentframe = currentframe + framesize*1000
                total += 1
#     print correct
#     print total
    Precision = round((float(correct)/float(total))*100, 2)
#     return Precision


def main():
    readAnswer('Answer.txt')
    readOutput('output1.txt')
    
    getPrecision()
    getRecall()

    print "Precision: " + str(Precision)
    print "Recall: " + str(Recall)

if __name__ == '__main__':
    main()  