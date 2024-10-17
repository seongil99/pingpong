class HomeButton extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  connectedCallback() {
    this.template();
  }

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
      <button>Go to Home Page</button>
    `;
  }
}

customElements.define("home-button", HomeButton);
export default HomeButton;
