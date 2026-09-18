(function () {
  const body = document.body;
  const toggleButtons = document.querySelectorAll(".theme-toggle");
  const savedTheme = localStorage.getItem("inkwell-theme");

  if (savedTheme === "dark") {
    body.setAttribute("data-theme", "dark");
  } else {
    body.setAttribute("data-theme", "light");
  }

  function syncThemeButton() {
    const isDark = body.getAttribute("data-theme") === "dark";
    toggleButtons.forEach((button) => {
      const icon = button.querySelector("i");
      if (!icon) return;
      icon.classList.toggle("fa-moon", !isDark);
      icon.classList.toggle("fa-sun", isDark);
      button.setAttribute(
        "title",
        isDark ? "Switch to light theme" : "Switch to dark theme",
      );
    });
  }

  syncThemeButton();

  toggleButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const nextTheme =
        body.getAttribute("data-theme") === "dark" ? "light" : "dark";
      body.setAttribute("data-theme", nextTheme);
      localStorage.setItem("inkwell-theme", nextTheme);
      syncThemeButton();
    });
  });
})();
