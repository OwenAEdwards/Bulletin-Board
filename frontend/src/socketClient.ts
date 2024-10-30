import { BulletinData, ServerResponse } from './types/BulletinTypes';

const socket = io('http://localhost:5000'); // Adjust the URL as needed

// Listen for connection event
socket.on('connect', () => {
    console.log('Connected to the WebSocket server');
});

// Listen for responses from the server
socket.on('response', (data: ServerResponse) => {
    console.log(data.message);
});

// Function to send a bulletin post
function postBulletin(sender: string, postDate: string, subject: string) {
    const data = {
        sender,
        postDate,
        subject
    };
    socket.emit('bulletin_post', data);
}

// Listen for bulletin responses
socket.on('bulletin_response', (data: BulletinData) => {
    console.log('Bulletin response:', data);
});

// Example usage
postBulletin('User1', new Date().toISOString(), 'Hello World!');