async function getTournamentData(type, params) {
	const url = `/api/v1/pingpong-history/event/${type}/${params}/`;
	try {
		const response = await fetch(url, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
		});
		if (!response.ok) {
			throw new Error("Not OK! Status Code: ", response.status);
		}
		const json = await response.json();
		console.log('json: ', json);

		return json;
	} catch (error) {
		console.error("Error: ", error);
	}
};

export default getTournamentData;