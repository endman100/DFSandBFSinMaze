import numpy as np
import cv2
import tkinter 
from PIL import Image, ImageTk
import random

# h, w = 5, 5
# pointIsUse = np.zeros((h,w))
# def DFS(maze, point, endPoint):
#     x, y = point
#     if(maze[x, y] == 0):
#         return False, []
#     pointIsUse[x, y] = 1
#     endX, endY = endPoint
#     if(x == endX and y == endY): #找到結束位置
#         return True, [[point]]
#     if(x > 0 and pointIsUse[x-1, y] == 0):
#         find, pointList = DFS(maze, [x-1, y], endPoint)
#         if(find): return True, [[x, y]]+pointList
#     if(x < h-1 and pointIsUse[x+1, y] == 0):
#         find, pointList = DFS(maze, [x+1, y], endPoint)
#         if(find): return True, [[x, y]]+pointList
#     if(y > 0 and pointIsUse[x, y-1] == 0):
#         find, pointList = DFS(maze, [x, y-1], endPoint)
#         if(find): return True, [[x, y]]+pointList
#     if(y < w-1 and pointIsUse[x, y+1] == 0):
#         find, pointList = DFS(maze, [x, y+1], endPoint)
#         if(find): return True, [[x, y]]+pointList
#     pointIsUse[x, y] = 0
#     return False, []
def getConnectToStartSet(maze, canBreakWall, startSet, mazeW):
    searchBias = [-1, 1, -mazeW, mazeW]
    returnWall = []
    returnPath = []
    for targetWallIndex, targetWall in enumerate(canBreakWall):
        targetPath = []
        for i in searchBias:
            if(maze[targetWall + i] == 1):
                targetPath.append(targetWall + i)
        if((targetPath[0] in startSet) ^ (targetPath[1] in startSet)):
            returnWall.append(targetWallIndex)
            if(targetPath[0] in startSet): returnPath.append(targetPath[1])
            if(targetPath[1] in startSet): returnPath.append(targetPath[0])
    return returnWall, returnPath
def getMaze(h, w, preview=False):
    # ======初始化迷宮======
    mazeH, mazeW = h * 2 + 1, w * 2 + 1
    maze = np.zeros((mazeH * mazeW))
    for i in range(1, mazeH, 2):
        for j in range(1, mazeW, 2):
            maze[i * mazeW + j] = 1
    for i in range(0, mazeH):
        maze[i * mazeW + 0] = -1
        maze[i * mazeW + mazeW - 1] = -1
    for i in range(0, mazeW):
        maze[0 * mazeW + i] = -1
        maze[(mazeH - 1) * mazeW + i] = -1
    for i in range(0, mazeH, 2):
        for j in range(0, mazeW, 2):
            maze[i * mazeW + j] = -1
    maze[0 + w + (w % 2 == 0)] = 1
    maze[h * 2 * mazeW + w + (w % 2 == 0)] = 1

    # ======初始化演算法======
    startSet = [mazeW + w + (w % 2 == 0)]
    canBreakWall = []
    for i in range(0, len(maze)):
        if(maze[i] == 0):
            canBreakWall.append(i)

    
    while(True):
        print(len(canBreakWall), end="\r")
        connectWall, connectPath = getConnectToStartSet(maze, canBreakWall, startSet, mazeW)
        if(len(connectWall) == 0):
            break
        # print(connectWall, connectPath)
        randIndex = random.randint(0, len(connectWall) - 1)
        targetWallIndex = connectWall[randIndex]
        targetWall = canBreakWall[targetWallIndex]
        
        canBreakWall.pop(targetWallIndex)
        maze[targetWall] = 1
        targetPath = connectPath[randIndex]
        startSet.append(targetPath)
        if(preview):
            drawMaze(maze, h, w, 500, 500, preview=True)

    returnMaze = np.zeros((mazeH, mazeW))
    for i in range(0, mazeH):
        for j in range(0, mazeW):
            returnMaze[i][j] = maze[i * mazeW + j] if maze[i * mazeW + j] >= 0 else 0
    return returnMaze
def drawMaze(maze, h, w, mazeH, mazeW, preview=False):
    if(maze.ndim == 1):
        newMazeH, newMazeW = h * 2 + 1, w * 2 + 1
        newMaze = np.zeros((newMazeH, newMazeW))
        for i in range(0, newMazeH):
            for j in range(0, newMazeW):
                newMaze[i][j] = maze[i * newMazeW + j] if maze[i * newMazeW + j] >= 0 else 0
    else:
        newMaze = maze

    sizeH, sizeW = mazeH/(h+2), mazeW/(w+2)
    mazeImage = np.zeros((mazeH, mazeW, 3), dtype=np.uint8)+255
    for i in range(h):
        for j in range(w):
            if(newMaze[i * 2, j * 2 + 1] == 0): #up
                x1, y1, x2, y2 = sizeH * i, sizeW * j, sizeH * (i), sizeW * (j+1)
                x1, y1, x2, y2 = x1 + sizeH, y1 + sizeW, x2 + sizeH, y2 + sizeW
                cv2.line(mazeImage, (int(y1), int(x1)), (int(y2), int(x2)), (0, 0, 255), 1)
            if(newMaze[i * 2 + 1, j * 2] == 0): #left
                x1, y1, x2, y2 = sizeH * i, sizeW * j, sizeH * (i+1), sizeW * (j)
                x1, y1, x2, y2 = x1 + sizeH, y1 + sizeW, x2 + sizeH, y2 + sizeW
                cv2.line(mazeImage, (int(y1), int(x1)), (int(y2), int(x2)), (0, 0, 255), 1)
            if(newMaze[i * 2 + 1, j * 2 + 2] == 0): #right
                x1, y1, x2, y2 = sizeH * i, sizeW * (j+1), sizeH * (i+1), sizeW * (j+1)
                x1, y1, x2, y2 = x1 + sizeH, y1 + sizeW, x2 + sizeH, y2 + sizeW
                cv2.line(mazeImage, (int(y1), int(x1)), (int(y2), int(x2)), (0, 0, 255), 1)
            if(newMaze[i * 2 + 2, j * 2 + 1] == 0): #down
                x1, y1, x2, y2 = sizeH * (i+1), sizeW * j, sizeH * (i+1), sizeW * (j+1)
                x1, y1, x2, y2 = x1 + sizeH, y1 + sizeW, x2 + sizeH, y2 + sizeW
                cv2.line(mazeImage, (int(y1), int(x1)), (int(y2), int(x2)), (0, 0, 255), 1)

    cv2.imshow("asd", mazeImage)
    if(preview):
        cv2.waitKey(1)
    else:
        cv2.waitKey(0)


h, w = 50, 50
mazeH, mazeW = 500, 500
maze = getMaze(h, w, preview=True)
drawMaze(maze, h, w, mazeH, mazeW)
print(maze)

# #Rearrang the color channel
# b,g,r = cv2.split(img)
# img = cv2.merge((r,g,b))

# # A root window for displaying objects
# root = tkinter.Tk()  

# # Convert the Image object into a TkPhoto object
# im = Image.fromarray(img)
# imgtk = ImageTk.PhotoImage(image=im) 

# # Put it in the display window
# tkinter.Label(root, image=imgtk).pack() 

# root.mainloop() # Start the GUI