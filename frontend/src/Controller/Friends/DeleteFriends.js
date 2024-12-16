export async function deleteFriend(params) {
    const url = "/api/v1/users/friends/" + params +"/";
    const response = await fetch(url,{
        method : 'DELETE',
        credentials: "include",
    });
    if(response.status >= 300 && response.status <= 199){
        throw console.error(response.status , 'error response');
    }
}

export default deleteFriend;