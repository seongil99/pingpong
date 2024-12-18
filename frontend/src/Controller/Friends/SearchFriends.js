async function searchFriends(params) {
    const url = "/api/v1/users/friendable/?search=" + params;
    const response = await (await fetch(url,{
        method : 'GET',
        headers :{
            "Content-Type": "application/json",
        }
    })).json();
    return response.results;
}

export default searchFriends;