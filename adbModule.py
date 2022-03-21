import os
import subprocess
import threading
import time
import json
import re
import statistics

fps = 0.0
path = time.strftime('%Y-%m-%d_%H_%M') + ' monitor.txt'
f = open(path,'w')
f.close

packageName = 'com.mitac.gemini.cdr'
frequency = 1
startTime = time.time()

def init(setting):
    global packageName
    global frequency
    packageName = setting['packageName']
    frequency = int(setting['frequencyInSec'])

def adb_listDevices():
    p=os.popen('adb devices')
    devicesList=p.read()
    p.close()
    lists = devicesList.split('\n')
    if(len(lists) < 2):
        return
    devicesNames = []
    for item in lists:
        if(str(item.strip()) == ""):
            continue
        if(item.startswith("List of")) :
            continue
        else:        
           devicesNames.append(item.split('\t')[0])
    return devicesNames

def adb_command(cmd):
    return subprocess.getstatusoutput(cmd)

def createTimer():
    t = threading.Timer(frequency, repeat)
    t.start()

def printCurrentTime():
    print('Now:', time.strftime('%Y/%m/%d/ %H:%M:%S',time.localtime()), file=f)

def repeat():
    f = open(path, 'a')
    print('Now:', time.strftime('%Y/%m/%d/ %H:%M:%S',time.localtime()), file=f)
    gpuLogger(f)
    memLogger(f)
    cpuLogger(f)
    fpsLogger(f)
    f.close()
    createTimer()
    
def memLogger(f):
    cmd = 'adb shell dumpsys meminfo ' + packageName
    memory = adb_command(cmd)
    memStart = str(memory).find("TOTAL:") # 'TOTAL  ' for 8 characters ex:TOTAL:    75238(after':'then 9 characters)
    #memEnd = str(memory).find(' ',memStart+8)
    memoryInMb = str(memory)[memStart+6:memStart+15]
    memoryInMb = memoryInMb.replace(" ","")
    mem = 0
    try:
        mem = int(memoryInMb) / 1000
    except:
        mem = 0
    if(type(mem) != float):
        print("Can't find memory", file=f)
    else:
        print('Memory total: ' + str(mem) + ' MB', file=f)
    return mem

def memLoggerNum():
    cmd = 'adb shell dumpsys meminfo ' + packageName
    memory = adb_command(cmd)
    memStart = str(memory).find("TOTAL:") # 'TOTAL  ' for 8 characters ex:TOTAL:    75238(after':'then 9 characters)
    memoryInMb = str(memory)[memStart+6:memStart+15]
    memoryInMb = memoryInMb.replace(" ","")
    mem = 0
    try:
        mem = int(memoryInMb) / 1000
    except:
        mem = 0
    if(type(mem) != float):
        print("Can't find memory", file=f)
    else:
        print('Memory total: ' + str(mem) + ' MB', file=f)
    return mem

def cpuLogger(f):
    cmd = 'adb shell dumpsys cpuinfo ' + packageName
    cpu = adb_command(cmd)
    cpuStart = str(cpu).rfind('\\n') # '\n' for 2 characters
    cpuEnd = str(cpu).find('TOTAL', cpuStart)
    print('CPU : ' + str(cpu)[cpuStart+2:cpuEnd], file=f)
    return str(cpu)[cpuStart+2:cpuEnd]

def cpuLoggerNum():
    cmd = 'adb shell dumpsys cpuinfo ' + packageName
    cpu = adb_command(cmd)
    cpuStart = str(cpu).rfind('\\n') # '\n' for 2 characters
    cpuEnd = str(cpu).find('TOTAL', cpuStart)
    print('CPU : ' + str(cpu)[cpuStart+2:cpuEnd], file=f)
    output = str(cpu)[cpuStart+2:cpuEnd].replace("%","")
    try:
        return float(output)
    except:
        return 0.0

def gpuLogger(f):
    cmd = 'adb shell cat /sys/class/kgsl/kgsl-3d0/gpu_busy_percentage'
    gpu = adb_command(cmd)
    gpu = str(gpu).replace("%","")    
    gpuStart = str(gpu).find('\'')
    gpuEnd = str(gpu).rfind('\'')    
    print('GPU : ' + str(gpu)[gpuStart+1:gpuEnd], file=f)

def gpuLoggerNum():
    cmd = 'adb shell cat /sys/class/kgsl/kgsl-3d0/gpu_busy_percentage'
    gpu = adb_command(cmd)
    gpu = str(gpu).replace("%","")
    gpuStart = str(gpu).find('\'')
    gpuEnd = str(gpu).rfind('\'')
    gpuNum = str(gpu)[gpuStart+1:gpuEnd]
    print('GPU : ' + str(gpu)[gpuStart+1:gpuEnd], file=f)
    print('GPU : ' + gpuNum)
    return int(gpuNum)

def nextLine():
    print('\n', file=f)    

def eslapseTime():
    return time.time() - startTime  

def adbPermission():
    cmd = 'adb root'
    print(adb_command(cmd))

def startRecord():
    adbPermission()
    print('List current devices: ' + str(adb_listDevices()))
    createTimer()

def fpsLogger():
    global fps,f
    logcat = subprocess.Popen('adb shell "logcat | grep FrameRateMonitor" ', stdout=subprocess.PIPE)
    while not logcat.poll():
        line = logcat.stdout.readline()
        if line:
            word = str(line)
            tmp = word[word.find("Camera ")+ 7:word.find(",")-4]
            try :
                fps = float(tmp)
            except :
                fps = 0.0
            print("FPS : " + str(fps), file=f)
        else:
            break
    print("Logcat no FPS output", logcat.returncode)