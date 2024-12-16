async function searchFriends(params) {
    const url = "/api/v1/users/friendable/?search=" + params;
    const response = await (await fetch(url,{
        method : 'GET',
        headers :{
            "Content-Type": "application/json",
        }
    })).json();
    return response.results.length > 0 ? response.results[0]: null;
}

export default searchFriends;