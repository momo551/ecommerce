// ===============================
// Django AJAX Forms (Login / Register / Profile)
// ===============================

// ---------- CSRF ----------
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// ---------- Handle AJAX Form Submission ----------
function handleAjaxForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(form);

    fetch(form.action || window.location.href, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "X-Requested-With": "XMLHttpRequest",
      },
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        // مسح كل الأخطاء القديمة
        form.querySelectorAll(".text-danger").forEach((el) => (el.textContent = ""));

        if (data.success) {
          if (data.redirect_url) {
            window.location.href = data.redirect_url;
          } else if (data.message) {
            alert(data.message);
          }
        } else if (data.errors) {
          // عرض الأخطاء تحت كل حقل
          for (const [field, messages] of Object.entries(data.errors)) {
            const el = document.getElementById(`error-${field}`);
            if (el) el.textContent = messages.join(", ");
          }
        }
      })
      .catch((err) => console.error(`${formId} error:`, err));
  });
}

// ---------- Cart & Quantity JS ----------
function initCart() {
  // Update Quantity Inputs
  document.querySelectorAll('input[id^="quantity-"]').forEach((input) => {
    input.addEventListener("change", function () {
      const productId = this.dataset.productId;
      const unitPrice = this.dataset.unitPrice;
      const quantity = parseInt(this.value);

      if (isNaN(quantity) || quantity < 1) {
        this.value = 1;
        return;
      }

      updateItemTotal(productId, quantity, unitPrice);
      updateCartQuantity(productId, quantity);
    });
  });

  // Add to Cart Buttons
  document.querySelectorAll(".btn-cart").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      const form = this.closest("form");
      const productId = this.dataset.productId;
      const formData = new FormData(form);

      fetch(`/cart/add/${productId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest",
        },
        body: formData,
      })
        .then((res) => res.json())
        .then(() => {
          window.location.href = "/cart/";
        })
        .catch((err) => console.error("Add to cart error:", err));
    });
  });
}

// ---------- Cart Total Calculation ----------
function updateItemTotal(productId, quantity, unitPrice) {
  const qty = parseInt(quantity);
  const price = parseFloat(unitPrice);
  if (isNaN(qty) || qty < 1 || isNaN(price)) return;

  const total = qty * price;
  const itemEl = document.getElementById(`item-total-${productId}`);
  if (itemEl) itemEl.textContent = `$${total.toFixed(2)}`;
  updateOverallTotal();
}

function updateOverallTotal() {
  let overallTotal = 0;
  document.querySelectorAll('[id^="item-total-"]').forEach((item) => {
    const val = parseFloat(item.textContent.replace("$", ""));
    if (!isNaN(val)) overallTotal += val;
  });
  const overallEl = document.getElementById("overall-total");
  if (overallEl) overallEl.textContent = `$${overallTotal.toFixed(2)}`;
}

function updateCartQuantity(productId, quantity) {
  if (quantity < 1) return;

  fetch(`/cart/update/${productId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "X-Requested-With": "XMLHttpRequest",
    },
    body: new URLSearchParams({ quantity }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success && data.total_price) {
        const overallEl = document.getElementById("overall-total");
        if (overallEl) overallEl.textContent = data.total_price;
      }
    })
    .catch((err) => console.error("Update cart error:", err));
}

// ---------- Init ----------
document.addEventListener("DOMContentLoaded", function () {
  handleAjaxForm("login-form");
  handleAjaxForm("register-form");
  handleAjaxForm("profile-form");
  initCart();
});
