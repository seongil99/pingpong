const FetchOneUserGameHistory = async (id) => {
	try {
		const response = await fetch(`/api/v1/pingpong-history/user/${id}`, {
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

export default FetchOneUserGameHistory;