const fetchQRcode = async () => {
    // URL to your QR code API endpoint
    try {
        const response = await fetch("/api/v1/users/accounts/mfa/qrcode/", {
            method: "GET",
            credentials: "include", // Include cookies if needed
        })
        if (!response.ok) {
            throw Error("No Data");
        }
        const data = response.json();
        return (data);
    } catch (error) {
        console.error("Error fetching QR Code: ", error);
    }
};

export default fetchQRcode;
