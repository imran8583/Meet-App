import random
import string
import json
from json import JSONDecodeError
from datetime import datetime, date

def autoGenerate_eventID():
    # generate a random Event ID
    event_ID = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return event_ID

def register_protocol(file_name, full_name, email, password):
    file = open(file_name, "r+")
    data = {"Full Name": full_name, "Email": email, "Password": password}
    try:
        content = json.load(file)
        if data not in content:
            content.append(data)
            file.seek(0)
            file.truncate()
            json.dump(content, file)
    except JSONDecodeError:
        l = []
        l.append(data)
        json.dump(l, file)
    file.close()

def register(file_type, json_file, full_name, email, password):
    """Register the member/organizer based on the type with the given details"""

    if file_type.lower() == "organizer":
        """Organizer Registration"""
        register_protocol(json_file, full_name, email, password)
    else:
        """Members Registration"""
        register_protocol(json_file, full_name, email, password)


def login(json_file, email, password):
    """Login Functionality || Return True if successful else False"""

    data = 0
    file = open(json_file, "r+")
    try:
        content = json.load(file)
    except JSONDecodeError:
        file.close()
        return False

    for i in range(len(content)):
        if content[i]["Email"] == email and content[i]["Password"] == password:
            # file.close()
            # return True
            data = 1
            break
        # else:
            # file.close()
            # return False
    if data == 0:
        file.close()
        return False

    file.close()
    return True

def create_event(org_name, events_json, event_ID, event_name, start_date, start_time, end_date, end_time, users_registered, seats_capacity, total_seats):
    """Create an Event with the details entered by organizer"""

    file = open(events_json, "r+")

    data = {
        "ID": event_ID,
        "Name": event_name,
        "Organizer": org_name,
        "Start Date": start_date,
        "Start Time": start_time,
        "End Date": end_date,
        "End Time": end_time,
        "Users Registered": users_registered,
        "Capacity": seats_capacity,
        "Seats Available": total_seats
    }

    try:
        content = json.load(file)
        if data not in content:
            content.append(data)
            file.seek(0)
            file.truncate()
            json.dump(data,file)
            file.close()
            return True

    except json.decoder.JSONDecodeError:
        lst = []
        lst.append(data)
        json.load(lst,file)
        file.close()
        return True

    return False


def view_events(org_name, event_json_file):
    """Return a list of all events created by the logged in organizer"""

    f=open(event_json_file,'r+')
    eventlist =[]
    content=json.load(f)

    for event in content:
        if event["Organizer"]==org_name:
            eventlist.append(event)
        return eventlist
    f.close()


def view_event_byID(event_json_file, event_id):
    '''Return details of the event for the event ID entered by user'''
    file = open(event_json_file, "r+")
    event_byID =[]
    content = json.load(file)

    for event in content:
        if event["ID"] == event_id:
            event_byID.append(event)
            return event_byID
    file.close()



def update_event(org_name, events_json_file, event_id, detail_to_be_updated, updated_detail):
    """Update Event by ID ||; Take the key name to be updated from member, then update the value entered by user for that key for the selected event
    || Return True if successful else False"""
    
    with open(events_json_file,"r+") as file:
        file_data=json.load(file)

        for event in range(len(file_data)):   
                 
            if file_data[event]["ID"]==event_id:
                dtba = detail_to_be_updated.title()
                dtbal = detail_to_be_updated.lower()

                file_data[event]["Organizer"]==org_name
                # Name || Start Date || Start Time || End Time || End Date

                if dtbal == "name":
                    file_data[event][dtba] = updated_detail

                if dtbal == "start date":
                    file_data[event][dtba] = updated_detail

                if dtbal == "start time":
                    file_data[event][dtba] = updated_detail

                if dtbal == "end time":
                    file_data[event][dtba] = updated_detail

                if dtbal == "end date":
                    file_data[event][dtba] = updated_detail
                
                file.seek(0)
                file.truncate()
                json.dump(file_data,file)
                file.close()
                return True

    return False

def delete_event(org_name,events_json_file,event_id):
    """Delete the Event with entered event ID ||   Return True if successful else return False"""
    with open(events_json_file,"r+") as file:
        file_data=json.load(file)

        for event in range(len(file_data)):
            if file_data[event]["ID"]==event_id:
                # print(file_data)
                # file_data.pop(i)
                del file_data[event]

                file.seek(0)
                file.truncate()
                json.dump(file_data,file)
                file.close()
                return True    
    return False


def fetch_all_events(events_json_file, mem_name, event_details, upcoming_ongoing):
    """View Registered Events | Fetch a list of all events of the logged in member"""
    """Append the details of all upcoming and ongoing events list based on the today's date/time and event's date/time"""
    date_today = str(date.today())
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    """Write your code below this line"""
    
    file = open(events_json_file, "r+")
    uce = upcoming_ongoing
    content = json.load(file)
    for event in content:
        if event["Users Registered"] == mem_name:
            uce.append(event)


def view_all_events(events_json_file):
    """Read all the events created | DO NOT change this function"""
    """Already Implemented Helper Function"""
    details = []
    file = open(events_json_file, "r")

    try:
        content = json.load(file)
        file.close()
    except JSONDecodeError:
        file.close()
        return details
    for i in range(len(content)):
        details.append(content[i])
    return details 


def register_for_event(events_json_file, event_id, mem_name):
    """Register the logged in member in the event with the event ID entered by member. 
    (append Full Name inside the "Users Registered" list of the selected event)
    Return True if successful else return False"""
    date_today = str(date.today())
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    """Write your code below this line"""
    
    file=open(events_json_file,'r+')
    try:
        content=json.load(file)
        for event in content:
            if event["ID"] == event_id and event["Seats Available"]==0:
                list_users = event["Users Registered"]
                list_users.append(mem_name)
                event["Users Registered"] = list_users

                json.dump(content,file)
                file.close()
                return True
            else:
                return False         
    except:
        return False


def update_password(members_json_file,mem_name, mem_password):
    """Update the password of the member by taking a new password || Return True if successful else return False"""
    file=open(members_json_file,'r+')
    try:
        content=json.load(file)
        for event in content:
            if event["Full Name"]== mem_name:
                event["Password"]= mem_password
                json.dump(content,file)
                file.close()
                return True
              
        else:
            file.close() 
            return False         
    except:
        return False