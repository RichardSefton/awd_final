import { fetchData } from '/static/scripts/fetchSvc.js';

const handleSubmit = async e => {
    const { target: { attributes: { comment: { value: commentId } } } } = e;
    const text = document.getElementById(`comment_text_${commentId}`).value;
    const response = await fetchData(`/api/${commentId}/comment`, 'post', {}, { text });
    console.log(response);
    if (response.saved)   
        window.location.reload();
};

const handleStart = e => {
    const { target: { attributes: { comment: { value: commentId } } } } = e;
    e.target.hidden = true;
    const commentDiv = document.getElementById(`comment_${commentId}`);
    commentDiv.hidden = false;
    const submitComment = document.getElementById(`comment_button_${commentId}`);
    submitComment.addEventListener('click', handleSubmit);
}

const onLoad = () => {
    const startBtns = document.querySelectorAll('[commentStart]');
    for(let i = 0; i < startBtns.length; i++) {
        startBtns[i].addEventListener('click', handleStart);
    }
};

window.addEventListener('load', onLoad);