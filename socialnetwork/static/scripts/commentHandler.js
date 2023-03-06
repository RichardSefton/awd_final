import { fetchData } from '/static/scripts/fetchSvc.js';

/**
 * @description: This function is called when the user submits a comment.  
 * 
 * @param {Event} e 
 */
const handleSubmit = async e => {
    //get the comment id from the events target
    const { target: { attributes: { comment: { value: commentId } } } } = e;
    //get the text to be submitted
    const text = document.getElementById(`comment_text_${commentId}`).value;
    //make a fetch request to post the comment to the server. 
    const response = await fetchData(`/api/${commentId}/comment`, 'post', {}, { text });
    //if the comment was saved, reload the page
    if (response.saved)   
        window.location.reload();
};

/**
 * @description: This function is called when the user clicks on the button
 * to start commenting on a post
 * 
 * @param {Event} e 
 */
const handleStart = e => {
    //get the comment id from the events target
    const { target: { attributes: { comment: { value: commentId } } } } = e;
    //hide the target. We don't need it anymore
    e.target.hidden = true;
    //get the relevant comment div container. 
    const commentDiv = document.getElementById(`comment_${commentId}`);
    //make it visible
    commentDiv.hidden = false;
    //attach a click event listener to the submit button
    document.getElementById(`comment_button_${commentId}`).addEventListener('click', handleSubmit);
}

/**
 * @description: This function is called when the page is loaded
 */
const onLoad = () => {
    const startBtns = document.querySelectorAll('[commentStart]');
    for(let i = 0; i < startBtns.length; i++) {
        startBtns[i].addEventListener('click', handleStart);
    }
};

//Attach the event listener to the window on load event
window.addEventListener('load', onLoad);