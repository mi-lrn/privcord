import json
import os
from typing import Dict, List
import time
import re

#the functions: save_messages dump_dir and dump_all are taken from https://github.com/ishnz/bulk_deletion_helper/blob/main/dumpallmessages.py

#creates a new csv file and puts the channel ids and associated message ids in the spreadsheet 
def save_messages(messages: Dict[str, List[int]]):
    try:
        with open("messages.csv", "w", encoding='utf8') as f:
            f.write('channelid, messageid\n')
            for channel, ids in messages.items():
                if ids is None or len(ids) == 0:
                    print(f'No messages found for channel: {channel} (skipping)')
                    continue
                print(f'Saving messages from channel: {channel}')
                for id in ids:
                    f.write(f"{str(channel)},{str(id)}\n")
    except:
         print("Error Saving Messages --> Make Sure Python Can Access the Directory")
         quit()

#retrieves message ids from the current channel path and returns them
def dump_dir(path: str) -> List[int]:
    try:
        messages = []
        if not os.path.isdir(path):
            return messages
        if not os.path.exists(f'{path}/messages.json'):
            print(f'No messages found in: {path}')
            return messages
        print(f'Dumping messages from: {path}')
        with open(f'{path}/messages.json', 'r', encoding='utf8') as f:
            messages_obj = json.load(f)
            for message in messages_obj:
                messages.append(message['ID'])
        return messages
    except:
        print("Error Parsing Messages --> Make Sure Your Messages Folder Is Correct")
        quit()

#creates a dictionary which contains dumped message ids for each channel --> each channel id is a key that is associated with its message ids then returns it
def dump_all(subdirs) -> Dict[str, List[int]]:
    try:
        messages = {}
        for channel in subdirs:
            if not os.path.isdir(channel):
                continue
            #calls dump_dir() for each channel and adds the message list output to the messages dict
            messages[os.path.basename(channel).replace('c', '', 1)] = dump_dir(channel)
        return messages
    except:
        print("Error Parsing Messages --> Make Sure Your Messages Folder Is Correct")
        quit()

#gets all the dumped message ids using the dump functions then saves them to a csv file using save_messages() in the path that was selected by the user
def delmsgs(subdirs, path):
    print("")
    print("------------------------------------------------------------------------------------------------")
    print("")
    print("Instructions: ")
    print("1. Find a Location to Store Your Formatted Messages to Submit for Deletion")
    print("2. Copy the Directory of the Location (Folder)")
    print("3. Paste the File Path Into the Tool")
    print("4. Further Instructions Will Be Provided Once Done")
    print("")
    print("------------------------------------------------------------------------------------------------")
    print("")
    print("Enter Dump Path: ")
    dumppath = input()
    if "\"" in dumppath:
        dumppath = dumppath.replace("\"", "")
    dumppath = r"{}".format(dumppath)
    print("")
    print("------------------------------------------------------------------------------------------------")
    print("")
    #calls dump function chain
    messages = dump_all(subdirs)
    #validates dumppath
    try:
        os.chdir(dumppath)
    except:
        print("Error Locating Path --> Make Sure The Path You Inputted Is Correct")
        quit()
    #saves the dump function chain's output to a csv file for uploading to discord support
    save_messages(messages)
    print("Dumped to messages.csv!")
    print("")
    print("------------------------------------------------------------------------------------------------")
    print("")
    print("Instructions: ")
    print("1. Go to This Link: https://support.discord.com/hc/en-us/requests/new?ticket_form_id=4750383925911")
    print("2. Fill Out Your Email Address")
    print("3. Enter the Subject As: \'Bulk Discord Message Delete - {Your Discord Username}\'")
    print("4. Make the Description Look Something Like This: https://github.com/victornpb/undiscord/discussions/429#discussioncomment-10312129")
    print("5. Select \'Delete your personal data on Discord\' under \'What do you need assistance with?\'")
    print("6. Check the Box Asking if You Read the Articles")
    print("7. Upload the messages.csv File That This Tool Generated")
    print("8. Press Submit")
    print("9. Wait")
    print("10. If Discord Does Not Take Action --> Check This Video: https://youtu.be/g5FbRfwMEuo?t=691")
    print("")
    #returns to main menu after completion
    time.sleep(2)
    menu(subdirs,path)

#calls the findPII() function for each subdirectory
def scanmsgs(subdirs, path):
    if subdirs == []:
        print("Error Locating Subfolders --> Make Sure Your Messages Folder Is Correct")
        quit()
    print("")
    print("------------------------------------------------------------------------------------------------")
    print("")
    count = 0
    for subdir in subdirs:
        if subdir == os.getcwd():
            continue
        os.chdir(subdir)
        count = findPII(count, subdir, path)
    #returns to the main menu after completion
    time.sleep(2)
    menu(subdirs, path)

#takes in the number of messages that have been found with PII, the current subdirectory, and the messages folder path
#prints every message that is found with PII with the following info: Message # (count+1), Time Sent, Location Sent, PII Detected
def findPII(count, subdir, path):
    #defines regex patterns for addresses, mentions, phone numbers, and email_patterns, so they can be detected
    address_pattern_4_1 = re.compile(
        r'\b\d{4}\s+(W|S|E|N|WEST|SOUTH|EAST|NORTH)\s+\w+\s+(St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Ln|Lane|Dr|Drive|Ct|Court|Pl|Place|Terr|Terrace|Way|Pkway|Parkway|Cir|Circle|Hwy|Highway|Apt|Apartment|Suite|Bldg|Building|Floor|Unit|Rte|Route|Cres|Crescent|Cove|Bypass|Loop|Pass|Pkwy|Terr|Way)\b',
        re.IGNORECASE
    )
    address_pattern_4_2 = re.compile(
        r'\b\d{4}\s+(W|S|E|N|WEST|SOUTH|EAST|NORTH)\s+\w+\b',
        re.IGNORECASE
    )
    address_pattern_4_3 = re.compile(
        r'\b\d{4}\s+(W|S|E|N|WEST|SOUTH|EAST|NORTH)\b',
        re.IGNORECASE
    )
    address_pattern_3_1 = re.compile(
        r'\b\d{3}\s+(W|S|E|N|WEST|SOUTH|EAST|NORTH)\s+\w+\s+(St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Ln|Lane|Dr|Drive|Ct|Court|Pl|Place|Terr|Terrace|Way|Pkway|Parkway|Cir|Circle|Hwy|Highway|Apt|Apartment|Suite|Bldg|Building|Floor|Unit|Rte|Route|Cres|Crescent|Cove|Bypass|Loop|Pass|Pkwy|Terr|Way)\b',
        re.IGNORECASE
    )
    address_pattern_3_2 = re.compile(
        r'\b\d{3}\s+(W|S|E|N|WEST|SOUTH|EAST|NORTH)\s+\w+\b',
        re.IGNORECASE
    )
    address_pattern_3_3 = re.compile(
        r'\b\d{3}\s+(W|S|E|N|WEST|SOUTH|EAST|NORTH)\b',
        re.IGNORECASE
    )
    mention_pattern = re.compile(r'<@\d{18,19}>')
    phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s])?(\(?\d{3}\)?[-.\s])\d{3}[-.\s]\d{4}(?=\s|$)')
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    try:
        #gets the channel id of the current subdirectory then translates it into english with the index.json file generated by discord
        with open("channel.json", 'r') as f:
            channel = json.load(f)
            id = str(channel["id"])
            os.chdir(f"{path}")
            with open("index.json", encoding='utf-8', errors='ignore') as x:
                reference = json.load(x)
                name = str(reference[id])
                if name == "None":
                    name = "Unnamed Group DM"
                elif name == "Unknown channel":
                    name = "Inaccessible Group DM"
        #checks each message in each channel for the regex patterns and displays ones that return a match for at least one pattern
        os.chdir(subdir)
        with open("messages.json", encoding='utf-8', errors='ignore') as f:
            messages = json.load(f)
            if messages == []:
                os.chdir("..")
                return count
            for message in messages:
                content = str(message["Contents"])
                checkcontent = re.sub(mention_pattern, "", content)
                output = False
                if bool(address_pattern_4_1.search(checkcontent)) or bool(address_pattern_3_1.search(checkcontent)):
                    count += 1
                    print(f'Message {count}: \n Content: {content} \n Sent At: {str(message["Timestamp"])} \n Sent In: {name} \n Address Match: Strong \n')
                    output = True
                elif bool(address_pattern_4_2.search(checkcontent)) or bool(address_pattern_3_2.search(checkcontent)):
                    count += 1
                    print(f'Message {count}: \n Content: {content} \n Sent At: {str(message["Timestamp"])} \n Sent In: {name} \n Address Match: Partial \n')
                    output = True
                elif bool(address_pattern_4_3.search(checkcontent)) or bool(address_pattern_3_3.search(checkcontent)):
                    count += 1
                    print(f'Message {count}: \n Content: {checkcontent} \n Sent At: {str(message["Timestamp"])} \n Sent In: {name} \n Address Match: Weak \n')
                    output = True
                if bool(phone_pattern.search(checkcontent)):
                    if output == False:
                        count += 1
                        print(f'Message {count}: \n Content: {content} \n Sent At: {str(message["Timestamp"])} \n Sent In: {name} \n Phone Number Match: Strong \n')
                    else:
                        print("Phone Number Match: Strong \n")
                if bool(email_pattern.search(checkcontent)):
                    count += 1
                    if output == False:
                        print(f'Message {count}: \n Content: {content} \n Sent At: {str(message["Timestamp"])} \n Sent In: {name} \n Email Match: Strong \n')
                    else:
                        print("Email Match: Strong \n")
        os.chdir("..")
        return count
    except:
        print("Error Parsing Messages --> Make Sure Your Messages Folder Is Correct")
        quit()

#takes in search terms, the number of messages that have been found with the search term(s), the current subdirectory, and the messages folder path
#prints every message that is found with the search terms with the following info: Message # (count+1), Time Sent, Location Sent
def findMsgContent(searchterms, count, subdir, path):
    try:
        #gets the channel id of the current subdirectory then translates it into english with the index.json file generated by discord
        with open("channel.json", 'r') as f:
            channel = json.load(f)
            id = str(channel["id"])
            os.chdir(path)
            with open("index.json", encoding='utf-8', errors='ignore') as x:
                reference = json.load(x)
                name = str(reference[id])
                if name == "None":
                    name = "Unnamed Group DM"
                elif name == "Unknown channel":
                    name = "Inaccessible Group DM"
        #checks each message in each channel for searchterm(s) and displays ones that contain the terms
        os.chdir(subdir)
        with open("messages.json", encoding='utf-8', errors='ignore') as f:
            messages = json.load(f)
            if messages == []:
                os.chdir("..")
                return count
            for message in messages:
                content = str(message["Contents"])
                display = True
                for term in searchterms:
                    if term not in content.lower():
                        display = False
                if display == True:
                    count += 1
                    print(f'Message {count}: \n Content: {content} \n Sent At: {str(message["Timestamp"])} \n Sent In: {name} \n')
        os.chdir("..")
        return count
    except:
          print("Error Parsing Messages --> Make Sure Your Messages Folder Is Correct")
          quit()

#gets search terms from the user and then calls the findMsgContent() function to search through each subdirectory
def srchmsgs(subdirs, path):
    if subdirs == []:
        print("Error Locating Subfolders --> Make Sure Your Messages Folder Is Correct")
        quit()
    inputs = []
    print("")
    print("------------------------------------------------------------------------------------------------")
    print("")
    option = input("Enter Search Term: ")
    inputs.append(option)
    print("")
    print("------------------------------------------------------------------------------------------------")
    option = None
    #gets more than one search term if needed
    while option != "":
        print("")
        print("Press Enter to Skip")
        option = input("Enter Another Search Term (Tool Returns Messages With All Terms In Them): ")
        if option != "":
            inputs.append(option)
        print("")
        print("------------------------------------------------------------------------------------------------")
    count = 0
    print("")
    #loops through all subdirectories and calls findMsgContent() for each
    for subdir in subdirs:
        if subdir == os.getcwd():
            continue
        os.chdir(subdir)
        count = findMsgContent(inputs, count, subdir, path)
    #returns to the main menu after completion
    time.sleep(2)
    menu(subdirs, path)

#prints the opening menu and takes in the messages file path input and validates it   
def main():
    print("------------------------------------------------------------------------------------------------")
    print("")
    print(r" ____       _        ____              _ ")
    print(r"|  _ \ _ __(_)_   __/ ___|___  _ __ __| |")
    print(r"| |_) | '__| \ \ / / |   / _ \| '__/ _` |")
    print(r"|  __/| |  | |\ V /| |__| (_) | | | (_| |")
    print(r"|_|   |_|  |_| \_/  \____\___/|_|  \__,_|")
    print("")
    print("Helps Protect Your Privacy on Discord")
    print("")
    print("Features: ")
    print("1. Search Through Your Messages")
    print("2. Scan Your Messages For Personal Info")
    print("3. Format Your Messages For Deletion")
    print("")
    print("------------------------------------------------------------------------------------------------")
    print("")
    print("Instructions: ")
    print("1. Open Discord")
    print("2. Click on Settings")
    print("3. Click on Data & Privacy")
    print("4. Scroll Down to the Bottom")
    print("5. Click On \'Request Data\'")
    print("6. Check the \'Messages\' Box Only")
    print("7. Confirm Your Choice")
    print("8. Wait to Get the Email")
    print("9. Download the Zip File")
    print("10. Extract the Zip File")
    print("11. Copy the File Path to the \'messages\' Folder")
    print("12. Paste the File Path Into the Tool")
    print("")
    print("------------------------------------------------------------------------------------------------")
    print("")
    print("Enter Messages Path (Or Press Enter to Exit): ")
    path = input("")
    if path == "":
        quit()
    if "\"" in path:
        path = path.replace("\"", "")
    path = r"{}".format(path)
    #tries to select the path
    try:    
        os.chdir(f"{path}")
    except:
        print("Error Locating Path --> Make Sure The Path You Inputted Is Correct")
        quit()
    #creates a list of all the subdirectories in the path (message folders)
    subdirs = [x[0] for x in os.walk(os.getcwd())]
    del subdirs[0]
    print("")
    #calls the main menu
    menu(subdirs, path)

#prints the main menu out with all options
def menu(subdirs, path):
    print("------------------------------------------------------------------------------------------------")
    print("")
    print("1. Search Your Messages")
    print("2. Scan Your Messages")
    print("3. Delete Your Messages")
    print("4. Exit")
    option = input("")
    if option == "1":
        srchmsgs(subdirs, path)
    elif option == "2":
        scanmsgs(subdirs, path)
    elif option == "3":
        delmsgs(subdirs, path)
    elif option == "4":
        quit()
    else:
        print("Invalid Option --> Make Sure You\'re Using the Associated Numbers (Ex Input: 1)")
        quit()

#runs the tool
if __name__ == "__main__":
    main()
