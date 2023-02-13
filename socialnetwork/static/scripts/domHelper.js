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
}

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
}