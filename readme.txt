Minuku Process is the Python script code that does the the same data processing as Minuku does. By this, we can keep the data processing job from mobile app.

Before running the code
1. make sure the AR.txt file in /logfiles is up-to-date.
2. Please always keep output.txt and output1.txt in the same directory as where the Python's code are.

Then,

1. Run "Step1_Transportation_Identification.py", then the necessary information in AR.txt would be captured into output.txt. At the same time, the transportation data will be summarized into segments and stored in output1.txt
2. Created the Answer.txt from the user generated data (The current Answer.txt is hard-code only for testing)
3. Run "Step2_Precision_Calculation.py", the precision and recall of Minuku's transportation type identification will be printed out 
