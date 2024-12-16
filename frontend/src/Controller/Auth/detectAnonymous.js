const detectAnonymous = async () => {
    try {
        const response = await fetch("/api/v1/users/accounts/check-anonymous/", {
            method: "GET",
            credentials: "include",
        });
        const data = await response.json();
        if (data.is_logged_in) return false;
        return true;
    } catch (error) {
        console.error(error);
    }
};

export default detectAnonymous;
