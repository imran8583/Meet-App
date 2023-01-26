import operations
import json
from json import JSONDecodeError


def registration_process():
    while True:
        print("1: Register as Organizer\n2: Register as Member\n0: Exit\n")
        try:
            registration_options = int(input())
        except ValueError:
            print("Please enter valid input")
            continue

        if registration_options == 1:
            """
                Registration process for the organizers
            """
            print("Enter Full Name:")
            org_full_name = input()
            print("Enter Email:")
            org_email = input()
            print("Enter Passwrod:")
            org_password = input()

            if (
                (len(org_full_name) * len(org_email) * len(org_password)) == 0
                or "@" not in org_email
                or ".com" not in org_email
            ):
                print("Please enter valid input")
            else:
                operations.register("organizer","organizers.json", org_full_name,org_email,org_password)
                print("Registered successfully as Organizer")

        elif registration_options == 2:
            """
                Registration process for the Members
            """
            print("Enter Full Name:")
            mem_full_name = input()
            print("Enter Email:")
            mem_email = input()
            print("Enter Passwrod:")
            mem_password = input()

            if (
                (len(mem_full_name) * len(mem_email) * len(mem_password)) == 0
                or "@" not in mem_email
                or ".com" not in mem_email
            ):
                print("Please enter valid input")
            else:
                operations.register("member","members.json", mem_full_name,mem_email,mem_password)
                print("Registered successfully as Member")

        elif registration_options == 0:
            break

        else:
            print("Please select from available options")


def login_process():
    while True:
        print("1: Login as Organizer\n2: Login as Member\n0: Exit\n")
        try:
            login_options = int(input())
        except ValueError:
            print("Please enter valid input")
            continue

        if login_options == 1:
            """
                Login process for the Organizers
            """
            org_email = input("Enter Email: ")
            org_password = input("Enter Password: ")
            org_login = operations.login("organizers.json", org_email, org_password)

            if org_login == False:
                print("Invalid Credentials")
                continue
            else:
                org_file = open("organizers.json", "r")
                contents = json.load(org_file)
                org_file.close()

                org_name = ""

                if len(contents) > 0:
                    for i in range(len(contents)):
                        if (
                            contents[i]["Email"] == org_email
                            and contents[i]["Password"] == org_password
                        ):
                            org_name = contents[i]["Full Name"]
                else:
                    print("Organization register database is currently empty")
                    print("You need to register first & try again.")
                print(f"Welcome {org_name}")

                while True:
                    print("Press :\n")
                    print(
                        "1: Create Event\n2: View all Events created\n3: View Event Details by ID\n4: Update Event\n5: Delete Event\n0: Logout"
                    )

                    try:
                        org_login_options = int(input())
                    except ValueError:
                        print("Please enter valid input")
                        continue

                    if org_login_options == 1:
                        """
                            Organizer will create an event from here
                        """
                        users_registered = []
                        event_ID = operations.autoGenerate_eventID()
                        print("Event ID Generated - " + str(event_ID))

                        print("Enter Event Name:")
                        event_name = input()

                        print("Enter Start Date (YYYY-MM-DD):")
                        start_date = input()

                        print("Enter Start Time (HH:MM:SS):")
                        start_time = input()

                        print("Enter End Date (YYYY-MM-DD):")
                        end_date = input()

                        print("Enter End Time (HH:MM:SS):")
                        end_time = input()
                        print("Enter Total Seats:")

                        try:
                            total_seats = int(input())
                            print("Enter Seats Capacity:")
                            seats_capacity = int(input())
                        except ValueError:
                            print("Please enter valid data")
                            continue

                        if (
                            (
                                len(event_name)
                                * len(start_date)
                                * len(start_time)
                                * len(end_date)
                                * len(end_time)
                                == 0
                            )
                            or len(start_date) != 10
                            or len(end_date) != 10
                            or len(start_time) != 8
                            or len(end_time) != 8
                            or start_date > end_date
                            or (start_time == end_time and start_time > end_time)
                            or total_seats < seats_capacity
                        ):
                            print("Please enter valid data")
                            continue
                        else:
                            operations.create_event(
                                org_name,
                                "events.json",
                                event_ID,
                                event_name,
                                start_date,
                                start_time,
                                end_date,
                                end_time,
                                users_registered,
                                seats_capacity,
                                total_seats,
                            )
                            print("Event created successfully")

                    elif org_login_options == 2:
                        """
                            Organizer will view all event from here
                        """
                        event_details = operations.view_events(org_name, "events.json")
                        
                        if len(event_details) == 0:
                            print("No Events created yet! \n")
                        else:
                            for i in range(len(event_details)):
                                print("Event ID: " + str(event_details[i]["ID"]))
                                print("Event Name: " + str(event_details[i]["Name"]))
                                print(
                                    "Organizer: " + str(event_details[i]["Organizer"])
                                )
                                print(
                                    "Start Date: " + str(event_details[i]["Start Date"])
                                )
                                print(
                                    "Start Time: " + str(event_details[i]["Start Time"])
                                )
                                print("End Date: " + str(event_details[i]["End Date"]))
                                print("End Time: " + str(event_details[i]["End Time"]))
                                print(
                                    "Total Users Registered: "
                                    + str(len(event_details[i]["Users Registered"]))
                                )
                                print("Capacity: " + str(event_details[i]["Capacity"]))
                                print(
                                    "Seats Available: "
                                    + str(event_details[i]["Seats Available"])
                                )
                                print("-" * 25)

                    elif org_login_options == 3:
                        """
                            Organizer will View Event Details by ID
                        """
                        print("Enter Event ID")
                        event_id = input()
                        events_file = open("events.json", "r")
                        try:
                            contents = str(json.load(events_file))
                            if event_id not in contents:
                                print("Invalid event ID")
                                continue
                        except JSONDecodeError:
                            print("Events not available")
                            continue
                        event_details = operations.view_event_byID(
                            "events.json", event_id
                        )

                        print("Event Name: " + str(event_details[0]["Name"]))
                        print("Organizer: " + str(event_details[0]["Organizer"]))
                        print("Start Date: " + str(event_details[0]["Start Date"]))
                        print("Start Time: " + str(event_details[0]["Start Time"]))
                        print("End Date: " + str(event_details[0]["End Date"]))
                        print("End Time: " + str(event_details[0]["End Time"]))
                        print("Capacity: " + str(event_details[0]["Capacity"]))
                        print(
                            "Seats Available: "
                            + str(event_details[0]["Seats Available"])
                        )
                        print("-" * 25)

                    elif org_login_options == 4:
                        """
                            Organizer will Update Event details
                        """
                        print("Enter Event ID: ")
                        event_id = input()

                        print(
                            "Enter detail to be Updated ( Name || Start Date || Start Time || End Time || End Date ): "
                        )
                        detail_to_be_updated = input().title()

                        print("Enter new value:")
                        updated_detail = input()

                        update_choices = operations.update_event(
                            org_name,
                            "events.json",
                            event_id,
                            detail_to_be_updated,
                            updated_detail,
                        )

                        if update_choices == True:
                            print("Event updated successfully !!")
                        else:
                            print("Event not updated !!")

                    elif org_login_options == 5:
                        """
                            Organizer will Delete Event details
                        """

                        print("Enter Product ID")
                        event_id = input()

                        f = open("events.json", "r")
                        try:
                            content = json.load(f)
                        except JSONDecodeError:
                            print("No products created !!")
                            continue

                        if event_id not in str(content):
                            print("Please Enter Valid Event ID")
                            continue
                        else:
                            delete_choices = operations.delete_event(
                                org_name, "events.json", event_id
                            )
                            if delete_choices == True:
                                print("Removed event successfully !!")
                                continue
                            else:
                                print("Cannot remove event !!")
                                continue

                    elif org_login_options == 0:
                        break

                    else:
                        print("Please select from available options")

        elif login_options == 2:
            """
                   Login process for the Members
            """
            mem_email = input("Enter Email: ")
            mem_password = input("Enter Password: ")
            mem_login = operations.login("members.json", mem_email, mem_password)

            if mem_login == False:
                print("Invalid Credentials")
                continue
            else:
                mem_file = open("members.json", "r")
                contents = json.load(mem_file)
                mem_file.close()

                mem_name = ""

                # if len(mem_file) > 0:
                for i in range(len(contents)):
                    if (
                        contents[i]["Email"] == mem_email
                        and contents[i]["Password"] == mem_password
                    ):
                        mem_name = contents[i]["Full Name"]
                # else:
                #     print("Members register database is currently empty")
                #     print("You need to register first & try again.")

                print(f"Welcome {mem_name}!")

                while True:
                    print("Press :\n")
                    print(
                        "1: View Registered Events\n2: Register for an Event\n3: Update Password\n4: View Event Details by ID\n0: Logout"
                    )

                    try:
                        mem_login_options = int(input())
                    except ValueError:
                        print("Please enter valid input")
                        continue

                    if mem_login_options == 1:

                        """
                            Members can view registered events
                        """
                        all_events = []
                        upcoming_ongoing = []
                        operations.fetch_all_events(
                            "events.json", mem_name, all_events, upcoming_ongoing
                        )
                        print("All Upcoming/Ongoing Events: ")

                        for i in range(len(upcoming_ongoing)):
                            print("Event Name: " + str(upcoming_ongoing[i]["Name"]))
                            print(
                                "Start Date: " + str(upcoming_ongoing[i]["Start Date"])
                            )
                            print(
                                "Start Time: " + str(upcoming_ongoing[i]["Start Time"])
                            )
                            print("End Date: " + str(upcoming_ongoing[i]["End Date"]))
                            print("End Time: " + str(upcoming_ongoing[i]["End Time"]))
                            print("Organizer: " + str(upcoming_ongoing[i]["Organizer"]))
                            print("-" * 70)

                    elif mem_login_options == 2:
                        """
                            Members can register for an events
                        """
                        all_event_list = operations.view_all_events("events.json")
                        if len(all_event_list) == 0:
                            print("No events available")
                        else:
                            print("All Events: ")
                            for i in range(len(all_event_list)):
                                an_event = all_event_list[i]
                                print("Event ID: " + str(an_event["ID"]))
                                print("Event Name: " + str(an_event["Name"]))
                                print("Organizer: " + str(an_event["Organizer"]))
                                print("Start Date: " + str(an_event["Start Date"]))
                                print("Start Time: " + str(an_event["Start Time"]))
                                print("End Date: " + str(an_event["End Date"]))
                                print("End Time: " + str(an_event["End Time"]))
                                print(
                                    "Seats Available: "
                                    + str(an_event["Seats Available"])
                                )
                                print("Total Seats: " + str(an_event["Capacity"]))
                                print("\n")
                        print("Enter Event ID: ")
                        event_id = input()
                        mem_event_registration = operations.register_for_event(
                            "events.json", event_id, mem_name
                        )
                        event_file = open("events.json", "r")
                        contents = str(json.load(event_file))

                        if event_id not in contents:
                            print("Invalid Event ID")

                        if mem_event_registration is True:
                            print("Successfully Registered")
                        else:
                            print("Event seats are full! \n")

                    elif mem_login_options == 3:
                        """
                            Members can update their password
                        """

                        print("Enter new password")
                        mem_password = input()
                        if (len(mem_password)) < 4:
                            print("Please enter valid data")
                            continue
                        op = operations.update_password(
                            "members.json", mem_name, mem_password
                        )
                        if op == True:
                            print("Password updated successfully")
                        else:
                            print("Cannot update password")

                    elif mem_login_options == 4:
                        """
                            Members can view event by ID
                        """
                        print("Enter Event ID")
                        event_id = input()
                        event_file = open("events.json", "r")
                        try:
                            contents = str(json.load(event_file))
                            if event_file not in contents:
                                print("Invalid event ID")
                                continue
                        except JSONDecodeError:
                            print("Events not available")
                            continue

                        an_event = operations.view_event_byID("events.json", event_id)
                        print("Event Name: " + str(an_event[0]["Name"]))
                        print("Start Date: " + str(an_event[0]["Start Date"]))
                        print("Start Time: " + str(an_event[0]["Start Time"]))
                        print("End Date: " + str(an_event[0]["End Date"]))
                        print("End Time: " + str(an_event[0]["End Time"]))
                        print("End Time: " + str(an_event[0]["End Time"]))
                        print("Organizer: " + str(an_event[0]["Organizer"]))
                        print("Seats Available: " + str(an_event[0]["Seats Available"]))
                        print("\n")

                    elif mem_login_options == 0:
                        break

                    else:
                        pass

        elif login_options == 0:
            break

        else:
            print("Please select from available options")
            continue


if __name__ == "__main__":
    print("Welcome to Meet App")
    while True:
        print("1: Register\n2: Login\n0: Exit\n")

        try:
            main_options = int(input())
        except:
            print("Please enter valid input")
            continue

        if main_options == 1:
            registration_process()
        elif main_options == 2:
            login_process()
        elif main_options == 0:
            break
        else:
            print("Please select from available options")
