const getCookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export const fetchData = async(url='', method='get', headers={}, body={}) => {
    const options = { 
        method, 
        headers: { 
            ...headers,
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json" 
        } 
    };
    if (method.toUpperCase() === 'POST') options.body = JSON.stringify(body);
    try {
        const response = await fetch(url, options);
        console.log(response);
        if (!response.ok) throw new Error(JSON.stringify(response));
        if (response.headers['content-type'].includes('application/json'))
            return await response.json();

        return {};
    } catch(err) {
        throw err;
    }
};