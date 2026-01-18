# Whatsapp-remainders

This project is a WhatsApp reminder bot made in python using Green API and Flask and APScheduler
This bot can send automatic reminder messages to WhatsApp groups
It supports multiple reminders on the same day at different times
All reminders are saved in a json file so nothing is lost when the bot restarts
Only the admin number can control the bot
The admin can add reminders
The admin can list all reminders
The admin can clear reminders of any day
The admin can also add multiple groups and set reminders for specific groups
When the bot starts it automatically loads the reminders file
If the file is not found it creates it
The bot checks time every thirty seconds
If the time matches any reminder it sends the message to the WhatsApp group
The bot also runs a small web server
This is useful for free hosting like Render so the service stays active
The bot connects to WhatsApp using Green API
You must create a Green API instance
You must scan the QR code to login WhatsApp
After login the bot can send and receive messages automatically
Admin commands supported
set day time message
list
clear day
addgroup name groupid
setgroup name day time message
This bot is useful for daily motivation study reminders work alerts and automation
Project created by Sαѕυкє  Ucнιнα
