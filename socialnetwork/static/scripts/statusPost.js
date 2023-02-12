const openNewStatusForm = () => {
    document.getElementById('statusPostContainer').hidden = false;
    document.getElementById('statusPostCreate').hidden = true;
};

const removeUnwantedClasses = () => {
    const status = document.getElementById('id_status');
    status.classList.remove('is-invalid');
    status.classList.remove('is-valid');

    const invalidFeedback = document.getElementsByClassName('invalid-feedback');
    if (invalidFeedback.length > 0) {
        invalidFeedback[0].hidden = true;
    }
};

const onLoad = () => {
    document.getElementById('statusPostCreateButton').addEventListener('click', openNewStatusForm);
    removeUnwantedClasses();
};

window.addEventListener("load", onLoad);