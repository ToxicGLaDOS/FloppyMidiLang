import sys, re


def formatTime(totalMillis):
    totalMillis = int(totalMillis)
    millis = int(totalMillis)%1000

    seconds=(totalMillis/1000)%60
    seconds = int(seconds)
    minutes=(totalMillis/(1000*60))%60
    minutes = int(minutes)
    hours=(totalMillis/(1000*60*60))%24

    return ("+%s:%s:%s:%s" % (format(hours, '02'), format(minutes, '02'), format(seconds,'02'), format(millis,'03')))

def midiNumber(letter, octave, shift):
    """ Get the midi number value of a note based on letter and octave """
    letter = letter.lower()
    difference = {'c':0,'d':2,'e':4,'f':5,'g':7,'a':9,'b':11}
    return 12 * (octave+1) + difference[letter] + shift




args = sys.argv
quarterNoteLength = float(args[1])
readFile = args[2]
writeFile = args[3]
# Time in millis between notes
notePadding = 50 


with open(readFile, "r") as read:
    with open(writeFile, "w") as write:
        data = read.read()
        # Match pound sign followed by any number of anything until either newline or end of string. 
        # End of string in this case is the end of file
        # ? Makes it non-greedy 
        nocomments = re.sub(r'//(.*?)(\n|\Z)', "",data)
        # we might want comments because sendmidi supports them...


        # Capture description:
        # 0: Any single letter a-g either capital or lowercase
        # 1: Sharp or flat (optional)
        # 2: Any single number 0-9
        # 3: At least one number from 0-9 (optional)
        # 4: Any amount of whitespace (optional)
        # Examples: 
        # c4 1000 \n\n
        # b1        \n \n               \n
        # DOES NOT SUPPORT NEGATIVE OCTAVES
        notes = re.findall(r'([A-Ga-g])([#|b])?([0-9])\s*([0-9]+)?(\s*)?', data)
        for note in notes:
            letter = note[0]
            shift = 0
            if note[1] == "#":
                shift = 1
            elif note[1] == "b":
                shift = -1

            octave = int(note[2])
            # Turnary operator in python
            # if duration is matched that is duration, otherwise use quarterNoteLength
            duration = quarterNoteLength * float(note[3]) if note[3] else quarterNoteLength
            write.write("on " + str(midiNumber(letter, octave, shift)) + " 127\n")
            write.write(formatTime(duration)+"\n")
            write.write("off " + str(midiNumber(letter, octave, shift)) + " 127\n")
            write.write(formatTime(notePadding)+"\n")
            







