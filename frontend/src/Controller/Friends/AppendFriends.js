async function AppendFriends(params) {
    const url = "/api/v1/users/friends/";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({
                friend_user: parseInt(params),
            }),
        });
        if (!response.ok) {
            throw new Error("Not OK! Status Code: ", response.status);
        }
        return await response.json();
    } catch (error) {
        console.error("Error: ", error);
        return false;
    }
}

export default AppendFriends;
