import { loadGameSocket } from '/static/scripts/sockets.js';

/**
 * @description: This function is called when the user clicks on the button
 * to accept the move
 */
const boardChange = () => {
    //get the board
    const board = document.getElementById('ct-1');
    //get the game pgn from the board in its current state
    const pgn = board.moveList._container.innerText;
    //get the game socket from the window object
    const { gameSocket } = window.websockets; 
    //send the move to the server via the game socket
    gameSocket.send(JSON.stringify({
        action: 'move',
        pgn
    }));
};

/**
 * @description: This function is called when the page is loaded
 */
const onLoad = () => {
    //load the game websocket socket
    loadGameSocket();
    //get the button to accept the move
    const btnmove = document.getElementById('ct-12');
    //attach a click event listener to the button
    btnmove.addEventListener('click', boardChange);
};

window.addEventListener('load', onLoad);

