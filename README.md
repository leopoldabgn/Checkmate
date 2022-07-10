*Create date: 04/2020*
# Checkmate
This project is a network chess game coded in Python. It is using the Tkinter and Pygame libraries. You can play with anyone who is connected to the same Wifi as yours. But you can also play anywhere. All you have to do is create a Wifi hotspot with your phone and you're done!

## How to install

### Clone the repo
You can clone the repository.

### Libraries
This project is using the tkinter and pygame libraries.
#### Tkinter
On ubuntu you can try :
```
sudo apt-get install python3-tk
```
Or this command :
```
pip3 install tk
```

#### Pygame
On every devices, just use pip3 to install it :
```
pip3 install pygame
```

## How to play

### Launch the game
It's a python project, so you can go in the folder and launch the following commands :
```
python3 checkmate.py
```

### Menu
There are two modes you can choose :
- Solo
- Multiplayer

### Solo
In Solo mode, you can play with a friend on the same computer (there is no AI). First, you can stop a game along the way and resume it later. Indeed, you have the possibility to select an old backup when launching the application (To save a game, press S during the game).
Then, you can start your game. When the game board is loaded, you just have to play your first move. When you are done, right click to rotate the game board. Player 2 can now take their turns and so on...

### Multiplayer
When you launched the application, the **ifconfig** command is executed in your terminal.

Before trying to start a multiplayer game, you have to be connected on the same Wifi as you friend. If you're not at home, you can try to start a **Wifi hotspot** with your phone. Then, the two computers have to be connected on your phone.  
After that, you can launch the app on the computers and click on the multiplayer's button :
- 1 person has to be the **host**
- 1 person has to be the **guest**
#### Host
To host the game, you need to write your ip adress and a port (12800 by default). To find your **ip** adress, just look at your terminal and get the adress who begins with **192.168.\*.\***. Now, click on host and wait your friend.  

When your friend has joined the game, you can select an old save. If you don't want to, you just have to click directly on **start** to start the game.

#### Guest
You have to join the game hosting by your friend. You just have to write your friend's ip adress and port. Finally, click on **join** and wait for your friend.
### Save a game
You can press S and the game will be automatically saved in the **saves** folder.
