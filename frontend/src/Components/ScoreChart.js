import createElement from "../Utils/createElement.js";

const ScoreChart = (session, sessionIdx) => {
	const chart = createElement("div", {id: `chart-container${sessionIdx}`}, []);
	const chartRapper = createElement("div", {class: "chart-wrapper"}, chart);
	return chartRapper;
}

export default ScoreChart;