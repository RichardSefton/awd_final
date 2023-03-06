import { friendRequestLoadingSpinner, friendRequestFinished } from '/static/scripts/domHelper.js';
import { fetchData } from '/static/scripts/fetchSvc.js';

/**
 * 
 * @param {Event} e 
 */
const handleFriendClick = async e => {
    //get the profile id from the events target
    const { target: { attributes: { profile: { value } } } } = e;
    const profileId = parseInt(value);

    //if the profile id is valid
    if (profileId) {
        //show the loading spinner
        friendRequestLoadingSpinner(profileId);
        try {
            //make a fetch request to send the friend request
            const sentRequest = await fetchData('/api/friend-request', 'post', {}, { profileId })
            if (sentRequest) {
                //if the request was sent, send a message to the server via the websocket
                const { userSocket } = window.websockets;
                try {
                    userSocket.send(JSON.stringify({
                        action: 'friend_request',
                        profileId
                    }))
                } catch(err) {
                    console.error(err);
                }
                //hide the loading spinner and show the success/failure message
                friendRequestFinished(true, profileId);
            } else throw Error('Could not send friend request');
        } catch(err) {
            console.error(err);
            //hide the loading spinner and show the success/failure message
            friendRequestFinished(false, profileId);
        }
    }
};

const onLoad = () => {
    //get all the elements with the attribute 'profile'
    const friends = document.querySelectorAll('[profile]');
    for(let i = 0; i < friends.length; i++) {
        //attach a click event listener to each element
        friends[i].addEventListener('click', handleFriendClick);
    }
};

window.addEventListener('load', onLoad);