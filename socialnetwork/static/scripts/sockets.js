import { friendRequestNotification } from '/static/scripts/domHelper.js';

/**
 * Function sets up the general active user socket and returns it.
 * 
 * This socket is used for general user events (friend request notifications etc)
 * 
 */
export const loadUserSocket = () => {
    const socket = new WebSocket(`ws://${window.location.host}/ws/user`);
    
    socket.onmessage = (e) => {
        friendRequestNotification();
    };

    socket.onerror = (e, err) => {
        console.error(err);
    };

    if (!window.websockets)
        window.websockets = {};

    window.websockets = {
        ...window.websockets,
        userSocket: socket
    }
};

/**
 * Function sets up the game socket and returns it.
 * 
 * This socket is used for game events (Move making, game ending etc)
 * 
 */
export const loadGameSocket = () => {
    const gameId = parseInt(window.location.pathname.split(['/'])[2]);
    const socket = new WebSocket(`ws://${window.location.host}/ws/game/${gameId}`);
    
    socket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        if (data.move_played)
            window.location.reload();s
    };

    socket.onerror = (e, err) => {
        console.error(err);
    };

    socket.onopen = (e, other) => {
        console.log(e, other);
    }

    if (!window.websockets)
        window.websockets = {};

    window.websockets = {
        ...window.websockets,
        gameSocket: socket
    };
};
