import { fetchData } from '/static/scripts/fetchSvc.js';

const handleFriendRequestAcceptClick = async (e) => {
    e.preventDefault();
    const button = e.target;
    const profileId = button.attributes['profile'].value;
    
    try {
        await fetchData(`/api/friends/${profileId}/confirm`, 'POST', {}, { profileId });
        location.reload();
    } catch(err) {
        console.error(err);
    }
};

const handleFriendRequestCancelClick = async (e) => {
    e.preventDefault();
    const button = e.target;
    const profileId = button.attributes['cancel'].value;

    try {
        await fetchData(`/api/friends/${profileId}/cancel`, 'POST', {}, { profileId });
        location.reload();
    } catch(err) {
        console.error(err);
    }
};

const handleFriendRequestDeclineClick = async (e) => {
    e.preventDefault();
    const button = e.target;
    const profileId = button.attributes['decline'].value;

    try {
        await fetchData(`/api/friends/${profileId}/decline`, 'POST', {}, { profileId });
        location.reload();
    } catch(err) {
        console.error(err);
    }
};

const handleUnfriendRequestClick = async (e) => {
    e.preventDefault();
    const button = e.target;
    const profileId = button.attributes['friend'].value;

    try {
        await fetchData(`/api/friends/${profileId}/unfriend`, 'POST', {}, { profileId });
        location.reload();
    } catch(err) {
        console.error(err);
    }
};

const pendingFriendsListLoaded = () => {
    const pendingRequestButtons = document.querySelectorAll('[profile]')
    for(let i = 0; i < pendingRequestButtons.length; i++) {
        pendingRequestButtons[i].addEventListener('click', handleFriendRequestAcceptClick);
    }

    const cancelRequestButtons = document.querySelectorAll('[cancel]');
    for(let i = 0; i < cancelRequestButtons.length; i++) {
        cancelRequestButtons[i].addEventListener('click', handleFriendRequestCancelClick);
    }

    const declineRequestButtons = document.querySelectorAll('[decline]');
    for(let i = 0; i < declineRequestButtons.length; i++) {
        declineRequestButtons[i].addEventListener('click', handleFriendRequestDeclineClick);
    }

    const unfriendButtons = document.querySelectorAll('[friend]');
    for(let i = 0; i < unfriendButtons.length; i++) {
        unfriendButtons[i].addEventListener('click', handleUnfriendRequestClick);
    }
};

window.addEventListener('load', pendingFriendsListLoaded);