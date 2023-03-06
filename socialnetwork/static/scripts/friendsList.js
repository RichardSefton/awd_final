import { fetchData } from '/static/scripts/fetchSvc.js';

/**
 * @description: This function is called when the user clicks on the button 
 * to accept a friend request
 * 
 * @param {Event} e 
 */
const handleFriendRequestAcceptClick = async (e) => {
    e.preventDefault();
    const button = e.target;
    //get the profile id from the button
    const profileId = button.attributes['profile'].value;
    
    try {
        //make a fetch request to accept the friend request
        await fetchData(`/api/friends/${profileId}/confirm`, 'POST', {}, { profileId });
        //reload the page
        location.reload();
    } catch(err) {
        console.error(err);
    }
};

/**
 * @description: This function is called when the user clicks on the button 
 * to cancel a friend request
 * 
 * @param {Event} e 
 */
const handleFriendRequestCancelClick = async (e) => {
    e.preventDefault();
    const button = e.target;
    //get the profile id from the button
    const profileId = button.attributes['cancel'].value;

    try {
        //make a fetch request to cancel the friend request
        await fetchData(`/api/friends/${profileId}/cancel`, 'POST', {}, { profileId });
        //reload the page
        location.reload();
    } catch(err) {
        console.error(err);
    }
};

/**
 * @description: This function is called when the user clicks on the button 
 * to decline a friend request
 * 
 * @param {Event} e 
 */
const handleFriendRequestDeclineClick = async (e) => {
    e.preventDefault();
    const button = e.target;
    //get the profile id from the button
    const profileId = button.attributes['decline'].value;

    try {
        //make a fetch request to decline the friend request
        await fetchData(`/api/friends/${profileId}/decline`, 'POST', {}, { profileId });
        //reload the page
        location.reload();
    } catch(err) {
        console.error(err);
    }
};

/**
 * @description: This function is called when the user clicks on the button 
 * to unfriend a user
 * 
 * @param {Event} e 
 */
const handleUnfriendRequestClick = async (e) => {
    e.preventDefault();
    const button = e.target;
    //get the profile id from the button
    const profileId = button.attributes['friend'].value;

    try {
        //make a fetch request to unfriend the user
        await fetchData(`/api/friends/${profileId}/unfriend`, 'POST', {}, { profileId });
        //reload the page
        location.reload();
    } catch(err) {
        console.error(err);
    }
};

/**
 * @description: This function is called when the page is loaded
 */
const onLoad = () => {
    //get all the buttons with the profile attribute and attach a click event listener to them
    //to accept the friend request
    const pendingRequestButtons = document.querySelectorAll('[profile]')
    for(let i = 0; i < pendingRequestButtons.length; i++) {
        pendingRequestButtons[i].addEventListener('click', handleFriendRequestAcceptClick);
    }

    //get all the buttons with the cancel attribute and attach a click event listener to them
    //to cancel the friend request
    const cancelRequestButtons = document.querySelectorAll('[cancel]');
    for(let i = 0; i < cancelRequestButtons.length; i++) {
        cancelRequestButtons[i].addEventListener('click', handleFriendRequestCancelClick);
    }

    //get all the buttons with the decline attribute and attach a click event listener to them
    //to decline the friend request
    const declineRequestButtons = document.querySelectorAll('[decline]');
    for(let i = 0; i < declineRequestButtons.length; i++) {
        declineRequestButtons[i].addEventListener('click', handleFriendRequestDeclineClick);
    }

    //get all the buttons with the friend attribute and attach a click event listener to them
    //to unfriend the user
    const unfriendButtons = document.querySelectorAll('[friend]');
    for(let i = 0; i < unfriendButtons.length; i++) {
        unfriendButtons[i].addEventListener('click', handleUnfriendRequestClick);
    }
};

window.addEventListener('load', onLoad);