// Bootstrap Form Switch 생성 함수
import createElement from "../Utils/createElement.js";
import PvpRequest from "../Controller/Game/PvpRequest.js";
function createFormSwitch(socket) {
    // 스위치 입력 생성
    const formCheckInput = createElement("input", {
        class: "form-check-input",
        type: "checkbox",
        id: "flexSwitchCheckDefault",
        events: {
            change: (event) => {
                switchStatusText.textContent = event.target.checked ? "공두개" : "공하나";
            },
        },
    });
    // 스위치 상태 텍스트 생성
    const switchStatusText = createElement(
        "p",
        {
            id: "switchStatusText",
            class: "mt-2 text-muted",
        },
        "공하나"
    );

    // 스위치 라벨 생성
    const formCheckLabel = createElement(
        "label",
        {
            class: "form-check-label",
            for: "flexSwitchCheckDefault",
        },
        "게임옵션 선택"
    );

    // 전송 버튼 생성
    const submitButton = createElement(
        "button",
        {
            type: "button",
            class: "btn btn-primary mt-3",
            id : "process-btn",
            events: {
                click: async () => {
                    console.log("this is secondcallback ",  "hiddenvalue", localStorage.getItem("matchType"));
                    if (socket && localStorage.getItem("matchType") !== "Pve") {
                        let message = null;
                        const type = localStorage.getItem("matchType");
                        const gameId = localStorage.getItem("gameId");
                        console.log("what is value", type, gameId);
                        if (type !== "tournament") {
                            message = {
                                type: "set_option",
                                game_id: localStorage.getItem("gameId"),
                                multi_ball: formCheckInput.checked,
                            };
                        } 
                        else {
                            message = {
                                type: "set_option",
                                tournament_id: localStorage.getItem("gameId"),
                                game_id : null,
                                multi_ball: formCheckInput.checked,
                            };
                        }
                        console.log("before sned message ", message);
                        socket.send(JSON.stringify(message));
                    }
                    else {
                        if (localStorage.getItem("matchType") === "Pve") {
                            console.log("distroyd");
                            const gameId = await PvpRequest(formCheckInput.checked);
                            // const modalElement = document.getElementById("modal-tartget");
                            // // 부모 엘리먼트를 얻기
                            // const parentElement = modalElement.parentElement;
                            // // 부모 엘리먼트에서 자식 제거
                            // if (parentElement) {
                            //     parentElement.removeChild(modalElement);
                            // }
                            // // Bootstrap 모달 인스턴스 얻기
                            // const modalInstance = bootstrap.Modal.getInstance(modalElement);
                            // modalInstance.hide();
                            console.log(gameId);
                            await window.router.navigate(`/playing/${gameId.game_id}`, false);
                        }
                    }
                }, // 콜백 실행
            },
        },
        i18next.t("process-btn")
    );

    // 스위치 컨테이너 생성
    const formCheck = createElement(
        "div",
        {
            id: "form-target",
            class: "form-check form-switch hide",
        },
        formCheckInput,
        formCheckLabel,
        switchStatusText,
        submitButton
    );

    return formCheck;
}

// 실행 예시
export default createFormSwitch;

