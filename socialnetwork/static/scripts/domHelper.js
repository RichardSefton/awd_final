import { fetchData } from '/static/scripts/fetchSvc.js';

export const friendRequestLoadingSpinner = (profileId=null) => {
    if (!profileId) return;
    const friendRequestButton = document.querySelector(`[profile="${profileId}"]`);
    friendRequestButton.innerHTML = '';

    const spinnerSpan = document.createElement('span');
    spinnerSpan.classList.add('spinner-border', 'spinner-border-sm');
    const spinnerText = document.createElement('span');
    spinnerText.innerHTML = 'Requesting...';

    friendRequestButton.append(spinnerSpan);
    friendRequestButton.append(spinnerText);
};

export const friendRequestFinished = (success=false, profileId) => {
    if (!success) {
        const friendRequestButton = document.querySelector(`[profile="${profileId}"]`);
        friendRequestButton.classList.remove('btn-primary');
        friendRequestButton.classList.add('btn-danger');
        friendRequestButton.innerHTML = 'Unable to send';
        friendRequestButton.disabled = true;
        return;
    }

    const friendRequestButton = document.querySelector(`[profile="${profileId}"]`);
    friendRequestButton.classList.remove('btn-primary');
    friendRequestButton.classList.add('btn-success');
    friendRequestButton.innerHTML = 'Request Sent';
    friendRequestButton.disabled = true;
};

export const friendRequestNotification = async () => {
    try {
        const data = await fetchData('/pending-friend-requests')
        const requestNotifications = document.getElementById('actionButtonNotification');
        console.log(requestNotifications);

        if (requestNotifications) {
            requestNotifications.innerHTML = data.length;
            document.getElementById('actionButtonNotificationContainer').hidden = data.length === 0;
        }
    } catch (err) {
        console.error(err);
    }
};