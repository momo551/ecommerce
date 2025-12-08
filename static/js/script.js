// Custom JavaScript for the fashion site

// Update item total price on quantity change
function updateItemTotal(productId, quantity, unitPrice) {
  const qty = parseInt(quantity);
  const price = parseFloat(unitPrice);
  const total = qty * price;
  const itemTotalElement = document.getElementById(`item-total-${productId}`);
  if (itemTotalElement) {
    itemTotalElement.textContent = `$${total.toFixed(2)}`;
  }
  updateOverallTotal();
}

// Update overall cart total
function updateOverallTotal() {
  let overallTotal = 0;
  const itemTotals = document.querySelectorAll('[id^="item-total-"]');
  itemTotals.forEach((item) => {
    const totalText = item.textContent.replace("$", "");
    overallTotal += parseFloat(totalText);
  });
  const totalEl = document.getElementById("overall-total");
  if (totalEl) totalEl.textContent = `$${overallTotal.toFixed(2)}`;
}

// Update cart quantity
function updateCartQuantity(productId, quantity) {
  const csrfToken = getCookie("csrftoken");

  fetch(`/cart/update/${productId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "X-Requested-With": "XMLHttpRequest",
    },
    body: new URLSearchParams({ quantity: quantity }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById(`quantity-${productId}`).value = quantity;
        const overall = document.getElementById("overall-total");
        if (overall) overall.textContent = data.total_price;
      }
    })
    .catch((error) => console.error("Error:", error));
}

// Get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// --- Silent Add to Cart ---
document.addEventListener("DOMContentLoaded", function () {
  const addToCartBtn = document.querySelector(".btn-cart");

  if (addToCartBtn) {
    addToCartBtn.addEventListener("click", function (e) {
      e.preventDefault(); // امنع الـ submit العادي

      const form = this.closest("form");
      const productId = this.getAttribute("data-product-id");
      const formData = new FormData(form);

      fetch(`/cart/add/${productId}/`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          // مفيش رسائل أو alert نهائيًا
          console.log("Product added silently.");
        })
        .catch((error) => console.error("Error:", error));
    });
  }

  // Add event listeners to quantity inputs
  const quantityInputs = document.querySelectorAll('input[id^="quantity-"]');
  quantityInputs.forEach((input) => {
    input.addEventListener("input", function () {
      const productId = this.getAttribute("data-product-id");
      const unitPrice = parseFloat(this.getAttribute("data-unit-price"));
      const quantity = this.value;
      updateItemTotal(productId, quantity, unitPrice);
    });
  });
});
