/**
 * Function sets up the general active user socket and returns it.
 * 
 * This socket is used for general user events (friend request notifications etc)
 * 
 * @returns socket
 */
export const loadUserSocket = () => {
    const socket = new WebSocket(`ws://${window.location.host}/ws/user`);
    socket.onmessage = (e) => {
        console.log('onmessage', {...e})
    };
    socket.onerror = (e, err) => {
        console.error(err);
    };

    return socket;
};

/**
 * const chatSocket = new WebSocket('ws://'+ window.location.host+ '/ws/'+roomName+ '/'
        );
        console.log(chatSocket);

        chatSocket.onerror = (e, err) => {
            console.log('error', e, err);
        }

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            document.querySelector('#chat-log').value += (data.message + '\n');
        };

        chatSocket.onclose = function(e) {
            console.log(e);
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
 */