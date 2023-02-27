import { friendRequestLoadingSpinner, friendRequestFinished } from '/static/scripts/domHelper.js';
import { fetchData } from '/static/scripts/fetchSvc.js';

const handleFriendClick = async e => {
    const { target: { attributes: { profile: { value } } } } = e;
    const profileId = parseInt(value);

    if (profileId) {
        friendRequestLoadingSpinner(profileId);
        try {
            const sentRequest = await fetchData('/api/friend-request', 'post', {}, { profileId })
            console.log(sentRequest)
            if (sentRequest) {
                const { userSocket } = window.websockets;
                try {
                    userSocket.send(JSON.stringify({
                        action: 'friend_request',
                        profileId
                    }))
                } catch(err) {
                    console.error(err);
                }
                friendRequestFinished(true, profileId);
            } else throw Error('Could not send friend request');
        } catch(err) {
            console.error(err);
            friendRequestFinished(false, profileId);
        }
    }
};

const loadPage = () => {
    const friends = document.querySelectorAll('[profile]');
    for(let i = 0; i < friends.length; i++) {
        friends[i].addEventListener('click', handleFriendClick);
    }
};

window.addEventListener('load', loadPage);