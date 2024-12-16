async function deleteFriend(params) {
    console.log('delete params: ', params);

    const url = "/api/v1/users/friends/" + params +"/";
    const response = await fetch(url,{
        method : 'DELETE',
        credentials: "include",
    });
    if(!response.ok){
        throw console.error(response.status , 'error response');
    }
}

export default deleteFriend;