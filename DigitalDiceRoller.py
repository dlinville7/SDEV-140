#Title: Digital WarGame Dice Roller
#Author: Dillon Linville
#Goal: To create a GUI program that allows for a user to roll dice to complete a Warhammer 40k combat sequence.

#Needs: Error Checking for inputs
#Create Exit button & function
#Add pictures
#Instructions Button / Window

#Import Modules
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from random import *


#Create Window Frame
MainWindow = Tk(screenName="Digital Dice Roller")
MainWindow.geometry("400x400")

#Create Inner Window Title
TopTitle = Label(MainWindow,text="Digital Dice Roller. ")
TopTitle.grid(row=0,column=0,columnspan=5)

#Create Labels for Entry Boxes
ShotsLabel = Label(MainWindow, text="Number of Shots: ")
ShotsLabel.grid(row=1,column=0)

BSLabel = Label(MainWindow, text="Ballistic Skill: ")
BSLabel.grid(row=2,column=0) 

StrengthLabel = Label(MainWindow, text="Attack Strength: ")
StrengthLabel.grid(row=3,column=0)

ToughnessLabel = Label(MainWindow, text="Target's Toughness: ")
ToughnessLabel.grid(row=4,column=0)

APLabel = Label(MainWindow, text="Armor Penetration: ")
APLabel.grid(row=5,column=0)

EnemySaveLabel = Label(MainWindow, text="Enemy's Save: ")
EnemySaveLabel.grid(row=6,column=0)

DmgLabel = Label(MainWindow, text="Damage: ")
DmgLabel.grid(row=7,column=0)

#Define Tuples for comboboxes
ShotsOption = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
BSOption = ["+2","+3","+4","+5","+6"]
StrengthOption = ["2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]
ToughnessOption = ["2","3","4","5","6","7","8","9"]
APOption = ["-1","-2","-3","-4","-5","-6","-7"]
EnemySaveOption = ["+2","+3","+4","+5","+6"] 
DamageOption = ["1","2","3","4","5","6","7","8","9","10","11","12"]

#Create Combo Boxes
ShotsCombo = ttk.Combobox(MainWindow, values=ShotsOption)
ShotsCombo.grid(row=1,column=1)

BSCombo = ttk.Combobox(MainWindow, values=BSOption,state="readonly")
BSCombo.grid(row=2,column=1)

StrengthCombo = ttk.Combobox(MainWindow,values=StrengthOption,state="readonly")
StrengthCombo.grid(row=3,column=1)

ToughnessCombo = ttk.Combobox(MainWindow,values=ToughnessOption,state="readonly")
ToughnessCombo.grid(row=4,column=1)

APCombo = ttk.Combobox(MainWindow, values=APOption,state="readonly")
APCombo.grid(row=5,column=1)

SaveCombo = ttk.Combobox(MainWindow, values=EnemySaveOption, state="readonly")
SaveCombo.grid(row=6,column=1)

DmgCombo = ttk.Combobox(MainWindow, values=DamageOption)
DmgCombo.grid(row=7,column=1)

#Output Display
LowerTitle = Label(MainWindow, text="Results: ")
LowerTitle.grid(row=9,column=0,columnspan=5)

HitsLabel = Label(MainWindow,text="Number of Hits: ")
HitsLabel.grid(row=10,column=0)

WoundsLabel = Label(MainWindow, text="Number of Wounds: ")
WoundsLabel.grid(row=12,column=0)

DmgDealtLabel = Label(MainWindow, text="Amount of Damage: ")
DmgDealtLabel.grid(row=14,column=0) 



#Main Calculation Function 
def Calculate():

    #Define Function Variables
    SaveCounter = 0
    Counter = 0 #Multi-use counter for while loops

    ShotList = [] #Shot rolls
    HitList = [] #Confirmed Hits
    WoundList = [] #Unconfirmed Wound rolls
    ConfWoundList = [] #Confirmed Wound Rolls
    SaveList = [] #Non-saved, Confirmed Wound Rolls

    NumWounds = 0
    NumHits = 0 #Length of HitList
    WoundChance = 0 #Calulated via Strength vs. Toughness matrix
    DmgDealt = 0 #Actual Dmg Dealt
    SaveCounter = 0 #Counter to determine number of sucessful save


    #Pull values from the entry boxes, w/ error handling
    try:
        Shots = int(ShotsCombo.get())
    except ValueError:
        messagebox.showerror(title="Error",message="Error! For Number of Shots enter an Integer. ") 
    
    try:
        BalSkill = int(BSCombo.get()) ##Add some error checking to ensure int is 1-6 
    except ValueError:
        messagebox.showerror(title="Error",message="Error! For Ballistic Skill enter an Integer between 1 & 6. ") 
    
    try:
        Strength = int(StrengthCombo.get())
    except ValueError: 
        messagebox.showerror(title="Error",message="Error! For Strength enter an Integer. ")
    
    try:
        Toughness = int(ToughnessCombo.get())
    except ValueError:
        messagebox.showerror(title="Error",message="Error! For Toughness enter an Integer. ")

    try:
        Ap = int(APCombo.get())
    except ValueError:
        messagebox.showerror(title="Error",message="Error! For Armor Penetration enter an Integer. ")
    
    try:
        Dmg = int(DmgCombo.get())
    except ValueError:
        messagebox.showerror(title="Error",message="Error! For Damage enter an Integer. ")

    try: 
        EnemySave = int(SaveCombo.get())
    except ValueError:
        messagebox.showerror(title="Error",message="Error! For Enemy Save enter an Integer. ")
    
    #Create the rolls for ShotList
    while Counter < Shots:
        holder = randrange(1,7)
        ShotList.append(holder)
        Counter += 1
    Counter = 0 #reset Counter
    print("ShotList: ",ShotList) 
   
    #Based on BS determine if rolls in Shotlist are hits.
    for x in ShotList:
        if x >= BalSkill:
            HitList.append(x) #Append rolls to new HitList if they hit
    
    NumHits = len(HitList) #Determine total number of sucessful hits
    HitsLabel.config(text=f"Number of Hits: {NumHits} ") #Display number of hits

    #Matrix to determine WoundChance, based on Toughness vs. Strength
    if (Strength / 2) >= Toughness: #if Strength Twice(or more) than Toughness
        WoundChance = 2 #Wound on 2+
    elif Strength > Toughness: #If Str is Greater than Tough
        WoundChance = 3 #Wound on 3+
    elif Strength == Toughness: #If Str equals Toughness
        WoundChance = 4 #Wound on 4+
    elif Strength < (Toughness / 2): #If Str is Half (or less) than Toughness
        WoundChance = 6 #Wound on 6+
    elif Strength < Toughness: #If Str is less (but not less than half) of Toughness
        WoundChance = 5 #Wound on 5+

    print("WoundChance: ",WoundChance)
    
    #Generate the list of wound rolls
    while Counter < NumHits:
        holder = randrange(1,7)
        WoundList.append(holder)
        Counter += 1
    Counter = 0 #reset counter
    print("WoundList: ",WoundList)

    #Generate the list of confirmed wound, test if they are >= to WoundChance
    for x in WoundList: 
        if x >= WoundChance:
            ConfWoundList.append(x) 
    print("ConfWoundList: ",ConfWoundList)

    #Determine number of confirmed Wounds
    NumWounds = len(ConfWoundList) 
    print("NumWound: ",NumWounds)
    
    #Roll enemy saving throws, one for each Confirmed Wound
    while Counter < NumWounds:
        holder = randrange(1,7)
        SaveList.append(holder)
        Counter += 1
    Counter = 0 #Reset Counter
    print("SaveList: ",SaveList)

    print("AP: ",Ap)

    #Determine if Saving throws are succesful
    for x in SaveList:
        if (x + Ap) >= EnemySave: #Rolled save (x) plus (negative)Ap value, must be greater than/equal to EnemySave to pass
            SaveCounter += 1 #If pass, add 1 to the SaveCounter
    print("Save Counter: ",SaveCounter)
    
    #Determine the number of confirmed, un-saved wounds 
    NumWounds -= SaveCounter
    WoundsLabel.config(text=f"Number of Wounds: {NumWounds} ") #Display this value to the user

    #Multply the number of confirmed, un-saved wounds by their Dmg value
    DmgDealt = NumWounds * Dmg #Calculate total Damage Dealt
    DmgDealtLabel.config(text=f"Amount of Damage Dealt: {DmgDealt} ") #Display this value to the user

    
#Clear Combobox options function
def ClearCombos():
    ShotsCombo.set('')
    BSCombo.set('')
    StrengthCombo.set('')
    ToughnessCombo.set('')
    APCombo.set('')
    SaveCombo.set('')
    DmgCombo.set('') 





#Buttons
CalcButton = Button(MainWindow, text="Calculate",command=Calculate)
CalcButton.grid(row=8,column=0,columnspan=5)

PlusHit = Button(MainWindow,text="Clear", command=ClearCombos)
PlusHit.grid(row=11,column=0,columnspan=5)

PlusWound = Button(MainWindow,text="+1 to Wound",state="disabled")
PlusWound.grid(row=13,column=0,columnspan=5)

#Mainloop to run window
MainWindow.mainloop()

