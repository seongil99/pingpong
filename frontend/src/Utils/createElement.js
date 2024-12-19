const changeIntoMap = (props) => {
    const map = new Map(Object.entries(props));
    map.forEach((value, key) => {
        if (typeof value === "object") {
            map.set(key, changeIntoMap(value));
        }
    });
    return map;
};

const createElement = (type, props, ...children) => {
    const elem = document.createElement(type);
    const attributes = changeIntoMap(props);
    attributes.forEach((value, key) => {
        if (key === "style") {
            value.forEach((v, k) => {
                elem.style[k] = v;
            });
        } else if (key === "events") {
            value.forEach((v, k) => {
                elem.addEventListener(k, v);
            });
        } else {
            elem.setAttribute(key, value);
        }
    });
    children.forEach((child) => {
        if (typeof child === "string") {
            elem.appendChild(document.createTextNode(child));
        } else if (child instanceof Node) {
            elem.appendChild(child);
        }
    });
    return elem;
};

export default createElement;
