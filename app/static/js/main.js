// ==============================
// Confirm before form submission (optional validation placeholder)
// ==============================
document.addEventListener("submit", function (e) {
  if (e.target && e.target.matches("form")) {
    // You can add form validation logic here if needed later
  }
});

// ==============================
// CTA Animation (Book Service Button)
// ==============================
document.addEventListener("DOMContentLoaded", () => {
  const cta = document.querySelector(".cta");
  if (!cta) return;

  const triggerPop = () => {
    cta.classList.add("pop-effect");
    setTimeout(() => cta.classList.remove("pop-effect"), 600);
  };

  // Auto pop every 5 seconds
  setInterval(triggerPop, 5000);

  // Extra pop on hover
  cta.addEventListener("mouseenter", triggerPop);

  // Optional: pop sound on click
  cta.addEventListener("click", () => {
    const audio = new Audio(
      "https://cdn.pixabay.com/download/audio/2021/08/04/audio_2c4cf9c29f.mp3?filename=pop.mp3"
    );
    audio.play().catch(() => {});
  });
});

// ==============================
// Service Selection Popup Logic (Inline Box Version)
// ==============================
document.addEventListener("DOMContentLoaded", () => {
  const popup = document.getElementById("servicePopup");
  const openBtn = document.getElementById("openServicePopup");
  const closeBtn = document.getElementById("closeServicePopup");
  const cancelBtn = document.getElementById("cancelServicePopup");
  const confirmBtn = document.getElementById("confirmServiceSelection");
  const hiddenInput = document.getElementById("selectedServicesInput");
  const searchInput = document.getElementById("serviceSearch");
  const selectedBox = document.getElementById("selectedServicesBox");

  const getCheckboxes = () => document.querySelectorAll(".service-checkbox");

  // === Open popup ===
  openBtn.addEventListener("click", () => {
    popup.classList.add("show");
    document.body.classList.add("popup-open");

    // ✅ Restore checked state from hidden input
    const selectedValues = hiddenInput.value
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    getCheckboxes().forEach((cb) => {
      const labelText = cb.nextElementSibling.textContent.trim();
      cb.checked = selectedValues.includes(labelText);
    });
  });

  // === Close popup ===
  const closePopup = () => {
    popup.classList.remove("show");
    document.body.classList.remove("popup-open");
  };
  closeBtn?.addEventListener("click", closePopup);
  cancelBtn?.addEventListener("click", closePopup);

  // === Search filter ===
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const query = e.target.value.toLowerCase().trim();
      document.querySelectorAll(".service-card").forEach((card) => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(query) ? "flex" : "none";
      });
    });
  }

  // === Confirm button ===
  confirmBtn.addEventListener("click", () => {
    const checkboxes = getCheckboxes();

    const selected = Array.from(checkboxes)
      .filter((ch) => ch.checked)
      .map((ch) => ch.nextElementSibling.textContent.trim());

    console.log("Selected services:", selected);

    // ✅ Store in hidden input for backend form submission
    hiddenInput.value = selected.join(", ");

    // ✅ Update inline "selected services" box
    selectedBox.innerHTML = "";
    if (selected.length > 0) {
      selected.forEach((srv) => {
        const div = document.createElement("div");
        div.className = "border rounded px-2 py-1 mb-1 bg-light";
        div.textContent = srv;
        selectedBox.appendChild(div);
      });
    } else {
      selectedBox.innerHTML =
        '<div class="text-muted small text-center">No services selected yet</div>';
    }

    closePopup();
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const bookingForm = document.getElementById("bookingForm");
  const successPopup = document.getElementById("bookingSuccessPopup");
  const closePopupBtn = document.getElementById("closeSuccessPopup");

  if (bookingForm) {
    bookingForm.addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent default form submission for demo

      // Simulate backend delay / response
      setTimeout(() => {
        successPopup.style.display = "flex"; // Show popup
        document.body.style.overflow = "hidden"; // Disable background scroll
      }, 400);
    });
  }

  if (closePopupBtn) {
    closePopupBtn.addEventListener("click", function () {
      successPopup.style.display = "none";
      document.body.style.overflow = "auto";
      bookingForm.reset();

      // ✅ Redirect to home page after closing popup
      window.location.href = "/";
    });
  }
});

// ===============================
// Header Navigation Toggle
// ===============================
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const header = document.querySelector(".site-header");

  if (toggle && header) {
    toggle.addEventListener("click", () => {
      header.classList.toggle("nav-open");
    });
  }
});
