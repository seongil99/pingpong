const fetchQRcode = () => {
    // URL to your QR code API endpoint
    const apiUrl = "/api/v1/accounts/mfa/qrcode/";

    fetch(apiUrl, {
        method: "GET",
        credentials: "include", // Include cookies if needed
    })
        .then((response) => response.json())
        .then((data) => {
            document.querySelector("#mfa-qrcode").src = data.qrcode;
        })
        .catch((error) => console.error("Error fetching QR code:", error));
};

export default fetchQRcode;
