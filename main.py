import os
import pickle
import tkinter
import tkinter as tk
from pkgutil import get_loader
from uuid import uuid4

from scraper import fill_data_into_rocket_reach
from scraper.objects import Scraper

driver = Scraper.initialize(proxy="")
driver.close()

COOKIE_FILE_NAME = "cookies.pkl"


def new_browser():
    global driver
    try:
        driver.close()
    except Exception as e:
        print(e)
    driver = Scraper.initialize(proxy="")

def _load_data_from_file(file_name, text_box):
    try:
        with open(file_name, "r") as f:
            file_data = f.read().strip().split('\n')

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, '\n'.join(file_data))

    except FileNotFoundError:
        print("No saved data found.")
    except Exception as e:
        print(f"Error loading data: {e}")

# Function to load data from files
def load_data():
    _load_data_from_file(
        file_name="names.txt",
        text_box=usernames_textbox,
    )

    _load_data_from_file(
        file_name="emails.txt",
        text_box=emails_textbox,
    )

    _load_data_from_file(
        file_name="limit_account.txt",
        text_box=limit_count_textbox,
    )

    _load_data_from_file(
        file_name="initial_link.txt",
        text_box=link_textbox,
    )

    _load_data_from_file(
        file_name="sleep_seconds.txt",
        text_box=sleep_seconds_textbox,
    )

    print("Data loaded successfully!")

def save_cookies():
    if not driver:
        new_browser()
    driver.get("https://web.whatsapp.com")
    try:
        pickle.dump(driver.get_cookies(), open(COOKIE_FILE_NAME, 'wb'))
    except:
        pass

def save_limit_link():
    account_length = int(limit_count_textbox.get("1.0", tk.END).strip())
    initial_link = link_textbox.get("1.0", tk.END).strip()
    sleep_seconds_text = sleep_seconds_textbox.get("1.0", tk.END).strip()

    with open("limit_account.txt", 'w') as file:
        file.write(str(account_length))

    with open("initial_link.txt", 'w') as file:
        file.write(initial_link)

    with open("sleep_seconds.txt", 'w') as file:
        file.write(sleep_seconds_text)

    print("Data saved successfully!")

def load_cookies():
    try:
        if os.path.isfile(COOKIE_FILE_NAME):
            with open(COOKIE_FILE_NAME, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    if not driver:
                        new_browser()
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

    try:
        driver.close()
    except Exception as e:
        print(e)
    new_browser()

    # Call the imported function
    processed, un_processed = fill_data_into_rocket_reach(data=data, driver=driver)

    # Remove processed and unprocessed items from original lists
    processed_usernames = [pair[0] for pair in processed]
    processed_emails = [pair[1] for pair in processed]

    un_processed_usernames = [pair[0] for pair in un_processed]
    un_processed_emails = [pair[1] for pair in un_processed]

    # Remove processed items from original lists
    remaining_usernames = [u for u in usernames if u.strip() not in processed_usernames]
    remaining_emails = [e for e in emails if e.strip() not in processed_emails]

    # Remove processed items from original lists
    remaining_usernames = [u for u in remaining_usernames if u.strip() not in un_processed_usernames]
    remaining_emails = [e for e in remaining_emails if e.strip() not in un_processed_emails]

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

    # Save updated data
    with open(f"invalid_names_{str(uuid4())}.txt", "w") as f:
        f.write('\n'.join(un_processed_usernames))

    with open(f"invalid_emails_{str(uuid4())}.txt", "w") as f:
        f.write('\n'.join(un_processed_emails))

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

frame_link = tk.Frame(root)
frame_link.pack(padx=10, pady=5)

link_label = tk.Label(frame_link, text="Enter link:")
link_label.pack(side=tk.LEFT)

link_textbox = tk.Text(frame_link, height=1, width=40)
link_textbox.pack(fill=tk.BOTH)

frame_seconds = tk.Frame(root)
frame_seconds.pack(padx=10, pady=5)

seconds_label = tk.Label(frame_link, text="Seconds:")
seconds_label.pack(side=tk.LEFT)

sleep_seconds_textbox = tk.Text(frame_link, height=1, width=2)
sleep_seconds_textbox.pack(fill=tk.BOTH)

limit_count_frame = tk.Frame(root)
limit_count_frame.pack(padx=10, pady=5)

limit_count_label = tk.Label(limit_count_frame, text="Enter limit:")
limit_count_label.pack(side=tk.LEFT)

limit_count_textbox = tk.Text(limit_count_frame, height=1, width=12)
limit_count_textbox.pack(side=tk.LEFT, fill=tk.X)

save_link_button = tk.Button(limit_count_frame, text="Save", command=save_limit_link)
save_link_button.pack(side=tk.RIGHT)

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