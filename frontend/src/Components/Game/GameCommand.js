import createElement from "../../Utils/createElement.js";

function createKeyboardGuideElement(idLabel, idContent) {
    const container = createElement("div", { class: "keyboard-guide-item" });

    const text = createElement(
        "div",
        { class: "keyboard-guide-label", id: idLabel },
        i18next.t(idLabel)
    );

    const kbd = createElement(
        "kbd",
        { class: "keyboard-guide-key", id: idContent },
        i18next.t(idContent)
    );

    container.appendChild(text);
    container.appendChild(kbd);

    return container;
}

const GameCommandInfo = () => {
    const container = createElement("div", {
        class: "keyboard-guide-container",
    });

    const keys = [
        { idLabel: "key_move_left_label", idContent: "key_move_left_key" },
        { idLabel: "key_move_right_label", idContent: "key_move_right_key" },
        {
            idLabel: "key_change_color_label",
            idContent: "key_change_color_key",
        },
        {
            idLabel: "key_toggle_music_label",
            idContent: "key_toggle_music_key",
        },
        { idLabel: "key_power_shot_label", idContent: "key_power_shot_key" },
    ];

    keys.forEach(({ idLabel, idContent }) => {
        container.appendChild(createKeyboardGuideElement(idLabel, idContent));
    });

    const Infos = createElement("div", { class: "command-body" }, container);
    return Infos;
};

export default GameCommandInfo;
