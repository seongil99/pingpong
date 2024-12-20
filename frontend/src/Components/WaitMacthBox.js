import createElement from "../Utils/createElement.js";
import CreateFormSwitch from "./CheckBox.js";
function createMessageModal(message,callback,socket) {
    // 메시지 표시 영역 생성
	const modalTitle = createElement(
        "div",
        { class: "modal-title" },
        createElement("h5", {}, `잠시만 기다려 주세요. `)
    );
    const modalBody = createElement(
        "div",
        { 
			id: "modal-body-target",
			class: "modal-body" },
        createElement("p", {}, message)
    );

    // 닫기 버튼 생성
    const btnClose = createElement(
        "button",
        {
			id: "modal-btn-target",
            type: "button",
            class: "btn btn-secondary",
            "data-bs-dismiss": "modal",
			events: {
				click: callback ? callback : null
			}
        },
        "Close"
    );

    // 모달 푸터 생성
    const modalFooter = createElement(
        "div",
        { class: "modal-footer" },
        btnClose
    );

    // 모달 콘텐츠 생성
    const modalContent = createElement(
        "div",
        { 	
			class: "modal-content" 
		},
		modalTitle,
        modalBody,
        modalFooter,
		CreateFormSwitch(socket),
    );

    // 모달 다이얼로그 생성
    const modalDialog = createElement(
        "div",
        { class: "modal-dialog modal-static" },  // 정적 모달 설정
        modalContent
    );

    // 모달 컨테이너 생성
    const modal = createElement(
        "div",
        {
			id: "modal-tartget",
            class: "modal",
            tabindex: "-1",
        },
        modalDialog
    );

    // DOM에 추가
    // Bootstrap 모달 인스턴스 생성
    const modalInstance = new bootstrap.Modal(modal, {
        backdrop: "static",  // 배경 클릭 비활성화
        keyboard: false,    // ESC 키 입력 비활성화
    });

    // 모달 열기
    return {element: modal, modal:modalInstance};

}
export default createMessageModal;