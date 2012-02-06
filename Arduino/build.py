# Build & upload an arduino program

# Because the Arduino IDE sucks and tries to hide the details of C++.
# And then breaks shit if you actaully know C++. >:[

# This script made from looking at the output of the arduino-1.0 build
# process the the Uno R3 with build.verbose=true and upload.verbose=true
# set in the preferences.txt file

# Assumptions made:
# - Uno R3
# - Win7x64


# TODO:
# - set the paths to arduino IDE and project better
# - display errors better
# - break on errors

import os
import sys
import shutil


def full(*path):
  return os.path.abspath(os.path.join(os.getcwd(), *path))

# TODO fix this

# Arduino IDE installation directory
ARDUINO = 'P:\\arduino-1.0'

# name of folder containing your project
NAME = 'Arduino'

BIN = full(ARDUINO, 'hardware\\tools\\avr\\bin')
INCLUDE = [
  full(ARDUINO, 'hardware\\arduino\\cores\\arduino'),
  full(ARDUINO, 'hardware\\arduino\\variants\\standard')
]

INCLUDE_FLAGS = ' '.join('-I%s' % i for i in INCLUDE)

GPP = (full(BIN, 'avr-g++.exe') +
  ' -c -g -Os -Wall -fno-exceptions -ffunction-sections -fdata-sections' +
  ' -mmcu=atmega328p -DF_CPU=16000000L -DARDUINO=100 ' + INCLUDE_FLAGS)


GCC = (full(BIN, 'avr-gcc.exe') +
  ' -c -g -Os -Wall -ffunction-sections -fdata-sections' +
  ' -mmcu=atmega328p -DF_CPU=16000000L -DARDUINO=100 ' + INCLUDE_FLAGS)

AR = (full(BIN, 'avr-ar.exe') + ' rcs')

if os.path.exists('Build'):
  shutil.rmtree('Build')

os.mkdir("Build")
os.mkdir("Build\\Environment")

# first make all the shit
CORE = full('Build', 'core.a')
for dirpath in INCLUDE:
  for lname in os.listdir(dirpath):
    name = full(dirpath, lname)
    if not (name.endswith('.c') or name.endswith('.cpp')): continue
    if name.endswith('.c'):   cc = GCC
    if name.endswith('.cpp'): cc = GPP
    obj = full('Build', 'Environment', '%s.o' % lname)
    cmd = "%s %s -o %s" % (cc, name, obj)

    print cmd
    os.system(cmd)


    cmd = '%s %s %s' % (AR, CORE, obj)
    print cmd
    os.system(cmd)


print
print

# now make our shit
objs = []
for dirpath, dirnames, filenames in os.walk(NAME):
  for lname in filenames:
    name = full(dirpath, lname)
    print name
    if not (name.endswith('.c') or name.endswith('.cpp')): continue
    if name.endswith('.c'):   cc = GCC
    if name.endswith('.cpp'): cc = GPP
    # assumes no lname conflicts
    obj = full('Build', '%s.o' % lname)
    objs.append(obj)
    cmd = "%s %s -o %s" % (cc, name, obj)

    print cmd
    os.system(cmd)



print
print
# do some more stuff

# avr-gcc -Os -Wl,--gc-sections -mmcu=atmega328p -o tmp\Blink.cpp.elf tmp\Blink.cpp.o tmp\core.a -Ltmp -lm
# avr-objcopy -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 tmp\Blink.cpp.elf tmp\Blink.cpp.eep
# avr-objcopy -O ihex -R .eeprom tmp\Blink.cpp.elf tmp\Blink.cpp.hex
# avrdude -CP:\arduino-1.0\hardware/tools/avr/etc/avrdude.conf -v -v -v -v -patmega328p -carduino -P\\.\COM3 -b115200 -D -Uflash:w:tmp\Blink.cpp.hex:i

ELF = full('Build', '%s.elf' % NAME)
EEP = full('Build', '%s.eep' % NAME)
HEX = full('Build', '%s.hex' % NAME)

cmd = '%s -Os -Wl,--gc-sections -mmcu=atmega328p -o %s %s %s -Ltmp -lm' % (
  full(BIN, 'avr-gcc.exe'), ELF, ' '.join(objs), CORE)

print cmd
os.system(cmd)


cmd = ('%s -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load '
  '--no-change-warnings --change-section-lma .eeprom=0 %s %s' % (
  full(BIN, 'avr-objcopy.exe'), ELF, EEP))

print cmd
os.system(cmd)


cmd = '%s -O ihex -R .eeprom %s %s' % (
  full(BIN, 'avr-objcopy.exe'), ELF, HEX)

print cmd
os.system(cmd)


cmd = '%s -C%s -v -v -v -v -patmega328p -carduino -P\\.\COM3 -b115200 -D -Uflash:w:%s:i' % (
  full(BIN, 'avrdude.exe'),
  full(ARDUINO, 'hardware/tools/avr/etc/avrdude.conf'),
  HEX)

print cmd
os.system(cmd)












