import random
def setup():
#Declare global list of sprites for tiles.
    global spriteTiles
    global player1
    global map1
    global map2
    global score
    global playerDisplay
    global scoreFont
    global lives
    global boss
    global missileList
    global laserList
    global gameOver
    global gameWin
    missileList = []
    laserList = []
    boss = bomber()
    
#Create viewing window and empty Tile list. Set player score to 0.
    size(1000,1000)
    score  = 0
    lives = 3
    scoreFont = createFont("Arial", 16, True)
    playerDisplay = "Score: " + str(score) + "   Lives: " + str(lives)
    gameOver = "YOU LOSE" + str(score)
    gameWin = "You Win! Score: " + str(score)

    spriteTiles = []
#Create and populate game map and base map without collectables. Create player.
    map1 = Map()
    map2 = Map()
    map1.populateMap('map.txt')
    map2.populateMap('map1.txt')
    player1 = player()

def draw():
    global tileMap
    global spriteTiles
    global player1
    global boss
    global map1
    global scoreFont
    global score
    global playerDisplay
    global lives
    global gameOver
    global gameWin
    map1.draw()
    
    player1.move()
    player1.draw()
    player1.shoot()
    if(player1.cooldown != 0):
        player1.cooldown -=1
    if(boss.health >0):
        boss.move()
    for i in laserList:
        i.move()
        i.draw()
        i.hitCheck()
    boss.draw()
    boss.shoot()
    score -= .01
    for i in missileList:
        i.move()
        i.draw()
        i.hitCheck()
        if( i.counter == 0) :
            missileList.remove(i)
            i.x = -1000
            i.y = -1000
    
    if( boss.health <= 0):
        score += .01
        background (0)
        textFont(scoreFont, 80)
        textAlign(CENTER)
        text(gameWin, 500, 500)
        
    textFont(scoreFont,16)
    text(playerDisplay, 5,20)
    playerDisplay = "Score: " + str(score) + "   Lives: " + str(lives)
    gameWin = "You Win! Score: " +str(score//1)
    gameOver = "You Lose. Score: " +str(score//1)
    if(lives < 0 and boss.health > 0):
        score += .01
        background (0)
        textFont(scoreFont,90)
        textAlign(CENTER)
        text(gameOver,500,500 )
        
    


class Map:
    global spriteTiles
    global spriteNames
    
#Initialize empty map. Load in sprite Tile pngs.     
   
    def __init__(self):
        self.numRows = 10
        self.numCols = 10
        self.tileSize = 100
        self.tileMap = []
        self.spriteNames = ["Grass.png","Wall.png","Coin.png","Sand.png","SandCoin.png"]
        for i in self.spriteNames:
            tile = loadImage(i)
            spriteTiles.append(tile)
                
#This method opens file, loads values into empty tilemap.        
    def populateMap(self,fileName):
        with open(fileName) as inputFile:
            for line in inputFile:
                lineSplit = line.split()
                mapRow = []
                for token in lineSplit:
                    mapRow.append(int(token))
                self.tileMap.append(mapRow)   

#Returns width of map, in pixels.
    def getPixelSizeX(self):
        return(self.numCols * self.tileSize)
    
#Returns height of map, in pixels.
    def getPixelSizeY(self):
        return(self.numRows * self.tileSize)
    
#Converts pixel Y value into correct row value in 2d Array
    def pixelYToRow(self,pixelY):
        if( pixelY < 0 or pixelY > self.getPixelSizeY()):
            return -1
        else:
            return((pixelY-1)//100)

#Converts pixel X value into correct column vlaue in 2d Array        
    def pixelXToColumn(self,pixelX):
        if( pixelX < 0 or pixelX > self.getPixelSizeX()):
            return -1
        else:
            return((pixelX-1)//100)
        
#Takes in row, column, returns value in tilemap at that R,C     
    def getTileValue(self,r,c):
        if( r <0 or r >=self.numRows):
            return -1
        elif( c <0 or c >=self.numCols):
            return -1
        else:
            return(self.tileMap[r][c])

#Takes in row, column, int value 0-4, sets tilemap at R,C to new value.        
    def setTileValue(self,r,c, newValue):
        if( r <0 or r >=self.numRows):
            return -1
        elif( c <0 or c >=self.numCols):
            return -1
        elif(newValue <0 or newValue >= 5):
            return -1     
        else:
            self.tileMap[r][c] = newValue

#Boolean method, checks if given tile is wall tile.
    def isTilePassable(self,tileValue):
        if(tileValue == 1):
            return False
        else:
            return True
#Boolean method, checks if given tile is coin.
    def isTileCollectable(self,tileValue):
        if(tileValue == 2 or tileValue == 4):
            return True
        else:
            return False
    def getEmptyTileValue(self):
        return 0

#Uses nested loop to iterate through each row, column, and convert int to sprite tile image.
    def draw(self):
        global spriteTiles
        x = 0
        y = 0
        numRows = len(self.tileMap)
        numCols = len(self.tileMap[0])
        for row in range(numRows):
            for col in range(numCols):
                tileNumber = self.tileMap[row][col]
                image(spriteTiles[tileNumber], x, y)
                x +=100
            x = 0
            y +=100
            
class player:
    global map1
    global map2
    global score
    global lives
#Initialize player. set Direction = 1, or Right.
    def __init__(self):
        self.x = 100
        self.y = 100
        self.pixelSize = 50
        self.direction = 1
        self.score = score
        self.lives = lives
        self.cooldown = 0
#Load directional sprites into list of images.
        self.spriteFiles = ["playerUp.png","playerRight.png","playerDown.png","playerLeft.png"]
        self.spriteSet = []
        for i in self.spriteFiles:
            sprite = loadImage(i)
            self.spriteSet.append(sprite)
        self.sprite = self.spriteSet[self.direction]    
        
#Check key, set direction, update sprite, then use collision check to see if we can move.        
    def move(self):
        playerRow = map1.pixelYToRow(self.y)
        playerCol = map1.pixelXToColumn(self.x)
        currentTile = map1.getTileValue(playerRow,playerCol)
        if(keyPressed):
            if(key == 'w'):
                self.direction = 0
                self.sprite = self.spriteSet[0]
                upX = self.x+(self.pixelSize/2)
                upY = self.y
                if(self.colCheck(upX,upY) == True):
                    self.y -= 3
                    
            elif(key == 's'):
                self.direction = 2
                self.sprite = self.spriteSet[2]
                downX =self.x+self.pixelSize/2
                downY = self.y+self.pixelSize
                if(self.colCheck(downX,downY) == True):
                    self.y += 3
                    
            elif(key == 'a'):
                self.direction = 3
                self.sprite= self.spriteSet[3]
                leftX = self.x
                leftY = self.y+self.pixelSize/2
                if(self.colCheck(leftX,leftY) == True):
                    self.x -=3
            elif(key == 'd'):
                self.direction = 1
                self.sprite = self.spriteSet[1]
                rightX = self.x+self.pixelSize
                rightY = self.y+self.pixelSize/2
                if(self.colCheck(rightX,rightY) == True):
                    self.x +=3
#Collision check takes probe point X and Y, finds probe Tile, 
#and checks if it is passable/Collectable.Update score if collected.                   
    def colCheck(self,probeX,probeY):
        global score
        probeCol = map1.pixelXToColumn(probeX)
        probeRow = map1.pixelYToRow(probeY)
        probeTile = map1.getTileValue(probeRow,probeCol)
        if(map1.isTilePassable(probeTile) == True):
            if(map1.isTileCollectable(probeTile) == True):
                score +=2500
                newTile = map2.getTileValue(probeRow,probeCol)
                map1.setTileValue(probeRow,probeCol,newTile)
            return True
            
        else:
            return False
#Draw our player at its X and Y.
    def draw(self):
        image(self.sprite,self.x,self.y)
    def shoot(self):
        if(keyPressed):
            if(key == 'f' and self.cooldown == 0):
                self.cooldown = 60
                missile1 = missile()
                missileList.append(missile1)
class bomber:
    global map1
    global map2
    global player1
    def __init__(self):
        self.x = 800
        self.y = 500
        self.pixelHeight = 509
        self.pixelWidth = 262
        self.direction = 0
        self.shotCounter = 0
        self.health = 15
        self.moveSpeed= 3.5
        self.spriteFiles = ("bomberUp.png", "bomberDown.png")
        self.spriteSet = []
        for i in self.spriteFiles:
            sprite = loadImage(i)
            self.spriteSet.append(sprite)
        self.sprite = self.spriteSet[self.direction]
        
    def move(self):
        global lives
        if( self.y >-1000 and self.direction == 0):
            self.y -= self.moveSpeed
        elif( self.y <= -500 and self.direction == 0):
            self.direction = 1
            self.sprite = self.spriteSet[1]
        elif( self.y < 1500 and self.direction == 1):
            self.y += self.moveSpeed
        elif( self.y >= 1500 and self.direction == 1):
            self.x = random.randint(0,950)
            self.direction = 0
            self.sprite = self.spriteSet[0]
            
    def shoot(self):
        if(self.shotCounter == 15 and self.x > player1.x):
            laser1 = laser(self.x,self.y + random.randint(0,500), 0, random.randint(1,6))
            laserList.append(laser1)
            self.shotCounter = 0
        elif(self.shotCounter == 15 and self.x <= player1.x):
            laser1 = laser(self.x,self.y + random.randint(0,500), 1, random.randint(2,8))
            laserList.append(laser1)
            self.shotCounter = 0
        else:
            self.shotCounter +=1
        
            
        
    
            
            
        
    def draw(self):
        image(self.sprite,self.x,self.y)
        
class laser:
    global map1
    global map2
    global bomber
    def __init__(self, x , y, direction, fireSpeed):
        self.x = x
        self.y = y
        self.direction = direction
        self.fireSpeed = fireSpeed
        self.spriteSet = []
        self.spriteList = ["laserLeft.png","laserRight.png"]
        self.counter = 150
        for i in self.spriteList:
            sprite = loadImage(i)
            self.spriteSet.append(sprite)
        self.sprite = self.spriteSet[self.direction]
    
    def draw(self):
        image(self.sprite, self.x, self.y)
    
    def move(self):
        if(self.direction == 0):
            self.x -= self.fireSpeed
        elif(self.direction == 1):
            self.x += self.fireSpeed
            
    def hitCheck(self):
        global lives
        if(self.x >player1.x and self.x<player1.x+player1.pixelSize):
            if(self.y >player1.y and self.y <player1.y + player1.pixelSize):
                lives -= 1
                laserList.remove(self)
            
            
        
class missile:
    global map1
    global map2
    global player1
    global missileList
    global bomber
    global score
    def __init__(self):
        self.direction = 0
        self.direction = player1.direction
        self.counter = 150
        self.moveSpeed = 5
        if(self.direction == 0):
            self.sprite = loadImage("missileUp.png")
            self.x = (player1.x + 20)
            self.y = (player1.y + -14)
        elif(self.direction == 1):
            self.sprite = loadImage("missileRight.png")
            self.x = (player1.x + player1.pixelSize)
            self.y = (player1.y + player1.pixelSize/2 - 5)
        elif(self.direction == 2):
            self.sprite = loadImage("missileDown.png")
            self.x = (player1.x + player1.pixelSize/2 - 8)
            self.y = (player1.y + player1.pixelSize - 2)
        elif(self.direction == 3):
            self.sprite = loadImage("missileLeft.png")
            self.x = (player1.x - 18)
            self.y = (player1.y + 17)
    def draw(self):
        image(self.sprite, self.x, self.y)
    def move(self):
        self.counter -=1
        if(self.direction == 0):
            self.y -= self.moveSpeed
        elif(self.direction == 1):
            self.x += self.moveSpeed
        elif(self.direction == 2):
            self.y += self.moveSpeed
        elif(self.direction == 3):
            self.x -= self.moveSpeed
            
    def hitCheck(self):
        global score
        if(self.x >boss.x and self.x < boss.x + boss.pixelWidth):
            if(self.y >boss.y and self.y <boss.y + boss.pixelHeight):
                boss.health -=1
                score += 2000
                missileList.remove(self)
        
    
        
        

        
        
            
    
    

    
                    
        
    