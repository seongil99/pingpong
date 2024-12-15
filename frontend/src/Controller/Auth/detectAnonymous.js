const detectAnonymous = async () => {
    try {
        const response = await fetch("/api/v1/users/accounts/check-anonymous/", {
            method: "GET",
            credentials: "include",
        });
        if (!response.ok) {
            throw Error("No Anonymous");
        }
        return true;
    } catch (error) {
        console.error(error);
    }
};

export default detectAnonymous;
