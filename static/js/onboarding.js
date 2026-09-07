// Image upload and crop
(function () {
  const fileInput = document.getElementById("profilePicInput");
  const preview = document.getElementById("profilePicPreview");
  const modal = document.getElementById("cropModal");
  const cropImage = document.getElementById("cropTargetImage");
  const confirmBtn = document.getElementById("cropConfirmBtn");
  const cancelBtn = document.getElementById("cropCancelBtn");

  let cropper = null;
  let originalFileName = "profile.jpg";

  fileInput.addEventListener("change", function (e) {
    const file = e.target.files[0];
    if (!file) return;
    originalFileName = file.name.replace(/\.[^/.]+$/, "") + ".jpg";

    const reader = new FileReader();
    reader.onload = function (ev) {
      cropImage.src = ev.target.result;
      modal.style.display = "flex";
      if (cropper) cropper.destroy();
      cropper = new Cropper(cropImage, {
        aspectRatio: 1,
        viewMode: 1,
        dragMode: "move",
        autoCropArea: 1,
        background: false,
        responsive: true,
      });
    };
    reader.readAsDataURL(file);
  });

  cancelBtn.addEventListener("click", function () {
    if (cropper) {
      cropper.destroy();
      cropper = null;
    }
    fileInput.value = "";
    modal.style.display = "none";
  });

  confirmBtn.addEventListener("click", function () {
    if (!cropper) return;
    const canvas = cropper.getCroppedCanvas({
      width: 500,
      height: 500,
      imageSmoothingQuality: "high",
    });
    canvas.toBlob(
      function (blob) {
        const croppedFile = new File([blob], originalFileName, {
          type: "image/jpeg",
        });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(croppedFile);
        fileInput.files = dataTransfer.files;
        preview.src = URL.createObjectURL(blob);
        cropper.destroy();
        cropper = null;
        modal.style.display = "none";
      },
      "image/jpeg",
      0.9,
    );
  });
})();
