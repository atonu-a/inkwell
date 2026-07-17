

// Function-ke window object-e diye global kora holo jate HTML er onclick ota khuje pay
window.likePost = function (btn) {
  const url = btn.dataset.url;

  // Django-r CSRF token prothom-e dynamic cookie theke khuje neya
  let csrfToken = "";
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookieArray = decodedCookie.split(";");
  for (let i = 0; i < cookieArray.length; i++) {
    let cookie = cookieArray[i].trim();
    if (cookie.indexOf("csrftoken=") === 0) {
      csrfToken = cookie.substring("csrftoken=".length, cookie.length);
      break;
    }
  }

  // Jodi cookie te na pay, HTML layout input field (jodi thake) theke nibe
  if (!csrfToken) {
    const tokenInput = document.querySelector("[name=csrfmiddlewaretoken]");
    if (tokenInput) csrfToken = tokenInput.value;
  }

  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken, // Dynamic calculated token pass kora holo
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

      if (countSpan) countSpan.textContent = data.total_likes;

      if (data.liked) {
        btn.classList.add("btn-default");
        btn.classList.remove("btn-dark");

        if (icon) {
          // Bounce animation
          icon.classList.remove("fa-beat");
          void icon.offsetWidth; // Restart animation
          icon.classList.add("fa-beat");

          setTimeout(() => {
            icon.classList.remove("fa-beat");
          }, 1000);
        }
      } else {
        btn.classList.add("btn-dark");
        btn.classList.remove("btn-default");
      }
    })
    .catch((error) => console.error("Error:", error));
};
// Function-ke window layer-e bosiye global kora holo jate HTML-er onclick eta khuje pay
window.toggleFollow = function (btn) {
  const userId = btn.getAttribute("data-user-id");
  const span = btn.querySelector("span");
  const i = btn.querySelector("i");

  // Cookie theke Django-r CSRF token ber kora
  let csrfToken = "";
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookieArray = decodedCookie.split(";");
  for (let j = 0; j < cookieArray.length; j++) {
    let cookie = cookieArray[j].trim();
    if (cookie.indexOf("csrftoken=") === 0) {
      csrfToken = cookie.substring("csrftoken=".length, cookie.length);
      break;
    }
  }

  // Cookie te na paile input field fallback check koro
  if (!csrfToken) {
    const tokenInput = document.querySelector("[name=csrfmiddlewaretoken]");
    if (tokenInput) csrfToken = tokenInput.value;
  }

  fetch(`/follow/${userId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken, // Dynamic token pass kora holo
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((res) => {
      if (!res.ok) throw new Error("Network response was not ok");
      return res.json();
    })
    .then((data) => {
      const countEl = document.getElementById("followers-count");

      if (data.status === "following") {
        if (span) span.textContent = "Following";
        if (i) i.className = "fa-solid fa-heart-circle-check";

        // Followers count safe update (NaN handling)
        if (countEl) {
          let currentCount = parseInt(countEl.textContent.trim()) || 0;
          countEl.textContent = currentCount + 1;
        }
      } else {
        if (span) span.textContent = "Follow";
        if (i) i.className = "fa-solid fa-heart-circle-plus";

        if (countEl) {
          let currentCount = parseInt(countEl.textContent.trim()) || 0;
          countEl.textContent = Math.max(0, currentCount - 1); // Follower jeno minus (-) na hoy
        }
      }
    })
    .catch((err) => console.error("Error:", err));
};

// Password Eye button
document.querySelectorAll(".input-group").forEach((group) => {
  const passwordInput = group.querySelector('input[type="password"]');
  const toggleBtn = group.querySelector('button[type="button"]');
  const icon = group.querySelector(".togglePasswordIcon");

  if (passwordInput && toggleBtn && icon) {
    toggleBtn.addEventListener("click", function () {
      const isPassword = passwordInput.getAttribute("type") === "password";
      passwordInput.setAttribute("type", isPassword ? "text" : "password");

      icon.classList.toggle("fa-eye");
      icon.classList.toggle("fa-eye-slash");
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const inputs = document.querySelectorAll("input, select, textarea");
  inputs.forEach((input) => {
    // 'form-control' is the standard Bootstrap class for text inputs
    // Use 'form-check-input' if you have checkboxes/radios
    if (input.type === "checkbox" || input.type === "radio") {
      input.classList.add("form-check-input");
    } else {
      input.classList.add("form-control");
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const loadingButtons = document.querySelectorAll(".btn-loading");

  loadingButtons.forEach((button) => {
    const parentForm = button.closest("form");

    if (parentForm) {
      parentForm.addEventListener("submit", function (event) {
        const btnText = button.dataset.text;
        console.log(btnText);
        button.dataset.originalHtml = button.innerHTML;

        button.innerHTML = `
          <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          ${btnText}
        `;
        button.disabled = true;
      });
    }
  });

  // --- Back Button Error Fixer ---

  window.addEventListener("pageshow", function (event) {
    if (event.persisted) {
      loadingButtons.forEach((button) => {
        if (button.dataset.originalHtml) {
          button.innerHTML = button.dataset.originalHtml;
        }
        button.disabled = false;
      });
    }
  });
});

// Infinite Scrolling
let currentPage = 2;
let loading = false;
let hasNext = true;

async function loadPosts() {
  if (loading || !hasNext) return;

  loading = true;
  console.log(1);

  document.getElementById("loading").style.display = "flex";

  const response = await fetch(`/load-posts?page=${currentPage}`);

  const data = await response.json();

  document
    .getElementById("posts-container")
    .insertAdjacentHTML("beforeend", data.html);
    console.log(2);

  hasNext = data.has_next;
  currentPage++;
  loading = false;
  console.log(3);
  document.getElementById("loading").style.display = "none";
  console.log(4);
}

const observer = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    loadPosts();
  }
});

observer.observe(document.getElementById("load-trigger"));