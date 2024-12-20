import changeTimeToDate from "./changeTimeToDate.js";

const calculateDiffDate = (date1, date2) => {
	const d1 = new Date(date1);
	const d2 = new Date(date2);

	const diffMilliseconds = Math.abs(d2 - d1);

	return changeTimeToDate(diffMilliseconds);
}

export default calculateDiffDate;