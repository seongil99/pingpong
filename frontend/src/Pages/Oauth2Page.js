class Oauth2Page {
  template() {
    // 컨테이너 div 생성
    const container = document.createElement("div");

    // "Oauth2 Page" 텍스트 추가
    const oauth2Text = document.createElement("h2");
    oauth2Text.textContent = "Oauth2 Page";

    const callCallback = async () => {
      const callBackUri =
        "https://localhost/api/v1/accounts/oauth2/fortytwo/login/finish/";
      const queryParam = new URLSearchParams(window.location.search);
      const code = queryParam.get("code");
      console.log(code);
      try {
        const csrftoken = document.cookie
          .split("; ")
          .find((row) => row.startsWith("csrftoken="))
          .split("=")[1];
      } catch (e) {
        console.log(e);
      }

      const response = await fetch(callBackUri, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ code }),
      });

      const data = await response.json();
      console.log(data);

      if (data.access_token) {
        document.getElementById("h2").textContent = " login success";
      } else {
        document.getElementById("h2").textContent = " login fail";
      }
    };

    const callCallbackButton = document.createElement("button");
    callCallbackButton.textContent = "Call Callback";
    callCallbackButton.onclick = callCallback;

    // DOM에 요소 추가
    container.appendChild(oauth2Text);
    container.appendChild(callCallbackButton);

    return container; // 최종 DOM을 반환
  }
}

export default new Oauth2Page();
