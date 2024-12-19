import createElement from "../Utils/createElement.js";
import fetchQRcode from "../Controller/Auth/fetchQRCode.js";

const MfaQRcode = async () => {
    const qrcodeImg = await fetchQRcode();
    const qrcode = createElement(
        "img",
        {
            src: qrcodeImg.qrcode,
            alt: "2FA QR Code",
            class: "authenticator-guide-step-img",
            id: "mfa-qrcode",
        },
        []
    );
    return qrcode;
};

export default MfaQRcode;
