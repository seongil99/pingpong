const FetchMatchData = async (matchId) => {
	try {
		const response = await fetch(`/api/v1/pingpong-history/${matchId}/detail/`, {
			method: "GET",
			credentials: "include"
		})
		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		const data = await response.json();
		return data;
	} catch(error) {
		console.error(error);
	}
}

export default FetchMatchData;