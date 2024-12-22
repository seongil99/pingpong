import createElement from "../Utils/createElement.js";
import handleEmailLogin from "../Controller/Auth/handleEmailLogin.js";

class LoginPage {
  async template(pathParam, queryParam) {
    // 제목 추가
    const title = createElement("h2", {}, "Login Page");
    const user = ["test1", "test2", "test3", "test4"];

    const fortytwoLoginBtn = createElement(
      "button",
      {
        events: {
          click: async () => {
            const host = "localhost";
            const clientId =
              "u-s4t2ud-80c35252b5c6defa03f294f295f7bc83623a37a929b5ade66bed0dbafce4f667";
            const redirectUri = `https%3A%2F%2F${host}%2Foauth2%2Fredirect`;
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
