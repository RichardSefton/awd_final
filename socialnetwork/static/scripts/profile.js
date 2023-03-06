/**
 * @description: This function is called when the user clicks on the profile picture
 */
const onLoad = () => {
    //attaches the upload buttons click event to the profile picture
    const upload = document.getElementById('id_profile_pic');
    const img = document.getElementById('profile-pic');
    img.addEventListener('click', () => upload.click());
}

window.addEventListener('load', onLoad)