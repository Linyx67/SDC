accountsFilepath = "accounts.txt"

def addAccount(user):
    with open(accountsFilepath, "r") as accountsFile:
        lines = accountsFile.readlines()
        for line in lines:
            if user.strip() == line.strip():
                return False

    with open(accountsFilepath, "a") as accountsFile:
        accountsFile.write("\n"+user)   
    return True

def hasAccount(user):
    with open(accountsFilepath, "r") as accountsFile:
        lines = accountsFile.readlines()
        for line in lines:
            if user.strip() == line.strip():
                return True
        
    return False


class Report():
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, "w") as self.reportsFile:
            self.reportsFile.write("Time(secs), Persons Detected, Crowd Density (persons per pixel), Violation Count")

    def writeLine(self, clock, persons, density, violations):
        with open(self.filepath, "a") as self.reportsFile:
            self.reportsFile.write("\n" + str(clock) + "," + str(persons) + "," + str(density) + "," + str(violations))