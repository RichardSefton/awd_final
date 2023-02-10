export const fetchData = async(url='', method='get', headers={}, body={}) => {
    const options = { method, headers: { ...headers, 'Content-Type': 'application/json' } };
    if (method.toUpperCase === 'POST') options.body = JSON.stringify(body);

    const response = await fetch(url, options);
    if (!response.ok) throw new Error(JSON.stringify(response));
    return await response.json();
};