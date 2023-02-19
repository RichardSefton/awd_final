import { fetchData } from '/static/scripts/fetchSvc.js';

const handleFriendRequestAcceptClick = async (e) => {
    e.preventDefault();
    const button = e.target;
    const profileId = button.attributes['profile'].value;
    
    try {
        await fetchData(`/friends/${profileId}/confirm`, 'POST', {}, { profileId });
        location.reload();
    } catch(err) {
        console.error(err);
    }
}

const pendingFriendsListLoaded = () => {
    const prndingRequestButtons = document.querySelectorAll('[profile]')
    for(let i = 0; i < prndingRequestButtons.length; i++) {
        prndingRequestButtons[i].addEventListener('click', handleFriendRequestAcceptClick);
    }
};

window.addEventListener('load', pendingFriendsListLoaded);