class HomePage {
  template() {
    // 컨테이너 div 생성
    const container = document.createElement("div");

    // "Home Page" 텍스트가 담긴 div 생성
    const homeText = document.createElement("div");
    homeText.textContent = "Home Page";

    // "Go to About Page" 버튼 생성
    const aboutButton = document.createElement("button");
    aboutButton.classList.add("navigate"); // 클래스 추가
    aboutButton.setAttribute("path", "/about"); // 경로 설정
    aboutButton.textContent = "Go to About Page"; // 버튼 텍스트

    // "Go to Not Found Page" 버튼 생성
    const notFoundButton = document.createElement("button");
    notFoundButton.classList.add("navigate"); // 클래스 추가
    notFoundButton.setAttribute("path", "/404"); // 경로 설정
    notFoundButton.textContent = "Go to Not Found Page"; // 버튼 텍스트

    // Go to login page button
    const loginButton = document.createElement("button");
    loginButton.classList.add("navigate");
    loginButton.setAttribute("path", "/login");
    loginButton.textContent = "Go to Login Page";

    // 컨테이너에 요소들 추가
    container.appendChild(homeText);
    container.appendChild(aboutButton);
    container.appendChild(notFoundButton);
    container.appendChild(loginButton);

    return container; // 컨테이너를 반환
  }
}

export default new HomePage();
