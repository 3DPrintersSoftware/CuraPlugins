#Name: Set Infill Parameters
#Info: Set fan speed for infill
#Depend: GCode
#Type: postprocess
#Param: iFanSpeed(int:0) Set infill fan speed
##Param: iInfillTemperature(integer:0) Set infill temperature

version = '1.0'

import re

def getValue(line, key, default = None):
    if not key in line or (';' in line and line.find(key) > line.find(';') and not ";TweakAtZ" in key and not ";LAYER:" in key):
        return default
    subPart = line[line.find(key) + len(key):] #allows for string lengths larger than 1
    if ";TweakAtZ" in key:
        m = re.search('^[0-3]', subPart)
    elif ";LAYER:" in key:
        m = re.search('^[+-]?[0-9]*', subPart)
    else:
        m = re.search('^[-]?[0-9]+\.?[0-9]*', subPart) #the minus at the beginning allows for negative values, e.g. for delta printers
        if m == None:
            return default
    try:
        return float(m.group(0))
    except:
        return default


with open(filename, "r") as f:
    lines = f.readlines()


SectionType = 'STARTOFFILE'
Layer = 0
LastFanSpeed = 0.0
#InfillFanSpeed = float(iFanSpeed)

with open(filename, "w") as f:
    for line in lines:
        f.write(line)
        if line.startswith( ';' ) :
            if line.startswith( ';LAYER:' ) :
                Layer = int( line[7:].strip() ) + 1
                SectionType = 'NEWLAYER'
            if line.startswith( ';TYPE:' ) :
                SectionType = line[6:].strip()
                if SectionType == 'FILL':
                    f.write("M106 S%d\n" % int(iFanSpeed))
                else:
                    f.write("M106 S%d\n" % int(LastFanSpeed))
        sCode = getValue(line, 'M', None)
        if sCode == 106:
            LastFanSpeed = getValue(line, 'S', 0.0)
