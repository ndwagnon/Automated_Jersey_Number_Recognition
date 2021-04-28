#Author: Noah Wagnon
#Description: Processes the raw detection
# results and makes them human readable


import json
import os
import glob
import sys

# path to use
path = 'debug/json'

#keeps up with frame count
count = 1

# #Alabama 2020 Roster
# roster = [
#     "Unknown Player",
#     "Ben Davis",
#     "Patrick Surtain or Keilan Robinson",
#     "Daniel Wright or Xavier Williams",
#     "Christopher Allen or Brian Robinson",
#     "Jalyn Armour-Davis or Javon Baker",
#     "Devonta Smith",
#     "Brandon Turnage or Braxton Barker",
#     "Christian Harris or John Metchie",
#     "Jordan Battle or Bryce Young",
#     "Ale Kaho or Mac Jones",
#     "Kristian Story or Traeshon Holden",
#     "Skyler DeLong or Logan Burnett",
#     "Malachi Moore",
#     "Brian Branch or Thaiu Jones-Bell",
#     "Eddie Smith or Paul Tyson",
#     "Will Reichard or Jayden George",
#     "Jaylen Waddle",
#     "LaBryan Ray or Slade Bolden",
#     "Jahleel Billingsley",
#     "Drew Sanders",
#     "Jahquez Robinson or Jase McClellan",
#     "Ronald Williams or Najee Harris",
#     "Jarez Parks or Roydell Williams",
#     "Clark Griffin or Trey Sanders",
#     "DJ Douglas or Jonathan Bennett",
#     "Marcus Banks",
#     "Joshua Robinson or Kyle Edwards",
#     "Josh Jobe",
#     "Demarco Hellams",
#     "King Mwikuta",
#     "Will Anderson or Shatarius Williams",
#     "Dylan Moses or CJ Williams",
#     "Jackson Bratton",
#     "Quandarrius Robinson",
#     "Shane Lee or Cooper Bishop",
#     "Bret Bolin",
#     "Demouy Kennedy",
#     "Jalen Edwards",
#     "Carson Ware",
#     "Joshua McMillon",
#     "Chris Braswell",
#     "Jaylen Moody or Sam Reed",
#     "Jordan Smith",
#     "Unknown Player",
#     "Thomas Fletcher",
#     "Christian Swann or Melvin Billingsley",
#     "Byron Young",
#     "Phidarian Mathis",
#     "Julian Lowenstein",
#     "Tim Smith or Gabe Pugh",
#     "Robert Ellis or Tanner Bowles",
#     "Braylen Ingraham",
#     "Matthew Barnhill",
#     "Kyle Flood",
#     "Emil Ekiyor",
#     "Charlie Skehan or Seth McLaughlin",
#     "Joe Donald or Javion Cohen",
#     "Christian Barmore",
#     "Bennett Whisenhunt or Jake Hall",
#     "Unknown Player",
#     "Unknown Player",
#     "Jackson Roby",
#     "Unknown Player",
#     "Unknown Player",
#     "Deonte Brown",
#     "Brandon Cade",
#     "Donovan Hardin",
#     "Alajujuan Sparks",
#     "Landon Dickerson",
#     "Alex Leatherwood",
#     "Darrian Dalcourt",
#     "Pierce Quick",
#     "Evan Neal",
#     "Damieon George",
#     "Tommy Brown",
#     "Unknown Player",
#     "Unknown Player",
#     "Amari Kight",
#     "Chris Owens",
#     "Michael Parker",
#     "Cameron Latu",
#     "Chase Allen",
#     "Richard Hunt",
#     "Joshua Lanier",
#     "Charlie Scott or Kendall Randolph",
#     "Carl Tucker",
#     "Miller Forristall",
#     "Major Tennison",
#     "Kyle Mann or Grant Krieger",
#     "Stephon Wynn",
#     "Gavin Reeder",
#     "Justin Eboigbe",
#     "Jah-Marien Latham or Tripp Slyman",
#     "DJ Dale",
#     "Jack Martin",
#     "Landon Bothwell",
#     "LT Ikner or Joseph Bulovas",
#     "Jamil Burroughs or Sam Johnson",
#     "Ty Perine"
# ]

#Alabama 2019 Roster
roster = [
    "Unknown Player",
    "Ben Davis",
    "Patrick Surtain or Keilan Robinson",
    "Daniel Wright",
    "Christopher Allen or Jerry Jeudy",
    "Shyheim Carter or Taulia Tagovailoa",
    "Devonta Smith",
    "Trevon Diggs or Braxton Barker",
    "Christian Harris or John Metchie",
    "Jordan Battle or Xavier Williams",
    "Mac Jones",
    "Scooby Carter or Henry Ruggs",
    "Skyler DeLong or Chadarius Townsend",
    "Tua Tagovailoa",
    "Brandon Turnage or Tyrell Shavers",
    "Xavier McKinney or Paul Tyson",
    "Will Reichard or Jayden George",
    "Jaylen Waddle",
    "Slade Bolden",
    "Jahleel Billingsley",
    "DJ Douglas or Ale Kaho",
    "Jared Mayden",
    "Jalyn Armour-Davis or Najee Harris",
    "Jarez Parks",
    "Terrell Lewis or Brian Robinson",
    "Eddie Smith",
    "Marcus Banks or Trey Sanders",
    "Joshua Robinson or Jerome Ford",
    "Josh Jobe",
    "Demarco Hellams",
    "King Mwikuta",
    "Michael Collins or AJ Gates",
    "Dylan Moses or Jalen Jackson",
    "Anfernee Jennings",
    "Unknown Player",
    "Shane Lee or De'Marquise Lockridge",
    "Markail Benton or Mac Hereford",
    "Unknown Player",
    "Sean Kelly or Eric Poellnitz",
    "Loren Ugheoke",
    "Joshua McMillon or Giles Amos",
    "Carson Ware",
    "Jaylen Moody or Sam Reed",
    "Daniel Powell",
    "Kevin Harris",
    "Thomas Fletcher",
    "Melvin Billingsley",
    "Byron Young",
    "Phidarian Mathis",
    "Unknown Player",
    "Hunter Brannon or Gabe Pugh",
    "Wes Baumhower or Tanner Bowles",
    "Preston Malone or Braylen Ingraham",
    "Unknown Player",
    "Julian Lowenstein",
    "William Cooper or Emil Ekiyor",
    "Unknown Player",
    "Joe Donald",
    "Christian Barmore",
    "Jake Hall",
    "Unknown Player",
    "Unknown Player",
    "Jackson Roby",
    "Rowdy Garza",
    "Unknown Player",
    "Deonte Brown",
    "Unknown Player",
    "Unknown Player",
    "Unknown Player",
    "Landon Dickerson",
    "Alex Leatherwood",
    "Darrian Dalcourt",
    "Pierce Quick",
    "Evan Neal",
    "Jedrick Wills",
    "Tommy Brown",
    "Scott Lashley",
    "Matt Womack",
    "Amari Kight",
    "Chris Owens",
    "Michael Parker",
    "Cameron Latu",
    "Richard Hunt",
    "John Parker",
    "Joshua Lanier",
    "Drew Kobayashi or Kendall Randolph",
    "Connor Adams or Quindarius Watkins",
    "Miller Forristall",
    "Major Tennison",
    "Labryan Ray or Grant Krieger",
    "Stephon Wynn",
    "Tevita Musika",
    "Justin Eboigbe",
    "Landon Bothwell or Tripp Slyman",
    "DJ Dale",
    "Ishmael Sopsher or Jack Martin",
    "Taylor Wilson",
    "Joseph Bulovas",
    "Mike Bernier",
    "Raekwon Davis or Ty Perine"
]
#Open and set the outfile
with open("detection_output.txt", mode="w") as outfile:

    sys.stdout = outfile
    # iterate through each json file
    # only process .JSON files in folder.

    for filename in sorted(glob.glob(os.path.join(path, '*.json'))):
        
        #Print the current frame count
        #print("Frame Number: " + str(count))

        #Open the file
        with open(filename, encoding='utf-8', mode='r') as currentFile:
            data = currentFile.read().replace('\n', '')

            #make the Json object
            frameData = json.loads(data)

            #Extract the raw frame number
            rawFrameNumber = frameData.get('raw_frame_number')

            #format with extra words
            #print("Index: " + str(rawFrameNumber))

            #format without extra words
            outfile.write( (str(rawFrameNumber) + ' '))

            #Extract the jersey number list and rois
            nums = frameData.get('class_names')
            rois = frameData.get("rois")

            #Keep track of reported players
            players_seen = []

            #Bool to know when to skip
            skip = False

            #Iterate through the jerseys seen
            for index,num in enumerate(nums):

                #Skip if this is second digit of 2-digit num
                if (skip):
                    skip = False #reset bool
                    continue
                
                #Process for determining if number is two-digit

                #ensure that this is not last element. If it is inflate the values for safety
                #y1,x1,y2,x2
                if (index <= ( len(nums) - 2)):
                    distanceY1 = abs(rois[index][0] - rois[index + 1][0])
                    distanceX1 = abs(rois[index][1] - rois[index + 1][1])
                    distanceY2 = abs(rois[index][2] - rois[index+1][2])
                    distanceX2 = abs(rois[index][3] - rois[index + 1][3])
                else:
                    distanceY1 = 1000
                    distanceX1 = 1000
                    distanceY2 = 1000
                    distanceX2 = 1000

                #The values are determined to be 2-digit or 1-digit
                if ( (distanceY2 < 40) and (distanceX1 < 30) and (distanceY2 < 40) and (distanceX2 < 40) ):
                    #Make sure numbers are in correct order
                    if ( (rois[index][1] - rois[index + 1][1]) > 0):
                        numIntStr = nums[index+1] + num
                        numInt = int(numIntStr)
                    else:
                        numIntStr = num + nums[index +1]
                        numInt = int(numIntStr)
                    skip = True
                else:
                    numIntStr = num
                    numInt = int(num)
                    skip  = False

                # #Format to include words
                # printStr = "Jersey number seen: " + numIntStr + ": "

                #format to only include info
                printStr = numIntStr + " "

                #Ensure a valid number and print name and number
                if ( numInt >= 0 and numInt <=99):
                    playerName = roster[numInt]
                else:
                    playerName = "Unknown Player"
                #uncomment to include player name    
                #printStr += playerName + ' '

                #Don't print Duplicates
                if(playerName not in players_seen):
                    outfile.write(printStr)

                #Mark player as seen
                players_seen.append(playerName)

            #denote end of frame and increment count
            #print('end frame\n')

            #remove extra words
            outfile.write('\n')
            count = count + 1
