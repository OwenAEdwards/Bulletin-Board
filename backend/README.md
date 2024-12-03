# Instructions

## How to Run
1. Enter the directory where the Python files live in the terminal. E.g. for me it's `C:\Users\owen1\Downloads\Computer Networks CS4065\Projects\Programming Assignment 2\backend` so I would set my directory in PowerShell using:
```powershell
Set-Location "C:\Users\owen1\Downloads\Computer Networks CS4065\Projects\Programming Assignment 2\backend"
```

NOTE: if you don't have python3, you can install it here:
https://www.python.org/downloads/

Then you can validate the install by typing this into any terminal (in Windows):
```
python3 --version
```

2. Run the client using python3 (again, make sure you're in the directory where the other python files live):
```
python3 .\socket_client.py
```

3. Enter the username you wish to use for the client

4. Run the server using python3 **in another terminal session** (again, make sure you're in the directory where the other python files live, you might need to set your location to where the python files live):
```powershell
Set-Location "C:\Users\owen1\Downloads\Computer Networks CS4065\Projects\Programming Assignment 2\backend"

python3 .\socket_server.py
```

5. Now go back to the client terminal session and connect to the server:
```
%connect localhost 5000
```

6. (Optional) You can join with multiple clients (up to 5) by repeating steps 1-3 and 5 (you can skip step 4 since there's already a server running)

## Usability Instructions

- How to post a message to public bulletin board (example below has a subject and content):
```
%post message subject | message content
```
- How to post a group message to a private board you've joined (example below has a group_id, subject, and content):
```
%grouppost 1 subject | message content
```
- All other special input commands should be the same as the instructions from the assignment

# Major Issues

## Issues Encountered

1. Broadcasting to the client upon joins, leaves, and posts was not as intuitive.
2. I wanted to separate the private boards and the public board to track the group_id on private boards.

## Solutions and Workarounds

1. We accomplished broadcasting by creating a separate thread on the client that's always listening for signal interrupts (a concept I learned in OS about interprocess communication) and a thread on the server for sending to the client (since we're using unicast sockets, one connection each). Each signal signifies a message being sent.
2. Although BulletinBoard (the main public board) and PrivateBoard (the multiple private group boards) are very similar, PrivateBoard has a group_id associated with it. Although there's more overhead by instantiating objects of these classes, I think it's better system design because of separation of concern.