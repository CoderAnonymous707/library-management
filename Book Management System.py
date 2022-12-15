from tkinter import *
import json
import tkinter.font as font
from datetime import date

# Font tuples
fTup_content = ('Roboto', 10)
fTup_title = ('Roboto', 12)
fTup_entry = ('Calibri', 12)
fTup_heading = ('Roboto', 16)

adFile = open("adminpass.txt", "r")
adPass = adFile.readlines()
adPass = adPass[0]

print(adPass)



# Function to change window (<from window> object and function that opens <to window>)
def changeWindow(fromObj, toObjFunc):
    fromObj.destroy()
    toObjFunc()

# Function for the show password button
def showPass(passBoxObj):
        if passBoxObj.cget("show") == "•":
            passBoxObj.config(show="")
        else:
            passBoxObj.config(show="•")

# Function for login window
def open_loginWindow():
    # Function to be called to show password
    def checkCreds():
        usersDB = open("database.json")
        data = json.load(usersDB)

        username = usernameBox.get().lower()
        password = passBox.get()

        for user in data['users']:
            if (username == user['username'] or username == user['fullname']) and password == user['password']:
                # lbOut.config(text="Correct username/password")
                if user['admin'] == True:
                    changeWindow(loginWindow, lambda:mainWindow_admin(user))
                else:
                    changeWindow(loginWindow, lambda:mainWindow_user(user))
                break
            else:
                lbOut.config(text="Incorrect username/password")

    loginWindow = Tk()

    # =============== [LOGIN UI] =============== #

    loginWindow.title("Library Management | Login")
    loginWindow.geometry("450x300")
    loginWindow.resizable(width=0, height=0)

    showPassVar = False
    lbSp = Label(loginWindow, text="\t\t")
    lbSp.grid(row=0, column=0)

    lbSp = Label(loginWindow, text="\t\t")
    lbSp.grid(row=1, column=0)

    lb1 = Label(loginWindow, text="Library Management System", font="Roboto")
    lb1.grid(row=1, column=1, pady=8)

    lbSp = Label(loginWindow, text="\t\t")
    lbSp.grid(row=3, column=0)

    lbOut = Label(loginWindow, text="Please Enter your Login Username and Password", width=36)
    lbOut.grid(row=3, column=1, pady=12)

    lbSp = Label(loginWindow, text="\t\t")
    lbSp.grid(row=4, column=0)

    lbUN = Label(loginWindow, text="Username", font="Roboto")
    lbUN.grid(row=4, column=0)

    usernameBox = Entry(loginWindow, width=25, font=("Calibri", 13))
    usernameBox.grid(row=4, column=1, pady=5)

    lbPass = Label(loginWindow, text="Password", font="Roboto")
    lbPass.grid(row=5, column=0)

    passBox = Entry(loginWindow, width=25, font=("Calibri", 13), show="•")
    passBox.grid(row=5, column=1, pady=5)

    lbSp = Label(loginWindow, text="     ")
    lbSp.grid(row=5, column=2)

    showPassBtn = Button(loginWindow, text="Show", command=lambda:showPass(passBox), font=("Roboto", 10))
    showPassBtn.grid(row=5, column=3)

    submitBtn = Button(loginWindow, text="Login", width=10, command=checkCreds, font=("Roboto", 10))
    submitBtn.grid(row=6, column=1, pady=15)

    newaccBtn = Button(loginWindow, text="Sign up", width=10, command=lambda:newAccWindow(loginWindow), font=("Roboto", 10))
    newaccBtn.grid(row=7, column=1)

    loginWindow.mainloop()

# Function for new account window (takes in login window object to destroy it)
def newAccWindow(loginWinObj):
    loginWinObj.destroy()
    newaccWin = Tk()
    newaccWin.title('Library Management | Create New Account')
    newaccWin.geometry("450x450")
    newaccWin.resizable(width=0, height=0)

    # Function to update details and get back to window
    def finishProcess(username, name, password, isAdmin, door, street, county, district, pin, currentWindowObj, ps):
        notFilled = False 
        dataList = [username, name, password, isAdmin, door, street, county, district, pin]

        print(isAdmin)

        if "" in dataList:
            notFilled = True

        do_it = False

        file = open("database.json", 'r+')
        data = json.load(file)
        
        if isAdmin:
            print("Is Admin")
            if ps == adPass:
                userData = {"username": username, 
                        "fullname": name,
                        "password": password,
                        "admin": isAdmin,
                        "address": {
                            "door": door, 
                            "street": street, 
                            "county": county,
                            "district": district,
                            "pin": pin
                        }
                    }

                do_it = True

            else:
                lb = Label(newaccWin, text="Incorrect Admin Password", font=fTup_content)
                lb.grid(row=13, column=1, pady=2)
            
            if ps == adPass and notFilled:
                lb = Label(newaccWin, text="Fill all the details", font=fTup_content)
                lb.grid(row=13, column=1, pady=2)
        else:
            if notFilled:
                lb = Label(newaccWin, text="Fill all the details", font=fTup_content)
                lb.grid(row=13, column=1, pady=2)
            else:
                userData = {"username": username, 
                        "fullname": name,
                        "password": password,
                        "admin": isAdmin,
                        "address": {
                            "door": door, 
                            "street": street, 
                            "county": county,
                            "district": district,
                            "pin": pin
                        }
                    }
                
                userData.update({"bookInfo": {"borrowed": {"books": [], "dates": []}, "read": {"books": [], "dates": []}}})
                
                do_it = True
            
        if do_it:
            data['users'].append(userData)
            file.seek(0)
            json.dump(data, file, indent = 4)
            file.close()

            changeWindow(currentWindowObj, open_loginWindow)

    lbSp = Label(newaccWin, text="\t\t\t")
    lbSp.grid(row=0, column=0)

    lb = Label(newaccWin, text="Create new account", font=fTup_title)
    lb.grid(row=0, column=1, pady=8)

    lb = Label(newaccWin, text="Type of Account", font=fTup_content)
    lb.grid(row=1, column=0, pady=8)

    global adminAcc
    adminAcc = False

    def adminPassControl(adminAcc):
        if adminAcc == False:
            adminAcc = True
            adminpassBox.config(state=NORMAL)
        else:
            adminAcc = False
            adminpassBox.config(state=DISABLED)

    rdBtnUser = Radiobutton(newaccWin, text="Library User", font=('Roboto', 10), variable=adminAcc, value=False,
    command=lambda:adminPassControl(adminAcc))
    rdBtnUser.grid(row=1, column=1)

    rdBtnUser = Radiobutton(newaccWin, text="Administrator", font=('Roboto', 10), variable=adminAcc, value=True,
    command=lambda:adminPassControl(adminAcc))
    rdBtnUser.grid(row=1, column=2)

    lb = Label(newaccWin, text="Admin Code*", font=fTup_content)
    lb.grid(row=2, column=0)

    adminpassBox = Entry(newaccWin, font=fTup_entry, state=DISABLED)
    adminpassBox.grid(row=2, column=1, pady=2)

    lb = Label(newaccWin, text="Username", font=fTup_content)
    lb.grid(row=3, column=0)

    usernameBox_reg = Entry(newaccWin, font=fTup_entry)
    usernameBox_reg.grid(row=3, column=1, pady=2)

    lb = Label(newaccWin, text="Password", font=fTup_content)
    lb.grid(row=4, column=0)

    passBox_reg = Entry(newaccWin, font=fTup_entry, show="•")
    passBox_reg.grid(row=4, column=1, pady=2)

    showBtn = Button(newaccWin, text="Show", font=fTup_content, command=lambda:showPass(passBox_reg))
    showBtn.grid(row=4, column=2)

    lb = Label(newaccWin, text="Full Name", font=fTup_content)
    lb.grid(row=5, column=0)

    nameBox_reg = Entry(newaccWin, font=fTup_entry)
    nameBox_reg.grid(row=5, column=1, pady=2)

    lb = Label(newaccWin, text="Residence Details", font=fTup_title)
    lb.grid(row=6, column=0)

    lb = Label(newaccWin, text="Door/Plot Number", font=fTup_content)
    lb.grid(row=7, column=0)

    doorBox_reg = Entry(newaccWin, font=fTup_entry)
    doorBox_reg.grid(row=7, column=1, pady=2)

    lb = Label(newaccWin, text="Street", font=fTup_content)
    lb.grid(row=8, column=0)

    streetBox_reg = Entry(newaccWin, font=fTup_entry)
    streetBox_reg.grid(row=8, column=1, pady=2)

    lb = Label(newaccWin, text="County", font=fTup_content)
    lb.grid(row=9, column=0)

    countyBox_reg = Entry(newaccWin, font=fTup_entry)
    countyBox_reg.grid(row=9, column=1, pady=2)

    lb = Label(newaccWin, text="District", font=fTup_content)
    lb.grid(row=10, column=0)

    districtBox_reg = Entry(newaccWin, font=fTup_entry)
    districtBox_reg.grid(row=10, column=1, pady=2)

    lb = Label(newaccWin, text="Residence Pincode", font=fTup_content)
    lb.grid(row=11, column=0)

    pinBox_reg = Entry(newaccWin, font=fTup_entry)
    pinBox_reg.grid(row=11, column=1, pady=2)

    submitBtn_reg = Button(newaccWin, text="Submit Details", font=fTup_content, command=lambda:finishProcess(
        usernameBox_reg.get().lower(),
        nameBox_reg.get(), 
        passBox_reg.get(), 
        adminAcc,
        doorBox_reg.get(), 
        streetBox_reg.get(), 
        countyBox_reg.get(), 
        districtBox_reg.get(),
        pinBox_reg.get(),
        newaccWin,
        adminpassBox.get()))
    
    submitBtn_reg.grid(row=12, column=1, pady=20)

    newaccWin.protocol("WM_DELETE_WINDOW", lambda:changeWindow(newaccWin, open_loginWindow))
    newaccWin.mainloop()

# Function to show the main window for user
def mainWindow_user(userDetails_dict):

    booksFound = []

    def searchBook(bookName):
        bookRequired = str()
        bookName = bookName.lower()

        def regtoDeliver(bkObj):
            bookName = bkObj['name']
            
            # Registering names in demands
            if userDetails_dict['username'] not in bookList[bookList.index(bkObj)]['demands']['requests']:
                bookList[bookList.index(bkObj)]['demands']['requests'].append(userDetails_dict['username'])
                bookList[bookList.index(bkObj)]['storeInfo']['borrowedUnits'] += 1

            file = open('books.json', 'w+')

            json.dumps(data, indent=4)
            dataToAdd = str()

            for i in str(data):
                if i == "'":
                    dataToAdd += '"'
                else:
                    dataToAdd += i

            file.write(str(dataToAdd))

        # Initialising the json file
        file = open('books.json', 'r+')
        data = json.load(file)
        file.close()

        bookList = data['books']

        booksFound = []

        for book in bookList:
            if bookName in book['name'].lower():
                booksFound.append(book)
        
        # mnWin.destroy()

        resltsWin = Tk()
        resltsWin.geometry('650x300')
        resltsWin.title("Search Results")

        lbsp = Label(resltsWin, text="  ")
        lbsp.grid(row=0, column=0)

        lb = Label(resltsWin, text="Results Found", font=fTup_title, fg="#eb345b")
        lb.grid(row=0, column=1, pady=10, sticky=W)

        beginRow = 1        
        listOfGetButtons = []

        # If there are no results
        if len(booksFound) == 0:
            lb = Label(resltsWin, text="Sorry, no such book available!", font=fTup_content)
            lb.grid(row=beginRow, column=1, sticky=W)
        else:
            lbTable = Label(resltsWin, text="Book ID", font=fTup_content)
            lbTable.grid(row=beginRow, column=1, pady=5)
            lbTable['font'] = font.Font(weight='bold')

            lbTable = Label(resltsWin, text="Name of Book", width=20, font=fTup_content)
            lbTable['font'] = font.Font(weight='bold')
            lbTable.grid(row=beginRow, column=2)

            lbTable = Label(resltsWin, text="Genre", width=7, font=fTup_content)
            lbTable['font'] = font.Font(weight='bold')
            lbTable.grid(row=beginRow, column=3)

            lbTable = Label(resltsWin, text="Rating", width=8, font=fTup_content)
            lbTable['font'] = font.Font(weight='bold')
            lbTable.grid(row=beginRow, column=4)

            lbTable = Label(resltsWin, text="Status", width=14, font=fTup_content)
            lbTable['font'] = font.Font(weight='bold')
            lbTable.grid(row=beginRow, column=5)

            for book in booksFound:
                lb = Label(resltsWin, text=book['id'], font=fTup_content)
                lb.grid(row=beginRow+1, column=1, sticky=W)

                lb = Label(resltsWin, text=book['name'], font=fTup_content)
                lb.grid(row=beginRow+1, column=2, sticky=W)

                lb = Label(resltsWin, text=book['genre'], font=fTup_content)
                lb.grid(row=beginRow+1, column=3, sticky=W)

                lb = Label(resltsWin, text=book['rating'], font=fTup_content)
                lb.grid(row=beginRow+1, column=4)

                # Calculate Availability
                availability = book['storeInfo']['availUnits'] - book['storeInfo']['borrowedUnits']

                if availability > 0 and book['name'] not in userDetails_dict['bookInfo']['borrowed']['books'] and userDetails_dict['username'] not in book['demands']['requests']:
                    lb = Label(resltsWin, text="Available", font=fTup_content, fg="#00a60e")
                    lb.grid(row=beginRow+1, column=5, sticky=W)

                    print(userDetails_dict['username'])

                    button = Button(resltsWin, text="Get", command=lambda bookObj=book: regtoDeliver(bookObj))
                    button.grid(row=beginRow+1, column=6, pady=5)
                else:
                    if book['name'] in userDetails_dict['bookInfo']['borrowed']['books']:
                        lb = Label(resltsWin, text="Borrowed", font=fTup_content, fg="#13419e")
                        lb.grid(row=beginRow+1, column=5, sticky=W)

                    elif userDetails_dict['username'] in book['demands']['requests']:
                        lb = Label(resltsWin, text="Already Requested", font=fTup_content, fg="#13419e")
                        lb.grid(row=beginRow+1, column=5, sticky=W)

                    else:
                        lb = Label(resltsWin, text="Unavailable", font=fTup_content, fg="#ba0c00")
                        lb.grid(row=beginRow+1, column=5, sticky=W)
                    
                    button = Button(resltsWin, text="Get", state=DISABLED)
                    button.grid(row=beginRow+1, column=6, pady=5)
                
                # Button object is getting appended in list
                listOfGetButtons.append(button)

                beginRow += 1

        # resltsWin.protocol("WM_DELETE_WINDOW", lambda:changeWindow(resltsWin, mainWindow_user(userDetails_dict)))
        resltsWin.mainloop()

    mnWin = Tk()
    mnWin.title("Library Dashboard | " + userDetails_dict['fullname'])
    mnWin.geometry("800x600")
    mnWin.resizable(width=0, height=1)

    lbsp = Label(mnWin, text="          ")
    lbsp.grid(row=0, column=0)

    head = Label(mnWin, font=fTup_heading, text="Welcome " + str(userDetails_dict['fullname']).split()[0])
    head.grid(row=0, column=1, pady=15, sticky=W)

    lbsp = Label(mnWin, text="          ")
    lbsp.grid(row=1, column=0)

    lb = Label(mnWin, font=fTup_title, text="What would you like to do today?")
    lb.grid(row=1, column=1, sticky=W)

    lb = Label(mnWin, text="Search for Books: ", font=fTup_title, fg="#13419e")
    lb.grid(row=2, column=1, pady=30)

    searchbkBox = Entry(mnWin, font=("Calibri", 14), width=30)
    searchbkBox.grid(row=2, column=2)

    searchbkBtn = Button(mnWin, text="Search", font=fTup_title, command=lambda:searchBook(searchbkBox.get()))
    searchbkBtn.grid(row=2, column=3, padx=25)

    lb = Label(mnWin, text="Currently Borrowed", font=fTup_title, fg="#eb345b")
    lb.grid(row=3, column=1, sticky=W, pady=10)

    bookInd = 0
    boldText = font.Font(weight='bold')

    if len(userDetails_dict['bookInfo']['borrowed']['books']) > 0:
        tableLb = Label(mnWin, text="Book(s) Borrowed", font=("Roboto", 12))
        tableLb.grid(row=4, column=1)
        tableLb['font'] = boldText

        tableLb = Label(mnWin, text="Borrowed at", font=("Roboto", 12))
        tableLb.grid(row=4, column=2)
        tableLb['font'] = boldText
    else:
        lb = Label(mnWin, text="You have borrowed no books yet!", font=fTup_content)
        lb.grid(row=4, column=1, sticky=W)

    # Variable to store the ending row of the table
    endingRow = 5

    for rw in range(5, 5 + len(userDetails_dict['bookInfo']['borrowed']['books'])):
        bookLb = Label(mnWin, text=userDetails_dict['bookInfo']['borrowed']["books"][bookInd], font=fTup_content)
        bookLb.grid(row=rw, column=1, pady=2, sticky=W)

        dateLb = Label(mnWin, text=userDetails_dict['bookInfo']['borrowed']['dates'][bookInd], font=fTup_content)
        dateLb.grid(row=rw, column=2)

        # When the loop reaches its last iteration
        if rw == 4 + len(userDetails_dict['bookInfo']['borrowed']['books']):
            endingRow = rw + 1

        bookInd += 1
    
    # Use 'row' as endingRow from here...

    lbsp = Label(mnWin, text="", font=('Calibri', 2))
    lbsp.grid(row=endingRow, column=1)

    lb = Label(mnWin, text="Your Reading History", font=fTup_title, fg="#eb345b")
    lb.grid(row=endingRow+1, column=1, pady=10, sticky=W)

    if len(userDetails_dict['bookInfo']['read']['books']) > 0:
        tableLb = Label(mnWin, text="Book(s) Read", font=("Roboto", 12))
        tableLb.grid(row=endingRow+2, column=1)
        tableLb['font'] = boldText

        tableLb = Label(mnWin, text="Returned at", font=("Roboto", 12))
        tableLb.grid(row=endingRow+2, column=2)
        tableLb['font'] = boldText
    else:
        lb = Label(mnWin, text="You have not read anything yet!", font=fTup_content)
        lb.grid(row=endingRow+2, column=1, sticky=W)

    bookInd = 0
    endingRow1 = endingRow+3

    for rw in range(endingRow+3, (endingRow+3) + len(userDetails_dict['bookInfo']['read']['books'])):
        bookLb = Label(mnWin, text=userDetails_dict['bookInfo']['read']["books"][bookInd], font=fTup_content)
        bookLb.grid(row=rw, column=1, pady=2, sticky=W)

        dateLb = Label(mnWin, text=userDetails_dict['bookInfo']['read']['dates'][bookInd], font=fTup_content)
        dateLb.grid(row=rw, column=2)

        # When the loop reaches its last iteration
        if rw == 4 + len(userDetails_dict['bookInfo']['read']['books']):
            endingRow1 = rw + 1

        bookInd += 1
    
    # Use 'row' as endingRow1 from here...
    
    lbsp = Label(mnWin, text="", font=('Calibri', 2))
    lbsp.grid(row=endingRow1, column=1)

    lb = Label(mnWin, text="Requested Books", font=fTup_title, fg="#eb345b")
    lb.grid(row=endingRow1+2, column=1, pady=10, sticky=W)

    username = userDetails_dict['username']

    booksDB = open('books.json')
    books = json.load(booksDB)['books']

    reqBooksID = []
    reqBooksName = []

    for i in books:
        if username in i['demands']['requests']:
            reqBooksID += [i['id']]
            reqBooksName += [i['name']]

    if len(reqBooksID) > 0:
        tableLb = Label(mnWin, text="Book Name", font=("Roboto", 12))
        tableLb.grid(row=endingRow1+3, column=1)
        tableLb['font'] = boldText

        tableLb = Label(mnWin, text="Book ID", font=("Roboto", 12))
        tableLb.grid(row=endingRow1+3, column=2)
        tableLb['font'] = boldText

        endingRow = endingRow1 + 4

        for i in range(len(reqBooksID)):
            nameLB = Label(mnWin, text=reqBooksName[i], font=fTup_content).grid(column=1, row=endingRow, sticky=W, pady=2)
            idLB = Label(mnWin, text=reqBooksID[i], font=fTup_content).grid(column=2, row=endingRow, pady=2)
            endingRow += 1
    else:
        lb = Label(mnWin, text="You have not requested any books, for now!", font=fTup_content)
        lb.grid(row=endingRow1+3, column=1, sticky=W)

    endingRow2 = endingRow1 + endingRow

    file = open('books.json')
    booksData = json.load(file)['books']
    file.close()

    logoutBtn = Button(mnWin, text="Logout", font=fTup_content, command=lambda:changeWindow(mnWin, open_loginWindow))
    logoutBtn.grid(row=0, column=4)

    bookInd = 0

    for rw in range(endingRow2+4, (endingRow2+4) + len(booksData[bookInd]['demands']['requests'])):
        '''bookLb = Label(mnWin, text=userDetails_dict['bookInfo']['read']["books"][bookInd], font=fTup_content)
        bookLb.grid(row=rw, column=1, pady=2, sticky=W)

        dateLb = Label(mnWin, text=userDetails_dict['bookInfo']['read']['dates'][bookInd], font=fTup_content)
        dateLb.grid(row=rw, column=2)'''

        if userDetails_dict['username'] in booksData[bookInd]['demands']['requests']:
            bookLb = Label(mnWin, text=booksData[bookInd]['name'], font=fTup_content)
            bookLb.grid(row=rw, column=1, pady=2, sticky=W)

            bookLb = Label(mnWin, text=booksData[bookInd]['id'], font=fTup_content)
            bookLb.grid(row=rw, column=2, pady=2)

        # When the loop reaches its last iteration
        if rw == 4 + len(userDetails_dict['bookInfo']['read']['books']):
            endingRow2 = rw + 1

        bookInd += 1
    
    mnWin.mainloop()

# Function to show the main window for admin
def mainWindow_admin(userDetails_dict):
    mnWin = Tk()
    mnWin.title("Library Admin Dashboard | " + userDetails_dict['fullname'])
    mnWin.geometry("800x600")

    lbsp = Label(mnWin, text="          ")
    lbsp.grid(row=0, column=0)

    head = Label(mnWin, font=fTup_heading, text="Welcome " + userDetails_dict['fullname'])
    head.grid(row=0, column=1, pady=15, sticky=W)

    lbsp = Label(mnWin, text="          ")
    lbsp.grid(row=1, column=0)

    logoutBtn = Button(mnWin, text="Logout", font=fTup_content, command=lambda:changeWindow(mnWin, open_loginWindow))
    logoutBtn.grid(row=0, column=4)

    lb = Label(mnWin, font=fTup_title, text="What would you like to do today?")
    lb.grid(row=1, column=1, sticky=W)

    lb = Label(mnWin, text=" ", font=("Arial", 12))
    lb.grid(row=2, column=1)

    lb = Label(mnWin, text="Requested Books", font=fTup_title, fg="#eb345b")
    lb.grid(row=3, column=1, pady=10, sticky=W)

    file = open('books.json')
    booksData = json.load(file)['books']
    file.close()

    file = open('database.json')
    usersData = json.load(file)['users']
    file.close()

    bookRequests = {}

    endingRow = 4

    for user in usersData:
        localList = []
        for book in booksData:
            if user['username'] in book['demands']['requests']:
                localList.append([book['name'], book['id']])
        dict = {user['fullname']: [user['fullname']] + localList}

        # Adding the key value pair to dictionary
        bookRequests.update(dict)

    def openBooksinWindow(bookList):
        booksWin = Tk()
        booksWin.title("Books requested by " + str(bookList[0]))
        booksWin.geometry("520x200")
        
        space = Label(booksWin, text="      ").grid(column=0, row=0)

        endingRow = 3

        daList = bookList.copy()

        name = daList.pop(0)

        title = Label(booksWin, text=str(len(daList)) + " Book(s) Requested by " + name.split()[0], font=fTup_title).grid(column=1, row=0, pady=10)

        head = Label(booksWin, text="Book Name", font=("Calibri", 13))
        head.grid(column=1, row=2, pady=5)
        # head['font'] = font.Font(weight='bold')

        head = Label(booksWin, text="Book ID", font=("Calibri", 13))
        head.grid(column=2, row=2)
        # head['font'] = font.Font(weight='bold')

        def deleteUserRequest(book, user):
            file = open('books.json', 'r+')
            jsonBooks = json.load(file)
            jsonUsers = json.load(open('database.json'))['users']
            file.close()

            for i in jsonUsers:
                if i['fullname'] == user:
                    username = i['username']
                    break

            # Removing the user from the requests list of the book (they have recieved it now)
            for i in range(len(jsonBooks['books'])):
                if jsonBooks['books'][i]['name'] == book[0] and jsonBooks['books'][i]['id'] == book[1]:
                    jsonBooks['books'][i]['demands']['requests'].remove(username)

            # Overwriting the new json code in the file
            file = open('books.json', 'w+')
            jsonForm = json.dumps(jsonBooks, indent=4)
            file.writelines(jsonForm)
            file.close()

            # Now we have to add the book to the 'borrowed' list in database.json
            userDB = open('database.json', 'r+')
            userJSON = json.load(userDB)
            users = userJSON['users']
            userDB.close()

            for user in users:
                if user['username'] == username:
                    user['bookInfo']['borrowed']['books'] += [book[0]]
                    user['bookInfo']['borrowed']['dates'] += [str(date.today())]
            
            userDB = open('database.json', 'w+')
            userDB.writelines(json.dumps(userJSON, indent=4))
            userDB.close()

            deliveredBtn.config(state = DISABLED)


        for i in daList:
            label = Label(booksWin, text=i[0], font=fTup_content).grid(column=1, row=endingRow, sticky=W)

            label = Label(booksWin, text=i[1], font=fTup_content).grid(column=2, row=endingRow)

            spc = Label(booksWin, text="     ").grid(column=3, row=endingRow)

            deliveredBtn = Button(booksWin, text="Mark as Delivered", font=fTup_content, command=lambda book=i, user=bookList[0]: deleteUserRequest(book, user))
            deliveredBtn.grid(column=4, row=endingRow)

            endingRow += 1
        
        booksWin.mainloop()

    available = False

    for i in bookRequests:
        if len(bookRequests[i]) > 1:
            button = Button(mnWin, text=i, font=('Roboto', 11), width=25, borderwidth=0, anchor='w', command=lambda bookObj=bookRequests[i]: openBooksinWindow(bookObj))
            button.grid(column=1, row=endingRow, sticky=W)

            booksStr = bookRequests[i][1][0]

            if len(bookRequests[i]) > 2:
                booksStr += "..."
            
            lbl = Label(mnWin, text=booksStr, font=fTup_content).grid(column=2, row=endingRow, sticky=W)

            endingRow += 1
            available = True
    
    if available == False:
        lbl = Label(mnWin, text="No book requests!", font=fTup_content).grid(column=1, row=endingRow)

    lb = Label(mnWin, text="Update Books", font=fTup_title, fg="#eb345b")
    lb.grid(row=endingRow+1, column=1, sticky=W)

    def addBook():
        addWin = Tk()
        addWin.geometry("400x260")

        space = Label(addWin, text="    ").grid(row=0, column=0)

        lbl = Label(addWin, text="Enter Book Details", font=fTup_title, fg="#eb345b").grid(row=0, column=2, pady=12)

        lbl = Label(addWin, text="ID", font=fTup_content).grid(row=1, column=1, sticky=W)
        lbl = Label(addWin, text="Name", font=fTup_content).grid(row=2, column=1, sticky=W)
        lbl = Label(addWin, text="Genre", font=fTup_content).grid(row=3, column=1, sticky=W)
        lbl = Label(addWin, text="Rating", font=fTup_content).grid(row=4, column=1, sticky=W)
        lbl = Label(addWin, text="Quantity      ", font=fTup_content).grid(row=5, column=1, sticky=W)

        idEntry = Entry(addWin, font=fTup_entry, width=30)
        idEntry.grid(row=1, column=2, sticky=W, pady=2)

        nameEntry = Entry(addWin, font=fTup_entry, width=30)
        nameEntry.grid(row=2, column=2, sticky=W, pady=2)

        genreEntry = Entry(addWin, font=fTup_entry, width=30)
        genreEntry.grid(row=3, column=2, sticky=W, pady=2)

        ratingEntry = Entry(addWin, font=fTup_entry, width=30)
        ratingEntry.grid(row=4, column=2, sticky=W, pady=2)

        quantityEntry = Entry(addWin, font=fTup_entry, width=30)
        quantityEntry.grid(row=5, column=2, sticky=W, pady=2)

        def addBook(id, name, genre, rating, quantity):
            db = open("books.json", "r+")

            dic = json.load(db)

            db.truncate(0)
            db.close()

            dic['books'] += [{'id': id, 'name': name, 'genre': genre, 'rating': rating, "storeInfo": {"availUnits": int(quantity), "borrowedUnits": 0}, "demands": {"requests": []}}]

            jsonObj = json.dumps(dic, indent=4)
            db = open("books.json", "w+")
            db.writelines(jsonObj)

            db.close()

            addWin.destroy()

        updateBtn = Button(addWin, text="Update Database", command=lambda:addBook(idEntry.get(), nameEntry.get(), genreEntry.get(), ratingEntry.get(), quantityEntry.get())).grid(row=6, column=2, pady=20)

        addWin.mainloop()

    lb = Label(mnWin, text="Update Books", font=fTup_title, fg="#eb345b")
    lb.grid(row=endingRow+1, column=1, pady=15, sticky=W)

    btn = Button(mnWin, text="Add Book", font=fTup_content, command=addBook)
    btn.grid(row=endingRow+2, column=1)

    lb = Label(mnWin, text="Search Books", font=fTup_title, fg="#eb345b")
    lb.grid(row=endingRow+3, column=1, pady=15, sticky=W)

    lb = Label(mnWin, text="Enter the Book here to get Details", font=fTup_content)
    lb.grid(row=endingRow+4, column=1, sticky=W)

    searchBox = Entry(mnWin, width=30, font=fTup_entry)
    searchBox.grid(row=endingRow+4, column=2)

    def searchBk():

        def provideInfo(info):
            infoWin = Tk()
            infoWin.geometry('420x350')
            infoWin.title(info['name'] + " | Information")

            sp = Label(infoWin, text="     ").grid(column=0, row=0)

            lbl = Label(infoWin, text=info['name'].split("-")[0], font=fTup_heading, fg="#eb345b").grid(column=1, row=0, pady=20)

            lbl = Label(infoWin, text="ID", font=("Roboto", 12), fg="#eb345b").grid(column=1, row=1, sticky=E)
            lbl = Label(infoWin, text="Name", font=("Roboto", 12), fg="#eb345b").grid(column=1, row=2, sticky=E)
            lbl = Label(infoWin, text="Genre", font=("Roboto", 10), fg="#eb345b").grid(column=1, row=3, sticky=E)
            lbl = Label(infoWin, text="Rating", font=("Roboto", 10), fg="#eb345b").grid(column=1, row=4, sticky=E)

            sp = Label(infoWin, text="     ").grid(column=2, row=1)

            lbl = Label(infoWin, text=info['id'], font=("Roboto", 12)).grid(column=3, row=1, sticky=W)
            lbl = Label(infoWin, text=info['name'], font=("Roboto", 12)).grid(column=3, row=2, sticky=W)
            lbl = Label(infoWin, text=info['genre'], font=("Roboto", 10)).grid(column=3, row=3, sticky=W)
            lbl = Label(infoWin, text=info['rating'], font=("Roboto", 10)).grid(column=3, row=4, sticky=W)

            lbl = Label(infoWin, text="Stocks", font=fTup_heading, fg="#eb345b").grid(column=1, row=5, pady=20)

            lbl = Label(infoWin, text="Available Units", font=("Roboto", 12), fg="#eb345b").grid(column=1, row=6, sticky=E)
            lbl = Label(infoWin, text="Units Borrowed", font=("Roboto", 10), fg="#eb345b").grid(column=1, row=7, sticky=E)
            lbl = Label(infoWin, text="Units Owned", font=("Roboto", 10), fg="#eb345b").grid(column=1, row=8, sticky=E)

            lbl = Label(infoWin, text=int(info["storeInfo"]["availUnits"]) - int(info["storeInfo"]["borrowedUnits"]), font=("Roboto", 12)).grid(column=3, row=6, sticky=W)
            lbl = Label(infoWin, text=info["storeInfo"]["borrowedUnits"], font=("Roboto", 10)).grid(column=3, row=7, sticky=W)
            lbl = Label(infoWin, text=info["storeInfo"]["availUnits"], font=("Roboto", 10)).grid(column=3, row=8, sticky=W)


            infoWin.mainloop()
        
        bookName = searchBox.get()

        file = open('books.json')
        booksDB = json.load(file)['books'].copy()

        foundBooks = []

        for book in booksDB:
            if bookName in book['name'].lower():
                foundBooks += [book]
        
        booksWin = Tk()
        booksWin.geometry('500x200')
        booksWin.title("Search results for " + '"' + searchBox.get() + '"')

        sp = Label(booksWin, text="     ").grid(column=0, row=0)

        lbl = Label(booksWin, text="Results found", font=fTup_title).grid(column=1, row=0, pady=10)

        endingRow = 1

        if len(foundBooks) == 0:
            lbl = Label(booksWin, text="No Books found", font=fTup_content).grid(column=1, row=endingRow)
        else:
            for i in foundBooks:
                lbl = Label(booksWin, text=i['name'], font=fTup_content).grid(column=1, row=endingRow, sticky=W)
                sp = Label(booksWin, text="     ").grid(column=2, row=endingRow)

                btn = Button(booksWin, text="Select this Book", font=fTup_content, command=lambda name=i: provideInfo(name))
                btn.grid(column=3, row=endingRow, pady=1)

                endingRow += 1

        booksWin.mainloop()

    sp = Label(mnWin, text="        ")
    sp.grid(row=endingRow+4, column=3)

    btn = Button(mnWin, text="Go!", font=fTup_content, command=searchBk)
    btn.grid(row=endingRow+4, column=4)

    mnWin.mainloop()

# Opening login window to start the process
open_loginWindow()