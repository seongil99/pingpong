export async function friendapi(type,api,params="") {
    const url = api + (params ? params + "/" : "");
    const response = await fetch(url,{
        method : type,
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
        }
    });
    if(!response.ok)
        throw console.error(response.status , 'error response');
    if(type === 'GET'){
        const ret = await response.json();
        return ret.results;
    }
}

export default friendapi;