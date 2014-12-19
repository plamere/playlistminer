# Playlist Miner support scripts

In order to support being able to sort tracks by distinctivness, the Playlist
Miner needs to know how frequently any particular track appears across all
playlists.  The scripts in this directory estimate the track frequencly for the
most popular tracks. The resulting output is a json file 'ppm.js' that can be
used by the web app. 

 - crawl.py - this script will process up to 10,000 playlists and aggregates the
   tracks across all the playlists. It saves the track counts and info into
   tracks.pkl. The crawl can be interrupted at any time. It will restart where
   it left off. The longer it runs the better the data.

 - proc.py - ths script reads the tracks.pkl and calculates the frequency of
   occurence for each track and creates the ppm.js file

Here's how to run the scripts:

% python crawl.py plamere  # replace plamere with your spotify name

  you will be prompted to authorize the app (auth is needed to read
  the contents of playlists)

    Let crawl.py run for a while. The more playlists it finds the better your
    results. 

% python proc.py 

    this will create the ppm.js from the output of the crawl

To start using the new track frequency data, cp the ppm.js to the web directory

% cp ppm.js ..



