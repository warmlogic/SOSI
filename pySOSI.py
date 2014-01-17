#!/usr/bin/python

from pyepl.locals import *
# use the random module to randomize the jitter
import random
# use shutil to copy instruction text into data dir
import shutil
import sys
import os

#import pdb
# debug
#pdb.set_trace()

# only add this if there really is a good reason to exclude
# earlier versions. i like 1.0.29 because it adds
# functionality for resetting accumulated timing error
MIN_PYEPL_VERSION = '1.0.29'

############################################################

def _verifyFiles(config):
    """
    Verify that all the files specified in the config are there so
    that there is no random failure in the middle of the experiment.
    
    This will call sys.exit(1) if any of the files are missing.
    """
    
    # make the list of files from the config vars
    files = (config.instruct_intro,
             config.instruct_study_practice,
             config.instruct_study,
             config.instruct_test_practice,
             config.instruct_test,
             config.instruct_getready,
             config.midSessionBreak,
             config.defaultFont)
        
    for f in files:
        if not os.path.exists(f):
            print '\nERROR:\nPath/File does not exist: %s\n\nPlease verify the config.\n' % f
            sys.exit(1)

    # Sanity checks: make sure the stimulus numbers are equal
    #
    # practice: listLen and recogTargets
    # if config.pracstudy_listLen != (config.practest_numTargets_Left + config.practest_numTargets_Right):
    #     print '\nERROR:\nNumber of study and target stimuli needs to match\npracstudy_listLen = %d, practest_numTargets_Left = %d, practest_numTargets_Right = %d' % (config.pracstudy_listLen,config.practest_numTargets_Left,config.practest_numTargets_Right)
    #     sys.exit(1)
    # practice: listLen and recogLures
    # if config.pracstudy_listLen != config.practest_numLures:
    #     print '\nERROR:\nNumber of study and lure stimuli needs to match\npracstudy_listLen = %d, practest_numLures = %d' % (config.pracstudy_listLen,config.practest_numLures)
    #     sys.exit(1)

    # exp: listLen and recogTargets
    # if config.study_listLen != (config.test_numTargets_Left + config.test_numTargets_Right):
    #     print '\nERROR:\nNumber of study and target stimuli needs to match\nlistLen = %d, test_numTargets_Left = %d, test_numTargets_Right = %d' % (config.study_listLen,config.test_numTargets_Left,config.test_numTargets_Right)
    #     sys.exit(1)
    # exp: listLen and recogLures
    # if config.study_listLen != config.test_numLures:
    #     print '\nERROR:\nNumber of study and lure stimuli needs to match\nlistLen = %d, test_numLures = %d' % (config.study_listLen,config.test_numLures)
    #     sys.exit(1)

############################################################

def _prepare(exp, config):
    """
    Set everything up before we try and run.
    """

    # verify that we have all the files
    _verifyFiles(config)

    # get the state
    state = exp.restoreState()

    random.seed()

#     # get the subject number so we can counterbalance the keys

#     # study:
#     # subjects ending in an odd number
#     # subjects ending in an even number
#     # subject ending in 1-5
#     # subject ending in 6-0

#     # test:
#     # subject ending in 1-5 get 'old' on left, 'new' on right;
#     # subject ending in 6-0 get 'new' on left, 'old' on right;

    expName = config.expName

    # make sure the subject number was formatted correctly
    subNum_orig = exp.getOptions()['subject']
    subNum = subNum_orig.strip(expName)
    if len(subNum) != 3:
        print '\nERROR:\nSubject number was not entered correctly. This is what was entered: %s.\nSubject number must be formatted like this: experiment abbreviation (%s) followed by 3 numbers with no spaces (e.g., %s001).\nDelete the ./data/%s folder and try again; to do this, copy and paste this command in the terminal, then press return: rm -r data/%s.\n' % (subNum_orig,expName,expName,subNum_orig,subNum_orig)
        sys.exit(1)
    
    if int(subNum[-1]) % 2 == 1:
        isodd = True
    elif int(subNum[-1]) % 2 == 0:
        isodd = False
    
    if int(subNum[-1]) > 0 and int(subNum[-1]) <= 5:
        is15 = True
    elif  int(subNum[-1]) == 0 or int(subNum[-1]) > 5:
        is15 = False


    # set up the keys and coords
    keys = {}
    coords = {}
    coords['mid_coord'] = config.mid_coord
    coords['left_coord'] = config.left_coord
    coords['right_coord'] = config.right_coord
    coords['bot_coord'] = config.bot_coord
    coords['fback_coord'] = config.fback_coord

    coords['test_source_left_x'] = config.test_source_left_x
    coords['test_source_right_x'] = config.test_source_right_x
    
    if is15:
        keys['sourceLeftKey_test'] = config.leftKeys_test[0]
        keys['sourceRightKey_test'] = config.rightKeys_test[0]
        keys['newKey_test'] = config.rightKeys_test[1]

        coords['test_new_x'] = config.test_new_x[1]

        keys['rsKey_test'] = keys['sourceLeftKey_test']
        keys['roKey_test'] = keys['sourceRightKey_test']
        keys['kKey_test'] = keys['newKey_test']
        
        coords['test_rs_x'] = config.test_rs_x[1]
        coords['test_ro_x'] = config.test_ro_x[1]
        coords['test_k_x'] = config.test_k_x[1]
    else:
        keys['newKey_test'] = config.leftKeys_test[0]
        keys['sourceLeftKey_test'] = config.leftKeys_test[1]
        keys['sourceRightKey_test'] = config.rightKeys_test[1]
        
        coords['test_new_x'] = config.test_new_x[0]

        keys['kKey_test'] = keys['newKey_test']
        keys['roKey_test'] = keys['sourceLeftKey_test']
        keys['rsKey_test'] = keys['sourceRightKey_test']
        
        coords['test_k_x'] = config.test_k_x[0]
        coords['test_ro_x'] = config.test_ro_x[0]
        coords['test_rs_x'] = config.test_rs_x[0]
    
    if isodd:
        keys['sureKey_test'] = keys['sourceLeftKey_test']
        keys['maybeKey_test'] = keys['sourceRightKey_test']
        
        coords['test_sure_x'] = config.test_sure_x[0]
        coords['test_maybe_x'] = config.test_maybe_x[0]
    else:
        keys['maybeKey_test'] = keys['sourceLeftKey_test']
        keys['sureKey_test'] = keys['sourceRightKey_test']
        
        coords['test_sure_x'] = config.test_sure_x[1]
        coords['test_maybe_x'] = config.test_maybe_x[1]

    # grab all instruction files
    instruct_intro = open(config.instruct_intro,'r').read()
    instruct_study_practice = open(config.instruct_study_practice,'r').read()
    instruct_study = open(config.instruct_study,'r').read()
    instruct_test_practice = open(config.instruct_test_practice,'r').read()
    instruct_test = open(config.instruct_test,'r').read()

    # set up the test text
    if keys['sourceRightKey_test'] == '.':
        sourceRightKey_str = 'Period'
    else:
        sourceRightKey_str = keys['sourceRightKey_test']
    if keys['roKey_test'] == '.':
        roKey_str = 'Period'
    else:
        roKey_str = keys['roKey_test']
    if keys['sureKey_test'] == '.':
        sureKey_str = 'Period'
    else:
        sureKey_str = keys['sureKey_test']
    if keys['maybeKey_test'] == '.':
        maybeKey_str = 'Period'
    else:
        maybeKey_str = keys['maybeKey_test']
    # text
    instruct_test_practice = str.replace(instruct_test_practice,'sourceLeftText_test',config.sourceLeftText_test)
    instruct_test_practice = str.replace(instruct_test_practice,'sourceRightText_test',config.sourceRightText_test)
    instruct_test_practice = str.replace(instruct_test_practice,'newText_test',config.newText_test)
    instruct_test_practice = str.replace(instruct_test_practice,'rememSourceText_test',config.rememSourceText_test)
    instruct_test_practice = str.replace(instruct_test_practice,'rememOtherText_test',config.rememOtherText_test)
    instruct_test_practice = str.replace(instruct_test_practice,'knowText_test',config.knowText_test)
    instruct_test_practice = str.replace(instruct_test_practice,'sureText_test',config.sureText_test)
    instruct_test_practice = str.replace(instruct_test_practice,'maybeText_test',config.maybeText_test)
    # keys
    instruct_test_practice = str.replace(instruct_test_practice,'sourceLeftKey_test',keys['sourceLeftKey_test'])
    instruct_test_practice = str.replace(instruct_test_practice,'sourceRightKey_test',sourceRightKey_str)
    instruct_test_practice = str.replace(instruct_test_practice,'newKey_test',keys['newKey_test'])
    instruct_test_practice = str.replace(instruct_test_practice,'rsKey_test',keys['rsKey_test'])
    instruct_test_practice = str.replace(instruct_test_practice,'roKey_test',roKey_str)
    instruct_test_practice = str.replace(instruct_test_practice,'kKey_test',keys['kKey_test'])
    instruct_test_practice = str.replace(instruct_test_practice,'sureKey_test',sureKey_str)
    instruct_test_practice = str.replace(instruct_test_practice,'maybeKey_test',maybeKey_str)

    # text
    instruct_test = str.replace(instruct_test,'sourceLeftText_test',config.sourceLeftText_test)
    instruct_test = str.replace(instruct_test,'sourceRightText_test',config.sourceRightText_test)
    instruct_test = str.replace(instruct_test,'newText_test',config.newText_test)
    instruct_test = str.replace(instruct_test,'rememSourceText_test',config.rememSourceText_test)
    instruct_test = str.replace(instruct_test,'rememOtherText_test',config.rememOtherText_test)
    instruct_test = str.replace(instruct_test,'knowText_test',config.knowText_test)
    instruct_test = str.replace(instruct_test,'sureText_test',config.sureText_test)
    instruct_test = str.replace(instruct_test,'maybeText_test',config.maybeText_test)
    # keys
    instruct_test = str.replace(instruct_test,'sourceLeftKey_test',keys['sourceLeftKey_test'])
    instruct_test = str.replace(instruct_test,'sourceRightKey_test',sourceRightKey_str)
    instruct_test = str.replace(instruct_test,'newKey_test',keys['newKey_test'])
    instruct_test = str.replace(instruct_test,'rsKey_test',keys['rsKey_test'])
    instruct_test = str.replace(instruct_test,'roKey_test',roKey_str)
    instruct_test = str.replace(instruct_test,'kKey_test',keys['kKey_test'])
    instruct_test = str.replace(instruct_test,'sureKey_test',sureKey_str)
    instruct_test = str.replace(instruct_test,'maybeKey_test',maybeKey_str)
    
    # write the instructions text into the data directory for this
    # session, so that you can refer to it later if you need to
    instruct_gen = {}
    inst_path_find = 'text'
    inst_path_replace = 'instruct'
    # create the directory to store the instructions in
    filePath_eeg = exp.session.fullPath()+os.path.join(inst_path_replace,'eeg')
    filePath_beh = exp.session.fullPath()+os.path.join(inst_path_replace,'beh')
    if not os.path.exists(filePath_eeg):
        os.makedirs(filePath_eeg)
    if not os.path.exists(filePath_beh):
        os.makedirs(filePath_beh)
    #######################
    instruct_gen['inst_intro_path'] = exp.session.fullPath()+str.replace(config.instruct_intro,inst_path_find,inst_path_replace)
    inst_intro = open(instruct_gen['inst_intro_path'], 'w')
    inst_intro.write(instruct_intro)
    inst_intro.close()
    #######################
    instruct_gen['inst_stud_prac_path'] = exp.session.fullPath()+str.replace(config.instruct_study_practice,inst_path_find,inst_path_replace)
    inst_stud_prac = open(instruct_gen['inst_stud_prac_path'], 'w')
    inst_stud_prac.write(instruct_study_practice)
    inst_stud_prac.close()
    ###########################
    instruct_gen['inst_test_prac_path'] = exp.session.fullPath()+str.replace(config.instruct_test_practice,inst_path_find,inst_path_replace)
    inst_test_prac = open(instruct_gen['inst_test_prac_path'], 'w')
    inst_test_prac.write(instruct_test_practice)
    inst_test_prac.close()
    ########################
    instruct_gen['inst_stud_path'] = exp.session.fullPath()+str.replace(config.instruct_study,inst_path_find,inst_path_replace)
    inst_stud = open(instruct_gen['inst_stud_path'], 'w')
    inst_stud.write(instruct_study)
    inst_stud.close()
    #######################
    instruct_gen['inst_test_path'] = exp.session.fullPath()+str.replace(config.instruct_test,inst_path_find,inst_path_replace)
    inst_test = open(instruct_gen['inst_test_path'], 'w')
    inst_test.write(instruct_test)
    inst_test.close()
    
    # get the image pool
    objstim = ImagePool(config.objectStimuli,config.PICTURE_SIZE)
    #objstimtxt = TextPool(config.objectStimuliTxt)
    objbuff = ImagePool(config.objectBuffers,config.PICTURE_SIZE)
    #objbufftxt = TextPool(config.objectBuffersTxt)
    
    # Shuffle the stimulus pool
    objstim.shuffle()
    # Shuffle the buffers
    objbuff.shuffle()
    
    # copy object text pool to sessions dir
    #shutil.copy(config.objectStimuliTxt,exp.session.fullPath())
    #shutil.copy(config.objectBuffersTxt,exp.session.fullPath())
    
    # possible coords for stims
    possibleXCoords = [coords['left_coord'],coords['right_coord']]
    possibleYCoords = [coords['mid_coord']]

    sliceStim = 0
    sliceBuff = 0

    sesStudyLists = []
    sesTargLists = []
    sesLureLists = []

    pracStudyLists = []
    pracTargLists = []
    pracLureLists = []

    # set up each session
    for sessionNum in range(config.numSessions):
        # Set the session so that we know the correct directory
        exp.setSession(sessionNum)

        # Get the session-specific config
        sessionconfig = config.sequence(sessionNum)

        trialStudyLists = []
        trialTargLists = []
        trialLureLists = []
        
        if sessionNum == 0:
            # set up the practice list, if we have one
            if sessionconfig.practiceList:
                isPractice = True
                
                for prac_listNum in range(sessionconfig.prac_numLists):
                    
                    listconfig = sessionconfig.sequence(prac_listNum)
                    
                    # -------------- Create prac study stimuli --------------

                    pracStudyLists,sliceBuff,sliceStim = createStudyList(state,config,
                                                                         objbuff,objstim,
                                                                         sliceBuff,sliceStim,
                                                                         pracStudyLists,
                                                                         listconfig.pracstudy_bufferStart,listconfig.pracstudy_bufferEnd,listconfig.pracstudy_listLen,
                                                                         prac_listNum,isPractice,
                                                                         possibleYCoords,possibleXCoords,
                                                                         coords)

                    # -------------- Create prac test stimuli --------------

                    pracTargLists,pracLureLists,sliceStim = createTestList(state,config,
                                                                           objstim,sliceStim,
                                                                           pracTargLists,pracLureLists,
                                                                           listconfig.pracstudy_bufferStart,listconfig.pracstudy_listLen,listconfig.practest_numLures,
                                                                           pracStudyLists,prac_listNum,isPractice,
                                                                           coords)
                
        # set up each list
        isPractice = False
        for listNum in range(sessionconfig.numLists):

            # Get the list specific config
            listconfig = sessionconfig.sequence(listNum)

            # -------------- Create expt study stimuli -------------------

            trialStudyLists,sliceBuff,sliceStim = createStudyList(state,config,
                                                                  objbuff,objstim,
                                                                  sliceBuff,sliceStim,
                                                                  trialStudyLists,
                                                                  listconfig.study_bufferStart,listconfig.study_bufferEnd,listconfig.study_listLen,
                                                                  listNum,isPractice,
                                                                  possibleYCoords,possibleXCoords,
                                                                  coords)
            
            # -------------- Create expt test stimuli -------------------
            
            trialTargLists,trialLureLists,sliceStim = createTestList(state,config,
                                                                     objstim,sliceStim,
                                                                     trialTargLists,trialLureLists,
                                                                     listconfig.study_bufferStart,listconfig.study_listLen,listconfig.test_numLures,
                                                                     trialStudyLists,listNum,isPractice,
                                                                     coords)

        # append the lists to the session
        sesStudyLists.append(trialStudyLists)
        sesTargLists.append(trialTargLists)
        sesLureLists.append(trialLureLists)

    # save the prepared data
    exp.saveState(state,
                  coords = coords,
                  keys = keys,
                  instruct_gen = instruct_gen,
                  listNum=0,
                  sessionNum=0,
                  sesStudyLists=sesStudyLists,
                  sesTargLists=sesTargLists,
                  sesLureLists=sesLureLists,
                  pracStudyLists=pracStudyLists,
                  pracTargLists=pracTargLists,
                  pracLureLists=pracLureLists,
                  practiceDone = 0,
                  studyDone = 0)

##############################################################

# code modified from:
# http://code.activestate.com/recipes/500268-all-k-subsets-from-an-n-set/

def k_subsets_i(n, k):
    '''
    Yield each subset of size k from the set of intergers 0 .. n - 1
    n -- an integer > 0
    k -- an integer > 0
    '''
    # Validate args
    if n < 0:
        raise ValueError('n must be > 0, got n=%d' % n)
    if k < 0:
        raise ValueError('k must be > 0, got k=%d' % k)
    # check base cases
    if k == 0 or n < k:
        yield set()
    elif n == k:
        yield set(range(n))

    else:
        # Use recursive formula based on binomial coeffecients:
        # choose(n, k) = choose(n - 1, k - 1) + choose(n - 1, k)
        for s in k_subsets_i(n - 1, k - 1):
            s.add(n - 1)
            yield s
        for s in k_subsets_i(n - 1, k):
            yield s

def k_subsets(s, k):
    '''
    Yield all subsets of size k from set (or list) s
    s -- a set or list (any iterable will suffice)
    k -- an integer > 0
    '''
    s = list(s)
    n = len(s)
    sets = []
    for k_set in k_subsets_i(n, k):
        sets.append([s[i] for i in k_set])
    return sets

##############################################################

def repeatChange(stims,dictKey,maxCount):
    """
    Check for repeats of a particular dictKey:value in a list of
    dictionaries and change the values so that only a certain number
    of items (maxCount) with the same dictKey:value are next to each
    other.  The number of items with each value stays the same.
    """

    allCats = []
    for eachStim in range(len(stims)):
        allCats.append(stims[eachStim].get(dictKey))

    cats = list(set(allCats))
    for eachStim in range(len(stims)):
        if eachStim == 0:
            catType = stims[eachStim].get(dictKey)
            counter = 1
        elif eachStim > 0:
            if stims[eachStim].get(dictKey) == catType:
                counter += 1
                if counter > maxCount:
                    replacementCats = []
                    for possCats in range(len(cats)):
                        if cats[possCats] != catType:
                            replacementCats.append(cats[possCats])
                    replaceCat = random.choice(replacementCats)
                    stims[eachStim][dictKey] = replaceCat
                    # find a replaceCat stim to replace with catType
                    replaced = 0
                    for restStim in range(eachStim+1,len(stims)):
                        if stims[restStim].get(dictKey) == replaceCat:
                            stims[restStim][dictKey] = catType
                            replaced = 1
                            break
                    if replaced != 1:
                        # if we didn't find one, start at the beginning
                        for beginStim in range(len(stims)):
                            if stims[beginStim].get(dictKey) == replaceCat:
                                stims[beginStim][dictKey] = catType
                                replaced = 1
                                break
                    if replaced == 1:
                        catType = stims[eachStim].get(dictKey)
                        counter = 1
            elif stims[eachStim].get(dictKey) != catType:
                catType = stims[eachStim].get(dictKey)
                counter = 1

    # # check the stims again
    # for eachStim in range(len(stims)):
    #     if eachStim == 0:
    #         catType = stims[eachStim].get(dictKey)
    #         counter = 1
    #     elif eachStim > 0:
    #         if stims[eachStim].get(dictKey) == catType:
    #             counter += 1
    #         elif stims[eachStim].get(dictKey) != catType:
    #             catType = stims[eachStim].get(dictKey)
    #             counter = 1
    
    if counter <= maxCount:
        #print 'repeatChange success'
        return stims
    elif counter > maxCount:
        #print 'repeatChange failure'
        return repeatChange(stims,dictKey,maxCount)

############################################################

def repeatSwap(stims,dictKey,maxCount):
    """
    Check for repeats of a particular dictKey:value in a list of
    dictionaries and move the items around so that only a certain
    number of items (maxCount) with the same dictKey:value are next to
    each other
    """

    for eachStim in range(len(stims)):
        if eachStim == 0:
            catType = stims[eachStim].get(dictKey)
            counter = 1
        elif eachStim > 0:
            if stims[eachStim].get(dictKey) == catType:
                counter += 1
                if counter > maxCount:
                    replacementStim = []
                    for restStim in range(eachStim,len(stims)):
                        # look for a valid stim to insert
                        if stims[restStim].get(dictKey) != catType:
                            replacementStim = stims[restStim]
                            stims.remove(stims[restStim])
                            stims.insert(eachStim,replacementStim)
                            catType = stims[eachStim].get(dictKey)
                            counter = 1
                            break
                    if not replacementStim:
                        # if we didn't find one, start at the beginning
                        for beginStim in range(len(stims)):
                            if stims[beginStim].get(dictKey) != catType:
                                replacementStim = stims[beginStim]
                                stims.remove(stims[beginStim])
                                stims.insert(eachStim,replacementStim)
                                catType = stims[eachStim].get(dictKey)
                                counter = 1
                                break
            elif stims[eachStim].get(dictKey) != catType:
                catType = stims[eachStim].get(dictKey)
                counter = 1
    
    # # check the stims again
    # for eachStim in range(len(stims)):
    #     if eachStim == 0:
    #         catType = stims[eachStim].get(dictKey)
    #         counter = 1
    #     elif eachStim > 0:
    #         if stims[eachStim].get(dictKey) == catType:
    #             counter += 1
    #         elif stims[eachStim].get(dictKey) != catType:
    #             catType = stims[eachStim].get(dictKey)
    #             counter = 1

    if counter <= maxCount:
        #print 'repeatSwap success'
        return stims
    elif counter > maxCount:
        #print 'repeatSwap failure'
        return repeatSwap(stims,dictKey,maxCount)

############################################################

def fixed_delay_with_keybeep(config,state,duration,bc,video,clock):
    '''Beep if a specified key is hit during the duration'''

    # keep it up for desired time
    startTime = clock.get()
    endTime = startTime + duration

    # get response
    button,bc_time = bc.waitWithTime(minDuration = None,
                                     maxDuration = duration,
                                     clock=clock)

    if button is not None:
        if config.playAudio:
            config.errorBeep.present()
        errshown = video.showProportional(config.fastStim,state.coords['mid_coord'],state.coords['fback_coord'])
        video.updateScreen()  # no clock needed b/c we want it now

        clock.delay(endTime-bc_time[0])
        
        video.unshow(errshown)
        video.updateScreen(clock)
        return (button,bc_time)
    else:
        return (button,bc_time)

############################################################

def countdown_with_interrupt(config,state,duration,bc,video,clock):
    '''Show a countdown timer; return if a specified key is hit;
    return after specified amount of time has passed'''

    seconds = duration/1000
    while seconds >= 0:
        time = Text('%d' % seconds,size=config.instruct_wordHeight,color='red')
        timeshown = video.showProportional(time, state.coords['mid_coord'], state.coords['fback_coord'])
        video.updateScreen()
        button,bc_time = bc.waitWithTime(minDuration = None,
                                         maxDuration = 1000,
                                         clock=clock)
        if button is None:
            video.unshow(timeshown)
            video.updateScreen(clock)
            seconds -= 1
        elif button is not None:
            if button.name == config.endImpedanceKey:
                seconds = duration/1000
                video.unshow(timeshown)
                video.updateScreen(clock)
            elif button.name == config.ILI_key:
                video.unshow(timeshown)
                video.updateScreen(clock)
                return (bc_time)
    else:
        return (clock.get())

############################################################

def createStudyList(state,config,
                    objbuff,objstim,
                    sliceBuff,sliceStim,
                    studyLists,
                    study_bufferStart,study_bufferEnd,study_listLen,
                    listNum,isPractice,
                    possibleYCoords,possibleXCoords,
                    coords):
    
    # -------------- Start create study stimuli -------------------

    maxCount = 3

    # slice the list - buffer start
    studyBuffStart = objbuff[sliceBuff:sliceBuff+study_bufferStart]
    # update the slice start - number of buffers at start
    sliceBuff += study_bufferStart

    # add info for each buffer in this list
    for eachStim in range(len(studyBuffStart)):
        if isPractice:
            studyBuffStart[eachStim]['itemType_study'] = 'PRACTICE_STUDY_BUFFER'
        else:
            studyBuffStart[eachStim]['itemType_study'] = 'STUDY_BUFFER'
        studyBuffStart[eachStim]['isTarget'] = 0
        # y-coord: put in the height coord
        studyBuffStart[eachStim]['y_coord'] = possibleYCoords[0]
        # x-coord: put in the horiz coord
        studyBuffStart[eachStim]['x_coord'] = random.choice(possibleXCoords)
        
    # shuffle the start buffers
    studyBuffStart.shuffle()
    # make sure there aren't more than maxCount of a particular x-coord in a row
    studyBuffStart = repeatSwap(studyBuffStart,'x_coord',maxCount)
    # put the start buffers in the study list
    studyList = studyBuffStart[:]

    # slice the list - study stimuli
    studyStim = objstim[sliceStim:sliceStim+study_listLen]
    # update the slice start - number of study stimuli
    sliceStim += study_listLen

    # add info for each stimulus in this list: item
    # status, coords (half left, half right)
    for eachStim in xrange(len(studyStim)/2):
        if isPractice:
            studyStim[eachStim]['itemType_study'] = 'PRACTICE_STUDY_TARGET'
        else:
            studyStim[eachStim]['itemType_study'] = 'STUDY_TARGET'
        studyStim[eachStim]['isTarget'] = 1
        # y-coord
        studyStim[eachStim]['y_coord'] = possibleYCoords[0]
        # x-coord: half left
        studyStim[eachStim]['x_coord'] = possibleXCoords[0]
    for eachStim in range(len(studyStim)/2,len(studyStim)):
        if isPractice:
            studyStim[eachStim]['itemType_study'] = 'PRACTICE_STUDY_TARGET'
        else:
            studyStim[eachStim]['itemType_study'] = 'STUDY_TARGET'
        studyStim[eachStim]['isTarget'] = 1
        # y-coord
        studyStim[eachStim]['y_coord'] = possibleYCoords[0]
        # x-coord: half right
        studyStim[eachStim]['x_coord'] = possibleXCoords[1]
    
    # shuffle the study stims
    studyStim.shuffle()
    # make sure there aren't more than maxCount of a particular x-coord in a row
    studyStim = repeatSwap(studyStim,'x_coord',maxCount)
    # put the stims in the study list
    studyList.extend(studyStim)

    # slice the list - buffer end
    studyBuffEnd = objbuff[sliceBuff:sliceBuff+study_bufferEnd]
    # update the slice start - number of buffers at end
    sliceBuff += study_bufferEnd

    # add info for each buffer in this list
    for eachStim in range(len(studyBuffEnd)):
        if isPractice:
            studyBuffEnd[eachStim]['itemType_study'] = 'PRACTICE_STUDY_BUFFER'
        else:
            studyBuffEnd[eachStim]['itemType_study'] = 'STUDY_BUFFER'
        studyBuffEnd[eachStim]['isTarget'] = 0
        # y-coord
        studyBuffEnd[eachStim]['y_coord'] = possibleYCoords[0]
        # x-coord
        studyBuffEnd[eachStim]['x_coord'] = random.choice(possibleXCoords)

    # shuffle the end buffers
    studyBuffEnd.shuffle()
    # make sure there aren't more than maxCount of a particular x-coord in a row
    studyBuffEnd = repeatSwap(studyBuffEnd,'x_coord',maxCount)
    # put the end buffers in the study list
    studyList.extend(studyBuffEnd)

    # add the study serial position
    for n in range(len(studyList)):
        studyList[n]['ser_pos'] = n+1

    # save the study list
    studyLists.append(studyList)

    # -------------- End create study stimuli -------------------

    # write out the entire study list (including buffers) to file
    if isPractice:
        prefix = 'p'
    else:
        prefix = ''
    studyListFile = exp.session.createFile('%ss%d.lst' % (prefix,listNum))
    for eachStim in studyBuffStart:
        studyListFile.write('%s\t%s\n' %
                            (getattr(eachStim,config.presentationAttribute),
                            eachStim.itemType_study))
    for eachStim in studyStim:
        studyListFile.write('%s\t%s\n' %
                            (getattr(eachStim,config.presentationAttribute),
                            eachStim.itemType_study))
    for eachStim in studyBuffEnd:
        studyListFile.write('%s\t%s\n' %
                            (getattr(eachStim,config.presentationAttribute),
                            eachStim.itemType_study))
    studyListFile.close()

    return (studyLists,sliceBuff,sliceStim)

############################################################

def createTestList(state,config,
                   objstim,sliceStim,
                   targLists,lureLists,
                   study_bufferStart,study_listLen,test_numLures,
                   studyLists,listNum,isPractice,
                   coords):
    
    # -------------- Start create test stimuli -------------------
    
    # get the list that we want the targets from
    studyList_old = studyLists[listNum]
    # get only the targets (exclude the buffers)
    studyStim = studyList_old[study_bufferStart:(study_bufferStart+study_listLen)]

    targetsAll = studyStim[:]
    # sort the targets by assigned side coordinate
    targetsAll.sortBy('x_coord')

    # Left coord targets are the first half of targets
    targetsL = targetsAll[:len(targetsAll)/2]
    targetsL.shuffle()
    # get the number of left targets that we want for recog test
    targetsL = targetsL[:config.test_numTargets_Left]
    
    # Right coord targets are the second half of targets
    targetsR = targetsAll[len(targetsAll)/2:]
    targetsR.shuffle()
    # get the number of right targets that we want for recog test
    targetsR = targetsR[:config.test_numTargets_Right]

    # put the L and R test stims together
    targetsAll = targetsL[:]
    targetsAll.extend(targetsR)
    
    for eachStim in range(len(targetsAll)):
        if isPractice:
            targetsAll[eachStim]['itemType_test'] = 'PRACTICE_TEST_TARGET'
        else:
            targetsAll[eachStim]['itemType_test'] = 'TEST_TARGET'
    
    # shuffle the targ stims
    targetsAll.shuffle()

    targLists.append(targetsAll)

    # slice the list - lure stimuli
    lures = objstim[sliceStim:sliceStim+test_numLures]
    # update the slice start - number of lure test stimuli
    sliceStim += test_numLures

    # put in the -1s denoting that lures don't get this info
    for eachStim in range(len(lures)):
        if isPractice:
            lures[eachStim]['itemType_test'] = 'PRACTICE_TEST_LURE'
        else:
            lures[eachStim]['itemType_test'] = 'TEST_LURE'
        lures[eachStim]['ser_pos'] = -1
        lures[eachStim]['isTarget'] = 0
        # lures didn't have a presenation side
        lures[eachStim]['x_coord'] = -1
        lures[eachStim]['y_coord'] = -1

    # shuffle the lure stims
    lures.shuffle()
    
    # then append all the lures
    lureLists.append(lures)

    # -------------- End create test stimuli -------------------

    # write the targets out to file
    if isPractice:
        prefix = 'p'
    else:
        prefix = ''
    targListFile = exp.session.createFile('%st%d.lst' % (prefix,listNum))
    for eachStim in targetsAll:
        targListFile.write('%s\t%s\n' %
                           (getattr(eachStim,config.presentationAttribute),
                            eachStim.itemType_test))
    targListFile.close()

    # write the lures out to file
    lureListFile = exp.session.createFile('%sl%d.lst' % (prefix,listNum))
    for eachStim in lures:
        lureListFile.write('%s\t%s\n' %
                           (getattr(eachStim,config.presentationAttribute),
                            eachStim.itemType_test))
    lureListFile.close()

    return (targLists,lureLists,sliceStim)

############################################################

def study_trial(exp,config,clock,log,video,audio,thisStudyList,isExperiment):
    """
    Run a trial that consists of presenting study and test
    stimuli. Only log if isExperiment == True.
    """
    # get the state
    state = exp.restoreState()

    # set up the button chooser for the study period
    #bc_studyResp = ButtonChooser(*map(Key,config.study_keys))
    
    # set up orienting fixation cross
    orientCross = Text(config.orientText,size=config.fixation_wordHeight)
    
    #imageDims = thisStudyList[0].content.getSize()
    #screenRes = video.getResolution()
    #noiseprop = imageDims[1] / screenRes[1]
    
    noisestim = ImagePool(config.noiseStimuli,config.PICTURE_SIZE)

    # ------------------- start study ---------------------

    if isExperiment:
        if config.ILI_timer:
            bc_ILI = ButtonChooser(Key(config.ILI_key),Key(config.endImpedanceKey))
            # put the text on the screen
            studyshown = video.showProportional(Text(config.studyBeginText % (state.listNum + 1)), state.coords['mid_coord'], state.coords['mid_coord'])
            video.updateScreen()
            # do a countdown so they wait the same amount of time
            timestamp = countdown_with_interrupt(config,state,config.ILI_dur,bc_ILI,video,clock)
            video.unshow(studyshown)
            video.updateScreen(clock)
        else:
            timestamp = waitForAnyKey(clock,Text(config.studyBeginText % (state.listNum + 1)))
        log.logMessage('STUDY_BEGIN_KEYHIT',timestamp)
    else:
        if config.ILI_timer:
            bc_ILI = ButtonChooser(Key(config.ILI_key),Key(config.endImpedanceKey))
            # put the text on the screen
            studyshown = video.showProportional(Text(config.studyPracBeginText), state.coords['mid_coord'], state.coords['mid_coord'])
            video.updateScreen()
            # do a countdown so they wait the same amount of time
            timestamp = countdown_with_interrupt(config,state,config.ILI_dur,bc_ILI,video,clock)
            video.unshow(studyshown)
            video.updateScreen(clock)
        else:
            timestamp = waitForAnyKey(clock,Text(config.studyPracBeginText))
        log.logMessage('PRACTICE_STUDY_BEGIN_KEYHIT',timestamp)

    # log the start of the trial
    if isExperiment:
        log.logMessage('STUDY_START')
    else:
        log.logMessage('PRACTICE_STUDY_START')

    # put up the "get ready" text
    timestamp = flashStimulus(Text(config.textAfterBlink,size=config.instruct_wordHeight),clk=clock,duration=config.pauseAfterBlink)
    # pause again so there is a blank screen before the
    # stims start again
    clock.delay(config.pauseAfterBlink)
    clock.wait()

    # show the noise stimuli
    noiseL = video.showProportional(noisestim[0].content, state.coords['left_coord'], state.coords['mid_coord'])
    noiseR = video.showProportional(noisestim[0].content, state.coords['right_coord'], state.coords['mid_coord'])

    # display the orienting fixation cross-hairs and leave it on the
    # screen until later
    orientShown = video.showProportional(orientCross, state.coords['mid_coord'], state.coords['mid_coord'])

    # actually put fixation cross and noise pics on the screen
    video.updateScreen(clock)

    # log the flash
    log.logMessage('ORIENT_ON')

    # pause before study so they can finish blinking; orienting cross
    # and noise stim are on screen here
    clock.delay(config.study_preStimDelay, config.study_preStimJitter)
    clock.wait()

    # start them study images
    for n, eachImage in enumerate(thisStudyList):
        # EEG: put in blink resting periods
        if isExperiment:
            # if we're part way through, not on the first list, and
            # not on the last list
            if config.isEEG and (n+1) % (len(thisStudyList)/(config.study_blinkBreaksPerList+1)) == 0 and (n+1) != 1 and (n+1) != len(thisStudyList) and (len(thisStudyList) - (n+1)) > 6:
                # delay before break; fixation cross and noise stim
                # are on screen here
                clock.delay(config.study_ISI,config.study_ISIJitter)
                clock.wait()
                # take the stuff off the screen
                video.unshow(noiseL)
                video.unshow(noiseR)
                video.unshow(orientShown)
                video.updateScreen(clock)
                log.logMessage('ORIENT_OFF')
                # log resting and wait for a key
                log.logMessage('BLINK_REST_START')
                timestamp = waitForAnyKey(clock,Text(config.blinkRestText_study,size=config.instruct_wordHeight))
                log.logMessage('BLINK_REST_KEYHIT',timestamp)
                # pause after blinking
                clock.delay(config.pauseAfterBlink)
                clock.wait()
                timestamp = flashStimulus(Text(config.textAfterBlink,size=config.instruct_wordHeight),clk=clock,duration=config.pauseAfterBlink)
                # pause again so there is a blank screen before the
                # stims start again
                clock.delay(config.pauseAfterBlink)
                clock.wait()

                # put the stuff back on the screen
                noiseL = video.showProportional(noisestim[0].content, state.coords['left_coord'], state.coords['mid_coord'])
                noiseR = video.showProportional(noisestim[0].content, state.coords['right_coord'], state.coords['mid_coord'])
                orientShown = video.showProportional(orientCross, state.coords['mid_coord'], state.coords['mid_coord'])
                video.updateScreen(clock)
                log.logMessage('ORIENT_ON')
                # pause before study so they can finish blinking;
                # orienting cross and noise stim are on screen here
                clock.delay(config.study_preStimDelay, config.study_preStimJitter)
                clock.wait()

        # get image specific config
        imageconfig = config.sequence(n)

        # present the image
        timestamp = flashStimulus(eachImage.content,duration = imageconfig.study_stimDuration,x = eachImage.x_coord,y = eachImage.y_coord,jitter = imageconfig.study_stimJitter,clk = clock)

        # log the study image presentation
        log.logMessage('%s\t%s\t%s\t%d\t%.3f\t%.3f\t%d' % (eachImage.itemType_study,imageconfig.presentationType,eachImage.name,eachImage.isTarget,eachImage.x_coord,eachImage.y_coord,eachImage.ser_pos), timestamp)

        # debug
        #print '%s (%d); study: %.3f' % (eachImage.name,eachImage.isTarget,eachImage.x_coord)
        
        # ISI before presenting each stim; fixation cross and noise
        # stim are on screen here
        clock.delay(config.study_ISI,config.study_ISIJitter)
        clock.wait()

    video.unshow(noiseL)
    video.unshow(noiseR)
    video.unshow(orientShown)
    log.logMessage('ORIENT_OFF')
    video.updateScreen(clock)

    # ------------------- end study ---------------------

    # log the end of the study period
    if isExperiment:
        log.logMessage('STUDY_END')
    else:
        log.logMessage('PRACTICE_STUDY_END')

############################################################

def recogsource(exp,
                config,
                clock,
                log,
                video,
                audio,
                targets,
                lures,
                isExperiment):
    """
    Run a generic recognition task.  You supply the targets and lures
    as Pools, which get randomized and presented one at a time
    awaiting a user response.  The attribute defines which present
    method is used, such as image, sound, or stimtext

    This function generates two types of log lines, one for the
    presentation (RECOG_PRES) and the other for the response
    (RECOG_RESP).  The columns in the log files are as follows:

    RECOG_PRES -> ms_time, max dev., RECOG_PRES, Pres_type, What_present, isTarget
    RECOG_RESP -> ms_time, max dev., RECOG_RESP, key_pressed, RT, max dev. isCorrect

    INPUT ARGS:
      targets- Pool of targets.
      lures- Pool of lures.
      attribute- String representing the Pool attribute to present.
      clk- Optional PresentationClock
      log- Log to put entries in.  If no log is specified, the method
           will log to recognition.log.
      test_stimDuration/test_stimJitter- Passed into the attribute's present method.
           Jitter will be ignored since we wait for a keypress.
      minRespDuration- Passed into the present method as a min time they
                   must wait before providing a response.
      test_ISI/test_ISIJitter- Blank ISI and jitter between stimuli, after
                   a response if given.
      targetKey- String representing the key representing targets.
      lureKey- String representing the key for the lure response.
      judgeRange- Tuple of strings representing keys for
                  confidence judgements.
                  If provided will replace targetKey and lureKey

    OUTPUT ARGS:


    TO DO:
    Try and see if mixed up the keys (lots wrong in a row)
    Pick percentage of targets from each list.
    """

    # get the state
    state = exp.restoreState()

    # concatenate the targets and lures
    stims = targets + lures

    # randomize them
    stims.shuffle()

    maxCount = 2
    stims = repeatSwap(stims,'x_coord',maxCount)
    maxCount = 3
    stims = repeatSwap(stims,'isTarget',maxCount)

    # create the button choosers
    bc_sourceNew = ButtonChooser(Key(state.keys['sourceLeftKey_test']), Key(state.keys['sourceRightKey_test']), Key(state.keys['newKey_test']))
    bc_rememKnow = ButtonChooser(Key(state.keys['rsKey_test']), Key(state.keys['roKey_test']), Key(state.keys['kKey_test']))
    bc_sureMaybe = ButtonChooser(Key(state.keys['sureKey_test']), Key(state.keys['maybeKey_test']))
    
    # create the source text
    sourceLeftText = Text(config.sourceLeftText_test,size=config.test_wordHeight)
    sourceRightText = Text(config.sourceRightText_test,size=config.test_wordHeight)
    # create the new text
    newText = Text(config.newText_test,size=config.test_wordHeight)
    # create the source judgment prompt
    sourceText = [('sourceLeftText',sourceLeftText,'PROP',(state.coords['test_source_left_x'], state.coords['mid_coord'])),('sourceRightText',sourceRightText,'PROP',(state.coords['test_source_right_x'], state.coords['mid_coord'])),('newText',newText,'PROP',(state.coords['test_new_x'], state.coords['mid_coord']))]
    sourceText_cs = CompoundStimulus(sourceText)

    # create the RK judgment text
    rememSourceText = Text(config.rememSourceText_test,size=config.test_wordHeight)
    rememOtherText = Text(config.rememOtherText_test,size=config.test_wordHeight)
    knowText = Text(config.knowText_test,size=config.test_wordHeight)
    # create the RK judgment prompt
    rkText = [('rememSourceText',rememSourceText,'PROP',(state.coords['test_rs_x'], state.coords['mid_coord'])),('rememOtherText',rememOtherText,'PROP',(state.coords['test_ro_x'], state.coords['mid_coord'])),('knowText',knowText,'PROP',(state.coords['test_k_x'], state.coords['mid_coord']))]
    rkText_cs = CompoundStimulus(rkText)
    
    # create the sure/maybe text for a "new" response
    sureText = Text(config.sureText_test,size=config.test_wordHeight)
    maybeText = Text(config.maybeText_test,size=config.test_wordHeight)
    # create the sure/maybe prompt
    smText = [('sureText',sureText,'PROP',(state.coords['test_sure_x'], state.coords['mid_coord'])),('maybeText',maybeText,'PROP',(state.coords['test_maybe_x'], state.coords['mid_coord']))]
    smText_cs = CompoundStimulus(smText)
    
    config.fastStim = Text('TOO FAST!',size=config.test_wordHeight,color='red')
    
    # set up orienting fixation cross
    orientCross = Text(config.orientText,size=config.fixation_wordHeight)

    # ------------------- start test ---------------------
    
    # log the start of recognition/source test period
    if isExperiment:
        log.logMessage('TEST_START')
    else:
        log.logMessage('PRACTICE_TEST_START')

    # press any key to begin test
    if isExperiment:
        if config.ILI_timer:
            bc_ILI = ButtonChooser(Key(config.ILI_key),Key(config.endImpedanceKey))
            # put the text on the screen
            studyshown = video.showProportional(Text(config.testBeginText % (state.listNum + 1)), state.coords['mid_coord'], state.coords['mid_coord'])
            video.updateScreen()
            # do a countdown so they wait the same amount of time
            timestamp = countdown_with_interrupt(config,state,config.ILI_dur,bc_ILI,video,clock)
            video.unshow(studyshown)
            video.updateScreen(clock)
        else:
            timestamp = waitForAnyKey(clock,Text(config.testBeginText % (state.listNum + 1)))
        log.logMessage('TEST_BEGIN_KEYHIT',timestamp)
    else:
        if config.ILI_timer:
            bc_ILI = ButtonChooser(Key(config.ILI_key),Key(config.endImpedanceKey))
            # put the text on the screen
            studyshown = video.showProportional(Text(config.testPracBeginText), state.coords['mid_coord'], state.coords['mid_coord'])
            video.updateScreen()
            # do a countdown so they wait the same amount of time
            timestamp = countdown_with_interrupt(config,state,config.ILI_dur,bc_ILI,video,clock)
            video.unshow(studyshown)
            video.updateScreen(clock)
        else:
            timestamp = waitForAnyKey(clock,Text(config.testPracBeginText))
        log.logMessage('PRACTICE_TEST_BEGIN_KEYHIT',timestamp)
    
    timestamp = flashStimulus(Text(config.textAfterBlink,size=config.instruct_wordHeight),clk=clock,duration=config.pauseAfterBlink)
    
    # delay before first stim to observe conf ratings; happens once
    # per list
    clock.delay(config.test_preStimDelay, config.test_preStimJitter)
    clock.wait()

    # display the orienting fixation cross
    orientShown = video.showProportional(orientCross, state.coords['mid_coord'], state.coords['mid_coord'])
    video.updateScreen(clock)
    log.logMessage('ORIENT_ON')

    # present and wait for response
    for n, stim in enumerate(stims):
        # EEG: blink breaks
        if isExperiment:
            # if we're part-way through the list, not on the first
            # list, and not on the last list, put up the blink
            # rest-period text
            if config.isEEG and (n+1) % (len(stims)/(config.test_blinkBreaksPerList+1)) == 0 and (n+1) != 1 and (n+1) != len(stims) and (len(stims) - (n+1)) > 6:
                # delay before break; fixation cross is still on
                # screen here
                clock.delay(config.test_ISI,config.test_ISIJitter)
                clock.wait()
                # remove orienting fixation cross
                video.unshow(orientShown)
                video.updateScreen(clock)
                log.logMessage('ORIENT_OFF')
                log.logMessage('BLINK_REST_START')
                timestamp = waitForAnyKey(clock,Text(config.blinkRestText_test,size=config.instruct_wordHeight))
                log.logMessage('BLINK_REST_END_KEYHIT',timestamp)
                # pause after blinking
                clock.delay(config.pauseAfterBlink)
                clock.wait()
                timestamp = flashStimulus(Text(config.textAfterBlink,size=config.instruct_wordHeight),clk=clock,duration=config.pauseAfterBlink)
                # display the orienting fixation cross
                orientShown = video.showProportional(orientCross, config.mid_coord, config.mid_coord)
                video.updateScreen(clock)
                log.logMessage('ORIENT_ON')
                # pause again so there is a blank screen before the
                # stims start again
                clock.delay(config.pauseAfterBlink)
                clock.wait()

        # delay with orientation cross before stimulus
        if config.test_preview:
            clock.delay(config.test_preview,config.test_previewJitter)
            clock.wait()

        #video.updateScreen(clock) # don't update here

        # present the stimulus
        prestime_stim = stim.content.present(clk = clock,
                                             duration = config.test_stimDuration,
                                             jitter = config.test_stimJitter)

        # Log the test item presentation
        log.logMessage('%s\t%s\t%s\t%d\t%d' %
                       (stim.itemType_test,config.presentationType,stim.name,stim.isTarget,stim.ser_pos),
                       prestime_stim)
        
        if isExperiment:
            # delay with orientation cross after stimulus before responses
            if config.test_preRespOrientDelay:
                clock.delay(config.test_preRespOrientDelay,config.test_preRespOrientJitter)
                clock.wait()
        else:
            # beep at them if they try to answer too early
            if config.test_preRespOrientDelay:
                fixed_delay_with_keybeep(config,state,config.test_preRespOrientDelay,bc_sourceNew,video,clock)

        # show the source options: left, right, and new
        prestime_src,button_src,bc_time_src = sourceText_cs.present(clk=clock,duration=config.test_maxRespDuration,bc=bc_sourceNew,minDuration=config.test_minRespDuration)

        # Process the source response
        if button_src is None:
            # They did not respond in time
            # Must give message or something
            bname_src = 'None'
            resp_src = 'NONE'
            isCorrect_src = -1
            if config.playAudio:
                config.errorBeep.present()
        else:
            # get the button name
            bname_src = button_src.name
            # what was the response and was it correct?
            if stim.isTarget == 1:
                if bname_src == state.keys['newKey_test']:
                    resp_src = 'NEW'
                    isCorrect_src = 0
                elif bname_src == state.keys['sourceLeftKey_test']:
                    resp_src = 'LEFT'
                    if stim.x_coord < .5:
                        isCorrect_src = 1
                    elif stim.x_coord > .5:
                        isCorrect_src = 0
                elif bname_src == state.keys['sourceRightKey_test']:
                    resp_src = 'RIGHT'
                    if stim.x_coord < .5:
                        isCorrect_src = 0
                    elif stim.x_coord > .5:
                        isCorrect_src = 1
            elif stim.isTarget == 0:
                if bname_src == state.keys['newKey_test']:
                    resp_src = 'NEW'
                    isCorrect_src = 1
                elif bname_src == state.keys['sourceLeftKey_test']:
                    resp_src = 'LEFT'
                    isCorrect_src = 0
                elif bname_src == state.keys['sourceRightKey_test']:
                    resp_src = 'RIGHT'
                    isCorrect_src = 0
        
        # Log the source response
        if isExperiment:
            log.logMessage('SOURCE_RESP\t%s\t%s\t%ld\t%d\t%d' %
                           (bname_src,resp_src,bc_time_src[0]-prestime_src[0],bc_time_src[1]+prestime_src[1],isCorrect_src),bc_time_src)
        else:
            log.logMessage('PRACTICE_SOURCE_RESP\t%s\t%s\t%ld\t%d\t%d' %
                           (bname_src,resp_src,bc_time_src[0]-prestime_src[0],bc_time_src[1]+prestime_src[1],isCorrect_src),bc_time_src)

        # debug
        #print '%s (%d); study: %.3f' % (stim.name,stim.isTarget,stim.x_coord)
        #print 'resp_src: %s (%s)' % (resp_src, bname_src)
        #print 'isCorrect_src: %d' % isCorrect_src
            
        # for a non-new response
        if bname_src != state.keys['newKey_test'] and button_src is not None:
            # show the remember/know text
            prestime_rk,button_rk,bc_time_rk = rkText_cs.present(clk=clock,duration=config.test_maxRespDuration,bc=bc_rememKnow,minDuration=config.test_minRespDuration)
            
            # Process the RK response
            if button_rk is None:
                # They did not respone in time
                # Must give message or something
                bname_rk = 'None'
                resp_rk = 'NONE'
                isCorrect_rk = -1
                if config.playAudio:
                    config.errorBeep.present()
            else:
                # get the button name
                bname_rk = button_rk.name
                #isCorrect_rk = -1
                if bname_rk == state.keys['rsKey_test']:
                    resp_rk = 'REMEMBER_SOURCE'
                elif bname_rk == state.keys['roKey_test']:
                    resp_rk = 'REMEMBER_OTHER'
                elif bname_rk == state.keys['kKey_test']:
                    resp_rk = 'KNOW'
                if stim.isTarget:
                    isCorrect_rk = 1
                else:
                    isCorrect_rk = 0

            # log the RK response
            if isExperiment:
                log.logMessage('RK_RESP\t%s\t%s\t%ld\t%d\t%d' %
                               (bname_rk,resp_rk,bc_time_rk[0]-prestime_rk[0],bc_time_rk[1]+prestime_rk[1],isCorrect_rk),bc_time_rk)
            else:
                log.logMessage('PRACTICE_RK_RESP\t%s\t%s\t%ld\t%d\t%d' %
                               (bname_rk,resp_rk,bc_time_rk[0]-prestime_rk[0],bc_time_rk[1]+prestime_rk[1],isCorrect_rk),bc_time_rk)

            # debug
            #print 'resp_rk: %s (%s)' % (resp_rk, bname_rk)
            #print 'isCorrect_rk: %d' % (isCorrect_rk)

        # for a new response
        elif bname_src == state.keys['newKey_test']:
            # show the sure/maybe text
            prestime_new,button_new,bc_time_new = smText_cs.present(clk=clock,duration=config.test_maxRespDuration,bc=bc_sureMaybe,minDuration=config.test_minRespDuration)
            
            # Process the response
            if button_new is None:
                # They did not respone in time
                # Must give message or something
                bname_new = 'None'
                resp_new = 'NONE'
                isCorrect_new = -1
                if config.playAudio:
                    config.errorBeep.present()
            else:
                # get the button name
                bname_new = button_new.name
                #isCorrect_new = -1
                if bname_new == state.keys['sureKey_test']:
                    resp_new = 'SURE'
                elif bname_new == state.keys['maybeKey_test']:
                    resp_new = 'MAYBE'
                if stim.isTarget:
                    isCorrect_new = 0
                else:
                    isCorrect_new = 1
            
            # log the new response
            if isExperiment:
                log.logMessage('NEW_RESP\t%s\t%s\t%ld\t%d\t%d' %
                               (bname_new,resp_new,bc_time_new[0]-prestime_new[0],bc_time_new[1]+prestime_new[1],isCorrect_new),bc_time_new)
            else:
                log.logMessage('PRACTICE_NEW_RESP\t%s\t%s\t%ld\t%d\t%d' %
                               (bname_new,resp_new,bc_time_new[0]-prestime_new[0],bc_time_new[1]+prestime_new[1],isCorrect_new),bc_time_new)
            
            # debug
            #print 'resp_new: %s (%s)' % (resp_new, bname_new)
            #print 'isCorrect_new: %d' % (isCorrect_new)
        
        # delay if wanted
        if config.test_ISI:
           clock.delay(config.test_ISI,config.test_ISIJitter)

    # remove fixation cross
    video.unshow(orientShown)
    video.updateScreen(clock)
    log.logMessage('ORIENT_OFF')
    
    if isExperiment:
        # Log end of recognition/source test period
        log.logMessage('TEST_END')
    else:
        log.logMessage('PRACTICE_TEST_END')

############################################################

def run(exp, config):
    """
    Run the entire experiment
    """

    # this is where the experiment code kicks off

    # verify that we have all the files
    _verifyFiles(config)

    # get the state
    state = exp.restoreState()

    # set up the session
    #
    # have we run all the sessions?
    if state.sessionNum >= len(state.sesStudyLists):
        print 'No more sessions!'
        return

    # set the session number
    exp.setSession(state.sessionNum)

    # get session specific config
    sessionconfig = config.sequence(state.sessionNum)

    # set up the logs
    video = VideoTrack('video')
    keyboard = KeyTrack('keyboard')
    if config.playAudio:
        # audio so we can play beeps
        audio = AudioTrack('audio')
    else:
        audio = None
    # this is the one i use for storing all my main
    # experiment data
    log = LogTrack('session')

    # set up the presentation clock
    try:
        # requires 1.0.29, auto-adjusts timing if there's a lag
        clock = PresentationClock(correctAccumulatedErrors=True)
    except:
        # if you don't have 1.0.29 loaded, then just
        # fall back (since the timing will probably be
        # fine anyway)
        clock = PresentationClock()

    # set the default font
    setDefaultFont(Font(sessionconfig.defaultFont))

    if config.playAudio:
        config.breakBeep = Beep(config.hiBeepFreq,
                                config.hiBeepDur,
                                config.hiBeepRiseFall)
        config.errorBeep = Beep(config.loBeepFreq,
                                config.loBeepDur,
                                config.loBeepRiseFall)

    # set up impedance key
    endImpedance = ButtonChooser(Key(config.endImpedanceKey))
    
    # log start
    timestamp = clock.get()
    log.logMessage('SESS_START\t%d' % (state.sessionNum + 1), timestamp)

    video.clear('black')
    # display the session number
    if len(state.sesStudyLists) > 1:
        waitForAnyKey(clock,Text(config.sesBeginText % (state.sessionNum + 1)))

    if state.sessionNum == 0 and state.practiceDone == 0:

        # record a resting period for EEG experiments
        timestamp = waitForAnyKey(clock,Text(config.restEEGPrep,size=config.instruct_wordHeight))
        log.logMessage('REST_EEG_KEYHIT',timestamp)
        video.clear('black')
        # show the text
        timestamp = flashStimulus(Text(config.restEEGText,size=config.instruct_wordHeight),clk=clock,duration=config.restEEGDuration)
        # log the resting period
        log.logMessage('REST_EEG', timestamp)

        # intro instructions
        video.clear('black')
        log.logMessage('INTRO_INSTRUCT')
        timestamp = instruct(open(state.instruct_gen['inst_intro_path'],'r').read(),size=config.instruct_wordHeight)

        # do a practice list
        if sessionconfig.practiceList:

            # tell that this is not the experiment so we don't log
            isExperiment = False

            for prac_listNum in range(sessionconfig.prac_numLists):

                listconfig = sessionconfig.sequence(prac_listNum)
                log.logMessage('PRACTICE_TRIAL_START')

                thisStudyList = state.pracStudyLists[prac_listNum]
                thisTargList = state.pracTargLists[prac_listNum]
                thisLureList = state.pracLureLists[prac_listNum]

                # show practice study instructions
                video.clear('black')
                log.logMessage('PRACTICE_STUDY_INSTRUCT')
                instruct(open(state.instruct_gen['inst_stud_prac_path'],'r').read(),size=config.instruct_wordHeight)

                # do the practice study period
                study_trial(exp,config,clock,log,video,audio,thisStudyList,isExperiment)

                # show practice test instructions
                video.clear('black')
                log.logMessage('PRACTICE_TEST_INSTRUCT')
                instruct(open(state.instruct_gen['inst_test_prac_path'],'r').read(),size=config.instruct_wordHeight)
                video.clear('black')

                # do the practice test period
                recogsource(exp,config,clock,log,video,audio,thisTargList,thisLureList,isExperiment)

                # save the state after the practice
                exp.saveState(state,practiceDone = (prac_listNum + 1))
                state = exp.restoreState()

                log.logMessage('PRACTICE_TRIAL_END')

        # Show getready instructions
        video.clear('black')
        instruct(open(sessionconfig.instruct_getready,'r').read(),size=config.instruct_wordHeight)

    # tell that this is the experiment so we log properly
    isExperiment = True

    # present each trial in the session
    while state.listNum < len(state.sesStudyLists[state.sessionNum]):
        # load list specific config
        listconfig = sessionconfig.sequence(state.listNum)

        # # do instructions on first trial of each session
        # if state.listNum == 0 and state.studyDone == 0:
            
        #     # Show main instructions
        #     video.clear('black')
        #     log.logMessage('STUDY_INSTRUCT')
        #     instruct(open(state.instruct_gen['inst_stud_path'],'r').read(),size=config.instruct_wordHeight)

        # Clear to start
        video.clear('black')

        # EEG: if partway through, give a break to adjust electrodes
        if state.listNum % 1 == 0 and state.listNum != config.numLists:
        #if state.listNum == (config.numLists/2):
            if config.playAudio:
                # play a beep so we know it's time
                config.breakBeep.present(clock)
            log.logMessage('REST_START', timestamp)
            # present the text
            breakText = Text(open(config.midSessionBreak,'r').read())
            video.showCentered(breakText)
            video.updateScreen(clock)

            # save the state at the impedance break
            exp.saveState(state)
            state = exp.restoreState()
            
            if config.isEEG:
                # wait for the endImpedanceKey to be hit
                endImpedance.waitChoice(1000,sessionconfig.maxImpedanceTime,clock)
                video.clear('black')
            else:
                # wait for the endImpedanceKey to be hit or for breakTime to pass
                config.endImpedance.waitChoice(1000,config.breakTime,clock)
                video.clear('black')
                if config.playAudio:
                    # play a beep so we know it's time
                    config.breakBeep.present(clock)
            # log the time the break ended
            log.logMessage('REST_END', timestamp)

            # save the state after the impedance break
            exp.saveState(state)
            state = exp.restoreState()
        
        # show the current trial and wait for keypress
        timestamp = waitForAnyKey(clock,Text(config.trialBeginText % (state.listNum + 1)))
        log.logMessage('TRIAL\t%d' % (state.listNum + 1),timestamp)

        thisStudyList = state.sesStudyLists[state.sessionNum][state.listNum]
        thisTargList = state.sesTargLists[state.sessionNum][state.listNum]
        thisLureList = state.sesLureLists[state.sessionNum][state.listNum]

        # ------------------- start trial ---------------------
        
        # log the start of the trial
        log.logMessage('TRIAL_START')

        if state.studyDone == 0:
            # Show study instructions
            video.clear('black')
            log.logMessage('STUDY_INSTRUCT')
            instruct(open(state.instruct_gen['inst_stud_path'],'r').read(),size=config.instruct_wordHeight)
            # Clear to start
            video.clear('black')
            
            # do the study period
            study_trial(exp,config,clock,log,video,audio,thisStudyList,isExperiment)
            
            # save the state after each study list and mark that we did the study period
            exp.saveState(state, studyDone = 1)
            state = exp.restoreState()

        #if state.listNum == 0:
        # show test instructions
        video.clear('black')
        log.logMessage('TEST_INSTRUCT')
        instruct(open(state.instruct_gen['inst_test_path'],'r').read(),size=config.instruct_wordHeight)
        video.clear('black')
        
        # do the test period
        recogsource(exp,config,clock,log,video,audio,thisTargList,thisLureList,isExperiment)
        
        # log the end of the trial
        log.logMessage('TRIAL_END')
        
        # update the listNum state
        state.listNum += 1
        
        # save the state after test list and reset studyDone to 0
        exp.saveState(state, studyDone = 0)
        state = exp.restoreState()

        # ------------------- end trial ---------------------
        
    # save the state when the session is finished
    exp.saveState(state,
                  listNum = 0,
                  sessionNum = state.sessionNum + 1)

    if config.playAudio:
        # play a beep so we know we're done
        config.breakBeep.present(clock)
    
    # Done
    timestamp = waitForAnyKey(clock,Text('Thank you!\nYou have completed the session.'))
    log.logMessage('SESS_END',timestamp)

    # Catch up
    clock.wait()

############################################################
# def main_interactive(config='config.py'):
            
#     """
#     If you want to run things interactively from ipython,
#     call this. It's basically the same as the main()
#     function.

#     from my_exp import *; exp = main_interactive()
    
#     OR if you want to load in a special config file:

#     from my_exp import *; exp = main_interactive('debug_config.py')
#     """
    
#     exp = pyRecSrc(subject='RS000',
#                  fullscreen=False,
#                  resolution=(640,480),
#                  config=config)
    
#     exp.go()
    
#     return exp

############################################################
#
# only do this if the experiment is run as a stand-alone program (not
# imported as a library)
if __name__ == '__main__':
    # make sure we have the min pyepl version
    checkVersion(MIN_PYEPL_VERSION)
    
    # start PyEPL, parse command line options, and do
    # subject housekeeping
    exp = Experiment()
    exp.parseArgs()
    exp.setup()
    
    # allow users to break out of the experiment with escape-F1 (the default key combo)
    exp.setBreak()
    
    # get subj. config
    config = exp.getConfig()

    # if there was no saved state, run the prepare function
    if not exp.restoreState():
        _prepare(exp, config)

    # now run the subject
    run(exp, config)
    
