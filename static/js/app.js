

window.addEventListener("load", () => {
  const rtrnToTop = document.querySelector("#return-to-top");
  rtrnToTop.addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

});


