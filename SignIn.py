import sys
import time 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Function to log into gmail account given an EmailAccount object
def getGmail(EmailAccount):
    # Added option to let the browser stay open and created webdriver.Chrome
    #   object to open chrome browser page to the gmail sign in page
    chromeOption = webdriver.ChromeOptions()
    chromeOption.add_experimental_option("detach", True)
    browser = webdriver.Chrome('/Users/CharlesNavera/desktop/chromedriver', options=chromeOption)
    browser.get('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    browser.fullscreen_window()

    # finds the email address input and enters in the email's address
    #   and clicks the "next" button
    loginAccount = browser.find_element_by_xpath('//*[@id="identifierId"]')
    loginAccount.send_keys(EmailAccount.getAccount())
    loginButton = browser.find_element_by_xpath('//*[@id="identifierNext"]')
    loginButton.click()
    time.sleep(3)

    # finds the password input, adds in email's password, and clicks 
    #   sign in button
    loginPW = browser.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    loginPW.send_keys(EmailAccount.getPassword())
    enterPWButton = browser.find_element_by_xpath('//*[@id="passwordNext"]')
    enterPWButton.click()


# Function to log into yahoo account given an EmailAccount
def getYahoo(EmailAccount):
    chromeOption = webdriver.ChromeOptions()
    chromeOption.add_experimental_option("detach", True)
    browser = webdriver.Chrome('/Users/CharlesNavera/desktop/chromedriver', options=chromeOption)
    browser.get('https://login.yahoo.com/config/login?.src=fpctx&.intl=us&.lang=en-US&.done=https%3A%2F%2Fwww.yahoo.com')
    browser.fullscreen_window()

    # finds the email address input and enters in the email's address
    #   and clicks the "next" button. Yahoo automatically opens up ad window
    #   so click login button again after switching back to original tab
    loginAccount = browser.find_element_by_xpath('//*[@id="login-username"]')
    loginAccount.send_keys(EmailAccount.getAccount())
    loginButton = browser.find_element_by_xpath('//*[@id="login-signin"]')
    loginButton.click()
    loginButton.click()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(5)

    # finds the password input, adds in email's password, and clicks 
    #   sign in button twice after switching back to oroginal tab
    loginPW = browser.find_element_by_xpath('//*[@id="login-passwd"]')
    loginPW.send_keys(EmailAccount.getPassword())
    enterPWButton = browser.find_element_by_xpath('//*[@id="login-signin"]')
    enterPWButton.click()
    enterPWButton.click()
    browser.switch_to.window(browser.window_handles[0])


# EmailAccount class to represent an email account that have properties
#    of an email address and an email password
class EmailAccount:
    
    # default constructor
    def __init__(self, account, password):
        self.account = account
        self.password = password
    
    # getter method for the email account
    def getAccount(self):
        return self.account
    
    # getter method for the password of the email
    def getPassword(self):
        return self.password

    # toString method to print both the account and password
    def toString(self):
        return "The account is " + self.getAccount() + " and the password is " + self.getPassword() + "."


# Dictionary list that holds available emails to sign into
emailList = {}


# Function to load existing email accounts into email dictionary obj
def loadDictionary():
    try:

        # Read Email_Accounts.txt file and load each line to emailList
        #   dictionary object
        emailFile = open("Email_Accounts.txt", "r")
        for line in emailFile:
            readEmailAccount = line.split()
            addEmailUN = readEmailAccount[0]
            addEmailPW = readEmailAccount[1]
            emailList[addEmailUN] = EmailAccount(addEmailUN, addEmailPW)
        emailFile.close()
    except:
        print("Error occured reading file into dictionary.")
    emailFile.close()

# Function to check if username is an email
def isEmail(emailName):
        if "@" not in emailName:
            return True
        return False

# function to add a new email to the email list
def addEmail():
    print("\nPlease enter in the proper information to add an email.")
    try:
        newEmailUN = input("Email Username: ")
        newEmailPW = input("Email Password: ")
        newEmail = EmailAccount(newEmailUN, newEmailPW)
        if newEmailUN in emailList.keys() or isEmail(newEmailUN):
            print("Email already exists of is not a valid email.")
            sys.exit()
        else:
            emailList[newEmailUN] = newEmail 
            emailFile = open("Email_Accounts.txt", "a")
            emailFile.write(newEmail.getAccount() + " " +  newEmail.getPassword() + "\n")
            print("\nadded new email\n")
            emailFile.close()
    except:
        print("Error occured please try again.")


# function to print all emails that are available to sign into
def checkList():
    # try catch block to print all emails in the email list dictionary
    try:
        print("----------------------Email List----------------------------")
        for v in emailList.keys():
            print(v)
        print("------------------------------------------------------------\n")
    except:
        print("Could not print out email list.\nPlease try again.")


# Function that prints out to the user the different commands the user
#   may use
def helpCommands():
    print("\nEmail commands: \n")
    print("add - Inserts a new email into available emails to sign into.")
    print("remove - Removes an email from available email accounts.\n")


# function to automatically open chrome web browser to sign into a gmail
#   account given valid email addresses
def logIn():
    
    # try/catch block to get input from command line
    try:
        loadDictionary()
        if sys.argv[1] == "help":
            helpCommands()
            sys.exit()
        elif sys.argv[1] == "list":
            checkList() 
            sys.exit()
        elif sys.argv[1] == "add": 
            addEmail()
            sys.exit()
        else:
            userName = sys.argv[1]
    except IndexError:
        print("No email entered.\nTry again.")
        sys.exit()
    if(len(sys.argv) > 2):
        print("Cannot enter more than one email. Please try again.")
        sys.exit()
    

    # checks if enter input is an email and then has a counter from
    #   beginning of entered email to the "@" to create substring
    #   from the "@" symbol to the end of the email
    userNameCount = 0
    if isEmail(userName):
        sys.exit()
    for c in userName:
        if c == "@":
            break
        userNameCount+=1
    
    # string that contains the email type
    #   ex: "@gmail.com", "@yahoo.com"
    emailType = userName[userNameCount:len(userName)]

    # email dictionary list
    if userName not in emailList:
        print("Can't sign into this email.")
        sys.exit() 
   
    # Email object with the email address and password retrieved from
    #   dictionary
    emailLog = emailList[userName.lower()]

    if emailType == "@gmail.com":
        getGmail(emailLog)
    elif emailType == "@yahoo.com":
        getYahoo(emailLog)
    else:
        print("error occured please try again.")
        sys.exit()

if __name__ == "__main__":
    logIn()