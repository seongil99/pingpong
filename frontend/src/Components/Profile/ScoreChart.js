import FetchMatchData from "../../Controller/Profile/FetchMatchData.js";
import FetchUserData from "../../Controller/Profile/FetchUserData.js";
import createElement from "../../Utils/createElement.js";

const ScoreChart = async (session) => {
    const chart = createElement(
        "div",
        { id: `chart-container`, class: "game-session-chart" },
        []
    );
    const user1Data = await FetchUserData(session.user1);
    const user2Data = await FetchUserData(session.user2);
    const matchData = await FetchMatchData(session.id);
    // D3.js로 차트 생성
    const margin = { top: 30, right: 100, bottom: 30, left: 100 };
    const width = 400 - margin.left - margin.right;
    const height = 200 - margin.top - margin.bottom;

    // 데이터
    const labels = [];
    const datasets = [
        {
            label: `${user1Data.username}`,
            data: [],
            color: "rgba(255, 99, 132, 0.5)",
        },
        {
            label: `${user2Data.username}`,
            data: [],
            color: "rgba(54, 162, 235, 0.5)",
        },
    ];

    // session.user1_score session.user2_score
    matchData.rounds.map((round, idx) => {
        datasets[0].data.push(round.user1_score);
        datasets[1].data.push(round.user2_score);
        labels.push(`Round ${idx + 1}`);
    });
    const svg = d3
        .select(chart)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // X축 및 Y축 스케일
    const xScale = d3
        .scaleLinear()
        .domain([0, d3.max(datasets.flatMap((d) => d.data))])
        .range([0, width]);

    const xAxis = d3.axisBottom(xScale).ticks(1).tickFormat(d3.format("d"));

    const yScale = d3
        .scaleBand()
        .domain(labels)
        .range([0, height])
        .padding(0.1);

    // 축 생성
    svg.append("g").call(d3.axisLeft(yScale)).attr("class", "y-axis");

    svg.append("g")
        .call(xAxis)
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${height})`);

    const tooltip = d3
        .select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("background", "rgba(0,0,0,0.7)")
        .style("color", "white")
        .style("padding", "5px")
        .style("border-radius", "5px")
        .style("display", "none"); // 처음엔 보이지 않게 설정
    // 데이터 그리기
    datasets.forEach((dataset, i) => {
        const group = svg.append("g").attr("class", `group-${i}`);
        // Tooltip 생성 (숨김 상태로 시작)
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
            .attr("fill", dataset.color)
            .on("mouseover", function (event, d) {
                const roundIdx = dataset.data.indexOf(d); // 현재 데이터가 어느 라운드인지 찾기
                const username = dataset.label; // 유저 이름 가져오기
                const score = d; // 점수

                // 툴팁에 유저명과 점수 표시
                tooltip
                    .style("display", "inline")
                    .html(`User: ${username}<br>Score: ${score}`)
                    .style("left", `${event.pageX - 50}px`)
                    .style("top", `${event.pageY}px`);
            })
            .on("mouseout", function () {
                // 마우스가 나가면 툴팁 숨기기
                tooltip.style("display", "none");
            });
    });
    const legend = svg
        .append("g")
        .attr("class", "legend")
        .attr("transform", `translate(${width / 3 * 2 + margin.left - 20}, 20)`);

    datasets.forEach((dataset, i) => {
        const legendItem = legend
            .append("g")
            .attr("transform", `translate(0, ${i * 20})`);

        legendItem
            .append("rect")
            .attr("width", 15)
            .attr("height", 15)
            .attr("fill", dataset.color);

        legendItem
            .append("text")
            .attr("x", 20)
            .attr("y", 12)
            .text(`${dataset.label}`)
            .style("font-size", "12px")
            .style("alignment-baseline", "middle");
    });
    const chartRapper = createElement("div", { class: "chart-wrapper" }, chart);
    return chartRapper;
};

export default ScoreChart;
