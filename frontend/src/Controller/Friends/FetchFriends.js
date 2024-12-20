const fetchFriends = async () => {
    const url = "/api/v1/users/friends";
    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });
        if (!response.ok) {
            throw new Error("Not OK! Status Code: ", response.status);
        }
        const json = await response.json();
        json.results.map(v => {
            v.friend_user.avatar = String(v.friend_user.avatar).replace("http://", "https://");
        });
        return json.results;
    } catch (error) {
        console.error("Error: ", error);
    }
};

export default fetchFriends;
