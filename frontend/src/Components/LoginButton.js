class LoginButton extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  connectedCallback() {
    this.template();
    this.shadowRoot
      .querySelector("button")
      .addEventListener("click", () => this.handleLogin());
  }

  async handleLogin() {
    const url = "https://api.example.com/login"; // 로그인 API 서버 URL
    const username = this.getAttribute("username"); // 속성으로 전달받은 사용자 이름
    const password = this.getAttribute("password"); // 속성으로 전달받은 비밀번호

    // POST 요청을 통해 서버에 로그인 요청을 보냄
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      console.log("Login successful:", data);
      alert("Login successful!");
    } catch (error) {
      console.error("Login failed:", error);
      alert("Login failed!");
    }
  }

  template() {
    this.shadowRoot.innerHTML = `
      <style>
        button {
          padding: 10px 20px;
          background-color: #28a745;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 16px;
        }
        button:hover {
          background-color: #218838;
        }
        button:active {
          background-color: #1e7e34;
        }
      </style>
      <button>Login</button>
    `;
  }
}

customElements.define("login-button", LoginButton);
export default LoginButton;
