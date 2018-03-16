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
deviceName = args[1]
quarterNoteLength = float(args[2])
notePadding = args[3]
readFile = args[4]
writeFile = args[5]
# Time in millis between notes



with open(readFile, "r") as read:
    with open(writeFile, "w") as write:
        data = read.read()
        # Match pound sign followed by any number of anything until either newline or end of string. 
        # End of string in this case is the end of file
        # ? Makes it non-greedy 
        nocomments = re.sub(r'//(.*?)(\n|\Z)', "",data)
        # we might want comments because sendmidi supports them...


        # Capture description:
        # 0: All notes including whitespace between and after (at least one required)
        # 1: The last note matched (useless)
        # 2: Any single letter a-g either capital or lowercase
        # 3: Sharp or flat (optional)
        # 4: Any single number 0-9
        # 5: At least one number from 0-9 (optional)
        # 6: Dot followed by any number of numbers (optional)
        # 7: Any amount of whitespace (optional)
        # Examples: 
        # c4 1000 \n\n
        # b1        \n \n               \n
        # DOES NOT SUPPORT NEGATIVE OCTAVES
        noteData = re.findall(r'((([A-Ga-g])([#|b])?([0-9])\s+)+)([0-9]+)?(.[0-9]*)?(\s*)?', data)
        write.write("dev " + "\"" + deviceName + "\"\n")
        for note_data in noteData:
            notes = note_data[0].split()
            notes = [note.strip() for note in notes]
            for note in notes:
                letter = note[0]
                shift = 0
                if note[1] == "#":
                    shift = 1
                elif note[1] == "b":
                    shift = -1

                octave = int(note[-1])
                # Turnary operator in python
                # if duration it's the duration time the length of a quarter note
                # otherwise it's just quarterNoteLength
                duration = quarterNoteLength * float(note_data[4] + note_data[5]) if note_data[4] else quarterNoteLength
                write.write("on " + str(midiNumber(letter, octave, shift)) + " 127\n")
            write.write(formatTime(duration)+"\n")
            for note in notes:
                letter = note[0]
                shift = 0
                if note[1] == "#":
                    shift = 1
                elif note[1] == "b":
                    shift = -1

                octave = int(note[-1])
                write.write("off " + str(midiNumber(letter, octave, shift)) + " 127\n")
            write.write(formatTime(notePadding)+"\n")
        







