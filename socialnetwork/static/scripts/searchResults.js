import { friendRequestLoadingSpinner, friendRequestFinished } from '/static/scripts/domHelper.js';
import { fetchData } from '/static/scripts/fetchSvc.js';
import { loadUserSocket } from '/static/scripts/sockets.js';

const handleFriendClick = async e => {
    const { target: { attributes: { profile: { value } } } } = e;
    const profileId = parseInt(value);


    if (profileId) {
        friendRequestLoadingSpinner(profileId);
        try {
            const req = await fetchData('/friend-request', 'post', {}, { profileId })
            friendRequestFinished(true, profileId);
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