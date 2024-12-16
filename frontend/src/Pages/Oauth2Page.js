class Oauth2Page {
  async template() {
    // 컨테이너 div 생성
    const container = document.createElement("div");

    // "Oauth2 Page" 텍스트 추가
    const oauth2Text = document.createElement("h2");
    oauth2Text.textContent = "Oauth2 Page";

    const callCallback = async () => {
      const callBackUri =
        "/api/v1/users/accounts/oauth2/fortytwo/login/callback/";
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
        redirect: "manual",
        headers: {
          "Content-Type": "application/json",
          // "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ code }),
      });

      const data = await response.json();
      console.log(data);
      console.log(data.status);
      console.log(response.status);
      if (response.ok) {
        window.router.navigate("/");
      } else if (data.status === "redirect") {
        window.router.navigate(data.url);
      } else {
        alert("Failed to login");
        window.router.navigate("/login");
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

export default Oauth2Page;
