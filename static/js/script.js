// ===============================
// Cart & Shop JavaScript (Django)
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

// ---------- Update Item Total ----------
function updateItemTotal(productId, quantity, unitPrice) {
  const qty = parseInt(quantity);
  const price = parseFloat(unitPrice);

  if (isNaN(qty) || qty < 1 || isNaN(price)) return;

  const total = qty * price;
  const itemTotalEl = document.getElementById(`item-total-${productId}`);

  if (itemTotalEl) {
    itemTotalEl.textContent = `$${total.toFixed(2)}`;
  }

  updateOverallTotal();
}

// ---------- Update Overall Total ----------
function updateOverallTotal() {
  let overallTotal = 0;

  document.querySelectorAll('[id^="item-total-"]').forEach((item) => {
    const value = parseFloat(item.textContent.replace("$", ""));
    if (!isNaN(value)) {
      overallTotal += value;
    }
  });

  const overallEl = document.getElementById("overall-total");
  if (overallEl) {
    overallEl.textContent = `$${overallTotal.toFixed(2)}`;
  }
}

// ---------- Update Quantity (AJAX) ----------
function updateCartQuantity(productId, quantity) {
  if (quantity < 1) return;

  fetch(`/cart/update/${productId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ quantity }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        const overallEl = document.getElementById("overall-total");
        if (overallEl && data.total_price) {
          overallEl.textContent = data.total_price;
        }
      }
    })
    .catch((err) => console.error("Update error:", err));
}

// ---------- Silent Add to Cart ----------
function initAddToCart() {
  document.querySelectorAll(".btn-cart").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();

      const form = this.closest("form");
      const productId = this.dataset.productId;
      const formData = new FormData(form);

      fetch(`/cart/add/${productId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
          "X-Requested-With": "XMLHttpRequest",
        },
        body: formData,
      })
        .then((res) => res.json())
        .then((data) => {
          // إضافة صامتة
          window.location.href = "/cart/";
        })
        .catch((err) => console.error("Add error:", err));
    });
  });
}

// ---------- Quantity Listeners ----------
function initQuantityInputs() {
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
}

// ---------- Init ----------
document.addEventListener("DOMContentLoaded", function () {
  initAddToCart();
  initQuantityInputs();
});
