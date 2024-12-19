async function getTournamentData(params){
		const url = "https://localhost/api/v1/tournament/" + parseInt(params)+ "/event/";
		// const url = "/api/v1/tournament/testcreate/";
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