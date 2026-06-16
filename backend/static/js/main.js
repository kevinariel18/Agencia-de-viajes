// TourPack Manager - Main JS

document.addEventListener("DOMContentLoaded", () => {
  // Toggle sidebar on mobile
  const toggleBtn = document.getElementById("sidebar-toggle");
  const sidebar = document.querySelector(".sidebar");
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      sidebar.classList.toggle("open");
    });
    document.addEventListener("click", (e) => {
      if (sidebar.classList.contains("open") &&
          !sidebar.contains(e.target) &&
          !toggleBtn.contains(e.target)) {
        sidebar.classList.remove("open");
      }
    });
  }

  // Auto-dismiss alerts after 4s
  document.querySelectorAll(".alert-auto-dismiss").forEach((el) => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert.close();
    }, 4000);
  });

  // Confirm dialogs
  document.querySelectorAll("[data-confirm]").forEach((el) => {
    el.addEventListener("click", (e) => {
      if (!confirm(el.dataset.confirm)) e.preventDefault();
    });
  });

  // Live price preview on reservation form
  const peopleInput = document.getElementById("id_number_of_people");
  const unitPrice = document.getElementById("unit-price-value");
  const totalDisplay = document.getElementById("total-display");
  if (peopleInput && unitPrice && totalDisplay) {
    const price = parseFloat(unitPrice.dataset.price || 0);
    peopleInput.addEventListener("input", () => {
      const people = parseInt(peopleInput.value) || 0;
      totalDisplay.textContent = "$" + (people * price).toFixed(2);
    });
  }
});
