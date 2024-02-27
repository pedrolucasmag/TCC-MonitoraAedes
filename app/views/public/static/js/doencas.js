(() => {
  let isScrolling = false;

  function scrollToAccordion(e) {
    if (!acc) {
      console.error("O elemento do accordion não foi encontrado");
      return;
    }

    const scrollOffset = acc.scrollTop + e.target.parentNode.offsetTop;

    if (!isScrolling) {
      isScrolling = true;

      setTimeout(() => {
        window.scroll({
          top: scrollOffset,
          left: 0,
          behavior: "smooth",
        });

        isScrolling = false;
      }, 200);
    }
  }

  const acc = document.getElementById("accordionDoencas");
  if (acc) {
    acc.addEventListener("shown.bs.collapse", scrollToAccordion);
  }
})();
