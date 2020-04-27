from psychopy import visual, event, sound, core, misc
import random
import numpy as np #python Matlab package



#set global stimuli to None outside of Functions so they can be changed within functions
window = None
int = None
star = None
rect1 = None
circle = None
rect2 = None
incorrect = None
mouse = None
tone = None
clock = None
log_file = None


#initialize stimuli for faster task loading and less buffering
def Initialize ():
    #declare global variable so outside functon window = instide function
    global window
    global mouse
    global int
    global star
    global circle
    global rect1
    global rect2
    global tone
    global incorrect
    global clock
    global trial
    global log_file
    
    #Initialize window
    window = visual.Window( 
        monitor = 'testMonitor', 
        fullscr = True, 
        screen = 0, 
        units = 'deg', 
        color = 'white'
    )
    #initialize initial rect stimuli for instruction screen
    int = visual.Rect(
        window, 
        width = 7, 
        height = 7, 
        units = 'deg', 
        lineWidth = 1.5, 
        lineColorSpace ='rbg', 
        fillColorSpace ='rgb',
        pos = [0,-7], 
        lineColor = 'black', 
        fillColor = None
    )
    
    
    #Initialize Star Stimulus for trial initialization for go and stop
    star = visual.ImageStim(
        window, 
        image = 'Star.jpeg', 
        units ='deg', 
        pos = [-12,-7]
    )
    
    #Initialize rectangle around the star stimulus for boundary purposes
    rect1 = visual.Rect(
        window, 
        width = 7, 
        height = 7, 
        units = 'deg', 
        lineWidth = 1.5, 
        lineColorSpace ='rbg', 
        fillColorSpace ='rgb',
        pos = [-12,-7], 
        lineColor = 'black', 
        fillColor = None
    )
    
    #Initialize Circle Stimulus for action during the trials both go and stop trials
    circle = visual.ImageStim(
        window, 
        image = 'Circle.jpeg', 
        units = 'deg',
        pos = [12,-7]
    )
    
    #Initialize rectangle around circle stimulus for boundary purposes
    rect2 = visual.Rect(
        window, 
        width = 7, 
        height = 7, 
        units = 'deg', 
        lineWidth = 1.5, 
        lineColorSpace ='rbg', 
        fillColorSpace ='rgb',
        pos = [12,-7], 
        lineColor = 'black', 
        fillColor = None
    )
    
    #initialize incorrect response large black rectangle encompassing the whole screen
    incorrect = visual.Rect(
        window, 
        width = 200, 
        height = 200, 
        units = 'deg', 
        fillColorSpace ='rgb', 
        pos = [0,0], 
        fillColor = 'black'
    )

    
    #initialize Tone used as the stop signal during stop trials
    tone = sound.Sound(
        value = 'C', 
        secs = 0.04, 
        octave = 7, 
        sampleRate = None,
        volume = .4
    )
    
    #initialize clock used to time the 2 seconds for the subject to respond in each trial
    clock = core.Clock()
    
    #initialize mouse. used instead of a keyboard beause this was supposed to be done on a touch screen
    mouse = event.Mouse()
    
    
    #create data file
    log_file = open('logfile.csv','a')
    

#Show beginning instructions for the task calls for mouse and int rectangle
def ShowInstructions():
    
    #declare global variable so outside functon window = instide function
    global window
    global mouse
    global int
    
    #create text stimuli for instructions
    ins = visual.TextStim(
        window, 
        height = .5, 
        wrapWidth = 20, 
        color = 'black',
        pos = (0,0)
    )
    
    #instruction text for people reviewing/using this task
    ins.text = "This program was made for animal research using a touch screen. Therefore, If you have a touch screen monitor it would be best to use that. \n \n As quickly as you can, press (or move the mouse over) the stimuli in the order that they are presented. If a black screen appears, that is an indicator that the response was incorrect.\
    \n \n \n Tap or move mouse over the open square to continue."
    
    #while the mouse is not in the rectangle keep presenting the text stimuli
    while not int.contains(mouse):
        ins.draw()
        int.draw()
        window.flip()
    
    
#perform Go trials calls for mouse, circle, star, both rect and incorrect stimuli from Initialize
#uses Trial from RunTrial()
#Output is a trial referred to as Go
def GoTrial():
    #declare global variable so outside functon window = instide function
    global window
    global star
    global circle
    global mouse
    global rect1
    global rect2
    global incorrect
    global clock
    global trial
    global log_file
    
    
    #trials assigned 1 = Go trials
    
    while trial > 0:
        #draw stimli for beginning of go trials
        star.draw()
        rect1.draw()
        window.flip()
        if rect1.contains(mouse):
            #if mouse is present in rect1 the loop breaks and continues
            break
        else:
            #no mouse present in rect1 = stimuli are continuously presented
            continue
            
    #resets mouse position to the center of the screen
    mouse.setPos(newPos=(0,0))
    
    #start with clicked = 0 to be changed later
    clickedg = 0
    
    #clock returned to 0 to allow for timed trial
    clock.reset()
    
    #clock get time would be 0 to allow the circle and rectangle to be presented for 2 seconds
    while clock.getTime () < 2.0:
        #present stimuli while clock.getTime is less than 2 seconds
        circle.draw()
        rect2.draw()
        window.flip()
        if rect2.contains(mouse):
            #if mouse present in rect1 break sequence and move to next trial
            #trial finished when clicked = 1
            clickedg = 1
            #clicked = 1 correct response
            #record the time that the mouse entered the rectangle for correct trials
            RT = clock.getTime()
            #break from the loop and end trial
            break
        else:
            #if mouse not present in rect1 after 2 sec counted as incorrect
            clickedg = 0
            #clicked = 0 incorrect response
            RT = 0
    window.flip()
    
    # if clicked = 0 perform this
    #an incorrect response = 5 secs of black screen
    if clickedg<1:
        #present black screen stimuli
        incorrect.draw()
        window.flip()
        core.wait(5)
    #write the results of the stop signal trial to the log_file
    #writing the binary for the trial go = 1
    #writing the response (clickends) 0 = not clicked (wrong) 1 = clicked (correct)
    #writing time between the beginning of the trial to when the mouse enters the rectangle
    log_file.write("Go Trial:," + str(trial) + "," + str(clickedg) + ',' + f"{RT:.4f}" + "\n")

#define stop tirals as a different function for ease of running the indiviual trials
#stop trials calls for mouse, circle, star, both rect, tione and incorrect stimuli from Initialize
#uses Trial from RunTrial()
#Output is a trial referred to as stop
def StopTrial():
    #declare global variable so outside functon window = instide function
    global window
    global star
    global circle
    global mouse
    global rect1
    global rect2
    global incorrect
    global clock
    global tone
    global trial
    global log_file
    
    #trials assigned 0 = stop trials
    
    while trial < 1:
        #draw stimli for beginning of go trials
        star.draw()
        rect1.draw()
        window.flip()
        if rect1.contains(mouse):
            #if mouse is present in rect1 the loop breaks and continues
            break
        else:
            #no mouse present in rect1 = stimuli are continuously presented
            continue
            
    #Reset mouse position
    mouse.setPos(newPos=(0,0))
    
    #randomly choose a delay time for stop-signal
    #choose randomly from a list
    t = random.choice([.05,.1, .2])
    
    #Set clicked to zero to set clicked variable 
    clickeds = 0
    
    #set playsound variable
    playsound = True
    
    #reset clock to 0 to allow for timing for trial
    clock.reset()
    #clock get time would be 0 to allow the circle and rectangle to be presented for 2 seconds
    while clock.getTime()< 2.0:
        #draw stimuli
        circle.draw()
        rect2.draw()
        #if playsound is true(which it is because it was set true earlier)
        #then continue to this loop
        if playsound:
            #Wait a randomized delay that was chose prior
            core.wait(t)
            #play tone
            tone.play()
            #To stop the tone and make sure it plays only once set playsounds to False
            playsound = False
        window.flip()
        #determine if the mouse enters the boundaries of a rectangle then break from while loop
        if rect2.contains(mouse):
            #if mouse is present in rect1 the loop breaks and continues
            clickeds = 0
            #Clicked variable is 0 indicating an incorrect response
            #get the reaction time for when the mouse enters the rectangle
            RT = clock.getTime()
            break
        else:
            #Clicked indicating that the mouse DID NOT enter the rectangle
            clickeds = 1
            #mouse never entered the rectangle therefore there would be no RT
            RT = 0
    #if clicked = 1 perform this
    #an incorrect response = 5 secs of black screen
    if clickeds <1:
        #present black screen stimuli for incorrect responses for 5 seconds
        incorrect.draw()
        window.flip()
        core.wait(5)
    #write the results of the stop signal trial to the log_file
    #writing the binary for the trial stop = 0
    #writing the response (clickends) 1 = not clicked (correct) 0 = clicked (wrong)
    #writing time between the beginning of the trial to when the mouse enters the rectangle
    #write the randomized delay between the start of the trial and the tone
    log_file.write("Stop Trial:," + str(trial) + "," + str(clickeds)  + "," + f"{RT:.4f}" + "," + str(t) + "\n")

#create the trials for the task using functions for stop trials and go trials.
def RunTask():
    #declare global variable so outside functon window = instide function
    global trial
    global totalTrials
    global log_file
    
    
    #create a list of 0 and 1 to be assigned to the variable trial
    list = (0,1)
    #randomly choose between the list (0 or 1) with weighted value so that 0 get chosen at a magnintude of 20 and 1 = 80
    #K is the number of choices want picked - if K is changed make sure to change trial.count in the following while loop
    trial = random.choices(list, weights = [20,80], k=150)
    #create a new boolian variable to run in a loop
    exp1 = True
    #make sure that the trial list contains an appropriate number of 0 and 1s
    while exp1 == True:
        #if the trial count contains more than 29 0s and more than 119 1s then break from this loop
        #If you change K in trials you must change 29 and 119 to appropriate numbers to make sure stop = 20% and  go = 80% of all trials
        if trial.count (0) > 29 and trial.count(1) > 119:
            exp1 = False
            print(trial)
            break
        else:
            #If the trial count does not contain above then continue to generate trial lists until the above criterion is met
            trial = random.choices(list, weights = [20,80], k=150)
            continue
            
    #create a randomized inter trial interval between presentations of trials
    ITI = random.randrange(2,4)
    
    #actually run the experiment
    #pulling the 0s and 1s from the trial variable
    for trial in trial:
        #determine if trial is greater than 0 perform a gotrial
        if trial>0:
            #perform the go trial function 
            GoTrial()
            #wait the length of the randomized ITI variable
            core.wait(ITI)
        else:
            #If trial is not greater than 0 then perform stop trial dunction
            StopTrial()
            #wait the legnth of the randomied ITI variable
            core.wait(ITI)

#end the task after all trials have been met 
def TerminateTask():
    #declare global variable so outside functon window = instide function
    global window
    global log_file
    #Close the log file
    log_file.close()
    #close the window
    window.close
    #end the clock
    core.quit

#run initialization function
Initialize()
#run the instructions function
ShowInstructions()
#run the task function
RunTask()
#run the termination function
TerminateTask()


#Thanks for coming along for the ride :)
