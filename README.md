# Networks-Project2

## Contributors

- Owen Edwards
- Elias Weitfle
- Viet Ton

## Add Later

> The README should contain instructions on how to compile and run your server/client programs (if certain
software or packages need to be installed, provide instructions as well), usability instructions ONLY if different
from suggested above, and a description of any major issues you came across and how you handled them (or
why you could not handle them).

## Project Structure

### frontend

- `/src/App.tsx`: Main React component.
- `/src/index.tsx`: Entry point for React.
- `/src/socketClient.ts`: TypeScript file handling the socket connection for the client.
- `/src/component/GroupList.tsx`: Component for list of available groups (Part 2 of project).
- `/src/component/Login.tsx`: User login component.
- `/src/component/MessageBoard.tsx`: Main message board UI component.
- `/src/component/MessageForm.tsx`: Form component for posting new messages.
- `/src/component/UserList.tsx`: Component that displays users in current group.

### backend

- `/tests/test_protocol.py`: Test cases for validating the message protocol.
- `app.py`: Flask server. Handles API requests, e.g., communication with frontend.
- `bulletin_board.py`: Core logic for the bulletin board system. Handles the structure of groups, messages, and user management within the application. This script interacts with the socket server to manage user activities.
- `client.py`: Client application for connecting to the bulletin board server. Handles user input, sends commands, and processes responses from the server.
- `requirements.txt`: List of dependencies for Flask and other Python packages.
- `socket_protocol.py`: Defines the message protocol for communication between the client and the server. This handles message formatting and parsing.
- `socket_server.py`: Manages the socket server setup, including binding the socket to a host and port, accepting connections, and dispatching messages between clients and the `bulletin_board.py`.