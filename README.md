# paison-haishin-get
Simple little script for checking for specified livestreams on Twitch
and Hitbox.


## Usage:
There are two ways to use this script.

The main way only requires simple configuration in "streams.conf".
Write the name of a streamer you wish to check, followed by a space, then
the name or abbreviation of the streaming service they are on. Once this
is done, simply run the script without arguments.  It will look for a
config file in the same directory as the script.

The alternative method is to run the script while supplying the info of a
a single streamer, in this fashion: "python haishin-get.py Vinesauce t".
This method will return information for just the one streamer, and ignore
config.  This method is useful when integrating this script into another
program.

