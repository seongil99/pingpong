// export const qrcodeImage = `<img src="https://localhost/api/v1/accounts/2fa_qr" alt="2fa QR code">`;
class mfaQRcode extends HTMLElement {
	constructor() {
		super();
		this.attachShadow({ mode: "open" })
		this.fetchQRcode();
	}

	connectedCallback() {
		this.template();
	}

	fetchQRcode() {
		// URL to your QR code API endpoint
		const apiUrl = "/api/v1/accounts/mfa/qrcode/";

		fetch(apiUrl, {
			method: "GET",
			credentials: "include"  // Include cookies if needed
		})
			.then(response => response.json())
			.then(data => {
				const imageData = data.qrcode;
				const img = this.shadowRoot.querySelector("img");
				img.src = imageData;
			})
			.catch(error => console.error("Error fetching QR code:", error));
	}

	template() {
		this.shadowRoot.innerHTML = `
      <style>
        img {
          width: 150px;  /* Set desired dimensions */
          height: 150px;
        }
      </style>
      <img alt="QR Code">
    `;
	}
}

customElements.define("mfa-qr-display", mfaQRcode);
export default mfaQRcode;
// export default mfaQRcode;