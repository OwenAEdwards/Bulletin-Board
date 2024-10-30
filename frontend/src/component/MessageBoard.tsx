import React, { useEffect } from 'react';
import io from 'socket.io-client';
import { BulletinData } from '../types/BulletinTypes';

const BulletinBoard: React.FC = () => {
    let socket: ReturnType<typeof io>

    useEffect(() => {
        const socket = io('http://localhost:5000');

        socket.on('connect', () => {
            console.log('Connected to the WebSocket server');
        });

        socket.on('bulletin_response', (data: BulletinData) => {
            console.log('Bulletin response:', data);
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    const postBulletin = (sender: string, postDate: string, subject: string) => {
        socket.emit('bulletin_post', { sender, postDate, subject });
    };

    return (
        <div>
            <h1>Bulletin Board</h1>
            <button onClick={() => postBulletin('User1', new Date().toISOString(), 'Hello World!')}>
                Post Bulletin
            </button>
        </div>
    );
};

export default BulletinBoard;
