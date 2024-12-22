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

    matchData.rounds.map((round, idx) => {
        datasets[0].data.push(round.user1_score);
        datasets[1].data.push(round.user2_score);
        labels.push(`Round ${idx + 1}`);
    });

    // 차트 렌더링 함수
    const renderChart = () => {
        const containerWidth = chart.clientWidth || 300; // 컨테이너의 현재 너비
        const margin = { top: 30, right: 80, bottom: 30, left: 80 };
        const width = containerWidth - margin.left - margin.right;
        const height = 150 - margin.top - margin.bottom;

        d3.select(chart).selectAll("*").remove(); // 기존 차트 제거

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
            .style("display", "none");

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
                .attr("fill", dataset.color)
                .on("mouseover", function (event, d) {
                    const roundIdx = dataset.data.indexOf(d);
                    const username = dataset.label;
                    const score = d;

                    tooltip
                        .style("display", "inline")
                        .html(`User: ${username}<br>Score: ${score}`)
                        .style("left", `${event.pageX - 50}px`)
                        .style("top", `${event.pageY}px`);
                })
                .on("mouseout", function () {
                    tooltip.style("display", "none");
                });
        });

        const legend = svg
            .append("g")
            .attr("class", "legend")
            .attr(
                "transform",
                `translate(${(width / 4) * 3 + margin.left - 20}, 20)`
            );

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
    };

    // 초기 차트 렌더링
    renderChart();

    // 리사이즈 이벤트 추가
    window.addEventListener("resize", renderChart);

    const chartWrapper = createElement(
        "div",
        { class: "chart-wrapper" },
        chart
    );
    return chartWrapper;
};

export default ScoreChart;
