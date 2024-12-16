const updateUserProfile = async (infos) => {
    try {
        const response = await fetch("/api/v1/users/me/", {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(infos),
        });
        if (!response.ok) throw new Error("Network response was not ok");
        const userData = await response.json();
        return userData;
    } catch (error) {
        console.error("Error fetching user profile:", error);
    }
};

export default updateUserProfile;
