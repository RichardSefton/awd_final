/**
 * @description: This function is used to get a cookie from the browser
 * document that matches the name passed in.
 * 
 * @param {String} name 
 * @returns {String} cookieValue
 */
const getCookie = (name='') => {
    //initialize the cookie value to null
    var cookieValue = null;
    //if the document.cookie is not null and the document.cookie is not an empty string
    if (document.cookie && document.cookie !== '') {
        //split the document.cookie by the semi-colon delimiter to get an array of cookies
        var cookies = document.cookie.split(';');
        //loop through the cookies array
        for (var i = 0; i < cookies.length; i++) {
            //trim the cookie
            var cookie = cookies[i].trim();
            //if the cookie starts with the name passed in, set the cookieValue to the cookie
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                //no need to go any further. Too many cookies will make you fat. 
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * @description: This function is used to fetch data from the server. Each request
 * has the X-CSRFToken header set to the csrftoken cookie value. If the request
 * method is POST, the body is stringified and the Content-Type header is set to
 * application/json.
 * 
 * If the response is json, the response is returned as json. Otherwise, an empty
 * object is returned.
 * 
 * @param {String} url 
 * @param {String} method 
 * @param {Object} headers 
 * @param {Object} body 
 * @returns {Object}
 */
export const fetchData = async(url='', method='get', headers={}, body={}) => {
    //set the fetch options. For the headers we will spread the headers passed in
    //And attach the appropriate headers for the request overwriting any headers
    //that were passed in with the same name.
    const options = { 
        method, 
        headers: { 
            ...headers,
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json" 
        } 
    };
    //If the method is a post request, attach the body. 
    if (method.toUpperCase() === 'POST') options.body = JSON.stringify(body);
    try {
        //make the request
        const response = await fetch(url, options);
        //if the response is not ok, throw an error
        if (!response.ok) throw new Error(JSON.stringify(response));
        //get the content type from the response headers
        const contentType = response.headers.get('content-type');
        //if the content type is application/json, return the response as json
        if (contentType === 'application/json')
            return await response.json();
        //otherwise, return an empty object
        return {};
    } catch(err) {
        //if there is an error, throw the error
        throw err;
    }
};