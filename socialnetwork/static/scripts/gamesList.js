import { fetchData } from '/static/scripts/fetchSvc.js';

/**
 * @description: This function is called when the user clicks on the button
 * to invite a friend to a game.
 * 
 * @param {Event} e 
 */
const inviteFriend = async e => {
    //get the friend id from the events target
    const friendId = e.target.attributes['invite'].value;

    try {
        //make a fetch request to invite the friend to a game
        const response = await fetchData(`/api/game/invite/${friendId}`, 'post');
        //go to the url for the game
        window.location.href = `/play/${response.id}`
    } catch(err) {
        console.error(err);
    }
};

/**
 * @description: This function is called when the user clicks on the button
 * to start a game. 
 * 
 * @param {Event} e 
 */
const playGame = async e => {
    //get the game id from the events target
    const gameId = e.target.attributes['play'].value;

    try {
        //go to the url for the game
        window.location.href = `/play/${gameId}`
    } catch(err) {
        console.error(err);
    }
};

/**
 * @description: This function is called when the page is loaded
 */
const onLoad = () => {
    //get all the buttons with the attribute 'invite'
    const inviteButtons = document.querySelectorAll('[invite]');
    for (let i = 0; i < inviteButtons.length; i++) {
        //attach a click event listener to each button
        inviteButtons[i].addEventListener('click', e => inviteFriend(e));
    }   

    //get all the buttons with the attribute 'play'
    const playButtons = document.querySelectorAll('[play]');
    for (let i = 0; i < playButtons.length; i++) {
        //attach a click event listener to each button
        playButtons[i].addEventListener('click', e => playGame(e));
    }
}

window.addEventListener('load', onLoad);