export const fetchPagePart = async (url='', method='get', headers={}, body={}) => {
    const options = { method, headers };
    if (method.toUpperCase() === 'POST' && (typeof body === 'object' || Array.isArray(body))) 
        options.body = JSON.stringify(body);
    try {
        const req = await fetch(url, options);
        return await req.text();
    } catch (err) {
        return `
            <div class="alert alert-warning">
                <b>The request to ${url} returned with an error that cause the page to fail loading<b>
                <br />
                ${err}
            </div>
        `
    }
};