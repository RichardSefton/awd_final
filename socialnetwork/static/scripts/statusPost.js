/**
 * @description: This function opens the new status form and hides the create status button
 */
const openNewStatusForm = () => {
    document.getElementById('statusPostContainer').hidden = false;
    document.getElementById('statusPostCreate').hidden = true;
};

/**
 * @description: This function removes unwanted classes from the status field
 */
const removeUnwantedClasses = () => {
    const status = document.getElementById('id_status');
    status.classList.remove('is-invalid');
    status.classList.remove('is-valid');

    const invalidFeedback = document.getElementsByClassName('invalid-feedback');
    if (invalidFeedback.length > 0) {
        invalidFeedback[0].hidden = true;
    }
};

/**
 * @description: This function is called when the page is loaded
 */
const onLoad = () => {
    //attach event listener to the create status button
    document.getElementById('statusPostCreateButton').addEventListener('click', openNewStatusForm);
    //remove the unwanted classes from the status field
    removeUnwantedClasses();
};

window.addEventListener("load", onLoad);