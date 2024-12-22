async function isEnded(params) {
	const url = `/api/v1/pingpong-history/${Number(params)}/is-ended/`;
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
			return true;
		}
		const json = await response.json();
		console.log(" is ended!!",json);
		return json.is_ended;
	} catch (error) {
		console.error("Error: ", error);
	}
};

export default isEnded;
