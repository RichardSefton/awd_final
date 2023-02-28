
const handleImageLoadError = (e) => {
    const { attributes: { status: { value } } } = e.target;
    const fallbacks = document.querySelectorAll('[profileThumbnailFallback]');
    for(let i = 0; i < fallbacks.length; i++) {
        const { attributes: { status: { value: fallbackStatus } } } = fallbacks[i];
        if (fallbackStatus === value) {
            fallbacks[i].hidden = false;
            e.target.hidden = true;
        }
    }
};



const onLoad = () => {
    const thumbnails = document.querySelectorAll('[profileThumbnail]');
    for(let i = 0; i < thumbnails.length; i++) {
        thumbnails[i].onerror = handleImageLoadError;
        thumbnails[i].src = thumbnails[i].src;
    }  
};

window.addEventListener('load', onLoad);