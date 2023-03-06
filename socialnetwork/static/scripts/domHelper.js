import { fetchData } from '/static/scripts/fetchSvc.js';

/**
 * @description: This function is called when the user submits a friend request.
 * and we want to show some ui response for longer requests. 
 * 
 * @param {String} profileId 
 * @returns 
 */
export const friendRequestLoadingSpinner = (profileId=null) => {
    if (!profileId) return; //If no profile id is passed, return

    //get the button and set the innerHTML to an empty string
    const friendRequestButton = document.querySelector(`[profile="${profileId}"]`);
    friendRequestButton.innerHTML = '';

    //create a spinner and a text element and set the appropriate bootstrap classes
    const spinnerSpan = document.createElement('span');
    spinnerSpan.classList.add('spinner-border', 'spinner-border-sm');
    const spinnerText = document.createElement('span');
    //set the text to 'Requesting...'
    spinnerText.innerHTML = 'Requesting...';

    //append the spinner and text to the button
    friendRequestButton.append(spinnerSpan);
    friendRequestButton.append(spinnerText);
};

/**
 * @description: This function is called when the friend request process has finished
 * 
 * @param {boolean} success 
 * @param {string} profileId 
 * @returns 
 */
export const friendRequestFinished = (success=false, profileId='') => {
    //if the request was not successful, change the button to a danger button
    //and set the text to 'Unable to send', and disable the button
    if (!success) {
        const friendRequestButton = document.querySelector(`[profile="${profileId}"]`);
        friendRequestButton.classList.remove('btn-primary');
        friendRequestButton.classList.add('btn-danger');
        friendRequestButton.innerHTML = 'Unable to send';
        friendRequestButton.disabled = true;
        return;
    }

    //if the request was successful, change the button to a success button
    //and set the text to 'Request Sent', and disable the button
    const friendRequestButton = document.querySelector(`[profile="${profileId}"]`);
    friendRequestButton.classList.remove('btn-primary');
    friendRequestButton.classList.add('btn-success');
    friendRequestButton.innerHTML = 'Request Sent';
    friendRequestButton.disabled = true;
};

/**
 * @description: This function is used to get the current logged on users
 * pending friend requests.
 */
export const friendRequestNotification = async () => {
    try {
        //get the pending friend requests
        const data = await fetchData('/api/pending-friend-requests')
        //get the notification badge
        const requestNotifications = document.getElementById('actionButtonNotification');

        //if the badge exists, set the innerHTML to the number of pending requests and
        //hide the badge if there are no pending requests
        if (requestNotifications) {
            requestNotifications.innerHTML = data.length;
            document.getElementById('actionButtonNotificationContainer').hidden = data.length === 0;
        }
    } catch (err) {
        console.error(err);
    }
};