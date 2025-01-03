import os
import pickle
import tkinter as tk
from uuid import uuid4

from scraper import fill_data_into_rocket_reach
from scraper.objects import Scraper

driver = Scraper.initialize(proxy="")

COOKIE_FILE_NAME = "cookies.pkl"


def new_browser():
    global driver
    driver = Scraper.initialize(proxy="")

# Function to load data from files
def load_data():
    try:
        # Load usernames from names.txt
        with open("names.txt", "r") as f:
            usernames = f.read().strip().split('\n')

        # Load emails from emails.txt
        with open("emails.txt", "r") as f:
            emails = f.read().strip().split('\n')

        # Clear existing text in textboxes
        usernames_textbox.delete("1.0", tk.END)
        emails_textbox.delete("1.0", tk.END)

        # Insert loaded data into textboxes
        usernames_textbox.insert(tk.END, '\n'.join(usernames))
        emails_textbox.insert(tk.END, '\n'.join(emails))

        print("Data loaded successfully!")
    except FileNotFoundError:
        print("No saved data found.")
    except Exception as e:
        print(f"Error loading data: {e}")


def save_cookies():
    driver.get("https://web.whatsapp.com")
    try:
        pickle.dump(driver.get_cookies(), open(COOKIE_FILE_NAME, 'wb'))
    except:
        pass

def load_cookies():
    try:
        if os.path.isfile(COOKIE_FILE_NAME):
            with open(COOKIE_FILE_NAME, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
    except:
        pass


# Function to save the usernames and emails to respective files
def save_data():
    usernames = usernames_textbox.get("1.0", tk.END).strip().split('\n')
    emails = emails_textbox.get("1.0", tk.END).strip().split('\n')

    # Save usernames to names.txt
    with open("names.txt", "w") as f:
        f.write('\n'.join(usernames))

    # Save emails to emails.txt
    with open("emails.txt", "w") as f:
        f.write('\n'.join(emails))

    print("Data saved successfully!")


# Function to process data
def process_data():
    # Get usernames and emails
    usernames = usernames_textbox.get("1.0", tk.END).strip().split('\n')
    emails = emails_textbox.get("1.0", tk.END).strip().split('\n')

    # Create pairs, taking only the minimum number of pairs possible
    min_length = min(len(usernames), len(emails))
    data = [[usernames[i].strip(), emails[i].strip()] for i in range(min_length)]

    # Call the imported function
    processed, un_processed = fill_data_into_rocket_reach(data=data, driver=driver)

    # Remove processed and unprocessed items from original lists
    processed_usernames = [pair[0] for pair in processed]
    processed_emails = [pair[1] for pair in processed]

    # Remove processed items from original lists
    remaining_usernames = [u for u in usernames if u.strip() not in processed_usernames]
    remaining_emails = [e for e in emails if e.strip() not in processed_emails]

    # Update textboxes and save files with remaining data
    usernames_textbox.delete("1.0", tk.END)
    emails_textbox.delete("1.0", tk.END)

    usernames_textbox.insert(tk.END, '\n'.join(remaining_usernames))
    emails_textbox.insert(tk.END, '\n'.join(remaining_emails))

    # Save updated data
    with open("names.txt", "w") as f:
        f.write('\n'.join(remaining_usernames))

    with open("emails.txt", "w") as f:
        f.write('\n'.join(remaining_emails))

    emails_data = "\n".join([
        email for _, email in processed
    ])

    if emails_data:
        with open(f"accounts_{uuid4()}.txt", "w") as f:
            f.write(emails_data)


# Function to run the process and save
def run_data():
    save_data()  # Save current state
    process_data()  # Process and update data


# Function to select all text in a Text widget
def select_all(event):
    event.widget.tag_add("sel", "1.0", "end")
    return "break"  # Prevent default action


# Set up the main window
root = tk.Tk()
root.title("Usernames and Emails")

new_browser_ = tk.Button(root, text="New Browser", command=new_browser)
new_browser_.pack(padx=10, pady=10)

# Create the labels
username_label = tk.Label(root, text="Enter Usernames:")
username_label.pack(padx=10, pady=5)

# Create a frame to hold the username textbox and its scrollbar
frame_usernames = tk.Frame(root)
frame_usernames.pack(padx=10, pady=5)

# Create the usernames text box
usernames_textbox = tk.Text(frame_usernames, height=10, width=40)
usernames_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the scrollbar for usernames
usernames_scrollbar = tk.Scrollbar(frame_usernames, command=usernames_textbox.yview)
usernames_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Link the scrollbar to the textbox
usernames_textbox.config(yscrollcommand=usernames_scrollbar.set)

# Bind Ctrl+A to select all text in the usernames textbox
usernames_textbox.bind("<Control-a>", select_all)

# Create the labels for emails
email_label = tk.Label(root, text="Enter Emails:")
email_label.pack(padx=10, pady=5)

# Create a frame to hold the email textbox and its scrollbar
frame_emails = tk.Frame(root)
frame_emails.pack(padx=10, pady=5)

# Create the emails text box
emails_textbox = tk.Text(frame_emails, height=10, width=40)
emails_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the scrollbar for emails
emails_scrollbar = tk.Scrollbar(frame_emails, command=emails_textbox.yview)
emails_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Link the scrollbar to the textbox
emails_textbox.config(yscrollcommand=emails_scrollbar.set)

# Bind Ctrl+A to select all text in the emails textbox
emails_textbox.bind("<Control-a>", select_all)

delay_frame = tk.Frame(root)
delay_frame.pack(padx=10, pady=5)

# Create Load button
load_button = tk.Button(root, text="Load", command=load_data)
load_button.pack(side=tk.LEFT, padx=10)

# Create Save button
save_button = tk.Button(root, text="Save", command=save_data)
save_button.pack(side=tk.LEFT, padx=10)

# Create Run button
run_button = tk.Button(root, text="Run", command=run_data)
run_button.pack(side=tk.LEFT, padx=10)

# Create Save button
load_cookies_ = tk.Button(root, text="Load Cookies", command=load_cookies)
load_cookies_.pack(side=tk.LEFT, padx=10)

# Create Run button
save_cookies_ = tk.Button(root, text="Save Cookies", command=save_cookies)
save_cookies_.pack(side=tk.LEFT, padx=10, pady=10)

# Automatically load existing data when the application starts
load_data()

# Start the Tkinter main loop
root.mainloop()