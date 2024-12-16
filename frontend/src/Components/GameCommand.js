import createElement from "../Utils/createElement.js";

// User Data Parameter 생략. API 연동 작업 때 추가 예정. 만약 추가하면 삭제 처리도 충분히 쉽게 할 수 있음
function createKeyboardGuideElement(label, content) {
    const container = document.createElement("div");
    container.className = "keyboard-guide-item";
  
    const text = document.createElement("div");
    text.className = "keyboard-guide-label";
    text.textContent = label;
  
    const kbd = document.createElement("kbd");
    kbd.className = "keyboard-guide-key";
  
    if (typeof content === "string") {
      kbd.textContent = content;
    } else {
      kbd.appendChild(content);
    }
  
    container.appendChild(text);
    container.appendChild(kbd);
  
    return container;
  }
const GameCommandInfo = () => {
  const container = document.createElement("div");
  container.className = "keyboard-guide-container";

  const keys = [
    { label: "왼쪽으로 이동", content: "◀ A" },
    { label: "오른쪽으로 이동", content: "D ▶"},
    { label: "색변경", content: "C" },
    { label: "브금온오프", content: "M" },
    { label: "파워샷", content: "SPACE" },
  ];

  keys.forEach(({ label, content }) => {
    container.appendChild(createKeyboardGuideElement(label, content));
  });
  const Infos = createElement(
    "div",
    {
        class: `command-body`,
    },
    container
);
return Infos;
}

export default GameCommandInfo;
