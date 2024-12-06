import NavBar from "../Components/Navbar.js";

class HomePage {
    template() {
        // 컨테이너 div 생성
        const container = document.createElement("div");

        const navBar = NavBar();

    // 컨테이너에 요소들 추가
    container.appendChild(navBar);
    container.appendChild(title);
    container.appendChild(aboutButton);
    container.appendChild(loginButton);
    container.appendChild(setHelloButton);
    container.appendChild(logoutButton);
    container.appendChild(matchingButton);

        return container; // 컨테이너를 반환
    }
}

export default HomePage;


// const getHello = async () => {
//   const url = "https://localhost/api/v1/users/accounts/hello/";
//   try {
//     const response = await fetch(url, {
//       method: "GET",
//       credentials: "include", // 쿠키 전송 허용
//     });
//     return response;
//   } catch (error) {
//     console.error("Error:", error);
//   }
// };

// const displayHello = async () => {
//   const response = await getHello();
//   if (response.ok) {
//     const hello = await response.json();
//     document.getElementById("h2").textContent =
//       hello.message + " login success";
//   } else {
//     document.getElementById("h2").textContent = "does not login";
//   }
// };

// const setHelloButton = document.createElement("button");
// setHelloButton.textContent = "is login?";
// setHelloButton.onclick = displayHello;

// const logout = async () => {
//   const url = "https://localhost/api/v1/users/accounts/logout/";
//   const csrftoken = document.cookie
//     .split("; ")
//     .find((row) => row.startsWith("csrftoken="))
//     .split("=")[1];
//   try {
//     const response = await fetch(url, {
//       method: "POST",
//       credentials: "include", // 쿠키 전송 허용
//       "X-CSRFToken": csrftoken, // CSRF 토큰을 헤더에 포함
//     });
//     return response;
//   } catch (error) {
//     console.error("Error:", error);
//   }
// };

// const logoutButton = document.createElement("button");
// logoutButton.textContent = "Logout";
// logoutButton.onclick = async () => {
//   const response = await logout();
//   if (response.ok) {
//     document.getElementById("h2").textContent = " logout success";
//   } else {
//     document.getElementById("h2").textContent = " logout fail";
//   }
// };

// const matchingButton = document.createElement("button");
// matchingButton.classList.add("navigate");
// matchingButton.setAttribute("path", "/matching");
// matchingButton.textContent = "Go to Matching Page";