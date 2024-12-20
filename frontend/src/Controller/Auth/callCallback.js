const callCallback = async () => {
  try {
    const callBackUri =
      "/api/v1/users/accounts/oauth2/fortytwo/login/callback/";
    const queryParam = new URLSearchParams(window.location.search);
    const code = queryParam.get("code");
    const response = await fetch(callBackUri, {
      method: "POST",
      redirect: "manual",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code }),
    });
    if (!response.ok) {
      return false;
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
};

export default callCallback;
