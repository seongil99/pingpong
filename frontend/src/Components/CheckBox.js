// Bootstrap Form Switch 생성 함수
import createElement from "../Utils/createElement.js";

function createFormSwitch(params) {
    // 스위치 입력 생성
    const formCheckInput = createElement(
        "input",
        {
            class: "form-check-input",
            type: "checkbox",
            id: "flexSwitchCheckDefault",
        }
    );

    // 스위치 라벨 생성
    const formCheckLabel = createElement(
        "label",
        {
            class: "form-check-label",
            for: "flexSwitchCheckDefault",
        },
        params
    );

    // 스위치 컨테이너 생성
    const formCheck = createElement(
        "div",
        {
            class: "form-check form-switch",
        },
        formCheckInput,
        formCheckLabel
    );

    // DOM에 추가
    return formCheck;
}

// 실행
export default createFormSwitch();
