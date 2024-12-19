async function getCurrentUserGameStatus(params){
		const url = "/api/online-status/";
		try {
			const response = await fetch(url, {
				method: "GET",
				// headers: {
				// 	"Content-Type": "application/json",
				// },
				// credentials: "include"
			});
			if (!response.ok) {
				throw new Error("Not OK! Status Code: ", response.status);
			}
			const json = await response.json();
			console.log('user data json: ', json);
			return json;
		} catch (error) {
			console.error("Error: ", error);
		}
	};
	
	export default getCurrentUserGameStatus;