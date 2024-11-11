import LoginButton from "../Components/LoginButton.js";
import NavBar from "../Components/Navbar.js";

class LoginPage {
  template() {
    // 컨테이너 div 생성
    const container = document.createElement("div");
    container.classList.add("login-container");

    const navBar = document.createElement("div");
    navBar.innerHTML = NavBar;

    // 제목 추가
    const title = document.createElement("h2");
    title.textContent = "Login Page";

    // 사용자 이름 입력 필드
    // const usernameLabel = document.createElement("label");
    // usernameLabel.textContent = "Username:";
    // const usernameInput = document.createElement("input");
    // usernameInput.setAttribute("type", "text");
    // usernameInput.setAttribute("placeholder", "Enter your username");
    // usernameInput.classList.add("login-input");

    // 비밀번호 입력 필드
    // const passwordLabel = document.createElement("label");
    // passwordLabel.textContent = "Password:";
    // const passwordInput = document.createElement("input");
    // passwordInput.setAttribute("type", "password");
    // passwordInput.setAttribute("placeholder", "Enter your password");
    // passwordInput.classList.add("login-input");

    // 로그인 버튼 생성
    const loginButton = document.createElement("login-button");

    const fortytwoLoginButton = document.createElement("button");
    fortytwoLoginButton.textContent = "42 Login";
    const fortytwoLogin = async () => {
      const clientId =
        "u-s4t2ud-f3c794a53848db3b102519cb5cd7123e14dae487ccdb02741f5ef3b8781504ef";
      const redirectUri = "https%3A%2F%2Flocalhost%2Foauth2%2Fredirect";

      window.location.href = `https://api.intra.42.fr/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code`;
    };
    fortytwoLoginButton.onclick = fortytwoLogin;

    // DOM에 요소 추가
    container.appendChild(navBar);
    container.appendChild(title);
    // container.appendChild(usernameLabel);
    // container.appendChild(usernameInput);
    // container.appendChild(passwordLabel);
    // container.appendChild(passwordInput);
    container.appendChild(loginButton);
    container.appendChild(fortytwoLoginButton);

    return container; // 최종 DOM 반환
  }
}

export default new LoginPage();
