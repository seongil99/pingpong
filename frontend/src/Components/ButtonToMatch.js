import createElement from "../Utils/createElement.js";

function createButton(params,callback) {
    // 왼쪽 버튼 생성
    const matchButton = createElement(
        "button",
        {
            type: "button",
            class: "btn btn-primary",
			id: params,
            events:{
                click : callback
            }
        },
        params
    );

    // 버튼 그룹 컨테이너 생성
    const buttonGroup = createElement(
        "div",
        {
            class: "btn-group",
            role: "group",
            "aria-label": "Basic example",
        },
        matchButton
    );

    // DOM에 추가
    return buttonGroup;
}

// 실행
export default createButton;
