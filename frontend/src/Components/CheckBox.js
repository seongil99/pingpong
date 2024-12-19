// Bootstrap Form Switch 생성 함수
import createElement from "../Utils/createElement.js";

function createFormSwitch(socket) {
    // 스위치 입력 생성
    const formCheckInput = createElement(
        "input",
        {
            class: "form-check-input",
            type: "checkbox",
            id: "flexSwitchCheckDefault",
			events:{
				change:(event)=>{
					switchStatusText.textContent = event.target.checked ? "공두개":"기본";
				}
			}
        }
    );

    // 스위치 상태 텍스트 생성
    const switchStatusText = createElement(
        "p",
        {
            id: "switchStatusText",
            class: "mt-2 text-muted",
        },
        "기본"
    );

    // 스위치 라벨 생성
    const formCheckLabel = createElement(
        "label",
        {
            class: "form-check-label",
            for: "flexSwitchCheckDefault",
        },
        "게임옵션 선택"
    )

    // 전송 버튼 생성
    const submitButton = createElement(
        "button",
        {
            type: "button",
            class: "btn btn-primary mt-3",
            events: {
                click: 
                    ()=>{
						console.log("this is secondcallback ",this,"hiddenvalue" ,socket);
						if (socket) {
								const v = document.getElementById("hidden-input");
								console.log("what is value", v);
								const message = {
									type: "set_option",
									game_id: parseInt(v.value),
									multi_ball : formCheckInput.checked,
								};
								console.log("before sned message ",message);
								socket.send(JSON.stringify(message));            
							}
						} // 콜백 실행
                },
            },
        "진행"
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
