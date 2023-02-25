import { fetchData } from '/static/scripts/fetchSvc.js';

const inviteFriend = async e => {
    const friendId = e.target.attributes['invite'].value;

    try {
        const response = await fetchData(`/api/game/invite/${friendId}`, 'post');
        window.location.href = `/play/${response.id}`
    } catch(err) {
        console.error(err);
    }
};

const playGame = async e => {
    const gameId = e.target.attributes['play'].value;

    try {
        window.location.href = `/play/${gameId}`
    } catch(err) {
        console.error(err);
    }
};

const onLoad = () => {
    const inviteButtons = document.querySelectorAll('[invite]');
    for (let i = 0; i < inviteButtons.length; i++) {
        inviteButtons[i].addEventListener('click', e => inviteFriend(e));
    }   

    const playButtons = document.querySelectorAll('[play]');
    for (let i = 0; i < playButtons.length; i++) {
        playButtons[i].addEventListener('click', e => playGame(e));
    }
}

window.addEventListener('load', onLoad);