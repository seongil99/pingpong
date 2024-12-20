async function PvpRequest(option) {
	const url = "/api/v1/matchmaking/pve/";
	try {
		const response = await fetch(url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				body: JSON.stringify({
					"multi_ball": option,
				}),
			},
			credentials: "include"
		});
		if (response.status !== 201) {
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

export default PvpRequest;