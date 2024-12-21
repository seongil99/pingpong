import createElement from "../../Utils/createElement.js";
import changeTimeToDate from "../../Utils/changeTimeToDate.js";

const StatDescription = (userHistoryData, userid) => {
    const gameTotalCount = userHistoryData.count;
    let gameCount = 0;
    let gameWinCount = 0;
    let playtime = 0;
    let longestRallyCount = 0;
    let averageRallyTotal = 0;
    const mode = { pvp: 0, tournament: 0 };
    for (let idx = 0; idx < gameTotalCount; idx++) {
        if (userHistoryData.results[idx].ended_at) {
            gameCount++;
            if (userHistoryData.results[idx].winner === userid) gameWinCount++;
            const start = new Date(userHistoryData.results[idx].started_at);
            const end = new Date(userHistoryData.results[idx].ended_at);
            const diff =
                userHistoryData.results[idx].ended_at !== null
                    ? end.getTime() - start.getTime()
                    : 0;
            playtime += diff;
            if (longestRallyCount < userHistoryData.results[idx].longest_rally)
                longestRallyCount = userHistoryData.results[idx].longest_rally;
            averageRallyTotal += userHistoryData.results[idx].average_rally;
            userHistoryData.results[idx].tournament_id
                ? (mode["tournament"] += 1)
                : (mode["pvp"] += 1);
        }
    }
    const gameWinRate = gameCount
        ? `${(gameWinCount / gameCount) * 100} %`
        : "게임을 한 판 이상하면 승률을 확인할 수 있습니다.";
    const longestRally = gameCount
        ? `${longestRallyCount} 회`
        : "게임을 한 판 이상하면 최장 랠리를 확인할 수 있습니다.";
    const averageRally = gameCount
        ? `약 ${Math.floor(averageRallyTotal / gameCount)} 회`
        : "게임을 한 판 이상하면 최장 랠리를 확인할 수 있습니다.";
    const modeCount = gameCount
        ? `PVP: ${mode["pvp"]}, 토너먼트: ${mode["tournament"]}`
        : "게임을 한 판 이상하면 가장 많이 한 모드 정보를 볼 수 있습니다.";
    const totalPlaytime = gameCount
        ? `${changeTimeToDate(playtime)}`
        : "게임을 한 판 이상하면 플레이타임 정보를 볼 수 있습니다.";
    // ** user game count
    const gameCountText = createElement(
        "span",
        { class: "stat-description-data" },
        `게임 수: ${gameCount} 회`
    );
    // ** user game win rate
    const winRateText = createElement(
        "span",
        { class: "stat-description-data" },
        `승률: ${gameWinRate}`
    );
    // ** user game win count and lose count
    const winLoseCountText = createElement(
        "span",
        { class: "stat-description-data" },
        `승 • 패: ${gameWinCount}/${gameCount - gameWinCount}`
    );
    // ** user longest rally
    const longestRallyText = createElement(
        "span",
        { class: "stat-description-data" },
        `최장 랠리: ${longestRally}`
    );
    // ** user average rally
    const averageRallyText = createElement(
        "span",
        { class: "stat-description-data" },
        `평균 랠리: ${averageRally}`
    );
    const modeCountText = createElement(
        "span",
        { class: "stat-description-data" },
        `게임 모드: ${modeCount}`
    );
    const totalPlaytimeText = createElement(
        "span",
        { class: "stat-description-data" },
        `플레이 시간: ${totalPlaytime}`
    );
    const stat = createElement(
        "div",
        { id: "profile-user-stat-description" },
        gameCountText,
        winRateText,
        winLoseCountText,
        longestRallyText,
        averageRallyText,
        modeCountText,
        totalPlaytimeText
    );
    return stat;
};

export default StatDescription;
