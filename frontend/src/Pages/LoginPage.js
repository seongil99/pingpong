import createElement from "../Utils/createElement.js";
import handleEmailLogin from "../Controller/Auth/handleEmailLogin.js";

class LoginPage {
  async template(pathParam, queryParam) {
    // 제목 추가
    const title = createElement("h2", {}, "Login Page");
    const user = ["test1", "test2", "test3", "test4"];

    // 로그인 버튼 생성
    // const loginBtn = createElement(
    //     "button",
    //     {
    //         events: {
    //             click: async () => {
    //                 user.map(async v=>{
    //                     const url = "/api/v1/users/accounts/registration/"; // 로그인 API 서버 URL
    //                     // POST 요청을 통해 서버에 로그인 요청을 보냄
    //                     try {
    //                         const response = await fetch(url, {
    //                             method: "POST",
    //                             headers: {
    //                                 "Content-Type": "application/json",
    //                                 // 'X-CSRFToken': csrfToken,
    //                             },
    //                             credentials: "include",
    //                             body: JSON.stringify({
    //                                 "username": v,
    //                                 "email": `${v}@example.com`,
    //                                 "password1": "wert2345",
    //                                 "password2": "wert2345"
    //                               }),
    //                         });

    //                         if (!response.ok) {
    //                             throw new Error(`Error: ${response.status}`);
    //                         }

    //                         const data = await response.json();
    //                         // updateNavBarLogin();
    //                         console.dir(response);
    //                         console.dir(data);
    //                     } catch (error) {
    //                         console.error("Login failed:", error);
    //                         alert("Login failed!");
    //                     }
    //                 })
    //             }
    //         },
    //     },
    //     "create Users"
    // );

    const fortytwoLoginBtn = createElement(
      "button",
      {
        events: {
          click: async () => {
            const host = "10.11.8.5";
            const clientId =
              "u-s4t2ud-80c35252b5c6defa03f294f295f7bc83623a37a929b5ade66bed0dbafce4f667";
            const redirectUri =
              `https%3A%2F%2F${host}%2Foauth2%2Fredirect`;
            window.location.href = `https://api.intra.42.fr/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code`;
          },
        },
      },
      "42 Login"
    );

    const container = createElement(
      "div",
      { class: "login-container" },
      title,
      fortytwoLoginBtn
    );

    user.map((v) => {
      container.append(
        createElement(
          "button",
          {
            events: {
              click: () => {
                handleEmailLogin(v);
              },
            },
          },
          v
        )
      );
    });
    return container; // 최종 DOM 반환
  }
}

export default LoginPage;
