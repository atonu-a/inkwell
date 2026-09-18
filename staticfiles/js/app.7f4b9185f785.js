try {
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
} catch (error) {
  console.log(error);
}
console.log("Hello");
// Image upload compression

const imgInput = document.getElementById("thumb-img");
const publishBtn = document.getElementById("publish-btn");
const imagePreview = document.getElementById("image-preview");
if (imgInput) {
  imgInput.addEventListener("change", async function () {
    const file = this.files[0];
    if (!file) return;
    if (!file.type.startsWith("image/")) return;

    if (imagePreview) {
      imagePreview.src = URL.createObjectURL(file);
      imagePreview.style.display = "block"; // ছবি সিলেক্ট করলেই ট্যাগটি দৃশ্যমান হবে
    }

    // ২ মেগাবাইটের কম হলে কম্প্রেস করার দরকার নেই
    if (file.size <= 2 * 1024 * 1024) return;

    try {
      if (publishBtn) {
        publishBtn.disabled = true;
      }
      console.log("Compressing image...");

      // কম্প্রেস প্রক্রিয়া শেষ হওয়া পর্যন্ত অপেক্ষা করবে
      const compressedFile = await compressImage(file);

      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(compressedFile);
      imgInput.files = dataTransfer.files;
      console.log("Files attached to input:", imgInput.files[0]);

      console.log("Original:", (file.size / 1024 / 1024).toFixed(2), "MB");
      console.log(
        "Compressed:",
        (compressedFile.size / 1024 / 1024).toFixed(2),
        "MB",
      );
    } catch (error) {
      console.error("Compression error:", error);
      alert("Image compression failed.");
    } finally {
      if (publishBtn) {
        publishBtn.disabled = false;
        publishBtn.innerText = "Publish Post";
      }
    }
  });

  function compressImage(file) {
    return new Promise((resolve, reject) => {
      const img = new Image();

      img.onload = function () {
        const MAX_WIDTH = 1200;
        const MAX_HEIGHT = 1200;
        let width = img.width;
        let height = img.height;

        if (width > MAX_WIDTH || height > MAX_HEIGHT) {
          const ratio = Math.min(MAX_WIDTH / width, MAX_HEIGHT / height);
          width = Math.round(width * ratio);
          height = Math.round(height * ratio);
        }

        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;

        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);

        canvas.toBlob(
          (blob) => {
            if (!blob) {
              reject(new Error("Canvas toBlob failed"));
              return;
            }

            const compressedFile = new File([blob], "blog-image.webp", {
              type: "image/webp",
              lastModified: Date.now(),
            });

            resolve(compressedFile);
          },
          "image/webp",
          0.6,
        );
      };

      img.onerror = function (error) {
        reject(error);
      };

      img.src = URL.createObjectURL(file);
    });
  }
}

// URl copy function
function copyUrl(url, button) {
  const fullUrl = window.location.origin + url;

  navigator.clipboard.writeText(fullUrl).then(() => {
    const originalText = button.innerHTML;

    button.innerHTML = `
                <i class="fa-solid fa-clipboard-check "></i> Copied!
            `;

    setTimeout(() => {
      button.innerHTML = originalText;
    }, 1500);
  });
}