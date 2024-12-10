const fetchFriends = async () => {
    const url = "https://localhost/api/v1/users/friends";
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
        return await response.json().results;
    } catch (error) {
        console.error("Error: ", error);
    }
};

export default fetchFriends;