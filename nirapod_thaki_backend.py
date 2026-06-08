import time
import random

# =====================================================================
# HELPER
# =====================================================================

def get_static_dist():
    directions = ["North", "South", "East", "West", "NE", "NW", "SE", "SW"]
    return f"{random.randint(20, 100)}m {random.choice(directions)}"

# =====================================================================
# APP DATA
# =====================================================================

user_info = {
    "Name": "Shova",
    "Blood Type": "A+",
    "Allergies": "Peanut"
}

emergency_contacts = {
    "Father": "01716449848",
    "Mother": "01868461888",
    "Brother": "01978517817",
    "Friend(Samin)": "015198465488"
}

comfort_zones = [
    {"name": "Aurora Cafe, Laxmipur",    "distance": get_static_dist()},
    {"name": "Samin's Home, Rajpara",    "distance": get_static_dist()},
    {"name": "Cousin's home, Uposhohor", "distance": get_static_dist()}
]

live_location = "Laxmipur, Rajshahi"

nearest_facilities = {
    "First Aid Zones": [
        {"name": "Large Pharma",       "distance": get_static_dist()},
        {"name": "Komla Pharmacy",     "distance": get_static_dist()},
        {"name": "Rajshahi Pharmacy",  "distance": get_static_dist()},
        {"name": "Red Pharmacy",       "distance": get_static_dist()}
    ],
    "Hospitals": [
        {"name": "Rajshahi Medical College",  "distance": get_static_dist()},
        {"name": "Popular Diagnostic Center", "distance": get_static_dist()}
    ],
    "Police Station": [
        {"name": "Rajpara Police Station", "distance": get_static_dist()}
    ],
    "Fire Service": [
        {"name": "Rajshahi Fire Service & Civil Defence Station",
         "distance": get_static_dist()}
    ],
    "Emergency Helplines": [
        {"name": "999",                              "distance": "N/A"},
        {"name": "Rajpara Police Station: 0721776080", "distance": "N/A"}
    ]
}

# =====================================================================
# LOGIC FUNCTIONS  (terminal versions — still work standalone)
# =====================================================================

def view_and_edit_data():
    while True:
        print("\n--- Current User Information ---")
        print("User Profile:")
        for key, value in user_info.items():
            print(f"  - {key}: {value}")

        print("\nEmergency Contacts:")
        for relation, number in emergency_contacts.items():
            print(f"  - {relation}: {number}")

        print("\nComfort Zones (Distance from Live Location):")
        for zone in comfort_zones:
            print(f"  - {zone['name']} [{zone['distance']}]")

        print("\n--- Edit Menu ---")
        print("1. Edit User Profile (Name, Blood Type, etc.)")
        print("2. Edit/Add Emergency Contact")
        print("3. Add a New Comfort Zone")
        print("4. Go Back to Main Menu")

        edit_choice = input("Select an option (1-4): ")

        if edit_choice == '1':
            print("\nFields: Name, Blood Type, Allergies")
            field = input("Which field do you want to edit? (Type exactly as shown): ")
            if field in user_info:
                new_value = input(f"Enter new value for {field}: ")
                user_info[field] = new_value
                print(f"[SUCCESS] {field} updated successfully.")
            else:
                print("[!] Error: Field not found.")

        elif edit_choice == '2':
            relation = input("\nEnter relation (e.g., Father, Sister, Uncle): ")
            number   = input("Enter contact number: ")
            emergency_contacts[relation] = number
            print(f"[SUCCESS] Contact for {relation} updated successfully.")

        elif edit_choice == '3':
            new_zone = input("\nEnter the new comfort zone location: ")
            comfort_zones.append({"name": new_zone, "distance": get_static_dist()})
            print("[SUCCESS] Comfort zone added. Estimated distance calculated.")

        elif edit_choice == '4':
            break
        else:
            print("[!] Invalid choice. Please try again.")


def display_nearest_facilities():
    print(f"\n--- Scanning Live Location: {live_location} ---")
    time.sleep(1)
    for category, places in nearest_facilities.items():
        print(f"\n{category}:")
        for place in places:
            if place['distance'] != "N/A":
                print(f"  -> {place['name']} [{place['distance']}]")
            else:
                print(f"  -> {place['name']}")
    input("\nPress Enter to return to menu...")


def trigger_sos_alert(trigger_type):
    print(f"\n[!] WARNING: {trigger_type} DETECTED [!]")
    time.sleep(1)
    print(f" -> Fetching Live Location: {live_location}")
    time.sleep(1)
    contact_list = ", ".join(emergency_contacts.keys())
    print(f" -> Transmitting location and alert to Emergency Contacts ({contact_list})...")
    time.sleep(1)
    print(" -> Transmitting alert to 999 and Rajpara Police Station...")
    print("\n[SUCCESS] SOS Alert dispatched successfully.")
    input("\nPress Enter to return to menu...")


def simulate_stealth_capture():
    print("\n--- Stealth Media Capture Activated ---")
    print(" -> Screen visually dimmed to 0% brightness (Blacked out).")
    time.sleep(3)
    print(" -> Recording audio and capturing background photos...")
    time.sleep(2)
    print(" -> Recording background Video...")
    time.sleep(4)
    print(" -> Media saved securely to encrypted local vault.")
    input("\nPress Enter to return to menu...")


def simulate_sms_fallback():
    print("\n--- Simulating Network Loss ---")
    print("[!] Error: No Internet Connection Detected.")
    time.sleep(1)
    print(" -> Activating SMS Fallback System...")
    time.sleep(1)
    print(f" -> Compressing GPS Coordinates ({live_location}) and SOS signal...")
    time.sleep(1)
    contact_list = ", ".join(emergency_contacts.keys())
    print(f" -> Blasting SMS to: {contact_list}.")
    print("\n[SUCCESS] Fallback SMS delivered.")
    input("\nPress Enter to return to menu...")


def main_menu():
    while True:
        print("\n=========================================")
        print("              NIRAPOD THAKI               ")
        print("=========================================")
        print("1. View/Edit User Data & Contacts")
        print("2. Check Nearest Facilities (Live Location)")
        print("3. Press SOS Button (Smartwatch/3 Clicks)")
        print("4. Active SOS via Voice ('Dattebayo')")
        print("5. Stealth Media Capture")
        print("6. No-Internet (SMS Fallback)")
        print("7. Exit App")
        print("=========================================")

        choice = input("Select an option (1-7): ")

        if   choice == '1': view_and_edit_data()
        elif choice == '2': display_nearest_facilities()
        elif choice == '3': trigger_sos_alert("HARDWARE BUTTON / SMARTWATCH TRIGGER")
        elif choice == '4': trigger_sos_alert("VOICE ACTIVATION (Dattebayo)")
        elif choice == '5': simulate_stealth_capture()
        elif choice == '6': simulate_sms_fallback()
        elif choice == '7':
            print("Exiting prototype... Stay safe!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main_menu()
