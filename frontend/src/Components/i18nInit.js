// 브라우저 환경에서 전역 변수 사용
async function translater(params) {
    // 로컬 스토리지 감지
    window.addEventListener("storage", (event) => {
        if (event.key === "lang" && event.newValue) {
            i18next.changeLanguage(event.newValue);  // 언어 업데이트
        }
    });

    // i18next 초기화
    return i18next.init(
        {
            lng: localStorage.getItem('lang') || "한국어",
            debug: true,
            resources: params,
        },
        (err) => {
            if (err) {
                console.error("i18next 초기화 오류:", err);
            }
        }
    );
}

export default translater;
