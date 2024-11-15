function VerificationButton(color, backgroundColor, content) {
    const btn = document.createElement("button");
    btn.classList.add("verification-btn");
    btn.style.color = color;
    btn.style.backgroundColor = backgroundColor;
    btn.textContent = content;

    return btn;
}

export default VerificationButton;
