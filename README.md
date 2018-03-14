# FloppyMidiLang
A small language to make writing simple tunes in SendMIDI easier.

This program will interpret a text file and generate another text file with corresponding SendMIDI code.

#Limitations:
This "language" is very simple and cannot currently support very much. Currently there is no support for playing multiple notes at the same time, note volume, audio channels and much more. This "language" is only intended to be used as a way to create SendMIDI code for single notes at a time.


The program takes 4 arugments.
1. Length of a quarter note in milliseconds
2. Length of pauses between notes in milliseconds
3. Relative path to input file
4. Relative path to output file

#Syntax:
(Note as a letter)(Flat or Sharp)(Octave) (Quarter note multiplier)

#Details:
(Note as a letter) - Acceptable values are a,b,c,d,e,f,g this is not case sensitive.

(Flat or Sharp) - Acceptable values are #,b. # indicates sharp and b indicates flat. This is optional and if not found will result in a normal note.

(Octave) - Acceptable values are 0,1,2,3,4,5,6,7,8,9. This determines which octave the note is in. Negative octaves are currently not supported.

(Quarter note multiplier) - Acceptable values are any number integer or decimal. This determines the length of the note. The note will be played for the duration of this many quarter notes. So if this value is 2 we have a half note, 4 is a whole note and 1.5 is a dotted quarter note. For convience this is optional and if not found will default to 1 (a quarter note).

#Examples:

##note-lang examples:
Here are various notes with the corresponding SendMIDI code they will generate and the musical meaning. This code was generated with 100 millisecond quarter notes and 50 milliseconds of note padding.

A C-sharp in the 4th octave dotted quarter note
'''
c#4 1.5
on 61 127
+00:00:00:150
off 61 127
+00:00:00:050
'''

An A-natural in the 5th octave half note
'''
a5 2
on 81 127
+00:00:00:200
off 81 127
+00:00:00:050
'''

A G-flat in the 7th octave half note
'''
gb7 2
on 102 127
+00:00:00:200
off 102 127
+00:00:00:050
'''
##Calling the script:
Lets say we want to create a song where a quarter note is half a second long and the space between notes is 50 milliseconds and we have a text file containing our input note data called input.txt and we want to create an output file name output.txt. We would call our script like so:

note-lang.py 500 50 input.txt output.txt