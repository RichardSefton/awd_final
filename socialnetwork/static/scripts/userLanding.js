import { loadUserSocket } from '/static/scripts/sockets.js';

const pageLoad = () => {
    loadUserSocket();
};

window.addEventListener('load', pageLoad);