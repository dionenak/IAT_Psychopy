from psychopy import core, visual, event, data, gui
import random

# Main experiment loop for practice blocks
def practiceBlock(conditions, keys, stimText, stimImage, win,inform):
    block = data.TrialHandler(conditions,1,extraInfo=inform)
    for trial in block:
        # Show image or text stimulus
        if '.' in trial['stimulus']:
            stimImage.setImage(trial['stimulus'])
            stimImage.draw()
        else:
            stimText.setText(trial['stimulus'])
            stimText.draw()
        win.flip()

        # Capture response
        clock = core.Clock()
        respond = event.waitKeys(keyList=['a', 'l'], timeStamped=clock)
        response, latency = respond[0]
        win.flip()

        # Check if the responce is correct
        if response == keys[trial['group'] ]: # check whether the key pressed matches the dictionary value of the inkcolor, as defined above ^^
            correct = True
        else:
            correct = False

        # Draw an error message if incorrect
        if not correct:
            errorMsg.draw()
            win.flip()
            core.wait(2)
        # Store data
        block.addData('response', response)
        block.addData('latency', latency)
        block.addData('correct', correct)

    return block

# Main experiment loop for target blocks
def targetBlock(conditions, keys, stimText, stimImage, win,inform):
    block = data.TrialHandler(conditions,1,extraInfo=inform)
    for trial in block:
        # Show image or text stimulus
        if '.' in trial['stimulus']:
            stimImage.setImage(trial['stimulus'])
            stimImage.draw()
        else:
            stimText.setText(trial['stimulus'])
            stimText.draw()
        win.flip()

        # Capture response
        clock = core.Clock()
        respond = event.waitKeys(keyList=['a', 'l'], timeStamped=clock)
        response, latency = respond[0]
        win.flip()

        # Check if the responce is correct
        if response == keys[trial['group'] ]: # check whether the key pressed matches the dictionary value of the inkcolor, as defined above ^^
            correct = True
        else:
            correct = False
        # Store data
        block.addData('response', response)
        block.addData('latency', latency)
        block.addData('correct', correct)

    return block


# Start the experiment with subject number, age and gender, record it, save it to a datafile
f = open('demographics.txt', 'a')
info = {'Subject' : 999, 'Age' : 21, 'Gender' : ['Male', 'Female', 'Other']}
dlg = gui.DlgFromDict(dictionary=info, title='experiment')
if dlg.OK:
    subject = info['Subject']
    f.write("{}\t{}\t{}\n".format(subject, info['Age'], info['Gender']))
else:
    subject = 999
f.close()

# Setting conditions for counterbalancing
if subject%2==0:
    counterbalance='A'
else:
    counterbalance='B'
info['Counterbalance'] = counterbalance

# create the conditions files
conditionWords = data.importConditions('words_DionysiaNakou_s1028129.xlsx')
conditionPics = data.importConditions('pics_DionysiaNakou_s1028129.xlsx')
conditionMixed = conditionPics + conditionWords

# Create the window
win = visual.Window(color='black')
# Create the first stim object with the instructions
instr = visual.TextStim(win,height=0.06, wrapWidth=2)
# Create image and a stim object for the trials
stimText = visual.TextStim(win)
stimImage = visual.ImageStim(win,size=[0.7,0.7])
# Create an error message
errorMsg = visual.TextStim(win, 'X', color = 'red')
# Create a second instruction
instr2 = visual.TextStim(win, height=0.05,wrapWidth=2)
instr2.setPos([0,-0.75])
instr2.setAutoDraw(True)

# Create a keymapping for checking if a response is correct.
wordkeys = {'positive': 'a', 'negative': 'l'}
if counterbalance=='A':
    imagekeys = {'animal': 'a', 'insect': 'l'}
else:
    imagekeys = {'insect': 'a', 'animal': 'l'}
mixkeys = wordkeys.copy()
mixkeys.update(imagekeys)

# First block
instr.setText('Categorize the following words into positive and negative.\nPress left (A) for a pleasant and right (L) for an unpleasant.\nPress A to continue.')
instr2.setText('Press left (A) for a positive word and right (L) for a negative word.')
instr.draw()
win.flip()
event.waitKeys(keyList=['a'])
Block1 = practiceBlock(conditionWords, wordkeys, stimText, stimImage, win,info)
Block1.saveAsExcel(fileName='Subject_'+str(subject),appendFile=True, sheetName = 'Practice block with words')

# Second block
if counterbalance=='A':
    instr.setText('Categorize the following pictures into animals and insects.\nPress left (A) for an animal and right (L) for an insect.\nPress A to continue.')
    instr2.setText('Press left (A) for an animal and right (L) for an insect.')
else:
    instr.setText('Categorize the following pictures into animals and insects.\nPress left (A) for an insect and right (L) for an animal.\nPress A to continue.')
    instr2.setText('Press left (A) for an insect and right (L) for an animal')
instr.draw()
win.flip()
event.waitKeys(keyList=['a'])
Block2 = practiceBlock(conditionPics, imagekeys, stimText, stimImage, win,info)
Block2.saveAsExcel(fileName='Subject_'+str(subject),appendFile=True, sheetName = 'Practice block with pictures')

# Third block
if counterbalance=='A':
    instr.setText('Categorize the following words and pictures.\nPress A to continue.')
    instr2.setText('Press left (A) for an animal or a positive word and right (L) for an insect or a negative word .')
else:
    instr.setText('Categorize the following words and pictures.\nPress A to continue.')
    instr2.setText('Press left (A) for an insect or a positive word and right (L) for an animal or a negative word .')
instr.draw()
win.flip()
event.waitKeys(keyList=['a'])
Block3 = targetBlock(conditionMixed, mixkeys, stimText, stimImage, win,info)
Block3.saveAsExcel(fileName='Subject_'+str(subject),appendFile=True,sheetName = 'Target block')

# New keys for category trial and combined trial
if counterbalance=='A':
    imagekeys={'animal': 'l', 'insect': 'a'}
else:
    imagekeys={'insect': 'l', 'animal': 'a'}
mixkeys=wordkeys.copy()
mixkeys.update(imagekeys)

# Fourth block
if counterbalance=='A':
    instr.setText('Categorize the following pictures into animals and insects.\nPress left (A) for an insect and right (L) for an animal.\nPress A to continue.')
    instr2.setText('Press left (A) for an insect and right (L) for an animal.')
else:
    instr.setText('Categorize the following pictures into animals and insects.\nPress left (A) for an animal and right (L) for an insect.\nPress A to continue.')
    instr2.setText('Press left (A) for an animal and right (L) for an insect')
instr.draw()
win.flip()
event.waitKeys(keyList=['a'])
Block4 = practiceBlock(conditionPics, imagekeys, stimText, stimImage, win,info)
Block4.saveAsExcel(fileName='Subject_'+str(subject),appendFile=True,sheetName='Practice block reversed')

# Fifth block
if counterbalance=='A':
    instr.setText('Categorize the following words and pictures.\nPress A to continue.')
    instr2.setText('Press left (A) for an insect or a positive word and right (L) for an animal or a negative word .')
else:
    instr.setText('Categorize the following words and pictures.\nPress A to continue.')
    instr2.setText('Press left (A) for an animal or a positive word and right (L) for an insect and a negative word .')
instr.draw()
win.flip()
event.waitKeys(keyList=['a'])
Block5 = targetBlock(conditionMixed, mixkeys, stimText, stimImage, win,info)
Block5.saveAsExcel(fileName='Subject_'+str(subject),appendFile=True,sheetName='Target block Reversed')

#The end
win.close()
