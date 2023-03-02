
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

    const commentFallbacks = document.querySelectorAll('[commentThumbnailFallback]');
    for(let i = 0; i < commentFallbacks.length; i++) {
        const { attributes: { comment: { value: commentFallbackStatus } } } = commentFallbacks[i];
        if (commentFallbackStatus === value) {
            commentFallbacks[i].hidden = false;
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
    
    const commentThumbnails = document.querySelectorAll('[commentThumbnail]');
    for(let i = 0; i < commentThumbnails.length; i++) {
        commentThumbnails[i].onerror = handleImageLoadError;
        commentThumbnails[i].src = commentThumbnails[i].src;
    }  
};

window.addEventListener('load', onLoad);