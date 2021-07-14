/**
 * Makes an async fetch request.
 * @param  {String} url  The url by which the request is made
 * @param  {String} method  Request method, is 'GET' by default
 * @param  {Object} data  Request data, is empty object by default
 **/

const getData = (url, method = 'GET', data = {}) => {
    let output;
    const request = async (url, method, data) => {
        try {
            const response = await fetch(url, {
                method: method,
                data: data,
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            return await response.json();
        } catch (e) {
            console.log(e);
        }
    }
    request(url, method, data).then(res => output = res);
    return output
}


export {getData}