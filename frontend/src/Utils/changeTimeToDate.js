const changeTimeToDate = (milliseconds) => {
    const seconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    const years = Math.floor(days / 365);

    const remainingDays = days % 365;
    const remainingHours = hours % 365;
    const remainingMinutes = minutes % 365;
    const remainingSeconds = seconds % 365;

    const yearsText = years ? `${years}년 ` : "";
    const daysText = remainingDays ? `${remainingDays}일 ` : "";
    const hoursText = remainingHours ? `${remainingHours}시간 ` : "";
    const minutesText = remainingMinutes ? `${remainingMinutes}분 ` : "";
    const secondsText = remainingSeconds ? `${remainingSeconds}초` : "";

    return `${yearsText}${daysText}${hoursText}${minutesText}${secondsText}`;
};

export default changeTimeToDate;