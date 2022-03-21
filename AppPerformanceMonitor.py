import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import adbModule
import collections
import json
import re
import threading

cpuEnable = True
memEnable = True
gpuEnable = True
interval = 60*1000
threads = []
fig = plt.figure(figsize=(15,6), facecolor='#DEDEDE')
cpu = collections.deque(np.zeros(5))
ram = collections.deque(np.zeros(5))
gpu = collections.deque(np.zeros(5))
fps = collections.deque(np.zeros(5))
plt.subplots_adjust(left=0.125,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.455,
                    hspace=0.35)
ax = plt.subplot(211)
ax1 = plt.subplot(234)
ax2 = plt.subplot(235)
ax3 = plt.subplot(236)

def loadSetting():
    global cpuEnable, memEnable, gpuEnable, fpsEnable, interval
    with open('setting.json') as jsonData:
         data = json.load(jsonData)
    adbModule.init(data)
    cpuEnable = data['enableCPU']
    memEnable = data['enableMem']
    gpuEnable = data['enableGPU']
    fpsEnable = data['enableFPS']
    interval = int(data['frequencyInSec'])
def updataData(i):
    # get data
    adbModule.printCurrentTime()
    if cpuEnable is True :
        global cpu,ram,gpu,fps,ax,ax1,ax2,ax3
        cpu.popleft()
        cpu.append(adbModule.cpuLoggerNum())
        # clear axis
        ax.cla()
        # plot cpu
        ax.plot(cpu)
        print(cpu[-1])
        ax.scatter(len(cpu)-1, cpu[-1])
        ax.text(len(cpu)-1, cpu[-1]+1, "{}%".format(cpu[-1]))
        ax.set_ylim(0,100)
        #ax.set_xlabel('Eslapse Time (s)')
        ax.set_ylabel('CPU (%)')
        ax.set_title('CPU Monitor')
    if memEnable is True :
        ram.popleft()
        ram.append(adbModule.memLoggerNum())
        # clear axis
        ax1.cla()
        # plot memory
        ax1.plot(ram)
        ax1.scatter(len(ram)-1, ram[-1])
        print(ram[-1])
        ax1.text(len(ram)-2, ram[-1]+5, "{} MB".format(ram[-1]))
        ax1.set_ylim(0,1000)
        #ax1.set_xlabel('Eslapse Time (s)')
        ax1.set_ylabel('Memory (mb)')
        ax1.set_title('Memory Monitor')
    if gpuEnable is True :
        gpu.popleft()
        gpu.append(adbModule.gpuLoggerNum())
        # clear axis
        ax3.cla()
        ax3.plot(gpu)
        ax3.scatter(len(gpu)-1, gpu[-1])
        if not gpu:
            ax3.text(0.1,0.5,"Cannot accesss GPU data")
        else:                       
            ax3.text(len(gpu)-1.5, gpu[-1]+1 , "{} %".format(gpu[-1]))
        #ax2.set_xlabel('Eslapse Time (s)')
        ax3.set_ylim(0,100)
        ax3.set_ylabel('GPU (%)')
        ax3.set_title('GPU Monitor')
    if fpsEnable is True :
        fps.popleft()
        fpsNum = adbModule.fps
        fps.append(fpsNum)
        print(fpsNum)
        ax2.cla()
        ax2.plot(fps)
        ax2.scatter(len(fps)-1, fps[-1])
        ax2.text(len(fps)-2, fps[-1], "{} ".format(fps[-1]))
        ax2.set_ylim(0,30)
        #ax1.set_xlabel('Eslapse Time (s)')
        ax2.set_title('Frame rate per sec(FPS)')    
    adbModule.nextLine()
def initialize():
    global ax,ax1,ax2,ax3
    # define and adjust figure
    ax.set_facecolor('#DEDEDE')
    ax1.set_facecolor('#DEDEDE')
    ax2.set_facecolor('#DEDEDE')
    ax3.set_facecolor('#DEDEDE')
    ax.set_ylim(0,100)
    ax1.set_ylim(0,1000)
    ax2.set_ylim(0,30)
    ax3.set_ylim(0,100)

loadSetting()
initialize()
adbModule.adbPermission()

getFPS = threading.Thread(target=adbModule.fpsLogger)
getFPS.start()

ani = animation.FuncAnimation(fig, updataData, interval=interval*1000)
plt.show()
