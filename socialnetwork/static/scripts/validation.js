const regex = {
    USERNAME: /[a-zA-Z][a-zA-Z0-9-_]{3,32}/,
    PASSWORD: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/,
    EMAIL: /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/g
}

export const validateUsername = (u='') => {
    return regex.USERNAME.test(u);
};

export const validateEmail = (e='') => {
    return regex.EMAIL.test(e);
};

export const validatePassword = (p='') => {
    return regex.PASSWORD.test(p);
};