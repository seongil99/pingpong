import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import FriendList from "../Components/FriendList.js";
import FriendModal from "../Components/FriendModal.js";

class HomePage {
    template() {
        const friendToggleBtn = createElement(
            "button",
            {
                events: {
                    click: () => {
                        const friends = document.querySelector("#friends");
                        const match = document.querySelector(".match-div");
                        friends.classList.toggle("hide");
                        match.classList.toggle("hide");
                        friendToggleBtn.textContent =
                            !friends.classList.contains("hide")
                                ? "X"
                                : "친구목록";
                    },
                },
            },
            "친구목록"
        );
        // 친구 목록 버튼 Div 안에 친구 목록 화면 활성화 버튼 추가
        const friendToggle = createElement(
            "div",
            { id: "friend-toggle" },
            friendToggleBtn
        );
        const friendList = FriendList();
        // 게임시작 Div에 게임시작 버튼 추가
        const matchingButton = createElement(
            "button",
            { class: "match-btn navigate", path: "/matching" },
            "Go to Matching Page"
        );
        const matching = createElement(
            "div",
            { class: "match-div" },
            matchingButton
        );
        // main 요소에 친구 목록 버튼 상자, 친구 목록 화면, 게임 시작 버튼 추가
        const main = createElement(
            "main",
            { id: "home-main" },
            friendToggle,
            friendList,
            matching
        );
        // 컨테이너에 모달, 네비게이션 바, main 요소 추가
        const modal = FriendModal();
        const navBar = NavBar();
        const container = createElement("div", {}, modal, navBar, main);
        return container; // 컨테이너를 반환
    }
}

export default HomePage;

// async template() {
//   // 컨테이너 div 생성
//   const container = document.createElement("div");

//   const title = document.createElement("h2");
//   title.id = "h2";
//   title.textContent = "Home Page";

//   const navBar = document.createElement("div");
//   navBar.innerHTML = NavBar;

//   // "Go to About Page" 버튼 생성
//   const aboutButton = document.createElement("button");
//   aboutButton.classList.add("navigate"); // 클래스 추가
//   aboutButton.setAttribute("path", "/about"); // 경로 설정
//   aboutButton.textContent = "Go to About Page"; // 버튼 텍스트

//   // Go to login page button
//   const loginButton = document.createElement("button");
//   loginButton.classList.add("navigate");
//   loginButton.setAttribute("path", "/login");
//   loginButton.textContent = "Go to Login Page";

//   const getHello = async () => {
//     const url = "/api/v1/users/accounts/verify/";
//     try {
//       const response = await fetch(url, {
//         method: "GET",
//         credentials: "include", // 쿠키 전송 허용
//       });
//       return response;
//     } catch (error) {
//       console.error("Error:", error);
//     }
//   };

//   const displayHello = async () => {
//     const response = await getHello();
//     if (response.ok) {
//       const hello = await response.json();
//       document.getElementById("h2").textContent =
//         "login success";
//     } else {
//       document.getElementById("h2").textContent = "does not login";
//     }
//   };

//   const setHelloButton = document.createElement("button");
//   setHelloButton.textContent = "is login?";
//   setHelloButton.onclick = displayHello;

//   const logout = async () => {
//     const url = "https://localhost/api/v1/users/accounts/logout/";
//     const csrftoken = document.cookie
//       .split("; ")
//       .find((row) => row.startsWith("csrftoken="))
//       .split("=")[1];
//     try {
//       const response = await fetch(url, {
//         method: "POST",
//         credentials: "include", // 쿠키 전송 허용
//         "X-CSRFToken": csrftoken, // CSRF 토큰을 헤더에 포함
//       });
//       return response;
//     } catch (error) {
//       console.error("Error:", error);
//     }
//   };

//   const logoutButton = document.createElement("button");
//   logoutButton.textContent = "Logout";
//   logoutButton.onclick = async () => {
//     const response = await logout();
//     if (response.ok) {
//       document.getElementById("h2").textContent = " logout success";
//     } else {
//       document.getElementById("h2").textContent = " logout fail";
//     }
//   };

//   const matchingButton = document.createElement("button");
//   matchingButton.classList.add("navigate");
//   matchingButton.setAttribute("path", "/matching");
//   matchingButton.textContent = "Go to Matching Page";

//   // 컨테이너에 요소들 추가
//   container.appendChild(navBar);
//   container.appendChild(title);
//   container.appendChild(aboutButton);
//   container.appendChild(loginButton);
//   container.appendChild(setHelloButton);
//   container.appendChild(logoutButton);
//   container.appendChild(matchingButton);

//   return container; // 컨테이너를 반환
// }
// }
