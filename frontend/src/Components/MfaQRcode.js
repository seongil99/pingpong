// export const qrcodeImage = `<img src="https://localhost/api/v1/accounts/2fa_qr" alt="2fa QR code">`;

import fetchQRcode from "../Controller/Auth/fetchQRCode.js";

const mfaQRCode = () => {
    const qrcode = createElement(
        "img",
        {
            src: "",
            alt: "QR Code",
            id: "mfa-qrcode",
            style: { width: "150px", height: "150px" },
        },
        []
    );
    fetchQRcode;
    return qrcode;
};

export default mfaQRCode;
