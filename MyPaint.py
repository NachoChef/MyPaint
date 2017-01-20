'''
File: MyPaint.py
Name: Justin Jones
Date:
Description: MyPaint.py displays a basic paint program that is capable of drawing rectangles, ovals, arcs, lines and free
            pen drawings. Fill may be set or disabled as desired. The color of the most recent drawing may be changed to
            current color if it is not a free drawing (this works for fill state as well). Pen size varies from 1 to 20
            for free drawings, and is changed with a right-click pop-up menu.

'''

from tkinter import *
import tkinter.messagebox

class MyPaint:
    def __init__(self):
        window1 = Tk()
        window1.title("MyPaint")
        window1.configure(background = 'gray')
        window1.minsize(width = 1250, height = 850)
        self.canvas = Canvas(window1, width=1200, height=800, bg='white')
        self.xStart, self.yStart, self.xEnd, self.yEnd = 0,0,0,0

        #frames
        menuFrame = Frame(window1)
        buttonFrame = Frame(window1, bg = 'gray')
        bottomFrame = Frame(window1, bg = 'gray')

        menuFrame.pack()
        buttonFrame.pack()
        self.canvas.pack()
        bottomFrame.pack()
        #end frames

        #basic pen menu setup
        self.pen = IntVar()
        self.pen.set(1)
        self.myPop = Menu(self.canvas, tearoff=0)
        self.myPop.add_command(label = 'Increase Pen Size', command = self.penUp)
        self.myPop.add_command(label = 'Decrease Pen Size', command = self.penDown)
        self.myPop.add_command(label = 'Reset', command = self.reset)
        #end pen setup

        #top menu
        menuBar = Menu(menuFrame)
        window1.config(menu = menuBar)
        fileMenu = Menu(menuBar, tearoff = 0)
        menuBar.add_cascade(label = 'File', menu = fileMenu)
        fileMenu.add_command(label = 'Save', command = self.processSave)
        fileMenu.add_command(label = 'Quit', command = window1.quit)

        #draw menu
        drawMenu = Menu(menuBar, tearoff = 0)
        drawMenu.add_command(label = 'Clear', command = self.processClear)
        drawMenu.add_command(label = 'Clear Recent', command = self.processRecent)
        drawMenu.add_command(label = 'Rectangle', command = self.drawRect)
        drawMenu.add_command(label = 'Oval', command = self.drawOval)
        drawMenu.add_command(label = 'Line', command = self.drawLine)
        drawMenu.add_command(label = 'Arc', command = self.drawArc)
        menuBar.add_cascade(label='Free Draw', menu=drawMenu)

        helpMenu = Menu(menuBar, tearoff = 0)
        menuBar.add_cascade(label = 'Help', menu = helpMenu)
        helpMenu.add_command(label = 'Help', command = self.processHelp)
        #end menu bar

        #button/top bar
        rectButton = Button(buttonFrame, text = 'Rectangle', command = self.drawRect)
        ovalButton = Button(buttonFrame, text = 'Oval', command = self.drawOval)
        octButton = Button(buttonFrame, text = 'Arc', command = self.drawArc)
        lineButton = Button(buttonFrame, text = 'Line', command = self.drawLine)
        drawButton = Button(buttonFrame, text = 'Draw', command = self.freeDraw)
        penLabel = Label(buttonFrame, text = 'Pen Size: ', bg = 'gray', fg = 'white')
        penSize = Entry(buttonFrame, textvariable = self.pen, width = 2, state = 'readonly')

        rectButton.pack(side = LEFT), ovalButton.pack(side = LEFT), octButton.pack(side = LEFT), lineButton.pack(side = LEFT)
        drawButton.pack(side = LEFT), penLabel.pack(side = LEFT), penSize.pack(side = LEFT)
        #end button bar

        #bottom bar items
        self.fill = IntVar()
        self.fill.set(0)
        self.color = 'white'
        self.outline = IntVar()
        self.outline.set(1)
        fillButton = Checkbutton(bottomFrame, text = 'Fill', variable = self.fill, onvalue = 1, offvalue = 0)
        outlineButton = Checkbutton(bottomFrame, text = 'Outline', variable = self.outline, onvalue = 0, offvalue = 1)
        clearButton = Button(bottomFrame, text = 'Clear All', command = self.processClear)
        clearRecButton = Button(bottomFrame, text = 'Clear Last', command = self.processRecent)
        changeRecButton = Button(bottomFrame, text = 'Update Last Shape', command = self.changeColor)
        colorLabel = Label(bottomFrame, text = 'Colors:', bg = 'gray', fg = 'white')
        redButton = Button(bottomFrame, bg = "red", width = 3, command = lambda: self.processRed(redButton))
        blueButton = Button(bottomFrame, bg = "blue", width = 3, command = lambda: self.processBlue(blueButton))
        greenButton = Button(bottomFrame, bg = "green", width = 3, command = lambda: self.processGreen(greenButton))
        orangeButton = Button(bottomFrame, bg = 'orange', width = 3, command = lambda: self.processOrange(orangeButton))
        violetButton = Button(bottomFrame, bg = 'violet', width = 3, command = lambda: self.processViolet(violetButton))
        whiteButton = Button(bottomFrame, bg = 'white', width = 3, command = lambda: self.processWhite(whiteButton))
        blackButton = Button(bottomFrame, bg = 'black', width = 3, command = lambda: self.processBlack(blackButton))
        self.prevButton = whiteButton
        self.prevButton.config(relief = SUNKEN)

        colorMenu = Menu(bottomFrame)
        color = Menu(colorMenu, tearoff = 0)
        colorMenu.add_cascade(label = 'Color', menu = color)
        color.add_command(label = 'Red')

        fillButton.pack(side = LEFT), outlineButton.pack(side = LEFT), clearButton.pack(side = LEFT),
        clearRecButton.pack(side = LEFT), changeRecButton.pack(side = LEFT), colorLabel.pack(side = LEFT),
        redButton.pack(side = LEFT), blueButton.pack(side = LEFT), greenButton.pack(side = LEFT),
        orangeButton.pack(side = LEFT), violetButton.pack(side = LEFT), whiteButton.pack(side = LEFT),
        blackButton.pack(side = LEFT)
        #end bottom button bar

        #event bindings
        self.canvas.bind('<Button-1>', self.startShape)
        self.canvas.bind('<B1-Motion>', self.drawShape)
        self.canvas.bind('<ButtonRelease-1>', self.drawShape)
        self.canvas.bind('<Button-3>', self.popup)
        #end event bindings

        #remaining instance variable declaration/initialization
        self.xStart, self.yStart, self.xEnd, self.yEnd = 0, 0, 0, 0
        self.currentShape = 'rectangle'
        window1.mainloop()

    def processSave(self):
        self.canvas.postscript(file="save.ps", colormode='color')

    #draw-related methods
    def penUp(self):
        if self.pen.get() < 20:     #limit size
            self.pen.set(self.pen.get() + 1)

    def penDown(self):
        if self.pen > 1:            #limit size
            self.pen.set(self.pen.get() - 1)

    def popup(self, event):
        self.myPop.post(event.x_root, event.y_root)

    def reset(self):
        self.pen.set(1)

    def drawRect(self):
        self.currentShape = 'rectangle'

    def drawOval(self):
        self.currentShape = 'oval'

    def drawLine(self):
        self.currentShape = 'line'

    def drawArc(self):
        self.currentShape = 'arc'

    def freeDraw(self):
        self.currentShape = 'draw'
    #end draw-related methods

    #color methods
    def processRed(self, b):
        self.buttonState(b)
        self.color = "red"

    def processBlue(self, b):
        self.buttonState(b)
        self.color = "blue"

    def processGreen(self, b):
        self.buttonState(b)
        self.color = 'green'

    def processWhite(self, b):
        self.buttonState(b)
        self.color = 'white'

    def processOrange(self, b):
        self.buttonState(b)
        self.color = "orange"

    def processViolet(self, b):
        self.buttonState(b)
        self.color = 'violet'

    def processBlack(self, b):
        self.buttonState(b)
        self.color = 'black'
    #end color methods

    def buttonState(self, newButton):
        self.prevButton.config(relief=RAISED)
        newButton.config(relief = SUNKEN)
        self.prevButton = newButton

    def processHelp(self):
        #using the line continuation character \ caused display errors
        tkinter.messagebox.showinfo("Help", "To Draw: Select a shape, click and drag on canvas.\nTo set fill: Indicate state with checkbox, choose color.\nTo choose color: Use the drop-menu to pick a color.\nTo change last color: Choose new color, click 'Change Recent Color'\nTo clear most recent shape: Click 'Clear Last'.\nTo save: File > Save, file will be in program directory.\nRight click to increase/decrease/reset pen size.")

    #check for fill button, returns color if fill
    #will default black is shape is line & color is white (otherwise it's invisible)
    def processFill(self):
        if bool(self.fill.get()):
            if self.tag is 'line' and self.color is 'white':
                return 'black'
            else: return self.color
        elif self.tag is 'line':
            return 'black'
        else: return 'white'

    def processOutline(self):
        if bool(self.outline.get()):
            return self.color
        else: return 'black'

    #clears all
    def processClear(self):
        self.canvas.delete("all")

    #clears last, by tag
    def processRecent(self):
        self.canvas.delete(self.tag)

    #redraws last item with newly selected color
    def changeColor(self):
        if self.currentShape is 'rectangle':
            self.canvas.delete('rect')
            self.canvas.create_rectangle(self.xStart, self.yStart, self.xEnd, self.yEnd, outline = self.processOutline(), fill = self.processFill(), tags = 'rect')
        elif self.currentShape is 'oval':
            self.canvas.delete('oval')
            self.canvas.create_oval(self.xStart, self.yStart, self.xEnd, self.yEnd, outline = self.processOutline(), fill = self.processFill(), tags = 'oval')
        elif self.currentShape is 'line':
            self.canvas.delete('line')
            self.canvas.create_line(self.xStart, self.yStart, self.xEnd, self.yEnd, fill = self.processFill(), tags = 'line')
        elif self.currentShape is 'arc':
            self.canvas.delete('arc')
            self.canvas.create_arc(self.xStart, self.yStart, self.xEnd, self.yEnd, outline = self.processOutline(), fill = self.processFill(), tags = 'arc' )


    def startShape(self, event):
        self.xStart, self.yStart = event.x, event.y

    def drawShape(self, event):
        self.xEnd, self.yEnd = event.x, event.y

        if self.currentShape is 'rectangle':
            self.tag = 'rect'
            self.canvas.delete('rect')
            self.canvas.create_rectangle(self.xStart, self.yStart, self.xEnd, self.yEnd, outline = self.processOutline(), fill = self.processFill(), tags = 'rect')
        elif self.currentShape is 'draw':
            self.tag = 'draw'
            self.xStart, self.yStart = self.xEnd, self.yEnd
            self.canvas.create_oval(self.xStart, self.yStart, self.xStart + 2 * self.pen.get(), self.yStart + 2 * self.pen.get(),\
                                    outline = self.color, fill = self.color, tags = 'draw')
        elif self.currentShape is 'oval':
            self.tag = 'oval'
            self.canvas.delete('oval')
            self.canvas.create_oval(self.xStart, self.yStart, self.xEnd, self.yEnd, outline = self.processOutline(), fill = self.processFill(), tags = 'oval')
        elif self.currentShape is 'line':
            self.tag = 'line'
            self.canvas.delete('line')
            self.canvas.create_line(self.xStart, self.yStart, self.xEnd, self.yEnd, fill = self.processFill(), tags = 'line')
        else:
            self.tag = 'arc'
            self.canvas.delete('arc')
            self.canvas.create_arc(self.xStart, self.yStart, self.xEnd, self.yEnd, outline = self.processOutline(), fill = self.processFill(), tags = 'arc' )


MyPaint()