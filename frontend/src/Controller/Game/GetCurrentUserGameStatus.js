async function getCurrentUserGameStatus() {
	const url = "/api/v1/users/me/current-game/";
	try {
		const response = await fetch(url, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include"
		});
		console.log(response)
		if (response.status !== 200) {
			if(response.status === 204) return null
			throw new Error("Not OK! Status Code: ", response.status);
		}
		console.log('response: ', response);
		const json = await response.json();
		console.log('user data json: ', json);
		return json;
	} catch (error) {
		console.error("Error: ", error);
	}
};

export default getCurrentUserGameStatus;
