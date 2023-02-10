import { validateUsername, validatePassword, validateEmail } from "/static/scripts/validation.js";

const validate = () => {
    const username = document.getElementById('id_username').value;
    const email = document.getElementById('id_email').value;
    const password1 = document.getElementById('id_password1').value;
    const password2 = document.getElementById('id_password2').value;

    let setDisabled = true;
    if (validateUsername(username) && 
        validateEmail(email) &&
        validatePassword(password1) &&
        validatePassword(password2)) 
        setDisabled = false

    if (password1 !== password2) setDisabled = true;

    console.log({
        username,
        usernameValid: validateUsername(username),
        email,
        emailValid: validateUsername(email),
        password1,
        password1Valid: validatePassword(password1),
        password2,
        password2Valid: validatePassword(password1),
        match: password1 === password2,
        disabled: setDisabled
    })
    
    document.getElementById('register_submit').disabled = setDisabled;

};

export const registerLoaded = () => {
    validate();

    document.getElementById('id_username').addEventListener('change', () => validate());
    document.getElementById('id_email').addEventListener('change', () => validate());
    document.getElementById('id_password1').addEventListener('change', () => validate());
    document.getElementById('id_password2').addEventListener('change', () => validate());
};

window.addEventListener('load', registerLoaded);
