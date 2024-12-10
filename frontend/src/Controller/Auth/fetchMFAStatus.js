const fetchMFAStatus = async () => {
    return await fetch("/api/v1/accounts/mfa/", {
        method: "GET",
        credentials: "include",
    })
        .then((response) => response.json())
        .then((data) => {
            return data.status;
        })
        .catch((error) => console.error("Error fetching MFA status:", error));
}

export default fetchMFAStatus;