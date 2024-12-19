export const handleClick = (e, router) => {
  // event.target.closest()를 사용하여 클릭된 요소나 상위 요소에서 .navigate를 찾음
  const target = e.target.closest(".navigate");
  if (target) {
    e.preventDefault();
    const pathname = target.getAttribute("path");
    router.navigate(pathname, false); // 경로 변경 및 렌더링
  }
};
