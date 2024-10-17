import HomeButton from "../Components/HomeButton.js";

class AboutPage {
  template() {
    // 컨테이너 div 생성
    const container = document.createElement("div");

    // "About Page" 텍스트 추가
    const aboutText = document.createElement("div");
    aboutText.textContent = "About Page";

    // home-button 커스텀 태그 생성 및 추가
    const homeButton = document.createElement("home-button");
    homeButton.classList.add("navigate");
    homeButton.setAttribute("path", "/");

    // DOM에 요소 추가
    container.appendChild(aboutText);
    container.appendChild(homeButton);

    return container; // 최종 DOM을 반환
  }
}

export default new AboutPage();
