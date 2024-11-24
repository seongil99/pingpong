import NavBar from "../Components/Navbar.js";

class HomePage {
    template() {
        // 컨테이너 div 생성
        const container = document.createElement("div");

        const navBar = NavBar();

        // 컨테이너에 요소들 추가
        container.appendChild(navBar);
        container.appendChild(title);

        return container; // 컨테이너를 반환
    }
}

export default new HomePage();

// const getHello = async () => {
//     const url = "https://localhost/api/v1/accounts/hello/";
//     try {
//         const response = await fetch(url, {
//             method: "GET",
//             credentials: "include", // 쿠키 전송 허용
//         });
//         return response;
//     } catch (error) {
//         console.error("Error:", error);
//     }
// };

// const displayHello = async () => {
//     const response = await getHello();
//     if (response.ok) {
//         const hello = await response.json();
//         document.getElementById("h2").textContent =
//             hello.message + " login success";
//     } else {
//         document.getElementById("h2").textContent = "does not login";
//     }
// };

// const setHelloButton = document.createElement("button");
// setHelloButton.textContent = "is login?";
// setHelloButton.onclick = displayHello;
