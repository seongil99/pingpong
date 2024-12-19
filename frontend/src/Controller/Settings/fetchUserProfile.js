const fetchUserProfile = async () => {
    try {
        const response = await fetch("/api/v1/users/me/", {
            method: "GET",
            credentials: "include",
        });
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
        data.avatar = data.avatar.replace("http://", "https://");
        return data;
    } catch (error) {
        console.error("Error fetching user profile:", error);
    }
};

export default fetchUserProfile;
