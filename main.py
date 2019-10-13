### IMPORTS ###
import tkinter as tk
import random, time, csv , math , os , sys , webbrowser

from threading import Thread
from winsound import *


class player():
    """This class corresponds to the cute little orange box controlled by the WASD keys by the player"""
    x = 0
    y = 0
    xdist = 0
    ydist = 0
    def __init__(self,canvas,x,y,onGround,id="player"):# ID is used for different collision protocols
        self.canvas = canvas
        self.x = x
        self.y = y
        self.onGround = onGround # onGround is the boolean variable to see if the player is allowed to jump
        self.id = id
        self.tempX,self.tempY = self.x,self.y
        
    def draw(self):
        self.simpleBox = self.canvas.create_rectangle(self.x-playerSize, self.y-playerSize, self.x+playerSize, self.y+playerSize, outline="black", fill="yellow", width=2) # Simple box is a rect or otherwise only influenced by x,y; as opposed to x1,x1,y1,y2
    def move(self):
        global movingLeft,movingRight,movingUp,Jumping,againstObj,onGround,items,endOfScreen,mycanvas,cameraMovingHorizontal,level,cameraMovingVertical,secondJump,secondJumpUsed,movedDownAmount,cameraMoveAmountX
        self.tempX,self.tempY = self.tempX + self.xdist,self.tempY - self.ydist
        if movingLeft == True:
                if againstObj == False or againstObj == ("Right"):
                    if self.xdist > -6.0:
                        if self.xdist < -0.7:
                            self.xdist -= slide + 0.2
                        else:
                            self.xdist -= 0.7# The -= 1 provides a uniform acceleration rather than immediate full speed
                    againstObj = False
        if movingRight == True:
                if againstObj == False or againstObj == ("Left"):
                    if self.xdist < 6.0:
                       self.xdist += 0.7
                    againstObj = False # againstObj is the variable to see if the player is against a wall, to stop them moving further through the wall
        if Jumping == True:
            self.ydist -= 0.5*playerSize + 8 # This means jump height depends on their size
            movingUp = True
            Jumping = False
        if secondJump == True:
            self.ydist -= 0.5*playerSize + 5 + self.ydist# The second jump is the double jump and works in a way such that timing the second jump allows for higher jumps
            if self.ydist >= 19:
                self.ydist = 19
            movingUp = True
            Jumping = False
            secondJump = False
        if onGround == False:  
            if self.ydist < 20:
                self.ydist += 1 # Limits terminal verocity to 11 px / frame
        else:
            secondJumpUsed = False
        if self.xdist > 0:
            self.xdist -= slide  # slide is the global resistance of the surphace they are on  
        else:
            self.xdist += slide
        if self.xdist <= slide and self.xdist >= -slide:
            self.xdist = 0 # this stops the player from jiggling left and right abit when they should be still.
        self.x = self.x + self.xdist 
        self.y = self.y + self.ydist # Ensures integrity of x,y positions
        self.canvas.move(self.simpleBox,self.xdist,self.ydist) # moves the player every frame
        if self.x > endOfScreen:
            cameraMovingHorizontal = ("Right")
        simpleBoxList = ["player","turret","bubble","bullet","sizeChange","textBox","scenary","shadow","trampoline","character","shop","mine","boulder"] # these are all objects that only have x,y; not x1,x2,y1,y2
        if cameraMovingHorizontal == ("Right"):
            cameraMoveAmountX += 6
            for obj in items: # moves every item to the left abit to create an illusion of moving
                if obj.id in simpleBoxList:
                      mycanvas.move(obj.simpleBox,-6,0)
                      obj.x -= 6
                elif obj.id == ("movingPlatform"):
                   mycanvas.move(obj.block,-6,0)
                   obj.x1 -= 6
                   obj.x2 -= 6
                   obj.minX -= 6
                   obj.maxX -= 6
                else:
                    mycanvas.move(obj.block,-6,0)
                    obj.x1 -= 6
                    obj.x2 -= 6
                    if obj.id == ("enemy"):
                        obj.x -= 6
                    if obj.id == ("jumpEnemy"):
                        obj.x -= 6
                        for i in range(len(obj.jumpTimes)):
                            obj.jumpTimes[i] -= 6   
            if self.x < middleOfScreen:
                cameraMovingHorizontal = False # this stops us moving to the right infinitely
        if self.x < beginningOfScreen:
            cameraMovingHorizontal = ("Left")
        if cameraMovingHorizontal == ("Left"):
            cameraMoveAmountX -= 6
            for obj in items:
                if obj.id in simpleBoxList:
                    mycanvas.move(obj.simpleBox,6,0) 
                    obj.x += 6
                elif obj.id == ("movingPlatform"):
                   mycanvas.move(obj.block,6,0)
                   obj.x1 += 6
                   obj.x2 += 6
                   obj.minX += 6
                   obj.maxX += 6
                else:
                    mycanvas.move(obj.block,6,0)
                    obj.x1 += 6
                    obj.x2 += 6
                    if obj.id == ("enemy"):
                        obj.x += 6
                    if obj.id == ("jumpEnemy"):
                        obj.x += 6
                        for i in range(len(obj.jumpTimes)):
                            obj.jumpTimes[i] += 6
            if self.x > middleOfScreen:
                cameraMovingHorizontal = False
        if self.y < topOfScreen:
            cameraMovingVertical = ("Up")
        if cameraMovingVertical == ("Up"):
            movedDownAmount -= 18
            for obj in items:  # This has to move up really fast to avoid horrible horrible horrible horrible bugs involving not being able to calculate collisions because the player is off screen
                if obj.id in simpleBoxList:
                   mycanvas.move(obj.simpleBox,0,18)
                   obj.y += 18
                else:
                    mycanvas.move(obj.block,0,18)
                    obj.y1 += 18
                    obj.y2 += 18
                    if obj.id == ("enemy"):
                        obj.y += 18
            if self.y > verticleMiddleOfScreen:
                cameraMovingVertical = False
        if self.y > bottomOfScreen:
            cameraMovingVertical = ("Down")  
        if cameraMovingVertical == ("Down"):
            movedDownAmount += 20
            for obj in items:
                if obj.id in simpleBoxList:
                   mycanvas.move(obj.simpleBox,0,-20)
                   obj.y -= 20
                else:
                    mycanvas.move(obj.block,0,-20)
                    obj.y1 -= 20
                    obj.y2 -= 20
                    if obj.id == ("enemy"):
                        obj.y -= 20
            if self.y < verticleMiddleOfScreen:
                cameraMovingVertical = False     
    def collision(self):
        global level,items,resetListValue,onGround,againstObj,onMovingPlatforms,resetListValue
        overlaps =(mycanvas.find_overlapping(self.x-playerSize,self.y-playerSize,self.x+playerSize,self.y+playerSize))
        allOverlaps = mycanvas.find_overlapping(-10000,-10000,10000,10000) # everything on the tkinter stack (yes it's a stack)
        #allOverlaps = mycanvas.find_overlapping(0,0,500,800)
        found2,found3 = False,False # These are seeing weather we have made contact with a moving platform specifically, or just ground of any type
        for item in overlaps:
            currentItem = allOverlaps.index(item) -1
            try:
                if item != overlaps[0]:
                    if items[currentItem].id == ("movingPlatform"):
                        found2 = True
                    if items[currentItem].id == ("movingPlatform") or items[currentItem].id == ("ground"):
                        found3 = True
            except:
                pass
        if found3 == False:
            onGround = False
            
            onMovingPlatforms = False
            againstObj = False
        if found2 == False:
            onGround = False
            onMovingPlatforms = False
        for item in overlaps:  # For every overlapping item the specific protocol is ran
            try:
                if item != overlaps[1] and item != overlaps[0]:
                        currentItem = allOverlaps.index(item) -1   # The -1 is there because... Oh yeah, the background image isn't counted so it offsets the tkinter stack by one
                        if items[currentItem].id != ("bullet") or items[currentItem].id != ("turret"): 
                            items[currentItem].collision()
            except:
                pass
        for item in items:
            if item.id == ("bullet"):      #  Bubbles and bullets always need their collision routines ran, whatever the weather.
                item.collision()

                
class playerShadow():
    """A imitation of the player, shown just infront of the player so that it dosen't disappear from view and go behind scenary items like bushes and things"""
    def __init__(self,canvas,x,y,id="shadow"): # A shadow, hidden from the night
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = id
    def draw(self):
        self.simpleBox = self.canvas.create_rectangle(self.x-playerSize, self.y-playerSize, self.x+playerSize, self.y+playerSize, outline="black", fill=playerState, width=2)#Looks just like the player
    def move(self):
        mycanvas.coords(self.simpleBox,items[0].x-playerSize,items[0].y-playerSize,items[0].x+playerSize,items[0].y+playerSize)# Always moves to whereever the player goes
    def collision(self):
        pass # if you collide with it nothing happends, ever.

    
class sizeChange():
    """A nice little block that changes the player size on collision."""
    x = 0
    y = 0
    xdist = 0
    ydist = 0
    def __init__(self,canvas,x,y,change,id="sizeChange"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = id
        self.change = change
    def draw(self):
        self.simpleBox = self.canvas.create_rectangle(self.x-15,self.y-15,self.x+15,self.y+15,fill="light gray") # This is the basic grey box
        if self.change > 0:
            self.plat = platform(mycanvas,self.x-5,self.x+5,self.y-10,self.y+3,"light green",0,0)
            self.plat2 = platform(mycanvas,self.x-10,self.x+10,self.y+3,self.y+5,"light green",0,0)
            self.plat3 = platform(mycanvas,self.x-8,self.x+8,self.y+5,self.y+7,"light green",0,0)
            self.plat4 = platform(mycanvas,self.x-6,self.x+6,self.y+7,self.y+9,"light green",0,0)
            self.plat5 = platform(mycanvas,self.x-4,self.x+4,self.y+9,self.y+11,"light green",0,0)
            self.plat6 = platform(mycanvas,self.x-2,self.x+2,self.y+11,self.y+13,"light green",0,0) # All these platform objects create the shape of an arrow like ->. Showing if your getting bigger or smaller
        else:
            self.plat =  platform(mycanvas,self.x-5,self.x+5,self.y+10,self.y-3,"light blue",0,0)
            self.plat2 = platform(mycanvas,self.x-10,self.x+10,self.y-3,self.y-5,"light blue",0,0)
            self.plat3 = platform(mycanvas,self.x-8,self.x+8,self.y-5,self.y-7,"light blue",0,0)
            self.plat4 = platform(mycanvas,self.x-6,self.x+6,self.y-7,self.y-9,"light blue",0,0)
            self.plat5 = platform(mycanvas,self.x-4,self.x+4,self.y-9,self.y-11,"light blue",0,0)
            self.plat6 = platform(mycanvas,self.x-2,self.x+2,self.y-11,self.y-13,"light blue",0,0)
        items.append(self.plat)
        items.append(self.plat2)
        items.append(self.plat3)
        items.append(self.plat4)
        items.append(self.plat5)
        items.append(self.plat6)# Needs to be added to the overall items list so that collisions don't get messed up      
    def move(self):
        pass     # This class never moves so dosen't need to be moved
    def collision(self):
        global invincibility
        colourList = ["light blue","hot pink","yellow","light green"]
        invincibility = 100
        if self.change > 0:
                for i in range(10):
                    makeSmall()
                    #mycanvas.move(items[0].playerBox,0,1)
                    #items[0].y += 1
                    for obj in items: 
                        if obj.id == ("shadow"):
                            obj.move() # keeps the shadow updated with the player model.
                    mywindow.update()
                    time.sleep(0.02)
                    items.append(bubble(self.canvas,random.randint(self.x-playerSize,self.x+playerSize),random.randint(self.y-playerSize,self.y+playerSize),0,random.choice(colourList)))
                    items[len(items)-1].draw()
        else:
                for i in range(10):
                    makeBig()
                    #mycanvas.move(items[0].playerBox,0,1)
                    #items[0].y += 1
                    for obj in items:
                        if obj.id == ("shadow"):
                            obj.move() # keeps the shadow updated with the player model.
                    mywindow.update()
                    time.sleep(0.02)
                    try:
                        items.append(bubble(self.canvas,random.randint(self.x-playerSize,self.x+playerSize),random.randint(self.y-playerSize,self.y+playerSize),0,random.choice(colourList)))
                        items[len(items)-1].draw()
                    except:
                        pass
        items.remove(self)
        items.remove(self.plat)
        items.remove(self.plat2)
        items.remove(self.plat3)
        items.remove(self.plat4)
        items.remove(self.plat5)
        items.remove(self.plat6)
        mycanvas.delete(self.simpleBox)
        mycanvas.delete(self.plat.block)
        mycanvas.delete(self.plat2.block)
        mycanvas.delete(self.plat3.block)
        mycanvas.delete(self.plat4.block)
        mycanvas.delete(self.plat5.block)
        mycanvas.delete(self.plat6.block)
        # This removes the arrow head and grey box from the screen so that it is not seen anymore.


class textBox():
    """An object that looks like a sign post, on collision a message is shown on the screen"""
    def __init__(self,canvas,x,y,textToWrite,id="textBox",read=False):# read=False, can only be read once, or else it would get in the way
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = id
        self.textToWrite = textToWrite
        self.read = read
    def draw(self):
        self.simpleBox = self.canvas.create_rectangle(self.x-23,self.y-12,self.x+23,self.y+12,fill="saddle brown")
        items.append(platform(mycanvas,self.x-3,self.x+3,self.y+12,self.y+32,"saddle brown",0.01,0))
        items.append(platform(mycanvas,self.x-20,self.x+20,self.y-10,self.y+10,"papaya whip",0.01,0))
        items.append(platform(mycanvas,self.x-15,self.x+15,self.y-6,self.y-5,"black",0.01,0))
        items.append(platform(mycanvas,self.x-15,self.x+15,self.y-3,self.y-2,"black",0.01,0))
        items.append(platform(mycanvas,self.x-15,self.x+15,self.y,self.y+1,"black",0.01,0))
        items.append(platform(mycanvas,self.x-15,self.x+15,self.y+3,self.y+4,"black",0.01,0)) # All these platforms make the shape of a little sign post, like how it was in super mario 64   http://insidermedia.ign.com/insider/image/article/568/568932/super-mario-64-face-off-20041124094038097.jpg
    def move(self):
        pass # Sign posts dont move last time I checked
    def collision(self):
        if self.read == False: 
            blackBox = mycanvas.create_rectangle(100,100,700,400,fill="black")
            whiteBox = mycanvas.create_rectangle(104,104,696,396,fill="white")
            textList = self.textToWrite.split("\\n")
            textItemList = []
            for i in range(len(textList)):
                textItemList.append(mycanvas.create_text(400,150 + i*20,text=textList[i],fill="black",font=("courier 16")))
            for i in range(len(self.textToWrite)):
                mywindow.update()
                # Creates a screen that pops up, gives you enough time to read the message
                if EButtonPressed == False:
                    mywindow.after(40)
                else:
                    break
            mycanvas.delete(blackBox)
            mycanvas.delete(whiteBox)
            for textItem in textItemList:
                mycanvas.delete(textItem)
            self.read = True # So can't be read again

            
class Scenary():
    """An image that is in the background, does not interact with the player."""
    def __init__(self,canvas,x,y,image,zoomDist,id="scenary"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = image
        self.id = id
        self.zoomDist = zoomDist
    def draw(self):
        self.simpleBox = tk.PhotoImage(file=(str(self.image) + ".gif")) # Loads the image
        if self.zoomDist > 0:
            self.simpleBox = self.simpleBox.zoom(self.zoomDist)
        else:
            self.simpleBox = self.simpleBox.subsample(abs(self.zoomDist))#Zooms in or out of the image
        self.label = tk.Label(image=self.simpleBox)
        self.label.image = self.simpleBox # Needs a label so that it dosen't fall into the void of nothingness. With nothing to hold onto, like an otter will hold onto drifwood to keep itself right.
        self.simpleBox = mycanvas.create_image(self.x,self.y,image=self.simpleBox)
    def move(self):
        pass
    def collision(self):
        pass
    def resolution(self):
        tempImage = tk.PhotoImage(file=(str(self.image) + ".gif"))
        return tempImage.width(),tempImage.height()


class Turret():
    """The biggest and baddest around, one hit one kill, never misses. Bam bam bam"""
    x = 0
    y = 0
    xdist = 0
    ydist = 0
    coolDown = 0 # Rate of fire
    def __init__(self,canvas,x,y,coolDown,homing,id="turret"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = id
        self.coolDown = coolDown
        self.homing = homing # homing is a boolean, which decided weather the trajectory is linear or ballistic
    def draw(self):
        self.simpleBox = self.canvas.create_rectangle(self.x-15,self.y-15,self.x+15,self.y+15,fill="light gray") # I need to imporve the apperace of the turret
    def move(self):
        if self.coolDown == 0:
            distanceTurretToPlayer = math.sqrt((self.x - items[0].x)**2 + (self.y - items[0].y)**2)#Calculates the distance of the player to the turret, so that we can find if the turret has a line of sight on the player to fire a shot.
            lineOfSight = self.canvas.create_line(self.x,self.y,items[0].x,items[0].y)#,state=tk.HIDDEN)
            allOverlaps = mycanvas.find_overlapping(-10000,-10000,10000,10000)
            canSee = True
            for item in items:
                if item.id == ("ground"): #or item.id == ("movingPlatform") or item.id == ("lava"):
                    overlaps = (mycanvas.find_overlapping(item.x1,item.y1,item.x2,item.y2))
                    if allOverlaps[len(allOverlaps)-1] in overlaps:
                        canSee = False
            if canSee == True and distanceTurretToPlayer < 700:
                if self.homing == ("TRUE"):
                    items.append(Bullet(self.canvas,self.x,self.y,0,0,[self.x,self.y],True))# Notice the change between TRUE
                else:
                    items.append(Bullet(self.canvas,self.x,self.y,0,0,[self.x,self.y],False))# and FALSE
                items[len(items)-1].draw()            
            mycanvas.delete(lineOfSight)
            self.coolDown = 100#This number can be changed to change the rate of fire
        else:
            self.coolDown -= 1 # every frame where you arn't caught in this mad man's sights, he counts down from 50, before he can unleash anohter shot upon an unsuspecting player.

    def collision(self):
        global level
        for obj in items:
            if obj.id == ("turret"):
                overlaps =(mycanvas.find_overlapping(obj.x-10,obj.y-10,obj.x+10,obj.y+10))
                allItems = (mycanvas.find_overlapping(0,0,800,500))
                if allItems[1] in overlaps:
                    if invincibility == False:
                        playerHit()



class Bullet():
    """A projectile that can be linear or ballistic depending on the homing boolean"""
    def __init__ (self,canvas,x,y,xdist,ydist,start,homing,id="bullet"):
        self.canvas = canvas
        self.start = start
        self.x = x
        self.y = y
        self.xdist = xdist
        self.ydist = ydist
        self.homing = homing
        if items[0].x -self.start[0] > 0:  
            self.xdist = 3
        else:
            self.xdist = -3
        if (items[0].y -self.y ) != 0:
            self.ydist = ((items[0].y -self.y ))/abs((items[0].x -self.x ))*3#/(abs(items[0].x - self.x)))
        else:
            self.ydist = 0
        if self.ydist > 5:
            self.ydist = 5
        if self.ydist < -5:
            self.ydist = -5
        self.id = id
    def draw(self):
        self.simpleBox = self.canvas.create_oval(self.start[0]-3,self.start[1]-3,self.start[0]+3,self.start[1]+3,fill="red")
        if items[0].x > self.start[0]:   
            mycanvas.move(self.simpleBox,10,0)
        else:
            mycanvas.move(self.simpleBox,-10,0)
    def move(self):
        if self.homing == True:
            if items[0].x -self.x > 0:  
                self.xdist += 0.25
            else:
                self.xdist -= 0.25
            if items[0].y -self.y > 0:    
                self.ydist = ((items[0].y -self.start[1] ) /(abs(items[0].x - self.start[0]))) *3
            else:
                self.ydist = -((items[0].y -self.start[1] ) /(abs(items[0].x - self.start[0]))) *3
        self.x += self.xdist
        self.y += self.ydist
        mycanvas.move(self.simpleBox,self.xdist,self.ydist)
    def collision(self):
        global level
        for obj in items:
            if obj.id == ("bullet"):
                overlaps =(mycanvas.find_overlapping(obj.x-3,obj.y-3,obj.x+3,obj.y+3))
                #allItems = (mycanvas.find_overlapping(-10000,-10000,10000,10000))
                allItems = (mycanvas.find_overlapping(0,0,800,500))
                if allItems[1] in overlaps:
                    if invincibility == False:
                        playerHit()
                        
                        
                if self.x > 800 or self.x < 0 or self.y > 500 or self.y < 0:
                    self.canvas.delete(self.simpleBox)
                    #Outside the screen
                    try:
                        items.remove(self)
                    except:
                        pass

                    
class platform():
    """A solid object the player can jump onto, walk into the side of, and it the source of must of my pain with bugs."""
    x1,x2,y1,y2 = 0,0,0,0
    def __init__(self,canvas,x1,x2,y1,y2,colour,xdist,ydist,sinking=False,id="ground"):
        self.canvas = canvas
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.colour = colour # colour can be any tkiner colour (wow that's really cool Jonathan)
        self.xdist = xdist
        self.ydist = ydist
        self.id = id
        self.sinking = sinking
    def move(self):
        self.canvas.move(self.block,self.xdist,self.ydist)
        self.x1 = self.x1 + self.xdist
        self.y1= self.y1 + self.ydist
        self.x2 = self.x2 + self.xdist
        self.y2= self.y2 + self.ydist
        if self.sinking == (True):
            self.ydist = 2               
    def draw(self):
        self.block = self.canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill=str(self.colour))# It's just a rectangle at the end of the day
    def collision(self):
        global onGround,items,againstObj,onGround,movingUp,mywindow,mycanvas,Jumping   
        if self.sinking == ("TRUE"):
            self.sinking = True
        # These collisions push the player either up or down on collision to put them on the surpace of the rectangle as opposed to inside it.
        if items[0].x+playerSize - 1 > self.x1 and items[0].x-playerSize + 1 < self.x2:
        # This line above fixed a bug where players could jump against a column of crates and appear to stick to the side boundry
        # When they shouldn't be able to, so an extra x check is now done to make sure that the player is within the boxes
        # coords to make sure it can actually land on the surphace of the box
            if items[0].y - playerSize < self.y1:
                tempYdist = (self.y1 - items[0].y - playerSize)
                if tempYdist <= 0:
                    mycanvas.move(items[0].simpleBox,0,tempYdist)
                    items[0].ydist = 0
                    items[0].y = 8
                    items[0].y = self.y1 - playerSize
                    onGround = True
            elif items[0].y - items[0].ydist - playerSize < self.y1:
                tempYdist = (self.y1 - items[0].y - playerSize)        
                if tempYdist <= 0:
                    mycanvas.move(items[0].simpleBox,0,tempYdist)
                    items[0].ydist = 0
                    items[0].y = self.y1 - playerSize
                    onGround = True
            else: # Hitting Roof
                if items[0].y + playerSize > self.y2 or  items[0].y + playerSize + items[0].ydist > self.y2:   
                    onGround = False
                    items[0].ydist = playerSize
                    items[0].y = items[0].y + items[0].ydist
                    mycanvas.move(items[0].simpleBox,0,items[0].ydist)
                    items[0].ydist = 0
        # Sides
        overlaps =(mycanvas.find_overlapping(self.x1,self.y1+1,self.x2,self.y2))
        allItems = (mycanvas.find_overlapping(-10000,-10000,10000,10000))
        if allItems[1] in overlaps:
            if items[0].x+playerSize-5 < self.x1 or items[0].x-playerSize+5 > self.x2:
                if items[0].x-playerSize-items[0].xdist - ((self.x1 + self.x2)/2) > 0:
                        againstObj = ("Left")
                        items[0].xdist = (self.x2 - items[0].x -items[0].xdist + playerSize ) +1
                        items[0].x = items[0].x + items[0].xdist
                        mycanvas.move(items[0].simpleBox,items[0].xdist,0)
                        items[0].xdist = 0 
                else: 
                        againstObj = ("Right")
                        items[0].xdist = -(items[0].x + playerSize - self.x1) -1
                        items[0].x = items[0].x + items[0].xdist
                        mycanvas.move(items[0].simpleBox,items[0].xdist,0)
                        items[0].xdist = 0
        if self.sinking == True:
            mycanvas.move(items[0].simpleBox,0,self.ydist)
            items[0].y += self.ydist  
        # Against Obj is used so the player can't continue walking through the solid object.
        # A great deal of bug fixing was done on this collision detection, as it is a very long segment so was prone to bugs of passing through walls and floor
        # occasionally. To fix this, the location of the prior frame was checked to make sure the trajectory was consistent.
        # Also the hitting a roof function was called incorrectly many times which was the primary reason for passing through walls or floor.
# FPS = 90 to 110
# FPS = 600 to 1000
# This was achieved by changing the way collisions with the platforms were carried out. In the prior version, platforms on collision would check every other
# Platform for a collision and carry out lots of lines of code. Avaliable in the class Platform of versions 2.4 and prior
# This reduced the time of collisions by a lot as every other platform did not need to be checked, as now
# the collisions were called depending on weatehr the player had collided with the platform so we alredy knew the collison had been done
# MASSIVE ongoing bug to do with moving platforms. Every time a moving platforms collision() is ran everything seems to mess up. In erratic ways. Some moving platforms
# start to fall by themselves, incorrect collisions are called. When coins are collided with incorrect coins will be triggered. I have yet to find a fix


class lava():
    """A firey bubbling behemoth, immediate death on impact"""
    x1,x2,y1,y2 = 0,0,0,0
    def __init__(self,canvas,x1,x2,y1,y2,id="lava"):
        self.canvas = canvas
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.id = id
    def move(self):
        randomX = random.randint(self.x1+12,self.x2-12)
        randomY = random.randint(self.y2-20,self.y2-12) # Creates a randomly positioned bubble
        if random.random() > 0.2: # so only one in every five times a bubble is made, to stop there being too many bubblies
            items.append(bubble(self.canvas,randomX,randomY,self.y1))
            items[len(items)-1].draw()
    def draw(self):
        self.block = self.canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill="red")# The lava itself is a red rectangle
    def collision(self):
        global onGround,items,againstObj,onGround,movingUp,mywindow,mycanvas,Jumping,level,lifes
        if invincibility == False:
            for obj in items:
                if obj.id == ("lava"):
                    overlaps =(mycanvas.find_overlapping(obj.x1+3,obj.y1,obj.x2-3,obj.y2))
                    allItems = (mycanvas.find_overlapping(-10000,-10000,10000,10000))
                    if allItems[1] in overlaps:
                        if invincibility == False:
                            level -= 1
                            lifes -= 1
                            newLevel()
                            obj.collision() # Instant death on collision


class enemy():
    """  patrols an area with death on impact"""
    def __init__(self,canvas,x,y,x1,x2,id="enemy"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.x1 = x1
        self.x2 = x2
        self.speed = 3
        self.frame = 1
        self.y1 = 0
        self.y2 = 0   
        self.id = id
        self.frames = [tk.PhotoImage(file="Enemy1.gif"),tk.PhotoImage(file="Enemy2.gif"),tk.PhotoImage(file="Enemy3.gif"),tk.PhotoImage(file="Enemy4.gif")]
        #self.frames   
    def draw(self):
        self.im = self.frames[self.frame] # Loads the image
        self.label = tk.Label(image=self.im)
        self.label.image = self.im # Needs a label so that it dosen't fall into the void of nothingness. With nothing to hold onto, like an otter will hold onto drifwood to keep itself right.
        self.block = mycanvas.create_image(self.x,self.y,image=self.im)
    def move(self):
        self.canvas.move(self.block,self.speed,0)
        self.x = self.x + self.speed
        self.frame += 1
        if self.frame == 4:
            self.frame = 0
        nextImage = self.frames[self.frame] # updates to the next  frame of the animation
        mycanvas.itemconfig(self.block,image=nextImage)
        self.label.configure(image=nextImage)
        self.label.image = nextImage
        if self.x > self.x2:
            self.speed = -3      
        if self.x < self.x1:
            self.speed = 3
    def collision(self):
        global level
        if items[0].x  > self.x-2*playerSize and items[0].x  < self.x+2*playerSize and items[0].y  > self.y-2*playerSize and items[0].y  < self.y+2*playerSize:
            if invincibility == False:
                playerHit()
#116.9 fps       
# to
# 1187 fps
# WOW, thats great news, The frame rate was improved from 116 all the way to 1187,
#this was achieved by loading all the animation frames initially,
#then calling them each frame,
#rather than loading a new image every frame. I didn't expect such a dramatic frame increase


class jumpEnemy():
    """  patrols an area with death on impact"""
    def __init__(self,canvas,x,y,x1,x2,jumpTimes,id="jumpEnemy"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.x1 = x1
        self.x2 = x2
        self.speed = 3
        self.frame = 1
        self.y1 = 0
        self.y2 = 0   
        self.id = id
        self.ydist = 0
        self.height = self.y
        self.jumping = False
        jumpTimes = jumpTimes.split(",")
        for i in range(len(jumpTimes)):
            jumpTimes[i] = float((float(self.x2)- float(self.x1)) * float(jumpTimes[i]) + float(self.x1)) 
        self.jumpTimes = jumpTimes
        self.frames = [tk.PhotoImage(file="JumpEnemy1.gif"),tk.PhotoImage(file="JumpEnemy2.gif"),tk.PhotoImage(file="JumpEnemy3.gif"),tk.PhotoImage(file="JumpEnemy4.gif")]
    def draw(self):
        self.im = self.frames[self.frame] # Loads the image
        self.label = tk.Label(image=self.im)
        self.label.image = self.im # Needs a label so that it dosen't fall into the void of nothingness. With nothing to hold onto, like an otter will hold onto drifwood to keep itself right.
        self.block = mycanvas.create_image(self.x,self.y,image=self.im)
    def move(self):
        self.canvas.move(self.block,self.speed,self.ydist)
        self.x = self.x + self.speed
        if self.x > self.x2:
            self.speed = -3      
        if self.x < self.x1:
            self.speed = 3
        self.frame += 1
        if self.frame == 4:
            self.frame = 1
        if self.jumping == False:
            if self.x in self.jumpTimes:
                self.jumping = True
                self.ydist = -15
        if self.jumping == True:
            if self.ydist < 14:
                self.ydist += 1
            else:
                self.jumping = False
                self.ydist = 0
        nextImage = self.frames[self.frame] # updates to the next  frame of the animation
        mycanvas.itemconfig(self.block,image=nextImage)
        self.label.configure(image=nextImage)
        self.label.image = nextImage       
    def collision(self):
        global level
        if invincibility == False:
            playerHit()

            
class mine():
    """On collision the mine explodes and shoots the player into a random direction"""
    def __init__(self,canvas,x,y,id="mine"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = id
        self.exploded = False
        self.frames = [tk.PhotoImage(file="Mine1.gif"),tk.PhotoImage(file="Mine2.gif"),tk.PhotoImage(file="Mine3.gif"),tk.PhotoImage(file="Mine4.gif"),tk.PhotoImage(file="Mine5.gif"),tk.PhotoImage(file="Mine6.gif"),tk.PhotoImage(file="Mine7.gif")]#,tk.PhotoImage(file="Mine5.gif"),tk.PhotoImage(file="Mine6.gif"),tk.PhotoImage(file="Mine7.gif")]#tk.PhotoImage(file="Mine4.gif")]
        self.frame = 1
    def draw(self):
        self.im = self.frames[0] # Loads the image
        self.label = tk.Label(image=self.im)
        self.label.image = self.im # Needs a label so that it dosen't fall into the void of nothingness. With nothing to hold onto, like an otter will hold onto drifwood to keep itself right.
        self.simpleBox = mycanvas.create_image(self.x,self.y,image=self.im)
    def collision(self):
        if self.exploded != ("Finished"):
            self.exploded = True
            items[0].xdist = random.randint(-20,20)
            items[0].ydist = random.randint(-25,-20)
    def move(self):
        if self.exploded == False:
            if self.frame == 1:
                nextImage = self.frames[1]
                self.frame = 2
            else:
                nextImage = self.frames[0]
                self.frame = 1
            mycanvas.itemconfig(self.simpleBox,image=nextImage)
            self.label.configure(image=nextImage)
            self.label.image = nextImage
        if self.exploded != ("Finished"):
            if self.exploded == True:
                self.frame += 0.25
                nextImage = self.frames[int(self.frame)]
                mycanvas.itemconfig(self.simpleBox,image=nextImage)
                self.label.configure(image=nextImage)
                self.label.image = nextImage
                if int(self.frame) == 6:
                    self.exploded = ("Finished")


class coin():
    """An image that is in the background, does not interact with the player."""
    def __init__(self,canvas,x,y,coinNumber=1,id="scenary"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.coinNumber = coinNumber
        self.id = id
        self.collided = False
        self.frames = [tk.PhotoImage(file="mine7.gif")]
    def draw(self):
        self.simpleBox = tk.PhotoImage(file="coin" + str(self.coinNumber) + ".gif") # Loads the image
        self.label = tk.Label(image=self.simpleBox)
        self.label.image = self.simpleBox # Needs a label so that it dosen't fall into the void of nothingness. With nothing to hold onto, like an otter will hold onto drifwood to keep itself right.
        self.simpleBox = mycanvas.create_image(self.x,self.y,image=self.simpleBox)
    def move(self):
        pass
    def collision(self):
        global numberOfCoins,numberOfCoinsGained,numberOfCoinsOnThisLevel
        if self.collided == False:
            numberOfCoinsOnThisLevel -= 1
            Thread(target=playSound,args=("CoinPickupSoundEffect",)).start()
            numberOfCoins += self.coinNumber
            numberOfCoinsGained += self.coinNumber
            self.collided = True
            nextImage = self.frames[0]
            mycanvas.itemconfig(self.simpleBox,image=nextImage)
            self.label.configure(image=nextImage)
            self.label.image = nextImage
            for i in range(2):
                if self.coinNumber == 1:
                    items.append(bubble(self.canvas,random.randint(self.x-10,self.x + 10),random.randint(self.y-10,self.y+10),self.y-300,"yellow",-5,2))
                if self.coinNumber == 10:
                    items.append(bubble(self.canvas,random.randint(self.x-10,self.x + 10),random.randint(self.y-10,self.y+10),self.y-300,"aqua",-5,2))
                items[len(items)-1].draw()
        if numberOfCoinsGained > 29:
            numberOfCoinsGained = 0
            playerUpgrade()
            

def playSound(fileToPlay):
    global soundJustPlayed
    if fileToPlay in ["ExtraLife","PlayerDegrade","PlayerUpgrade"]:
        PlaySound(str(fileToPlay) + (".wav"), SND_ASYNC| SND_FILENAME) # important sounds
        soundJustPlayed = ("Important")
    else:
        try:
            if soundJustPlayed == ("Important"):
                PlaySound(str(fileToPlay) + (".wav"),SND_ASYNC| SND_FILENAME|SND_NOSTOP) # uninportant
            else:
                PlaySound(str(fileToPlay) + (".wav"),SND_ASYNC| SND_FILENAME) # uninportant
            soundJustPlayed = ("Unimportant")
        except:
            pass

    
class character():
    def __init__(self,canvas,x,y,dialogue,characterNumber,colour,read,id="character"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = id
        self.dialogue = dialogue
        self.characterNumber = characterNumber
        self.colour = colour
        self.read = False
        self.frames = [tk.PhotoImage(file="Character " + str(characterNumber) + "-1.gif"),tk.PhotoImage(file="Character " + str(characterNumber) + "-2.gif")]
    def draw(self):
        self.im = self.frames[0] # Loads the image
        self.label = tk.Label(image=self.im)
        self.label.image = self.im # Needs a label so that it dosen't fall into the void of nothingness. With nothing to hold onto, like an otter will hold onto drifwood to keep itself right.
        self.simpleBox = mycanvas.create_image(self.x,self.y,image=self.im)
    def collision(self):       
            if items[0].x > self.x:
                nextImage = self.frames[0] 
            else:
                nextImage = self.frames[1]
            mycanvas.itemconfig(self.simpleBox,image=nextImage)
            self.label.configure(image=nextImage)
            self.label.image = nextImage
            if self.read == False:
                blackBox = mycanvas.create_rectangle(100,100,700,400,fill="black")
                whiteBox = mycanvas.create_rectangle(104,104,696,396,fill="white")
                textList = self.dialogue.split("\\n")
                textItemList = []
                for i in range(len(textList)):
                    textItemList.append(mycanvas.create_text(400,150 + i*20,text=textList[i],fill=self.colour,font=("courier 16")))
                # Creates a screen that pops up, gives you enough time to read the message
                for i in range(len(textItemList)*50):
                    mywindow.update()
                    if EButtonPressed == False:
                        mywindow.after(40)  
                    else:
                        break
                mycanvas.delete(blackBox)
                mycanvas.delete(whiteBox)
                for textItem in textItemList:
                    mycanvas.delete(textItem)
                self.read = True # So can't be read again

class bubble():
    """Lives a simple life of floating to the surphace and then popping."""
    global items
    def __init__(self,canvas,x,y,maxHeight,colour="red",speed=1.5,spread=1,size=[1,6],id="bubble"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = id
        self.maxHeight = maxHeight
        self.colour = colour
        self.speed = speed
        self.spread = spread
        self.size = size
        self.bubbleSize = random.randint(self.size[0],self.size[1])# different sized bubbles
    def move(self):
        randomY = random.randint(-self.spread,self.spread)
        self.canvas.move(self.simpleBox,randomY,-self.speed)
        self.y -= self.speed
        if self.y <= self.maxHeight or self.y > 500: # when above the surphace
            
            self.canvas.delete(self.simpleBox)
            try:
                items.remove(self)
            except:
                pass
        if self.colour in ["saddle brown","slate gray","light gray","sienna4","light slate gray"]:
            self.speed -= 0.2
    def draw(self):
        self.simpleBox = self.canvas.create_oval(self.x+self.bubbleSize,self.y-self.bubbleSize,self.x-self.bubbleSize,self.y+self.bubbleSize,fill=self.colour,outline="white")
    def collision(self):
        global level
        if self.colour == ("red") or self.colour in ["saddle brown","slate gray","light gray","sienna4","light slate gray"]:
            if invincibility == False:
                playerHit()


class levelEnd():
    """The goal of the level, to get to the end of the level"""
    x1,x2,y1,y2 = 0,0,0,0
    def __init__(self,canvas,x1,x2,y1,y2,xdist,ydist,id="levelEnd"):
        self.canvas = canvas
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.xdist = xdist
        self.ydist = ydist
        self.id = id
        self.timeToEnd = 60
        self.hasCollided = False 
    def move(self):
        global invincibility
        self.canvas.move(self.block,self.xdist,self.ydist)
        self.x1 = self.x1 + self.xdist
        self.y1 = self.y1 + self.ydist
        self.x2 = self.x2 + self.xdist
        self.y2 = self.y2 + self.ydist
        if self.hasCollided == True:
            invincibility = 100
            self.timeToEnd -= 1
            for i in range(10):
                items.append(bubble(self.canvas,random.randint(self.x1-playerSize,self.x1+playerSize),random.randint(self.y1-playerSize,self.y1+playerSize),0,"yellow",random.randint(-5,5),20))
                items[len(items)-1].draw()
            mywindow.attributes("-alpha", 1 - ((60-self.timeToEnd)/100))
            if self.timeToEnd == 0:
                mywindow.attributes("-alpha",1)
                invincibility = False
                self.timeToEnd = 60
                if numberOfCoinsOnThisLevel == 0:
                        playerUpgrade() # the playerUpgrades are done seperately so that both sound FX can be heard.     
                newLevel()
                
    def draw(self):
        self.block = self.canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill=("yellow"))# I think yellow is a good colour
    def collision(self):
        global onGround,items,movingUp,onGround,Jumping,mywindow,mycanvas
        found = False
        for obj in items:
            if obj.id == ("levelEnd"):
                if self.hasCollided == False:
                    if numberOfCoinsOnThisLevel == 0:
                        playerUpgrade()
                    overlaps =(mycanvas.find_overlapping(obj.x1+3,obj.y1,obj.x2-3,obj.y2))  #  Changed: overlaps =(mycanvas.find_overlapping(obj.x1,obj.y1,obj.x2,obj.y2))
                    allItems = (mycanvas.find_overlapping(0,0,800,500))
                    if allItems[1] in overlaps:
                        self.hasCollided = True


def myround(x, base=5):
    """I won't lie I goodled this"""
    #http://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python
    return int(base * round(float(x)/base)) 


def setxy(event):
    """This updates every mouse movement to keep the mouse coords accurate """
    global mousex,mousey,currentCoords,tempRect,deleteNextItem,onOption,mainMenuOption
    mousex = event.x
    mousey = event.y
    if mainMenu == True:
        updateImage = False
        onOption = False
        if mousex > 60 and mousex < 174 and mousey > 48 and mousey < 66:
            nextImage = frames[0] # updates to the next  frame 
            updateImage = True
            mainMenuOption = 0
        if mousex > 60 and mousex < 143 and mousey > 82 and mousey < 97:
            nextImage = frames[1] # updates to the next  frame 
            updateImage = True
            mainMenuOption = 1
        if mousex > 60 and mousex < 185 and mousey > 116 and mousey < 131:
            nextImage = frames[2] # updates to the next  frame 
            updateImage = True
            mainMenuOption = 2
        if mousex > 60 and mousex < 129 and mousey > 152 and mousey < 167:
            nextImage = frames[3] # updates to the next  frame of the animation
            updateImage = True
            mainMenuOption = 3
        if mousex > 60 and mousex < 176 and mousey > 185 and mousey < 203:
            nextImage = frames[4] # updates to the next  frame of the animation
            updateImage = True
            mainMenuOption = 4
        if updateImage == True:
            onOption = True
            mycanvas.itemconfig(menuLabelsimpleBox,image=nextImage)
            menuLabel.configure(image=nextImage)
            menuLabel.image = nextImage
    if createLevel == True:
        try:
            mycanvas.delete(tempRect)
        except:
            pass
        try:
            if deleteNextItem == True:
                if items[len(items)-1].id == ("scenary"):
                    mycanvas.delete(items[len(items)-1].simpleBox)
                    items.remove(items[len(items)-1])
                    deleteNextItem = False
        except:
            pass
                    #This is for the nice grey shadowy thing in the level editor
        if len(currentCoords) == 1:
            tempRect = mycanvas.create_rectangle(myround(currentCoords[0][0],gridSpacing),myround(currentCoords[0][1],gridSpacing),myround(mousex,gridSpacing),myround(mousey,gridSpacing),fill="gray",stipple="gray50")
        if len(currentCoords) == 0 and itemChoicesVar.get() == ("Text Box"):
            tempRect = mycanvas.create_rectangle(mousex-23,mousey-12,mousex+23,mousey+31,fill="gray",stipple="gray50")
        if len(currentCoords) == 0 and itemChoicesVar.get() == ("Trampoline"):
            tempRect = mycanvas.create_rectangle(mousex-20,mousey-10,mousex+20,mousey+10,fill="gray",stipple="gray50")
        if len(currentCoords) == 0 and itemChoicesVar.get() == ("Scenary"):
            scenaryItem = scenaryChoicesVar.get()
            spriteSize = spriteSlider.get()
            items.append(Scenary(mycanvas,myround(mousex,gridSpacing),myround(mousey,gridSpacing),scenaryChoicesVar.get(),spriteSize//20)) # Makes a temporary picture on the screen
            currentResolution = items[len(items)-1].resolution() # finds the resolution of it
            currentResolution = [currentResolution[0]*spriteSize//20,currentResolution[1]*spriteSize//20] # changes depending on res
            items.remove(items[len(items)-1]) # then deletes it from the screen
            items.append(Scenary(mycanvas,myround(mousex,gridSpacing),myround(mousey,gridSpacing)-(currentResolution[1]//2),scenaryChoicesVar.get(),spriteSize//20)) # makes a new picture with teh coordinates rounded in such a way so that the picture lies flush on the grid squares, rather than in the centre where the x,y coords are. Instead the picture gets put where the x+ res,y+ res coords are :p
            items[len(items)-1].draw()
            deleteNextItem = True
        if len(currentCoords) == 0 and itemChoicesVar.get() == ("Objects"):
            scenaryItem = scenaryChoicesVar.get()
            spriteSize = spriteSlider.get()
            items.append(Scenary(mycanvas,myround(mousex,gridSpacing),myround(mousey,gridSpacing),objectsChoicesVar.get(),spriteSize//20))
            currentResolution = items[len(items)-1].resolution() # finds the resolution of it
            currentResolution = [currentResolution[0]*spriteSize//20,currentResolution[1]*spriteSize//20] # changes depending on res
            items.remove(items[len(items)-1]) # then deletes it from the screen
            items.append(Scenary(mycanvas,myround(mousex,gridSpacing),myround(mousey,gridSpacing)-(currentResolution[1]//2),objectsChoicesVar.get(),spriteSize//20))
            items[len(items)-1].draw()
            deleteNextItem = True
        if len(currentCoords) == 0 and itemChoicesVar.get() == ("Enemy") or itemChoicesVar.get() == ("Jumping Enemy"):
            tempRect = mycanvas.create_rectangle(mousex-20,mousey-20,mousex+20,mousey+20,fill="gray",stipple="gray50")
def middleclickMotion(event):
    global mouseCoords,extraX,extraY  # The extraX and extraY are used for when the level editor is moved to keep the actual quornites in the correct position
    mouseCoords.append([event.x,event.y])
    if spawnUsed == True or loadLevel != False:
        if len(mouseCoords) == 4:
            mouseCoords = mouseCoords[len(mouseCoords)-2:]
            changeInX = mouseCoords[1][0] - mouseCoords[0][0]
            changeInY = mouseCoords[1][1] - mouseCoords [0][1]
            if changeInX < 0 :
                changeInX = -gridSpacing
            if changeInX > 0:
                changeInX = + gridSpacing
            if changeInY < 0:
                changeInY = -gridSpacing
            if changeInY > 0:
                changeInY = gridSpacing
            extraX += changeInX
            extraY += changeInY
            for obj in items:
                try:
                    if obj.id in ["player","turret","bubble","bullet","sizeChange","textBox","scenary","shadow","trampoline","character","shop","mine","boulder"]:
                        mycanvas.move(obj.simpleBox,changeInX,changeInY)
                        obj.x += changeInX
                        obj.y += changeInY
                    else:
                        mycanvas.move(obj.block,changeInX,changeInY)
                        obj.x1 += changeInX
                        obj.x2 += changeInX
                        obj.y1 += changeInY
                        obj.y2 += changeInY
                except: # Means it must be a moving platform as this cannot have an obj id, because of the stipple
                    mycanvas.move(obj,changeInX,changeInY)   
            mouseCoords = []
def mouseclickWindow(event):
    if mousex < 127 and mousey > 20:
        updateGrid()

        
def mouseclick(event):	
    global mousex,mousey,currentCoords,newLevelObjectList,items,mycanvas,errorMessage,errorLabel,spawnUsed,gridSnap,gridSpacing,mainMenu,playCredits,Instructions,createLevel
    if createLevel == True:
        errorLabel.configure(text="Level Creator")
        objectToCreate = itemChoicesVar.get()
        # means it's a simple Box type obhect
        if objectToCreate != ("Scenary") and objectToCreate != ("Objects"):
            currentCoords.append([myround(mousex,gridSpacing),myround(mousey,gridSpacing)])
        else:
            currentCoords.append([mousex,mousey])
        try:
            currentColour = colourTextBox.get('1.0','end-1c')
        except:
            try:
                currentText = textTextBox.get('1.0','end-1c')
            except:
                pass
            pass
        if len(currentCoords) == 1:   
            if spawnUsed == False:
                if objectToCreate == ("Player Start"):
                    spawnUsed = True
                    newLevelObjectList.append(["player",currentCoords[0][0]-extraX,currentCoords[0][1]-extraY,True])
                    items.append(player(mycanvas,currentCoords[0][0],currentCoords[0][1],True))
                    items[len(items)-1].draw()
                    currentCoords = []
            else:
                if objectToCreate == ("Player Start"):
                    currentCoords = []
                    errorMessage = ("Only One Player\n Start Allowed")
            if objectToCreate == ("Turret"):
                newLevelObjectList.append(["turret",currentCoords[0][0]-extraX,currentCoords[0][1]-extraY,"FALSE"])
                items.append(Turret(mycanvas,currentCoords[0][0],currentCoords[0][1],0,"FALSE"))
                items[len(items)-1].draw()
                currentCoords = []
            if objectToCreate == ("Turret") and homingTurret == True:
                newLevelObjectList.append(["turret",currentCoords[0][0]-extraX,currentCoords[0][1]-extraY,"TRUE"])
                items.append(Turret(mycanvas,currentCoords[0][0],currentCoords[0][1],0,"TRUE"))
                items[len(items)-1].draw()
                currentCoords = []
            if objectToCreate == ("Size Down"):
                newLevelObjectList.append(["sizeChange",currentCoords[0][0]-extraX,currentCoords[0][1]-extraY,10])
                items.append(platform(mycanvas,currentCoords[0][0]-15,currentCoords[0][0]+15,currentCoords[0][1]-15,currentCoords[0][1]+15,"gray",0,0))
                items[len(items)-1].draw()
                currentCoords = []
            if objectToCreate == ("Size Up"):
                newLevelObjectList.append(["sizeChange",currentCoords[0][0]-extraX,currentCoords[0][1]-extraY,-10])
                items.append(platform(mycanvas,currentCoords[0][0]-15,currentCoords[0][0]+15,currentCoords[0][1]-15,currentCoords[0][1]+15,"gray",0,0))
                items[len(items)-1].draw()
                currentCoords = []
            if objectToCreate == ("Text Box"):
                currentText = textTextBox.get('1.0','end-1c')
                if len(currentText) > 0:
                    newLevelObjectList.append(["textBox",currentCoords[0][0]-extraX,currentCoords[0][1]-extraY,currentText])
                    items.append(platform(mycanvas,currentCoords[0][0]-23,currentCoords[0][0]+23,currentCoords[0][1]-12,currentCoords[0][1]+32,"saddle brown",0,0))
                    items[len(items)-1].draw()
                    currentCoords = []
                else:
                    errorMessage = ("No Text For Text Box")
                    currentCoords = []
            if objectToCreate == ("Scenary") or objectToCreate == ("Objects"):
                    spriteSize = spriteSlider.get()
                    currentResolution = items[len(items)-1].resolution() # finds the resolution of it # then deletes it from the screen
                    currentResolution = [currentResolution[0]*spriteSize//20,currentResolution[1]*spriteSize//20]
                    scenaryItem = scenaryChoicesVar.get()
                    if objectToCreate == ("Objects"):
                        scenaryItem = objectsChoicesVar.get()
                    items.append(platform(mycanvas,myround(currentCoords[0][0],gridSpacing)-(currentResolution[0]//2),myround(currentCoords[0][1],gridSpacing)-(currentResolution[1]),myround(currentCoords[0][0],gridSpacing)+(currentResolution[0]//2),myround(currentCoords[0][1],gridSpacing),"grey",0,0))
                    newLevelObjectList.append([scenaryItem,myround(currentCoords[0][0],gridSpacing)-extraX,myround(currentCoords[0][1],gridSpacing)-extraY-(currentResolution[1]//2),spriteSize//20])
                    currentCoords = []
            if objectToCreate == ("Trampoline"):
                items.append(trampoline(mycanvas,myround(currentCoords[0][0],gridSpacing),myround(currentCoords[0][1],gridSpacing)))
                items[len(items)-1].draw()
                newLevelObjectList.append(["trampoline",myround(currentCoords[0][0],gridSpacing)-extraX,myround(currentCoords[0][1],gridSpacing)-extraY])
                currentCoords = []
            if objectToCreate == ("Coin"):
                items.append(coin(mycanvas,myround(currentCoords[0][0],gridSpacing),myround(currentCoords[0][1],gridSpacing)))
                items[len(items)-1].draw()
                newLevelObjectList.append(["coin",myround(currentCoords[0][0],gridSpacing)-extraX,myround(currentCoords[0][1],gridSpacing)-extraY])
                currentCoords = []    
        if len(currentCoords) == 2:
            if currentCoords[0][0] > currentCoords[1][0]:
                currentCoords[0][0],currentCoords[1][0] = currentCoords[1][0],currentCoords[0][0]
            if currentCoords[0][1] > currentCoords[1][1]:
                currentCoords[0][1],currentCoords[1][1] = currentCoords[1][1],currentCoords[0][1]
            if objectToCreate == ("Platform"):
                if len(colourTextBox.get('1.0','end-1c')) != 0:
                    try:
                        if sinkingCheckBox.var.get() == ("0"):
                            newLevelObjectList.append(["platform",currentCoords[0][0]-extraX,currentCoords[1][0]-extraX,currentCoords[0][1]-extraY,currentCoords[1][1]-extraY,str(colourTextBox.get('1.0','end-1c')),0,0])
                        if sinkingCheckBox.var.get() == ("1"):
                            newLevelObjectList.append(["platform",currentCoords[0][0]-extraX,currentCoords[1][0]-extraX,currentCoords[0][1]-extraY,currentCoords[1][1]-extraY,str(colourTextBox.get('1.0','end-1c')),0,0,"True"])
                        items.append(platform(mycanvas,currentCoords[0][0],currentCoords[1][0],currentCoords[0][1],currentCoords[1][1],str(colourTextBox.get('1.0','end-1c')),0,0))
                        items[len(items)-1].draw()
                        currentCoords = []
                    except:
                        errorMessage = ("Please enter\na valid colour")
                        currentCoords = []
                else:
                    errorMessage = ("Please enter a colour")
                    currentCoords = []
            if objectToCreate == ("Level End"):
                newLevelObjectList.append(["level end",currentCoords[0][0]-extraX,currentCoords[1][0]-extraX,currentCoords[0][1]-extraY,currentCoords[1][1]-extraY,0,0])
                items.append(levelEnd(mycanvas,currentCoords[0][0],currentCoords[1][0],currentCoords[0][1],currentCoords[1][1],0,0))
                items[len(items)-1].draw()
                currentCoords = []
            if objectToCreate == ("Lava"):
                if currentCoords[1][0] - currentCoords[0][0] > 24:
                    newLevelObjectList.append(["lava",currentCoords[0][0]-extraX,currentCoords[1][0]-extraX,currentCoords[0][1]-extraY,currentCoords[1][1]-extraY])
                    items.append(lava(mycanvas,currentCoords[0][0],currentCoords[1][0],currentCoords[0][1],currentCoords[1][1]))
                    items[len(items)-1].draw()
                    currentCoords =[]
                else:
                    currentCoords = []
                    errorMessage = ("Lava block too small, i cant fit\nany bubbles in there")
            if objectToCreate == ("Enemy") or objectToCreate == ("Jumping Enemy"):
                if objectToCreate == ("Jumping Enemy"):
                    jumpCoords = jumpCoordsBox.get('1.0','end-1c')
                    newLevelObjectList.append(["jumpEnemy",currentCoords[0][0]-extraX,currentCoords[0][1]-extraY,currentCoords[0][0]-extraX,currentCoords[1][0]-extraX,jumpCoords])
                    items.append(jumpEnemy(mycanvas,currentCoords[0][0],currentCoords[0][1],currentCoords[0][0],currentCoords[1][0],jumpCoords))
                else:
                    newLevelObjectList.append(["enemy",currentCoords[0][0]-extraX,currentCoords[0][1]-extraY,currentCoords[0][0]-extraX,currentCoords[1][0]-extraX])
                    items.append(enemy(mycanvas,currentCoords[0][0],currentCoords[0][1],currentCoords[0][0],currentCoords[1][0]))
                items[len(items)-1].draw()
                items.append(platform(mycanvas,currentCoords[0][0],currentCoords[1][0],currentCoords[0][1]-20,currentCoords[0][1]+20,"gray",0,0))
                items[len(items)-1].draw()
                currentCoords = []
        if len(currentCoords) == 3:
            if objectToCreate == ("Moving Platform"):
                speed = speedTextBox.get('1.0','end-1c')
                if len(speed) > 0:
                    try:
                        maxDistance = currentCoords[2][0]-(currentCoords[1][0]-currentCoords[0][0])  # #
                        newLevelObjectList.append(["movingPlatform",currentCoords[0][0]-extraX,currentCoords[1][0]-extraX,currentCoords[0][1]-extraY,currentCoords[1][1]-extraY,str(colourTextBox.get('1.0','end-1c')),currentCoords[0][0]-extraX,maxDistance-extraX,speed])
                        items.append(platform(mycanvas,currentCoords[0][0],currentCoords[1][0],currentCoords[0][1],currentCoords[1][1],str(colourTextBox.get('1.0','end-1c')),0,0))
                        items.append(platform(mycanvas,currentCoords[2][0]-(currentCoords[1][0]-currentCoords[0][0]),currentCoords[2][0],currentCoords[0][1],currentCoords[1][1],str(colourTextBox.get('1.0','end-1c')),0,0))
                        items[len(items)-1].draw()
                        items[len(items)-2].draw()
                        items.append(mycanvas.create_rectangle(currentCoords[0][0],currentCoords[0][1],currentCoords[2][0],currentCoords[1][1],fill=str(colourTextBox.get('1.0','end-1c')),stipple="gray50"))
                        currentCoords = []
                    except:
                        errorMessage = ("Please enter\na valid colour\nValid speed.")
                        currentCoords = []
                else:
                    currentCoords = []
                    errorMessage = ("Please give a speed\nfor the moving platform.")
        errorLabel.configure(text=str(errorMessage))

    if mainMenu == True:
        if onOption == True:
            if mainMenuOption == 0:
                mainMenu = False
            if mainMenuOption == 3:
                playCredits = True
            if mainMenuOption == 1:
                Instructions = True
            if mainMenuOption == 2:
                webbrowser.open("https://www.youtube.com/watch?v=dfi83HLLE8A")
            if mainMenuOption == 4:
                createLevel = True
                
                mainManu = False

         
class movingPlatform():
    """A platform that moves."""
    x1,x2,y1,y2 = 0,0,0,0
    def __init__(self,canvas,x1,x2,y1,y2,colour,minX,maxX,speed,id="movingPlatform"):
        self.canvas = canvas
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.colour = colour
        self.maxX = maxX
        self.minX = minX
        self.speed = speed
        self.id = id
    def move(self):
        self.canvas.move(self.block,self.speed,0)
        if onMovingPlatforms == True:
                overlaps =(mycanvas.find_overlapping(self.x1+3,self.y1,self.x2-3,self.y2))
                allItems = (mycanvas.find_overlapping(0,0,800,500))
                if allItems[1] in overlaps:
                    self.canvas.move(items[0].simpleBox,self.speed,0)
                    items[0].x = items[0].x + self.speed
        self.x1 = self.x1 + self.speed
        self.x2 = self.x2 + self.speed
        if self.x1 > self.maxX:          
            self.speed = self.speed - 2*self.speed
        if self.x1 < self.minX:
            self.speed = abs(self.speed)
    def draw(self):
        self.block = self.canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill=str(self.colour))
    def collision(self):
        global onGround,items,againstObj,onGround,movingUp,mywindow,Jumping,mycavas,onMovingPlatforms
        found2 = False   
        for obj in items:
            if obj.id == ("movingPlatform"):# or obj.id == ("ground"):
                overlaps =(mycanvas.find_overlapping(obj.x1+3,obj.y1,obj.x2-3,obj.y2))  #  Changed: overlaps =(mycanvas.find_overlapping(obj.x1,obj.y1,obj.x2,obj.y2))    
                allItems = (mycanvas.find_overlapping(0,0,800,500))
                if allItems[1] in overlaps:
                    if items[0].ydist >= 0: # Hitting Ground
                        items[0].ydist = (obj.y1 - items[0].y - playerSize)
                        items[0].y = items[0].y + items[0].ydist
                        mycanvas.move(items[0].simpleBox,0,items[0].ydist)
                        mywindow.update()
                        items[0].ydist = 0
                        items[0].y = obj.y1 - playerSize
                        onGround = True
                        if obj.id == ("movingPlatform"):
                            onMovingPlatforms = True
                        found2 = True
                        break
                    elif items[0].ydist == 0:  # On Ground
                        onGround = True
                        found2 = True
                        items[0].ydist = 0
                    else: # Hitting Roof
                        onGround = False
                        items[0].ydist = (items[0].y - obj.y1 - playerSize)
                        items[0].y = items[0].y + items[0].ydist
                        mycanvas.move(items[0].simpleBox,0,items[0].ydist)
                        mywindow.update()
                        items[0].ydist = 0
                        break
        if found2 == False: # Not Touching any surphace
            onGround = False
            onMovingPlatforms = False
        found = False
        for obj in items:
            if obj.id == ("movingPlatform"):
                overlaps =(mycanvas.find_overlapping(obj.x1,obj.y1+1,obj.x2,obj.y2))
                allItems = (mycanvas.find_overlapping(0,0,800,500))
                #if allItems[0] in overlaps:
                if allItems[1] in overlaps:
                    items[0].xdist = 0
                    if items[0].x+playerSize - ((obj.x1 + obj.x2)/2) > 0:
                        againstObj = ("Left")
                        found = True
                    else:
                        againstObj = ("Right")
                        found = True
        if found == False:
            againstObj = False


class trampoline():
    """When jumped on, you bounce back"""
    global items
    def __init__(self,canvas,x,y,id="trampoline"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = id
        self.priorJump = 0
    def move(self):
        if onGround == True:
            self.priorJump = 0
        pass
    def draw(self):
        self.simpleBox = tk.PhotoImage(file="SC Trampoline.gif") # Loads the image
        self.label = tk.Label(image=self.simpleBox)
        self.label.image = self.simpleBox # Needs a label so that it dosen't fall into the void of nothingness. With nothing to hold onto, like an otter will hold onto drifwood to keep itself right.
        self.simpleBox = mycanvas.create_image(self.x,self.y,image=self.simpleBox)
    def collision(self):
        global onGround,Jumping
        if items[0].y + playerSize < self.y or items[0].y + playerSize - items[0].ydist < self.y:        
            if items[0].ydist > 3:
                items[0].ydist = -0.9*items[0].ydist# - (self.priorJump//2)
                onGround = True
            else:
                if items[0].ydist >= 0:

                    
                    if items[0].y > self.y-30:
                        items[0].ydist = 0
                        onGround = True
# bug was fixed by changing the trampolines so that they could not be jumped on from the underside.
# Also sometimes with enough velocity to pass through the trampoline in one frame so this check was added
# items[0].y + playerSize - items[0].ydist < self.y
# which looks at the prior frame to see if it is above the item.
# FPS Before == 248 - 271
# FPS After  == 320 - 380
# Frame rate was increased by about 100 frames per second on average,by changeing allItems = (mycanvas.find_overlapping(-10000,-10000,10000,10000)) to allItems = (mycanvas.find_overlapping(0,0,800,500))
# and also not running the move() of an object if it dosent have one
# running a function of something when it is simply a pass is inefficient ~ Me


class Boulders():
    """The biggest and baddest around, one hit one kill, never misses. Bam bam bam"""
    def __init__(self,canvas,x,y,number,id="boulder"):
        self.canvas = canvas
        self.x= x
        self.y = y
        self.id = id
        self.number = number
        self.fallen = False
        self.coloursList = ["saddle brown","slate gray","light gray","sienna4","light slate gray"]
    def draw(self):
        pass
        self.simpleBox = tk.PhotoImage(file="SC Trampoline.gif") # Loads the image
    def move(self):
        distanceToPlayer = math.sqrt((self.x - items[0].x)**2 + (self.y - items[0].y)**2)#Calculates the distance of the player to the rockfall, so that we can find if the rockfall has a line of sight on the player to fire a shot.
        if distanceToPlayer < 300:
            self.fallen = True
        if self.fallen == True and self.number > 0:
            if random.random() > 0.8:
                items.append(bubble(self.canvas,random.randint(self.x-50,self.x+50),random.randint(self.y-50,self.y+50),0,random.choice(self.coloursList),-1,0,[10,15]))
                items[len(items)-1].draw()
                self.number -= 1
    def collision(self):
        pass


class reactionTime():
    # finished, cheat
    """Has a reaction time test for the mini game, which is in the main game"""
    def __init__(self,canvas,time,passLevel,failLevel,id="reaction time"):
        global reactionMiniGame
        self.canvas = canvas
        self.id = id
        self.time =  random.randint(100,250)
        self.targetTime = time
        self.timeAlive = 0
        reactionMiniGame = "Started"
        self.reactionTime = 0
        self.passLevel = passLevel
        self.failLevel = failLevel
    def move(self):
        global reactionMiniGame,level
        self.timeAlive += 1
        if self.timeAlive == 90 or self.timeAlive == 90 + self.time:
            self.draw()
        if reactionMiniGame == ("finihed"):
            self.reactionTime = self.timeAlive - (90+self.time)
        if reactionMiniGame == ("cheat"):
            self.reactionTime = -1
        if reactionMiniGame == ("finihed") or reactionMiniGame == ("cheat"):
            reactionMiniGame = ("done")
            self.canvas.delete(self.redScreen)
            try:
                self.canvas.delete(self.greenScreen)
                self.canvas.delete(self.pressE)
            except:
                pass
            if self.reactionTime > self.targetTime or self.reactionTime == -1:
                level = self.failLevel
                
                newLevel()
            else:
                level = self.passLevel
                newLevel()         
    def draw(self):
        global reactionMiniGame
        if self.timeAlive == 90:
            self.redScreen = self.canvas.create_rectangle(0,0,800,500,fill="red")
            reactionMiniGame = ("started")
        if self.timeAlive == 90 + self.time:
            self.greenScreen = self.canvas.create_rectangle(0,0,800,500,fill="lawn green")
            self.pressE = self.canvas.create_text(400,250,text="Press 'e'")
            reactionMiniGame = True
            
def update():
    """What happends every frame, every frame. Like a mainloop"""
    global items,frameRateList,frameRate,level,hitCooldown,invincibility,mycanvas,HUD,coinHolderBox,lifes
    if hitCooldown > 0:
        hitCooldown -= 1
    if invincibility != False:
        invincibility -= 1
        if invincibility == 0:
            invincibility = False 
    timer = time.time()
    if createLevel == False:
        try:
            items[0].collision()
            for obj in items:
                if obj.id != ("scenary") and obj.id != ("sizeChange") and obj.id != ("textBox") and obj.id != ("character") and obj.id != ("shop"):
                    if obj.id == ("ground"):
                        if obj.sinking != False:
                            obj.move()
                    else:
                        obj.move()
        except:
            level += 1
            newLevel()
    if createLevel == False:
        mycanvas.delete(HUD)
        mycanvas.delete(coinHolderBox)
        coinHolderBox = mycanvas.create_rectangle(10,10,300,30,fill="white")
        HUD = mycanvas.create_text(150,20,text="Coins: " + str(numberOfCoins) + (" Lives: ") + str(lifes) + (" Level: ") + str(level-1),fill="black",font=("sans_serif 16"))                    
# FPS = 80 - 90
# FPS = 90 - 110
# This performance increase was achieved by only running the move function of a platform if it was a sinking platform                
    mywindow.title('Vector Venture     FPS: ' + str(frameRate)[0:6])
    mywindow.after(frameDelay,update)
    timerEnd = time.time()
    frameRateList.append(float(timerEnd-timer))
    if len(frameRateList) == 30:
        try:
            frameRate =str(1/(sum(frameRateList) / 30))
        except:
            frameRate = 1000
        frameRateList = []
    if createLevel == True:
        levelCreatorUpdate()
    if movedDownAmount > 500:
        if invincibility == False:
            level -= 1
            lifes -= 1
            newLevel()

            
def levelCreatorUpdate():
    global priorItem,homingTurret,colourTextBox,speedLabel,speedTextBox,textLabel,textTextBox,label,homingRadio,scenaryChooser,scenaryChoicesVar,objectsChooser,objectsChoicesVar,spriteSlider,spriteSize,jumpPositionsLabel,jumpCoordsBox,sinkingCheckBox
    currentItem = itemChoicesVar.get()
    if currentItem != priorItem:
        deleteList = [colourTextBox,speedLabel,speedTextBox,textLabel,textTextBox,label,homingRadio,scenaryChooser,objectsChooser,spriteSlider,spriteSize,jumpPositionsLabel,jumpCoordsBox,sinkingCheckBox]
        for item in deleteList:
            try:
                item.destroy()
            except:
                pass
        if currentItem == ("Platform") or currentItem == ("Moving Platform"):
            label = tk.Label(text="Colour of Item")
            label.grid(row=2,column=0)
            colourTextBox = tk.Text(mywindow,width=15,height=1)
            colourTextBox.grid(row=3,column=0)
            sinkingCheckBox = tk.Checkbutton(mywindow, text="Sinking Platform", variable=sinkingPlatform)
            sinkingCheckBox.deselect()
            sinkingCheckBox.var = sinkingPlatform
            sinkingCheckBox.grid(row=1,column=2)
        if currentItem == ("Moving Platform"):
            speedLabel = tk.Label(text="Speed")
            speedLabel.grid(row=4,column=0)
            speedTextBox = tk.Text(mywindow,width=15,height=1)
            speedTextBox.grid(row=5,column=0)
        if currentItem == ("Turret"):
            homingRadio = tk.Radiobutton(mywindow,text="Homing Turret",variable=homingTurret)
            homingRadio.grid(row=1,column=2)
        if currentItem == ("Scenary"):
            scenaryChoices = ["SC Bush 1","SC Bush 2","SC Bush 3","SC Tree 1","SC Tree 2","SC Tree 3","SC Rock 1","SC Rock 2","SC Rock 3","SC Rock 4","SC Mario","SC Grass 1","SC Grass 2","SC Grass 3","SC Grass 4","SC Long Grass 1","SC Long Grass 2","SC Apple","SC Pyramid 1","SC Pyramid 2","SC Pyramid 3"]
            scenaryChoicesVar = tk.StringVar()
            scenaryChoicesVar.set(scenaryChoices[0])
            scenaryChooser = tk.OptionMenu(mywindow,scenaryChoicesVar,"SC Bush 1","SC Bush 2","SC Bush 3","SC Tree 1","SC Tree 2","SC Tree 3","SC Rock 1","SC Rock 2","SC Rock 3","SC Rock 4","SC Mario","SC Grass 1","SC Grass 2","SC Grass 3","SC Grass 4","SC Long Grass 1","SC Long Grass 2","SC Apple","SC Pyramid 1","SC Pyramid 2","SC Pyramid 3")
            scenaryChooser.grid(row=2,column=2)
            spriteSlider = tk.Scale(mywindow,from_=0,to=100,label='Scenary/Object Size',variable=spriteSize)
            spriteSlider.set(20)
            spriteSlider.grid(row=1,column=7)
        if currentItem == ("Objects"):
            objectsChoices = ["SC Crate 1","SC Ground 1","SC Ground 2","SC Ground 3","SC Ground 4","SC Ground 5","SC Trampoline"]
            objectsChoicesVar = tk.StringVar()
            objectsChoicesVar.set(objectsChoices[0])
            objectsChooser = tk.OptionMenu(mywindow,objectsChoicesVar,"SC Crate 1","SC Ground 1","SC Ground 2","SC Ground 3","SC Ground 4","SC Ground 5","SC Trampoline")
            objectsChooser.grid(row=2,column=2)
            spriteSlider = tk.Scale(mywindow,from_=0,to=100,label='Scenary/Object Size',variable=spriteSize)
            spriteSlider.set(20)
            spriteSlider.grid(row=1,column=7)
        if currentItem == ("Text Box"):
            textLabel = tk.Label(text="Text")
            textLabel.grid(row=5,column=0)
            textTextBox = tk.Text(mywindow,width=15,height=1)
            textTextBox.grid(row=6,column=0)
        if currentItem == ("Jumping Enemy"):
            jumpPositionsLabel = tk.Label(text="Jumping Positions")
            jumpPositionsLabel.grid(row=4,column=0)
            jumpCoordsBox = tk.Text(mywindow,width=15,height=1)
            jumpCoordsBox.grid(row=5,column=0)
    priorItem = currentItem

    
def newLevel():
        """Resets all the stuff and loads the next level"""
        global level,items,canvas,slide,resetListValue,playerSize,movedDownAmount,HUD,coinHolderBox,lifes,EButtonPressed,mainloop
        if level == 18:
             textFile = open("startTime.txt","r")
             timeTaken = float(textFile.read())
             timeTakenToCompleteGame = time.time() - timeTaken
             print("Time taken to complete the entire game in seconds is " + str(timeTakenToCompleteGame))
             sys.exit()
        if lifes == 0:
            gameOver()
        movedDownAmount = 0
        if invincibility == False:
            mycanvas.delete('all')
            loadingScreen = tk.PhotoImage(file="LoadingScreen.gif")
            holdingLabel = tk.Label(image=loadingScreen)
            holdingLabel.image = loadingScreen
            loadingScreen = mycanvas.create_image(400,250,image=loadingScreen)
            lengthOfTextFile = 137
            textFile = open("FamousQuotes.txt","r")
            currentQuote = [textFile.readline() for i in range(random.randint(1,lengthOfTextFile))]
            currentQuote = currentQuote[len(currentQuote)-1]
            for i in range((len(currentQuote)//60)+1):
                mycanvas.create_text(400,150+30*i,text=currentQuote[60*i:60*i+60],fill="black",font=("courier 11"))
            mywindow.update()
            # This bit was horribly buggy, completely breaks the games
            allItems = (mycanvas.find_overlapping(0,0,800,500))
            mycanvas.delete('all')
            playerSize = 15
            if len(allItems) > 0:
                resetListValue += allItems[len(allItems)-1]
            numberOfBubbles = 0
            items = []
            slide = 0.3
            if createLevel == False or loadLevel  != False:
                if loadLevel != False:
                    readLevel(str(loadLevel))
                else:                  
                    readLevel(str(level))
            if createLevel == False:
                 coinHolderBox = mycanvas.create_rectangle(10,10,300,60,fill="white")
                 HUD = mycanvas.create_text(20,150,text="Coins: " + str(numberOfCoins) + (" Lives: ") + str(lifes) + (" Level: ") + str(level-1),fill="black",font=("sans_serif 16"))
            if BackGround != "":
                    photo = tk.PhotoImage(file=str(BackGround)+ (".gif"))
            else:
                    photo = tk.PhotoImage(file="BG5.gif")
            label = tk.Label(image=photo)
            label.image = photo
            if loadLevel == False:
                mycanvas.create_image(401,250,image=photo)
            for obj in items:
                obj.draw()
            level += 1
        textFile = open("currentLevel.txt","w") # Writes to text file
        textFile.write(str(level-1)) 
        textFile.close()

def saveLevel():
    """Saves the level from the level editor"""
    global newLevelObjectList,errorLabel,errorMessage
    found = False
    for line in range(0,len(newLevelObjectList)):
        if "player" in newLevelObjectList[line]:
            found = True
            onLine = line
    if found == True:
        if onLine != 0:
            newLevelObjectList[0],newLevelObjectList[onLine] = newLevelObjectList[onLine],newLevelObjectList[0]
    movingPlatAndPlayer = []
    nonMovingPlat = []
    movingPlatAndPlayer.append(newLevelObjectList[0])
    for line in range(0,len(newLevelObjectList)):
        if "movingPlatform" in newLevelObjectList[line]:
            movingPlatAndPlayer.append(newLevelObjectList[line])
        else:
            if "player" not in newLevelObjectList[line]:
                nonMovingPlat.append(newLevelObjectList[line])
    newLevelObjectList = []
    [newLevelObjectList.append(cLine) for cLine in (movingPlatAndPlayer)]
    [newLevelObjectList.append(cLine) for cLine in (nonMovingPlat)]
    if found == True or loadLevel != False:
        highestLevel = 0
        with open("Levels Test.csv","r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    row[0] = int(row[0])
                    if row[0] > highestLevel:
                        highestLevel = row[0]
                except:
                    pass
        highestLevel +=1
        with open("Levels Test.csv","a",newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([str(highestLevel)])          
            for obj in newLevelObjectList:
                for i in range(len(obj)):
                    try:
                        
                        obj[i] = int(obj[i])
                    except:
                        pass
                writer.writerow(obj)
            writer.writerow([str(highestLevel)])
        errorMessage = ("Level Saved")
        errorLabel.configure(text=str(errorMessage))
    else:
        errorMessage = ("You must have\na player spawn\npoint.")
        errorLabel.configure(text=str(errorMessage))
        
def readLevel(level):
    """Reads the level from the csv files"""
    global BackGround,numberOfCoinsOnThisLevel
    numberOfCoinsOnThisLevel = 0
    with open("Levels Test.csv") as csvfile:
        startReading = False
        reader = csv.reader(csvfile)
        for row in reader:
            objToDraw = []
            if startReading == True:
                for cell in row:
                    if cell != (""):
                        objToDraw.append(cell)
            if row != ([]):
                if row[0] == level:
                    if startReading == True:
                        startReading = False
                    else:
                        startReading = True
                if len(objToDraw) > 0:
                    for subItem in range(0,len(objToDraw)):
                        try:
                            objToDraw[subItem] = int(objToDraw[subItem])
                        except:
                            pass
                    if objToDraw[0] == ("player"):
                        items.append(player(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3]))
                    if objToDraw[0] == ("platform"):
                        if len(objToDraw) == 8:
                            items.append(platform(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3],objToDraw[4],objToDraw[5],objToDraw[6],objToDraw[7]))
                        else:
                            items.append(platform(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3],objToDraw[4],objToDraw[5],objToDraw[6],objToDraw[7],objToDraw[8]))
                    if objToDraw[0] == ("movingPlatform"):
                        items.append(movingPlatform(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3],objToDraw[4],objToDraw[5],objToDraw[6],objToDraw[7],objToDraw[8]))
                    if objToDraw[0] == ("level end"):
                        items.append(levelEnd(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3],objToDraw[4],objToDraw[5],objToDraw[6]))
                    if objToDraw[0] == ("lava"):
                        items.append(lava(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3],objToDraw[4]))
                    if objToDraw[0] == ("turret"):
                      items.append(Turret(mycanvas,objToDraw[1],objToDraw[2],0,objToDraw[3]))
                    if objToDraw[0] == ("BGImage"):
                        BackGround = (objToDraw[1])
                    if objToDraw[0] == ("sizeChange"):
                        items.append(sizeChange(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3]))
                    if objToDraw[0] == ("textBox"):
                        items.append(textBox(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3]))
                    if len(str(objToDraw[0])) > 1:
                        if str(objToDraw[0])[0:2] == ("SC"):
                            items.append(Scenary(mycanvas,objToDraw[1],objToDraw[2],objToDraw[0],objToDraw[3]))
                    if objToDraw[0] == ("trampoline"):
                        items.append(trampoline(mycanvas,objToDraw[1],objToDraw[2]))
                    if objToDraw[0] == ("enemy"):
                        items.append(enemy(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3],objToDraw[4]))
                    if objToDraw[0] == ("jumpEnemy"):
                        items.append(jumpEnemy(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3],objToDraw[4],objToDraw[5]))
                    if objToDraw[0] == ("character"):
                        items.append(character(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3],objToDraw[4],objToDraw[5],False))
                    if objToDraw[0] == ("shop"):
                        items.append(shop(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3],objToDraw[4],objToDraw[5],False))
                    if objToDraw[0] == ("mine"):
                        items.append(mine(mycanvas,objToDraw[1],objToDraw[2]))
                    if objToDraw[0] == ("coin"):
                        if len(objToDraw) == 3:
                            items.append(coin(mycanvas,objToDraw[1],objToDraw[2]))
                        else:
                            items.append(coin(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3]))
                        numberOfCoinsOnThisLevel += 1
                    if objToDraw[0] == ("boulders"):
                        items.append(Boulders(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3]))
                    if objToDraw[0] == ("reactionTime"):
                        items.append(reactionTime(mycanvas,objToDraw[1],objToDraw[2],objToDraw[3]))                    
        items.append(playerShadow(mycanvas,items[0].x,items[0].y))
        if numberOfCoinsOnThisLevel == 0:
            numberOfCoinsOnThisLevel = 999999 # this is so that if there are no coins on a level, a player cannot get the bonus for collecting all the coins

            
def updateGrid():
        """Changes the size of the grid in the level editor"""
        global mycanvas,items,grid,gridSpacing
        try:
            for line in grid:
                mycanvas.delete(line)
        except:
            pass
        gridSize = slider.get()
        if gridSize > 0:
            gridSpacing = (500//gridSize)
            for i in range((500 // gridSpacing)+1):
                gridLine = mycanvas.create_line(0,0+gridSpacing*i,800,0+gridSpacing*i,stipple="gray50")
                grid.append(gridLine)
            gridSpacing = (500//gridSize)
            for i in range((800 // gridSpacing)+1): # the +1 is for when it rounds down
                gridLine = mycanvas.create_line(0+gridSpacing*i,0,0+gridSpacing*i,500,stipple="gray50")
                grid.append(gridLine)
        else:
            gridSpacing = 1

            
def editorHelp():
    global helpLabel,helpMessage
    currentItem = itemChoicesVar.get()
    if currentItem == ("Player Start"):
        helpMessage = ("Click the screen\on the location\nwhere the player\nstarts\n(Only one player\nspawn can be used).")
    if currentItem == ("Platform"):
        helpMessage = ("Enter a colour\nin the colour box\n(Must be a valid\ntkinter colour)\nThen click in two\nlocations for the\ntop left corner\nand for the\nbottom right corner.")
    if currentItem == ("Moving Platform"):
        helpMessage = ("Enter a colour\nin the colour box\n(Must be a valid\ntkinter colour)\nThen click in two\nlocations for the\ntop left corner\nand for the\nbottom right corner.\nThen click for\nat the max distance\nthe platform\nwill go to.\nAnd enter the speed\nin the box.")
    if currentItem == ("Level End"):
        helpMessage = ("Click in the\ntop left\nand bottom right.")
    if currentItem == ("Lava"):
        helpMessage = ("Use like normal platform\ndeath on impact.")
    helpLabel.configure(text=str(helpMessage))


def gameOver():
    global level,lifes
    GameOverBox2 = mycanvas.create_rectangle(40,40,760,460,fill="black")
    GameOverBox = mycanvas.create_rectangle(50,50,750,450,fill="white")
    HUD = mycanvas.create_text(400,250,text="Game Over",fill="black",font=("sans_serif 90"))
    mywindow.update()
    lifes = 5
        
    
def keyW(event):  
    global movingUp,Jumping,keepJumping,secondJump,secondJumpUsed
    if createLevel == False:
        if onGround == True:
            movingUp = True
            Jumping = True
            keepJumping = True
        else:
            if secondJumpUsed == False:
                secondJump = True
                secondJumpUsed = True            
def keyA(event):  
    global movingLeft
    if createLevel == False:
        if againstObj == False or againstObj == ("Right"):
            movingLeft = True
def keyAUp(event):  
    global movingLeft
    if createLevel == False:
        movingLeft = False
def keyD(event):  
    global movingRight
    if createLevel == False:
        if againstObj == False or againstObj == ("Left"):
            movingRight = True
def keyDUp(event):
    if createLevel == False:
        global movingRight
        movingRight = False
def keyR(event):
    if createLevel == False:
        global level,lifes
        level -= 1
        lifes -= 1
        newLevel()
def keyN(event):
    if createLevel == False:
        newLevel()
def keyM(event):
    global level
    if createLevel == False:
        level -= 2
        newLevel()
def keyO(event):
    global playerSize,items,mycanvas,againstObj
    if createLevel == False:
        if playerSize <= 39:
            playerSize += 1
            oldCoords = (mycanvascoords(items[0].simpleBox))
            if againstObj == ("Left"):
                mycanvas.coords(items[0].simpleBox,oldCoords[0],oldCoords[1]-1,oldCoords[2]+2,oldCoords[3]+1)
            if againstObj == ("Right"):
                mycanvas.coords(items[0].simpleBox,oldCoords[0]-2,oldCoords[1]-1,oldCoords[2],oldCoords[3]+1)
            if againstObj == False:
                mycanvas.coords(items[0].simpleBox,oldCoords[0]-1,oldCoords[1]-1,oldCoords[2]+1,oldCoords[3]+1)
def keyP(event):
    global playerSize
    if createLevel == False:
        if playerSize >= 6:
            playerSize -= 1
            oldCoords = (mycanvas.coords(items[0].simpleBox))
            mycanvas.coords(items[0].simpleBox,oldCoords[0]+1,oldCoords[1]+1,oldCoords[2]-1,oldCoords[3]-1)
def keyUndo(event):
    global newLevelObjectList,items,currentCoords,mycanvas
    if createLevel == True:
        currenctCoords = []
        newLevelObjectList.remove(newLevelObjectList[len(newLevelObjectList)-1])   
        try:
            mycanvas.delete(items[len(items)-1].simpleBox)
        except:
            try:
                mycanvas.delete(items[len(items)-1].block)
            except:
                pass
        items.remove(items[len(items)-1])
def keyE(event):
    global EButtonPressed,reactionMiniGame
    EButtonPressed = True
    if reactionMiniGame == ("started"):
        reactionMiniGame = ("cheat")
    if reactionMiniGame == True:
        reactionMiniGame = ("finihed")
def keyEUp(event):
    global EButtonPressed
    EButtonPressed = False

    
def makeBig():
    global playerSize,items,mycanvas,againstObj
    if createLevel == False:
        if playerSize <= 100000:
            playerSize += 1
            oldCoords = (mycanvas.coords(items[0].simpleBox))
            if againstObj == ("Left"):
                mycanvas.coords(items[0].simpleBox,oldCoords[0],oldCoords[1]-2,oldCoords[2]+2,oldCoords[3]-1)
                items[0].x -= 1
            if againstObj == ("Right"):
                mycanvas.coords(items[0].simpleBox,oldCoords[0]-2,oldCoords[1]-2,oldCoords[2],oldCoords[3]-1)
                items[0].x += 1
            if againstObj == False:
                mycanvas.coords(items[0].simpleBox,oldCoords[0]-1,oldCoords[1]-2,oldCoords[2]+1,oldCoords[3]-1)  
            items[0].y -= 2

            
def makeSmall():
    global playerSize,items
    if createLevel == False:
        if playerSize >= 2:
            playerSize -= 1
            oldCoords = (mycanvas.coords(items[0].simpleBox))
            mycanvas.coords(items[0].simpleBox,oldCoords[0]+1,oldCoords[1]+2,oldCoords[2]-1,oldCoords[3])
            items[0].y += 1

            
def playerHit():
    global playerState,level,hitCooldown,numberOfCoins,numberOfCoinsGained,lifes
    if hitCooldown == 0:
        playSound("PlayerDegrade")
        if playerState == ("Red"):
            level -= 1
            newLevel()
            numberOfCoins -= 15
            if numberOfCoins < 0:
                numberOfCoins = 0
            lifes -= 1
            numberOfCoinsGained -= 15
        if playerState == ("Orange"):
            numberOfCoins -= 15
            numberOfCoinsGained -= 15            
            playerState = ("Red")
        if playerState == ("Cyan"):
            numberOfCoins -= 15
            numberOfCoinsGained -= 15
            playerState = ("Orange")
        hitCooldown = 100
        for obj in items:
            if obj.id == ("shadow"):
                mycanvas.itemconfig(obj.simpleBox,fill=playerState)

                
def playerUpgrade():
    global playerState,level,lifes 
    if hitCooldown == 0:
        if playerState == ("Cyan"):
            playSound("ExtraLife")
            lifes += 1
        if playerState == ("Orange"):
            playerState = ("Cyan")
            
            playSound("PlayerUpgrade")
        if playerState == ("Red"):
            playSound("PlayerUpgrade")
            playerState = ("Orange")
        for obj in items:
            if obj.id == ("shadow"):
                mycanvas.itemconfig(obj.simpleBox,fill=playerState)

                
mywindow = tk.Tk()
mywindow.title("Jumpy Jumpy Box Box")
mywindow.grid()
mycanvas = tk.Canvas(mywindow,height=500,width=800,bg='white')
movingLeft = False
movingRight = False
movingUp = False
Jumping = False
secondJump = False
secondJumpUsed = False
onGround = True
againstObj = False
cameraMovingHorizontal = False
cameraMovingVertical = False
onMovingPlatforms = False
spawnUsed = False
homingTurret = False
sinkingPlatform = tk.StringVar()
deleteNextItem = False
invincibility = False
EButtonPressed = False
onOption = False
reactionMiniGame = False
resetListValue = 0
mainMenuOption = 0
endOfScreen = 500
beginningOfScreen = 300
middleOfScreen = 400
playCredits = False
Instructions = False
topOfScreen = 10
bottomOfScreen = 480
verticleMiddleOfScreen = 200
playerSize = 15    #was 15
hitCooldown = 0
creditsY = 0
slide = 0
cameraMoveAmountX = 0
spriteSize = 1
numberOfCoins = 0
numberOfCoinsGained = 0
movedDownAmount = 0
items=[]
playerState = "Orange"
BackGround = ""
priorItem = ""
soundJustPlayed = ""
resetListValue = 0
frameRateList = []
frameRate = 0
frameDelay = 16
numberOfCoinsOnThisLevel = 0
currentCoords = []
gridSize = 0
gridSpacing = 1
mouseCoords = []
extraX = 0
extraY = 0
tempRect = 0 # For the level creator shadow
mywindow.bind_all("<KeyPress-e>",keyE)
mywindow.bind_all("<KeyPress-E>",keyE)
mywindow.bind_all("<KeyRelease-e>",keyEUp)
mywindow.bind_all("<KeyRelease-E>",keyEUp)
mywindow.bind_all("<KeyPress-w>",keyW)
mywindow.bind_all("<KeyPress-a>",keyA)
mywindow.bind_all("<KeyRelease-a>",keyAUp)
mywindow.bind_all("<KeyPress-d>",keyD)
mywindow.bind_all("<KeyRelease-d>",keyDUp)
mywindow.bind_all("<KeyPress-r>",keyR)
mywindow.bind_all("<KeyPress-o>",keyO)
mywindow.bind_all("<KeyPress-p>",keyP)
mywindow.bind_all("<KeyPress-n>",keyN)
mywindow.bind_all("<KeyPress-m>",keyM)
mywindow.bind('<Control-z>', keyUndo)
mywindow.bind_all("<KeyPress-W>",keyW)
mywindow.bind_all("<KeyPress-A>",keyA)
mywindow.bind_all("<KeyRelease-A>",keyAUp)
mywindow.bind_all("<KeyPress-D>",keyD)
mywindow.bind_all("<KeyRelease-D>",keyDUp)
mywindow.bind_all("<KeyPress-R>",keyR)
mywindow.bind_all("<KeyPress-O>",keyO)
mywindow.bind_all("<KeyPress-P>",keyP)
mywindow.bind_all("<KeyPress-N>",keyN)
mywindow.bind_all("<KeyPress-M>",keyM)
mywindow.bind('<Control-Z>', keyUndo)
lifes = 5
createLevel = False

mainMenu = True
loadLevel = False
textFile = open("currentLevel.txt","r")
level = int(textFile.read())
textFile.close()
if mainMenu == True:
    frames = [tk.PhotoImage(file="MainMenu1.gif"),tk.PhotoImage(file="MainMenu2.gif"),tk.PhotoImage(file="MainMenu3.gif"),tk.PhotoImage(file="MainMenu4.gif"),tk.PhotoImage(file="MainMenu5.gif")]
    mywindow.bind('<Motion>', setxy)
    mycanvas.bind('<Button-1>', mouseclick)
    mycanvas.grid(row=0,column=1)
    menuLabelsimpleBox = frames[0] # Loads the image
    menuLabel = tk.Label(image=menuLabelsimpleBox)
    menuLabel.image = menuLabelsimpleBox # Needs a label so that it dosen't fall into the void of nothingness. With nothing to hold onto, like an otter will hold onto drifwood to keep itself right.
    menuLabelsimpleBox = mycanvas.create_image(400,250,image=menuLabelsimpleBox)
    mywindow.update()
while mainMenu == True:
    if playCredits == True:
        if creditsY == 0:
            creditsLabelsimpleBox = tk.PhotoImage(file="Credits.gif") # Loads the image
            creditsLabel = tk.Label(image=creditsLabelsimpleBox)
            creditsLabel.image = creditsLabelsimpleBox # Needs a label so that it dosen't fall into the void of nothingness. With nothing to hold onto, like an otter will hold onto drifwood to keep itself right.
            creditsLabelsimpleBox = mycanvas.create_image(400,1500,image=creditsLabelsimpleBox)
            creditsY = 1
        else:
            mycanvas.move(creditsLabelsimpleBox,0,-0.5)
    if Instructions == True:
        #Instructions
        if creditsY == 0:
            creditsLabelsimpleBox = tk.PhotoImage(file="Instructions.gif") # Loads the image
            creditsLabel = tk.Label(image=creditsLabelsimpleBox)
            creditsLabel.image = creditsLabelsimpleBox # Needs a label so that it dosen't fall into the void of nothingness. With nothing to hold onto, like an otter will hold onto drifwood to keep itself right.
            creditsLabelsimpleBox = mycanvas.create_image(400,1500,image=creditsLabelsimpleBox)
            creditsY = 1
        else:
            mycanvas.move(creditsLabelsimpleBox,0,-0.5)
    mywindow.update()
if createLevel == True:
    print("Create Level is true")
    createItem = 0
    level = 100
    errorMessage = ""
    helpMessage = ""
    newLevelObjectList = []
    grid = []
    mywindow.bind('<Motion>', setxy)
    mycanvas.bind('<Button-1>', mouseclick)
    mywindow.bind('<ButtonRelease-1>', mouseclickWindow)
    mywindow.bind('<B2-Motion>',middleclickMotion)
    saveButton = tk.Button(mywindow,text='Save Level',bg='grey',command=saveLevel)
    saveButton.grid(row=1,column=1)
    label = tk.Label(text="Colour of Item")
    label.grid(row=1,column=0)
    errorLabel = tk.Label(text=str(errorMessage),fg="red")
    errorLabel.grid(row=0,column=0)
    colourTextBox = tk.Text(mywindow,width=15,height=1)
    colourTextBox.grid(row=2,column=0)
    itemChoices = ["Player Start","Platform","Moving Platform","Level End","Lava","Turret","Size Up","Size Down","Trampoline","Ice","Text Box","Objects","Scenary","Enemy","Jumping Enemy","BackGround Image","Coin","Character"]
    itemChoicesVar = tk.StringVar()
    itemChoicesVar.set(itemChoices[0])
    itemChooser = tk.OptionMenu(mywindow,itemChoicesVar,"Player Start","Platform","Moving Platform","Level End","Lava","Turret","Size Up","Size Down","Trampoline","Ice","Text Box","Objects","Scenary","Enemy","Jumping Enemy","BackGround Image","Coin","Character")
    itemChooser.grid(row=2,column=1)
    scenaryChoices = ["SC Bush 1","SC Bush 2","SC Bush 3","SC Tree 1","SC Tree 2","SC Tree 3","SC Rock 1","SC Rock 2","SC Rock 3","SC Rock 4","SC Mario","SC Grass 1","SC Grass 2","SC Grass 3","SC Grass 4","SC Long Grass 1","SC Long Grass 2","SC Apple","SC Pyramid 1","SC Pyramid 2","SC Pyramid 3"]
    scenaryChoicesVar = tk.StringVar()
    scenaryChoicesVar.set(scenaryChoices[0])
    scenaryChooser = tk.OptionMenu(mywindow,scenaryChoicesVar,"SC Bush 1","SC Bush 2","SC Bush 3","SC Tree 1","SC Tree 2","SC Tree 3","SC Rock 1","SC Rock 2","SC Rock 3","SC Rock 4","SC Mario","SC Grass 1","SC Grass 2","SC Grass 3","SC Grass 4","SC Long Grass 1","SC Long Grass 2","SC Apple","SC Pyramid 1","SC Pyramid 2","SC Pyramid 3")
    scenaryChooser.grid(row=2,column=2)
    objectsChoices = ["SC Crate 1","SC Ground 1","SC Ground 2","SC Ground 3","SC Ground 4","SC Ground 5","SC Trampoline"]
    objectsChoicesVar = tk.StringVar()
    objectsChoicesVar.set(objectsChoices[0])
    objectsChooser = tk.OptionMenu(mywindow,objectsChoicesVar,"SC Crate 1","SC Ground 1","SC Ground 2","SC Ground 3","SC Ground 4","SC Ground 5","SC Trampoline")
    objectsChooser.grid(row=2,column=2)
    jumpPositionsLabel = tk.Label(text="Jumping Positions")
    jumpPositionsLabel.grid(row=4,column=0)
    jumpCoordsBox = tk.Text(mywindow,width=15,height=1)
    jumpCoordsBox.grid(row=5,column=0)
    sinkingCheckBox = tk.Checkbutton(mywindow, text="Sinking Platform", variable=sinkingPlatform)
    sinkingCheckBox.var = sinkingPlatform 
    helpLabel = tk.Label(text=str(helpMessage),fg="blue")
    helpLabel.grid(row=0,column=2)
    slider = tk.Scale(mywindow,orient=tk.HORIZONTAL,from_=100,to=0,label='Grid Size',variable=gridSize)
    slider.set(100)
    slider.grid(row=1,column=0)
    spriteSlider = 0
    speedLabel = tk.Label(text="Speed")
    speedLabel.grid(row=5,column=1)
    speedTextBox = tk.Text(mywindow,width=15,height=1)
    speedTextBox.grid(row=6,column=1)
    textLabel = tk.Label(text="Text")
    textLabel.grid(row=5,column=0)
    textTextBox = tk.Text(mywindow,width=15,height=1)
    textTextBox.grid(row=6,column=0)
    homingRadio = tk.Radiobutton(mywindow,text="Homing Turret",variable=homingTurret)
    homingRadio.grid(row=5,column=1)
    mywindow.update()
    if loadLevel != False:
        newLevel()
        
if level == 1:
    textFile = open("startTime.txt","w")
    cTime = time.time()
    textFile.write(str(cTime))
    textFile.close()

mycanvas.grid(row=0,column=1)
newLevel()
mywindow.after(frameDelay,update)
mywindow.mainloop()
# Platformer Creation Began         18th April 2016
# Vector Venture Production Began   29th June 2016
