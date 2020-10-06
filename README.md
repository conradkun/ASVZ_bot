# ASVZ_bot
Bot to be the first to enrol to a particular class offered by ASVZ. All you need is your credentials and the URL of the class.

## Requirements

This bot uses Python 3.8 (although any version of Python 3 will probably work). To install all the necessary requirements move to the repository root folder and run:

`pip install -r requirements.txt`

## Usage

To run the bot, use:

`python ASVZ_handler.py --user <USERNAME> --password <PASSWORD> --url <URL>`

Where `<USERNAME>` is your ETH username, `<PASSWORD>` is your ETH password and `<URL>` is the URL of the class you want to enrol in. The bot needs to be running during the time enrolment starts, so your computer must be on during that time (unless you choose to run this on a VM on the cloud or some server). When you run it, it will wait until 1 minute before enrolment to log in, and 10 milliseconds after enrolment to refresh the page and enrol. Use it responsibly!