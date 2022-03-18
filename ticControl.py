import subprocess
import yaml
import time
import atexit



settingFilePath = "/home/pi/MSCS/" # where the settings are located, this still needs to be checked
debugFlag = True
calibratePos = 0 # temporary calibration position, substitute for a homeing switch
calibrateFlag = False
homePos = 10000 # position of slide right above rollers, in front of camera
upPos = 2000 # top most position of slide
downPos = 15000 # bottom most position of slide
calStepSize = 1000 # step size for manual calibration / homing
LAsettings = {
  "currentpos": 0
  "homepos": 10000
  "uppos": 2000
  "downpos": 15000
} # dictionary for variable storage to file

def start():
  atexit.register(exit_handler)
  log("starting linear actuator")
  loadSettings()
  ticcmd("--exit-safe-start")
  ticcmd('--halt-and-set-position', calibratePos)

def log(msg):
  if debugFlag:
    print(msg)

def ticcmd(*args):
  return subprocess.check_output(['ticcmd'] + list(args))

def gotoHome():
  goto(homePos)

def loadSettings():
  log("loading LA settings from file")
  ticcmd('--settings', settingFilePath + "tic_settings.txt")
  lasettings = settingFilePath + "LASettings.yaml"
  with open(lasettings, "r") as file:
    LAsettings = yaml.load(file, Loader=yaml.FullLoader)

def exit_handler():
  lasettings = settingFilePath + "LASettings.yaml"
  with open(lasettings, "w") as file:
    LAsettings = yaml.dump(file, Loader=yaml.FullLoader)

# manually lowers the slide by a set step size, used to manually home the LA
def down(num):
  goto(getPos() + calStepSize) # this is addition because LA is mounted upside down

# manually raises the slide by a set step size, used to manually home the LA
def up(num):
  goto(getPos() - calStepSize) # this is subtraction because LA is mounted upside down

# goes to input position on the linear actuator, pos is int, returns when position is achieved
def goto(pos):
  ticcmd('--position', str(pos)) # execute ticcmd to goto

  while True: # wait loop to return only when the target position is achieved
    currentPosition = getPos()
    log("going to " + str(pos) + "currently at " + str(currentPosition))
    if currentPosition == pos:
      return
    time.sleep(0.1)

def getPos():
  status = yaml.load(ticcmd('-s', '--full'))
  position = status['Current position']
  log("getPos " + str(position))
  return position
  

def calibrate():
  calibrateFlag = True
  ticcmd('--halt-and-set-position', calibratePos)



