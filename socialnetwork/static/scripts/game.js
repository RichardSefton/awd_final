import { loadGameSocket } from '/static/scripts/sockets.js';

const boardChange = (e) => {
    const board = document.getElementById('ct-1');
    const pgn = board.moveList._container.innerText;
    const { gameSocket } = window.websockets; 
    gameSocket.send(JSON.stringify({
        action: 'move',
        pgn
    }));
};

const pageLoad = () => {
    loadGameSocket();
    const btnmove = document.getElementById('ct-12');
    btnmove.addEventListener('click', boardChange);
};

window.addEventListener('load', pageLoad);