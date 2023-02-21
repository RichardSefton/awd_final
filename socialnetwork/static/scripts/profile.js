const profileLoad = () => {
    const upload = document.getElementById('id_profile_pic');
    const img = document.getElementById('profile-pic');
    img.addEventListener('click', () => upload.click());
}

window.addEventListener('load', profileLoad)