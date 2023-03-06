//Regular expressions for validation
const regex = {
    USERNAME: /[a-zA-Z][a-zA-Z0-9-_]{3,32}/,
    PASSWORD: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/,
    EMAIL: /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/g
}

//username validation
export const validateUsername = (u='') => regex.USERNAME.test(u);

//email validation
export const validateEmail = (e='') => regex.EMAIL.test(e);

//password validation
export const validatePassword = (p='') => regex.PASSWORD.test(p);