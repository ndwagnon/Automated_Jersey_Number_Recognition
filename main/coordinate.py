#author: Noah Wagnon
#description: Extract roster info and id which
#players correspond to which play. Post to API.

import os
import json
import requests

#hard code the home and away teams
home = 'Alabama'
away = 'South Carolina'

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

#open ocr results
infileOCR = open("ocr_filtered_output.txt", 'r')

#open detection results
infileDetection = open("detection_output.txt", 'r')


#List of all lines in detection results
detectionLines = infileDetection.readlines()

for line in infileOCR:
    values = line.split()

    #extract play number
    playNumber = values[0]

    #extract quarter
    quarterNumber = values[1]

    #extract frames
    startFrame = values[2]
    endFrame = values[3]

    #extract start clock
    startClock = values[4]
    clockStartSec = startClock[-2:]
    startClock = startClock[:-2]
    startClock = startClock + ':' + clockStartSec

    #extract stop clock
    stopClock = values[5]
    clockStopSec = stopClock[-2:]
    stopClock = stopClock[:-2]
    stopClock = stopClock + ':' + clockStopSec
    
    #list of numbers within a play
    numberSeenWithinPlay = []

    
    #loop through detection file for values within the play parameters
    for detectionLine in detectionLines:
        detectionValues = detectionLine.split()

        #get frame
        currentFrame = detectionValues[0]

        #ignore results if before play started
        if (currentFrame < startFrame):
            detectionLines.pop(0)
            continue
            
        #break the loop if next play has begun
        if (currentFrame > endFrame):
            break

        #remove frame from list
        detectionValues.pop(0)

        #append numbers to list
        for number in detectionValues:
            if not (number in numberSeenWithinPlay) and not(len(numberSeenWithinPlay) >= 11):
                numberSeenWithinPlay.append(number)

        #remove line from remaining lines to be processed
        detectionLines.pop(0)

    seen = []
    for number in numberSeenWithinPlay:
        name = roster[int(number)]
        playerStr = str(number) + ': ' + name
        seen.append(playerStr)

    play_json_object = {'play_number': playNumber, 'quarter': quarterNumber, 'start_time': startClock, 'end_time': stopClock,
    'home': home, 'away': away, 'participating_players': seen }

    #ensure proper sorting
    if (int(playNumber) >= 10):
        jsonPath = 'play_' + str(playNumber) + '_players_seen.json'
    else:
        jsonPath = 'play_' + '0' + str(playNumber) + '_players_seen.json'
    
    #save as json outfile
    with open(os.path.join('plays/json', jsonPath), 'w') as outfile:
        json.dump(play_json_object, outfile)
    
    #create the url
    url = f"""http://127.0.0.1:5000/plays?play_number={playNumber}&quarter={quarterNumber}
    &start_time={startClock}&end_time={stopClock}&home={home}&away={away}"""

    #add all players to request
    for player in seen:
        url = url + f"&participating_players={player}"
    
    #post to the api
    response = requests.post(url)
    print(response)

    

