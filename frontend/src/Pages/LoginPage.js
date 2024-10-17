import LoginButton from "../Components/LoginButton.js";

class LoginPage {
  template() {
    // 컨테이너 div 생성
    const container = document.createElement("div");
    container.classList.add("login-container");

    // 제목 추가
    const title = document.createElement("h2");
    title.textContent = "Login Page";

    // 사용자 이름 입력 필드
    const usernameLabel = document.createElement("label");
    usernameLabel.textContent = "Username:";
    const usernameInput = document.createElement("input");
    usernameInput.setAttribute("type", "text");
    usernameInput.setAttribute("placeholder", "Enter your username");
    usernameInput.classList.add("login-input");

    // 비밀번호 입력 필드
    const passwordLabel = document.createElement("label");
    passwordLabel.textContent = "Password:";
    const passwordInput = document.createElement("input");
    passwordInput.setAttribute("type", "password");
    passwordInput.setAttribute("placeholder", "Enter your password");
    passwordInput.classList.add("login-input");

    // 로그인 버튼 생성
    const loginButton = document.createElement("login-button");

    // DOM에 요소 추가
    container.appendChild(title);
    container.appendChild(usernameLabel);
    container.appendChild(usernameInput);
    container.appendChild(passwordLabel);
    container.appendChild(passwordInput);
    container.appendChild(loginButton);

    return container; // 최종 DOM 반환
  }
}

export default new LoginPage();
