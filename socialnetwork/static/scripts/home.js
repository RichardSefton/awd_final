import { fetchPagePart } from '/static/scripts/fetchSvc.js';


const pageLoaded = () => {
    fetchPagePart('/home')
        .then((p) => {
            const root = document.getElementById('root');
            root.innerHTML = p
        });
};

window.addEventListener('load', pageLoaded);