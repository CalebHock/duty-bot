# Duty Bot

Duty Bot is an interactive Discord bot for use of residential life departments to manage their RA staff within the on call scheduling.

## Features

### Commands

#### Identify
`!id [name]` The id command links the discord user to a their name. The user should match the name that is on the schedule imported.

#### Staff
`!staff [staff name]` The staff command links the discord user to a specific staff on campus. It will assign them the role of the staff they belong to.

#### Duty
`!duty MM/DD/YYYY` The duty command will list out who is on duty for a specific day. The command can be ran in formats MM/DD/YYYY, MM/DD, and DD. The command can also be ran without a date, which then will automatically set the date to the upcoming Friday.

#### Transfer
`!transfer @owner @recipient MM/DD/YYYY` The transfer command will change in the schedule database who a duty shift belongs to.

## Installation

##### 1. Clone this project to the computer hosting the bot

```
cd  /path/to/project/folder
git clone https://github.com/CalebHock/duty-bot.git
```

##### 2. Install the latest version of Python3

```
sudo apt install python3 python3-pip
```

##### 3. Install the required packages in order to run the bot

```
cd duty-bot
pip3 install -r requirements.txt
```

## Setup

##### 1. Create a discord application

https://discord.com/developers/applications

a. Click `New Application`<br/>
b. Give it a name<br/>
c. Navigate to bot page</br>
d. Click `Add Bot`</br>

##### 2. Fill out `.env-template` and rename to `.env`

GUILD_ID<br/>
a. In your discord settings under appearance, enable developer mode<br/>
b. Right click on your discord server you are adding the bot to<br/>
c. Copy the ID and paste it in the `.env` under GUILD_ID<br/>
