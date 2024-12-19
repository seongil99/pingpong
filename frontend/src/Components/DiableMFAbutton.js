class DisableMFAbutton extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  connectedCallback() {
    this.template();
    this.shadowRoot
      .querySelector("button")
      .addEventListener("click", this.handleDisableMFA);
  }
  connectedCallback() {
    this.template();
    this.shadowRoot
      .querySelector("button")
      .addEventListener("click", this.handleDisableMFA);
  }

  template() {
    this.shadowRoot.innerHTML = `
  template() {
    this.shadowRoot.innerHTML = `
      <style>
        button {
          padding: 10px;
          background-color: #007bff;
          color: white;
          border: none;
          cursor: pointer;
        }
        button:hover {
          background-color: #0056b3;
        }
      </style>
      <button>Disable MFA</button>
    `;
  }
  }

  async handleDisableMFA() {
    const url = "https://localhost/api/v1/users/accounts/mfa/"; // MFA 비활성화 API 서버 URL
  async handleDisableMFA() {
    const url = "https://localhost/api/v1/users/accounts/mfa/"; // MFA 비활성화 API 서버 URL

    try {
      const response = await fetch(url, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
    try {
      const response = await fetch(url, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      console.log("MFA disabled:", data);
      alert("MFA disabled!");
    } catch (error) {
      console.error("MFA disable failed:", error);
      alert("MFA disable failed!");
    }
  }
}

customElements.define("disable-mfa-button", DisableMFAbutton);
export default DisableMFAbutton;

