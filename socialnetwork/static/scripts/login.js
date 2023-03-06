import { validateUsername, validatePassword } from '/static/scripts/validation.js'; 

/**
 * @description: This function is called when the user chnges the username or password fields
 */
const validate = () => {
    //get the username and password from the form
    const username = document.getElementById('id_username').value;
    const password = document.getElementById('id_password').value;

    //disabled the submit button if the username or password is invalid
    document.getElementById('login_submit').disabled = !validateUsername(username) && !validatePassword(password);
}

/**
 * @description: This function is called when the page is loaded
 */
const onLoad = () => {
    //validate the form in its current state
    validate();
    //attach event listeners to the username and password fields to listen for changes
    document.getElementById('id_username').addEventListener('change', () => validate());
    document.getElementById('id_password').addEventListener('change', () => validate());
}

window.addEventListener('load', onLoad);