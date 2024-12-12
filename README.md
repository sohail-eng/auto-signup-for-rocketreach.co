# auto-signup-for-rocketreach.co
It will get emails and usernames from the user through TK-Inter UI and saved into text files, moreover, user can provide directly through the files. It have a run button that will automatically get the email and username from the files and signup on the `rocketreach.co` site. then it will removed this email and username from the file.

This application provides a user-friendly GUI for automating signup processes on Rocket Reach using provided usernames and emails. The tool allows users to:
- Load and save username and email lists
- Process signups with configurable delay
- Automatically manage processed and unprocessed entries

## Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

## Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sohail-eng/auto-signup-for-rocketreach.co.git
cd rocket-reach-signup
```

### 2. Create a Virtual Environment (Recommended)
#### Windows
```cmd
python -m venv venv
venv\Scripts\activate
```

#### Ubuntu/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Running the Application

#### Using run.sh (Linux/Ubuntu)
```bash
chmod +x run.sh
./run.sh
```

#### Using Command Line
##### Windows
```cmd
python main.py
```

##### Ubuntu/Linux
```bash
python3 main.py
```

## Application Usage
1. Open the application
2. Enter usernames in the top text box
3. Enter corresponding emails in the bottom text box
4. Set desired delay between signups
5. Click "Run" to start processing

### Features
- Load existing username/email lists
- Save current lists
- Automatically remove processed entries
- Configurable delay between signups

## Troubleshooting
- Ensure all dependencies are installed
- Check internet connection
- Verify usernames and emails are correctly formatted

## Notes
- The application requires an active internet connection
- Respect the website's terms of service
- Use responsibly and ethically

## License
[Add your license information here]

## Contributing
[Add contribution guidelines if applicable]