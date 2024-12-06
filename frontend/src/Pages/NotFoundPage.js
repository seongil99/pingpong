import HomeButton from "../Components/HomeButton.js";
import NavBar from "../Components/Navbar.js";

class AboutPage {
    template() {
        // 컨테이너 div 생성
        const container = document.createElement("div");

        const navBar = NavBar();

        // "Not Found Page" 텍스트 추가
        const aboutText = document.createElement("div");
        aboutText.textContent = "Not Found Page";

        // home-button 커스텀 태그 생성 및 추가
        const homeButton = document.createElement("home-button");
        homeButton.classList.add("navigate");
        homeButton.setAttribute("path", "/");

        // DOM에 요소 추가
        container.appendChild(navBar);
        container.appendChild(aboutText);
        container.appendChild(homeButton);

        return container; // 최종 DOM을 반환
    }
}

export default AboutPage;
