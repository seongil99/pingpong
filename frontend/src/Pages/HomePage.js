import NavBar from "../Components/Navbar.js";

class HomePage {
  template() {
    // 컨테이너 div 생성
    const container = document.createElement("div");

    const title = document.createElement("h2");
    title.id = "h2";
    title.textContent = "Home Page";

    const navBar = document.createElement("div");
    navBar.innerHTML = NavBar;

    // "Go to About Page" 버튼 생성
    const aboutButton = document.createElement("button");
    aboutButton.classList.add("navigate"); // 클래스 추가
    aboutButton.setAttribute("path", "/about"); // 경로 설정
    aboutButton.textContent = "Go to About Page"; // 버튼 텍스트

    // Go to login page button
    const loginButton = document.createElement("button");
    loginButton.classList.add("navigate");
    loginButton.setAttribute("path", "/login");
    loginButton.textContent = "Go to Login Page";

    const getHello = async () => {
      const url = "https://localhost/api/v1/accounts/hello/";
      try {
        const response = await fetch(url, {
          method: "GET",
          credentials: "include", // 쿠키 전송 허용
        });
        const data = await response.json();
        return data;
      } catch (error) {
        console.error("Error:", error);
      }
    };

    const displayHello = async () => {
      const hello = await getHello();
      if (hello) {
        document.getElementById("h2").textContent =
          hello.message + " login success";
      } else {
        document.getElementById("h2").textContent = " login fail";
      }
    };

    const setHelloButton = document.createElement("button");
    setHelloButton.textContent = "Set Hello";
    setHelloButton.onclick = displayHello;

    const logout = async () => {
      const url = "https://localhost/api/v1/accounts/logout/";
      const csrftoken = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        .split("=")[1];
      try {
        const response = await fetch(url, {
          method: "POST",
          credentials: "include", // 쿠키 전송 허용
          "X-CSRFToken": csrftoken, // CSRF 토큰을 헤더에 포함
        });
        const data = await response.json();
        return data;
      } catch (error) {
        console.error("Error:", error);
      }
    };

    const logoutButton = document.createElement("button");
    logoutButton.textContent = "Logout";
    logoutButton.onclick = async () => {
      const logoutData = await logout();
      if (logoutData) {
        document.getElementById("h2").textContent = " logout success";
      } else {
        document.getElementById("h2").textContent = " logout fail";
      }
    };

    // 컨테이너에 요소들 추가
    container.appendChild(navBar);
    container.appendChild(title);
    container.appendChild(aboutButton);
    container.appendChild(loginButton);
    container.appendChild(setHelloButton);
    container.appendChild(logoutButton);

    return container; // 컨테이너를 반환
  }
}

export default new HomePage();
