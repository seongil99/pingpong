async function searchFriends(params) {
    const url = "/api/v1/users/friendable/?search=" + params;
    const response = await (await fetch(url,{
        method : 'GET',
        headers :{
            "Content-Type": "application/json",
        }
    })).json();
    response.results.map(v=>{
        v.avatar = v.avatar.replace("http://", "https://");
    })
    console.log('response: ', response);
    return response.results;
}

export default searchFriends;