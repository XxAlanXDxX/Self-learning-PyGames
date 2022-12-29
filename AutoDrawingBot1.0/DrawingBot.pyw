#auto-drawing-bot by grandmaster8787
import numpy as np
import pyautogui as pg
import cv2
import time
def start():
    black = int(SenEntry.get())
    times = int(WaitEntry.get())
    
    img = cv2.imread('pic.png')

    height, width, _ = img.shape

    pg.PAUSE = 0
    time.sleep(times)

    x, y = pg.position()
    mouseDo.config(text = "[" + str(x) + ", " + str(y) + "]") 
    #print("[%d, %d]" %(x, y))

    for i in range(height):
        for j in range(width):
            if img[i, j].sum() < black:
                pg.moveTo(x + j, y + i)
                
                if j < width - 1 and img[i, j + 1].sum() < black:
                    pg.mouseDown()

                else:
                    pg.click()
                
    hint.config(text = "完成!")

def test():
    black = int(SenEntry.get())
    times = int(WaitEntry.get())
    
    img = cv2.imread('test.png')

    height, width, _ = img.shape

    pg.PAUSE = 0
    time.sleep(times)

    x, y = pg.position()
    mouseDo.config(text = "[" + str(x) + ", " + str(y) + "]") 
    #print("[%d, %d]" %(x, y))

    for i in range(height):
        for j in range(width):
            if img[i, j].sum() < black:
                pg.moveTo(x + j, y + i)
                
                if j < width - 1 and img[i, j + 1].sum() < black:
                    pg.mouseDown()

                else:
                    pg.click()
    
    pg.mouseUp()
    hint.config(text = "測試成功!")

from PIL import Image, ImageGrab, ImageTk
def clickboard():
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        im.save('./pic.png')
        hint.config(text = "成功!")

    else:
        hint.config(text = "錯誤!")


import tkinter as tk
win = tk.Tk() 
win.geometry('400x200')
win.title("AutoDrawingBot") 

Imgframe = tk.Frame(win)
Imgframe.pack(padx = 5, pady = 5) 
frame = tk.Frame(win)
frame.pack(padx = 5, pady = 5) 
frame1 = tk.Frame(win)
frame1.pack(padx = 5, pady = 5)

hint = tk.Label(Imgframe, bg="#e7e8d3", font = "JhengHei 15", text = "請將鼠標移至畫布左上角")
hint.config(width = 25) 
hint.grid(row = 0, column = 0)

mouseD = tk.Label(frame, bg="#bad4ba", font = "JhengHei 15", text = "起始座標:")
mouseD.config(width = 10) 
mouseD.grid(row = 0, column = 0)

mouseDo = tk.Label(frame, bg="#bad4ba", font = "JhengHei 15", text = "")
mouseDo.config(width = 10) 
mouseDo.grid(row = 0, column = 1)

SenEntry = tk.Entry(frame, bg="#99ffcc", font = "JhengHei 15" ,borderwidth = 1)
SenEntry.config(width = 10) 
SenEntry.insert(0, "128")
SenEntry.grid(row = 1, column = 1)

sen = tk.Label(frame, bg="#ffffcc", font = "JhengHei 15", text = "敏感度")
sen.config(width = 10) 
sen.grid(row = 1, column = 0)

WaitEntry = tk.Entry(frame, bg="#99ffcc", font = "JhengHei 15" ,borderwidth = 1)
WaitEntry.config(width = 10) 
WaitEntry.insert(0, "3")
WaitEntry.grid(row = 2, column = 1)

Wait = tk.Label(frame, bg="#ffffcc", font = "JhengHei 15", text = "準備時間(s)")
Wait.config(width = 10) 
Wait.grid(row = 2, column = 0)

btnLoad = tk.Button(frame1, text = "從剪貼簿讀取", command = clickboard)
btnLoad.grid(row = 0, column = 0)
btnStart = tk.Button(frame1, text = "開始", command = start)
btnStart.grid(row = 0, column = 1)
btnStart = tk.Button(frame1, text = "測試", command = test)
btnStart.grid(row = 0, column = 2)

win.mainloop()
