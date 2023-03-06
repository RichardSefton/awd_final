import { loadUserSocket } from '/static/scripts/sockets.js';

/**
 * @description: This function is called when the page is loaded
 */
const onLoad = () => {
    //load the user socket
    loadUserSocket();
};

window.addEventListener('load', onLoad);