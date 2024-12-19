const FetchUserData = async (userid) => {
    try {
        const response = await fetch(`/api/v1/users/${userid}`, {
            method: "GET",
            credentials: "include",
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        data.avatar = data.avatar.replace("http://", "https://");
        return data;
    } catch (error) {
        console.error(error);
    }
};

export default FetchUserData;
