const fetchUserProfile = async () => {
    try {
        const response = await fetch("/api/v1/users/me/", {
            method: "GET",
            credentials: "include",
        });
        if (!response.ok) throw new Error("Network response was not ok");

        const userData = await response.json(); // Assuming it returns { username: '...', email: '...' }
        // Populate the profile info

        userData.avatar = String(userData.avatar).replace("http://", "https://");

        return userData;
    } catch (error) {
        console.error("Error fetching user profile:", error);
    }
};

export default fetchUserProfile;
