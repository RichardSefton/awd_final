import { validateUsername, validatePassword, validateEmail } from "/static/scripts/validation.js";

/**
 * @description: This function is called when the user changes the username, email, or password fields
 */
const validate = () => {
    //get the input values from the form
    const username = document.getElementById('id_username').value;
    const email = document.getElementById('id_email').value;
    const password1 = document.getElementById('id_password1').value;
    const password2 = document.getElementById('id_password2').value;

    //disabled the submit button if the username or password is invalid
    let setDisabled = true;
    if (validateUsername(username) && 
        validateEmail(email) &&
        validatePassword(password1) &&
        validatePassword(password2)) 
        setDisabled = false

    if (password1 !== password2) setDisabled = true;
    
    document.getElementById('register_submit').disabled = setDisabled;

};

/**
 * @description: This function is called when the page is loaded
 */
export const onLoad = () => {
    //validate the form in its current state
    validate();
    //attach event listeners to the username and password fields to listen for changes
    document.getElementById('id_username').addEventListener('change', () => validate());
    document.getElementById('id_email').addEventListener('change', () => validate());
    document.getElementById('id_password1').addEventListener('change', () => validate());
    document.getElementById('id_password2').addEventListener('change', () => validate());
};

window.addEventListener('load', onLoad);
