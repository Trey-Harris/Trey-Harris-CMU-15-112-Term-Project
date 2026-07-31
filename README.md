Sky Scavenger - AVR Flight Simulator:
A realistic flight expirience designed to give players a taste of the Advanced 
Vertical Robotics competition without risking an expensive drone. This emulates
the real compeition: Fly over a wall to collect dumpsters and fly them back 
over to the open dropoff spots. The faster you do this, the more points you get. 
($5 to whoever beats the 112 Dragon) 

Video Link: https://drive.google.com/file/d/1VMtZG0uuREL_CWmZ8ZTE4a0Og7JwS54f/view?usp=sharing

The only file needed to be run is the main file, the rest of the files in GitHub
just store functions for the game. Download pygame and numpy for the drone controller
and 3D projections to work (also PIL for the images to load).

Shortcuts:
- r resets the game
- m switches to phase 2 early
- h warps the drone to the right side of the field (if the wall is too difficult for the user)
- g warps the drone to the left side of the field

General Gameplay Advice (b/c this game is hard):
- WASD for drone tilt
- Up and down for altitude
- USE VERY SMALL INPUTS!!! The drone moves faster the more tilted it is. Start 
  with small, incremental movements and work your way up to larger, faster ones.
- When picking up/dropping off the containers, align the bottom 1/3 of the drone's
  shadow with the top of the dumpster/dropoff area.
- Make sure to have at least a little altitude above 0 when dropping a container
  otherwise the container will automatically reattach (reflects real life where
  magnets would auto-connect)
- If you can, try to use the controller as it is less laggy than the keyboard controls.
- That said, because the timer decreases by step (not real-world time), the slower 
  movement of the drone is accounted for by a slower countdown, so scores should be
  similar with or without lag. It should run smoothly on a laptop with 16GB RAM. 
  Plugging your laptop in (even if it's at high battery) will also help handle 
  the additional computation required by 3D graphics.