import createElement from "../Utils/createElement.js";

const ScoreChart = async (session, sessionIdx) => {
    const chart = createElement(
        "div",
        { id: `chart-container${sessionIdx}` },
        []
    );
	const user1Data = await FetchUserData(session.user1);
	const user2Data = await FetchUserData(session.user2);
	const matchData = await 
    // D3.js로 차트 생성
    const margin = { top: 40, right: 120, bottom: 30, left: 100 };
    const width = 600 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    const svg = d3
        .select(chart)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // 데이터
    const labels = [];
    const datasets = [
        {
            label: `${user1Data.username}`,
            data: [0, 0, 1, 2, 3],
            color: "rgba(255, 99, 132, 0.5)",
        },
        {
            label: `${user2Data.username}`,
            data: [1, 2, 2, 2, 2],
            color: "rgba(54, 162, 235, 0.5)",
        },
    ];
	session.user1_score session.user2_score

    // X축 및 Y축 스케일
    const xScale = d3
        .scaleLinear()
        .domain([0, d3.max(datasets.flatMap((d) => d.data))])
        .range([0, width]);

    const yScale = d3
        .scaleBand()
        .domain(labels)
        .range([0, height])
        .padding(0.1);

    // 축 생성
    svg.append("g").call(d3.axisLeft(yScale)).attr("class", "y-axis");

    svg.append("g")
        .call(d3.axisBottom(xScale).ticks(5))
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${height})`);

    // 데이터 그리기
    datasets.forEach((dataset, i) => {
        const group = svg.append("g").attr("class", `group-${i}`);

        group
            .selectAll(`.bar-${i}`)
            .data(dataset.data)
            .join("rect")
            .attr("class", `bar-${i}`)
            .attr("x", 0)
            .attr(
                "y",
                (d, idx) =>
                    yScale(labels[idx]) +
                    (i * yScale.bandwidth()) / datasets.length
            )
            .attr("height", yScale.bandwidth() / datasets.length)
            .attr("width", (d) => xScale(d))
            .attr("fill", dataset.color);
    });
    const chartRapper = createElement("div", { class: "chart-wrapper" }, chart);
    return chartRapper;
};

export default ScoreChart;
