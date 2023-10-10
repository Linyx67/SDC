from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

import accounts, computerVision, topView


def textboxMessage(box, message, tag):
    box.configure(state="normal")
    box.delete(1.0, END)
    if (tag == ""):
        box.insert(END, message)
    else:
        box.insert(END, message, tag)
    box.configure(state="disabled")

def addAccount(event):
    if accounts.createAccount(usernameEntry.get()) is True:
        print("Account created.")
        mainWindow.title(appName + " - " + usernameEntry.get())
        loginWindow.state("withdrawn")
        mainWindow.deiconify()
    else:
        textboxMessage(textbox, "Error. Possible causes: User " + usernameEntry.get() + " already exists or Invalid username.", "tag-center")
        print("Account NOT created.")

def signin(event):
    if accounts.login(usernameEntry.get()) is True:
        print("Log in successful.")
        mainWindow.title(appName + " - " + usernameEntry.get())
        loginWindow.state("withdrawn")
        mainWindow.deiconify()
    else:
        textboxMessage(textbox, "Error. Possible causes: User does not exist or Invalid entry.", "")
        print("Log in unsuccessful.")
    
def logout(event):
    textboxMessage(textbox, loginScreenPrompt, "")
    textboxMessage(reportTextbox, "", "")
    mainWindow.state("withdrawn")
    loginWindow.deiconify()
    usernameEntry.delete(0, END)

def confirmDestroy():
    prompt = messagebox.askquestion("Exit", "Are you sure?")
    if prompt == "yes":
           mainWindow.destroy()

def loadVtestReport(event):
    reportTextbox.configure(state="normal")
    reportTextbox.delete(1.0, END)
    with open("reports/vtest_feed_testrun.csv", "r") as vtestFile:
        reader = csv.reader(vtestFile, delimiter=",")
        data = list()
        for line in reader:
            if line[0] == "Time(secs)":
                heading = [line[0].strip(' '), line[1].strip(' {}'), line[2].strip(' {}'), line[3].strip(' {}')]
            else:
                data.append([round(float(line[0]), 2), line[1], line[2], line[3]])
    reportTextbox.insert(END, tabulate(data, headers=heading))
    reportTextbox.configure(state="disabled")

def loadPedReport(event):
    reportTextbox.configure(state="normal")
    reportTextbox.delete(1.0, END)
    with open("reports/pedestrians_feed_testrun.csv", "r") as vtestFile:
        reader = csv.reader(vtestFile, delimiter=",")
        data = list()
        for line in reader:
            if line[0] == "Time(secs)":
                heading = [line[0].strip(' '), line[1].strip(' {}'), line[2].strip(' {}'), line[3].strip(' {}')]
            else:
                data.append([round(float(line[0]), 2), line[1], line[2], line[3]])
    reportTextbox.insert(END, tabulate(data, headers=heading))
    reportTextbox.configure(state="disabled")

def loadReport(event):
    textboxMessage(reportTextbox, "", "")

    filepath = filepathTextbox.get(1.0, END)
    if len(filepathTextbox.get(1.0, END)) <= 4 or filepath[ ( filepath.rfind(".") ) + 1:len( filepath ) ].strip() not in ["mkv", "avi", "mp4", "mov", "wmv", "flv"]:
        textboxMessage(reportTextbox, "No video file found. Cannot generate logs.", "")
        return

    filepath = "reports/" + filepath[ ( filepath.rfind("/") ) + 1:filepath.rfind(".") ].strip() + ".csv"
    if os.path.isfile("./"+filepath) != True:
        textboxMessage(reportTextbox, "Log file not found. Click \"Show/Evaluate video file\" button.", "")
        return

    # "reports/pedestrians_feed_testrun.csv"
    reportTextbox.configure(state="normal")
    with open(filepath, "r") as vtestFile:
        reader = csv.reader(vtestFile, delimiter=",")
        data = list()
        for line in reader:
            if line[0] == "Time(secs)":
                heading = [line[0].strip(' '), line[1].strip(' {}'), line[2].strip(' {}'), line[3].strip(' {}')]
            else:
                data.append([round(float(line[0]), 2), line[1], line[2], line[3]])
    reportTextbox.insert(END, tabulate(data, headers=heading))
    reportTextbox.configure(state="disabled")

def viewGraph(event):
    filepath = filepathTextbox.get(1.0, END)
    if len(filepathTextbox.get(1.0, END)) <= 4 or filepath[ ( filepath.rfind(".") ) + 1:len( filepath ) ].strip() not in ["mkv", "avi", "mp4", "mov", "wmv", "flv"]:
        textboxMessage(reportTextbox, "No video file found. Cannot generate graph.", "")
        return

    filepath = "reports/" + filepath[ ( filepath.rfind("/") ) + 1:filepath.rfind(".") ].strip() + ".csv"
    if os.path.isfile("./"+filepath) != True:
        textboxMessage(reportTextbox, "Log file not found. Click \"Show/Evaluate video file\" button.", "")
        return

    times = list()
    personCounts = list()
    violationCounts = list()

    with open(filepath, "r") as vtestFile:
        reader = csv.reader(vtestFile, delimiter=",")
        for line in reader:
            if line[0] != "Time(secs)" and float(line[0]) <= 15:
                times.append( str( round( float(line[0]), 1) ) )
                personCounts.append(int(line[1]))
                violationCounts.append(int(line[3]))

            if line[0] != "Time(secs)" and float(line[0]) > 15:
                break

    barWidth = 0.25 
    bars1 = personCounts
    bars2 = violationCounts
 
    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
 
    plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Person count')
    plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='Violation Count')
 
    # Add xticks on the middle of the group bars
    plt.title("Person Count and Violation Count vs. Time")
    plt.xlabel('Time (s)', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(bars1))], times, rotation=90)
 
    # Create legend & Show graphic
    plt.legend()
    plt.show()


def viewVtestCamera(event):
    computerVision.testDetector1()
    #topView.testVideo1();

def viewPedCamera(event):
    computerVision.testDetector2()
    #topView.testVideo1();

def viewCamera(event):
    filepath = filepathTextbox.get(1.0, END)
    
    if (len(filepathTextbox.get(1.0, END)) <= 4):
        textboxMessage(filepathTextbox, "No file chosen.", "")
        textboxMessage(reportTextbox, "No file chosen.", "")
        return
    
    if filepath[(filepath.rfind("."))+1:len(filepath)].strip() in ["mkv", "avi", "mp4", "mov", "wmv", "flv"]:
        windowTitle = filepath[(filepath.rfind("/"))+1:filepath.rfind(".")].strip()
        computerVision.testDetector(filepath, windowTitle)
    else:
        textboxMessage(reportTextbox, "Invalid file path. Choose a video file.", "")
    

def viewCameraTopView(event):
    filepath = filepathTextbox.get(1.0, END)
    if len(filepathTextbox.get(1.0, END)) <= 4 or filepath[ ( filepath.rfind(".") ) + 1:len( filepath ) ].strip() not in ["mkv", "avi", "mp4", "mov", "wmv", "flv"]:
        textboxMessage(reportTextbox, "No video file found. Cannot generate transformation.", "")
        return

    topView.testVideo(filepath)

def browse(event):
    textboxMessage(reportTextbox, "", "")
    file = filedialog.askopenfilename(initialdir = "C:/Users/", title = "Select a video file to evaluate", filetypes = (("All files", "*.*"), ("AVI", "*.avi"), ("FLV", "*.flv"), ("MKV", "*.mkv"), ("MOV", "*.mov"), ("MP4", "*.mp4"), ("WMV", "*.wmv")))
    textboxMessage(filepathTextbox, file, "")


# CONSTANTS
appIconFilepath = "logo.png"

appName = "COVID Vision"
username = "Username: "
signIn = "Sign In"
createAccount = "Create Account"
loginScreenPrompt = "Fill out the form then click 'Sign In' to sign in or 'Create Account' to create an account."
formatLabelText = "Alphanumeric characters only. No spaces.\nMaximum of 15 characters allowed."

backgroundColor = "#263D42"
lightGray = "#DCDCDC"
padLarge = 45
padMed = 30
padSmall = 15
padXSmall = 5


# GUI variable initializations: window, labels, textbox, entry fields, buttons
# section 1: variables for main window, which is laid out in two frames, one on the left and one on the right
# main window
mainWindow = Tk()
mainWindow.title(appName)
mainWindow.minsize(width=500, height=450)
mainWindow.geometry("950x500")
mainWindow.configure(bg=backgroundColor)
mainWindow.state("withdrawn")
mainWindow.protocol("WM_DELETE_WINDOW", confirmDestroy)

# left frame of main window which holds menu to view reports and camera feeds
mainLeftFrame = Frame(mainWindow, bg=backgroundColor)
mainLeftFrame.pack(fill=X, padx=padXSmall, pady=padSmall, side="left", anchor="n")

logoutButton = Button(mainLeftFrame, text="Logout", bg=backgroundColor, fg=lightGray, relief=RIDGE)
logoutButton.pack(expand=True, fill=X, side="top", padx=padXSmall, pady=padSmall, ipadx=padLarge, ipady=padXSmall)
logoutButton.bind("<Button-1>", logout)
logoutButton.bind("<Return>", logout)

menuLabel = Label(mainLeftFrame, text="MENU", bg=backgroundColor, fg=lightGray, anchor="w")
menuLabel.pack(expand=True, fill=X, side="top", pady=(padSmall, padXSmall))

chooseVideoLabel = Label(mainLeftFrame, text="Choose a video file:", bg=backgroundColor, fg=lightGray, anchor="w")
chooseVideoLabel.pack(expand=True, fill=X, padx=padXSmall, side="top", pady=padXSmall)

fileExplorerFrame = Frame(mainLeftFrame, bg=backgroundColor)
fileExplorerFrame.pack(expand=True, fill=X, padx=0, side="top")

filepathTextbox = Text(fileExplorerFrame, bg=backgroundColor, fg=lightGray, borderwidth=1, relief=SUNKEN, width=15, height=2, wrap="char")
filepathTextbox.pack(expand=True, fill=X, side="left", pady=padXSmall, padx=(padXSmall, 1), ipadx=padLarge, ipady=padXSmall)

browseButton = Button(fileExplorerFrame, bg=backgroundColor, fg=lightGray, text="Browse", relief=RIDGE)
browseButton.pack(expand=True, side="right", pady=padXSmall, padx=(1, padXSmall), ipadx=padXSmall, ipady=2*padXSmall)
browseButton.bind("<Button-1>", browse)
browseButton.bind("<Return>", browse)

analyzeButton = Button(mainLeftFrame, bg=backgroundColor, fg=lightGray, text="Show/Evaluate video file", relief=RIDGE)
analyzeButton.pack(expand=True, fill=X, padx=padXSmall, pady=(padSmall, padXSmall), side="top", ipady=padXSmall)
analyzeButton.bind("<Button-1>", viewCamera)
analyzeButton.bind("<Return>", viewCamera)

quitInstructLabel = Label(mainLeftFrame, bg=backgroundColor, fg=lightGray, text="Press \"Q\" to exit video")
quitInstructLabel.pack(expand=True, fill=X, padx=padXSmall, pady=(0, padXSmall), side="top")

displayButtonFrame = Frame(mainLeftFrame, bg=backgroundColor)
displayButtonFrame.pack(expand=True, fill=X, padx=0, side="top")

displayLogsButton = Button(displayButtonFrame, bg=backgroundColor, fg=lightGray, text="Display log", relief=RIDGE)
displayLogsButton.pack(expand=True, fill=X, padx=padXSmall, pady=padSmall, side="left", ipady=padXSmall)
displayLogsButton.bind("<Button-1>", loadReport)
displayLogsButton.bind("<Return>", loadReport)

displayGraphButton = Button(displayButtonFrame, bg=backgroundColor, fg=lightGray, text="Display graph", relief=RIDGE)
displayGraphButton.pack(expand=True, fill=X, padx=padXSmall, pady=padSmall, side="left", ipady=padXSmall)
displayGraphButton.bind("<Button-1>",viewGraph)
displayGraphButton.bind("<Return>", viewGraph)

topViewButton = Button(mainLeftFrame, bg=backgroundColor, fg=lightGray, text="Show top view", relief=RIDGE)
topViewButton.pack(expand=True, fill=X, padx=padXSmall, pady=(padSmall, padXSmall), side="top", ipady=padXSmall)
topViewButton.bind("<Button-1>", viewCameraTopView)
topViewButton.bind("<Return>", viewCameraTopView)

quitInstructLabel2 = Label(mainLeftFrame, bg=backgroundColor, fg=lightGray, text="Press \"Q\" to exit video")
quitInstructLabel2.pack(expand=True, fill=X, padx=padXSmall, pady=(0, padXSmall), side="top")

# right frame of main window which holds textbox to display reports
mainRightFrame = Frame(mainWindow, bg=backgroundColor)
mainRightFrame.pack(expand=True, fill=BOTH, padx=padXSmall, pady=padXSmall, side="left")

reportTextbox = Text(mainRightFrame, wrap="none", fg=lightGray, bg=backgroundColor)
reportTextbox.configure(state="disabled")
reportTextbox.grid(row=0, column=0, sticky="nsew")

vertScroll = Scrollbar(mainRightFrame, orient="vertical", command=reportTextbox.yview)
vertScroll.grid(row=0, column=1, sticky="ns")

horScroll = Scrollbar(mainRightFrame, orient="horizontal", command=reportTextbox.xview)
horScroll.grid(row=1, column=0, sticky="ew")

reportTextbox.configure(yscrollcommand=vertScroll.set, xscrollcommand=horScroll.set)
mainRightFrame.grid_rowconfigure(0, weight=1)
mainRightFrame.grid_columnconfigure(0, weight=1)


# section 2: variables for login window
# login window
loginWindow = Toplevel()

# prompt frame holds main textbox prompt to user
promptFrame = Frame(loginWindow, bg=backgroundColor)
textbox = Text(promptFrame, bd=0, height=2, width=50, wrap="word", fg=lightGray, bg=backgroundColor, padx=padSmall)

# holds rest of GUI
bodyFrame = Frame(loginWindow, bg=backgroundColor)

# left frame holds app icon label and app name label
leftFrame = Frame(bodyFrame, bg=backgroundColor)
logo = PhotoImage(file=appIconFilepath)
logoLabel = Label(leftFrame, image=logo, bg=backgroundColor)
appNameLabel = Label(leftFrame, text=appName, bg=backgroundColor, fg=lightGray)

# right frame holds prompt textbox, username and password fields, submit and create account buttons
rightFrame = Frame(bodyFrame, bg=backgroundColor)

# label indicating username and password format
formatLabel = Label(rightFrame, text=formatLabelText, bg=backgroundColor, fg=lightGray)

# Frame holding Username label and entry field
userFrame = Frame(rightFrame)
usernameLabel = Label(userFrame, text=username, bg=backgroundColor, fg=lightGray)
usernameEntry = Entry(userFrame, bg=lightGray)

# frame holding sign in and create new account buttons
buttonFrame = Frame(rightFrame, bg=backgroundColor)
createButton = Button(buttonFrame, text=createAccount)
submitButton = Button(buttonFrame, text=signIn)



def gui():
    # login window
    loginWindow.title("Login")
    loginWindow.geometry("580x330")
    loginWindow.resizable(0,0)
    loginWindow.configure(bg=backgroundColor)
    loginWindow.protocol("WM_DELETE_WINDOW", confirmDestroy)

    # prompt frame holds main textbox prompt to user
    promptFrame.pack(expand=True, fill=X, padx=padMed, pady=0)

    # textbox used as main prompt to user
    textbox.tag_configure("tag-center", justify="center")
    textbox.insert(END, loginScreenPrompt, "tag-center")
    textbox.configure(state="disabled")
    textbox.pack(expand=True)

    bodyFrame.pack(expand=True, fill=BOTH)

    # left frame holds app icon and app name
    leftFrame.pack(expand=True, side="left", pady=(0, padMed), padx=(padSmall, 0))

    # app icon
    logoLabel.pack(expand=True, fill=BOTH)  # fill=BOTH

    # app name
    appNameLabel.pack(fill=X, expand=True, pady=padSmall)

    # right frame holds prompt textboxes, username field, password field, submit and create account buttons
    rightFrame.pack(fill=BOTH, expand=True, side="left", padx=(padSmall, padMed), pady=(0, padSmall))

    # label indicating username and password format
    formatLabel.pack(fill=X, expand=True)

    # Frame holding Username label and entry field
    userFrame.pack(fill=X, expand=True, padx=padLarge)
    usernameLabel.pack(fill=X, expand=True, side="left")
    usernameEntry.pack(fill=X, expand=True, side="left")
    usernameEntry.focus()
    usernameEntry.bind("<Return>", signin)

    # frame holding submit and create new account buttons
    buttonFrame.pack(fill=X, expand=True, pady=padSmall)

    # button to create a new account    
    createButton.bind("<Button-1>", addAccount)
    createButton.bind("<Return>", addAccount)
    createButton.pack(fill=X, side="left", expand=True, padx=padMed)

    # submit button
    submitButton.pack(fill=X, expand=True, side="left", padx=padSmall)
    submitButton.bind("<Button-1>", signin)
    submitButton.bind("<Return>", signin)

    # keep window open until you close it
    mainWindow.mainloop()


gui()