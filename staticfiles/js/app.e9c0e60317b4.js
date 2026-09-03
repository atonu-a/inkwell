document.addEventListener("DOMContentLoaded", function () {
  console.log("app.js successfully loaded with pure JS!");
  function likePost(btn) {
    const url = btn.dataset.url;

    fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": "{{ csrf_token }}",
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
      })
      .then((data) => {
        const countSpan = btn.querySelector(".like-count");
        const icon = btn.querySelector("i");

        countSpan.textContent = data.total_likes;

        if (data.liked) {
          btn.classList.add("btn-default");
          btn.classList.remove("btn-dark");

          // Bounce animation
          icon.classList.remove("fa-beat");
          void icon.offsetWidth; // Restart animation
          icon.classList.add("fa-beat");

          setTimeout(() => {
            icon.classList.remove("fa-beat");
          }, 1000);
        } else {
          btn.classList.add("btn-dark");
          btn.classList.remove("btn-default");
        }
      })
      .catch((error) => console.error("Error:", error));
  }
});
