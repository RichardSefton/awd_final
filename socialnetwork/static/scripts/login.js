import { validateUsername, validatePassword } from '/static/scripts/validation.js'; 

const validate = () => {
    const username = document.getElementById('id_username').value;
    const password = document.getElementById('id_password').value;

    document.getElementById('login_submit').disabled = !validateUsername(username) && !validatePassword(password);
}

const loginLoaded = () => {
    validate();
    document.getElementById('id_username').addEventListener('change', () => validate());
    document.getElementById('id_password').addEventListener('change', () => validate());
}

window.addEventListener('load', loginLoaded);