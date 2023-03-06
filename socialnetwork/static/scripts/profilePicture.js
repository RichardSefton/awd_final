/**
 * @description: This function is called when an image fails to load
 * It will load the fallback image for the profile picture
 * 
 * @param {Event} e 
 */
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


/**
 * @description: This function is called when the page is loaded
 */
const onLoad = () => {
    //get all the profile thumbnails and attach an error event listener to them
    //This will load the fallback image if the profile picture fails to load
    const thumbnails = document.querySelectorAll('[profileThumbnail]');
    for(let i = 0; i < thumbnails.length; i++) {
        thumbnails[i].onerror = handleImageLoadError;
        thumbnails[i].src = thumbnails[i].src;
    } 
    
    //get all the comment thumbnails images and attach an error event listener to them
    //This will load the fallback image if the profile picture fails to load
    const commentThumbnails = document.querySelectorAll('[commentThumbnail]');
    for(let i = 0; i < commentThumbnails.length; i++) {
        commentThumbnails[i].onerror = handleImageLoadError;
        commentThumbnails[i].src = commentThumbnails[i].src;
    }  
};

window.addEventListener('load', onLoad);