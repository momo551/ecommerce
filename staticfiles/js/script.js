// Custom JavaScript for the fashion site
console.log("Script loaded");

// Update item total price on quantity change
function updateItemTotal(productId, quantity, unitPrice) {
  console.log("updateItemTotal called with:", productId, quantity, unitPrice);
  const qty = parseInt(quantity);
  const price = parseFloat(unitPrice);
  const total = qty * price;
  console.log("Calculated total:", total);
  const itemTotalElement = document.getElementById(`item-total-${productId}`);
  if (itemTotalElement) {
    itemTotalElement.textContent = `$${total.toFixed(2)}`;
    console.log("Updated item total element");
  } else {
    console.log("Item total element not found:", `item-total-${productId}`);
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
  document.getElementById(
    "overall-total"
  ).textContent = `$${overallTotal.toFixed(2)}`;
}

// Update cart quantity
function updateCartQuantity(productId, quantity) {
  console.log("updateCartQuantity called with:", productId, quantity);
  const csrfToken = getCookie("csrftoken");
  console.log("CSRF token:", csrfToken);
  fetch(`/cart/update/${productId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "X-Requested-With": "XMLHttpRequest",
    },
    body: new URLSearchParams({ quantity: quantity }),
  })
    .then((response) => {
      console.log("Response status:", response.status);
      return response.json();
    })
    .then((data) => {
      console.log("Response data:", data);
      if (data.success) {
        // Update the quantity display
        document.getElementById(`quantity-${productId}`).value = quantity;
        // Update the total price
        document.getElementById("overall-total").textContent = data.total_price;
        // Show success message
        alert("Cart updated successfully!");
      } else {
        alert("Error updating cart: " + data.error);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error updating cart");
    });
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

// Add to cart functionality
function addToCart(productId) {
  const csrfToken = getCookie("csrftoken");
  console.log("CSRF_TOKEN:", csrfToken);
  console.log("Sending request to:", `/cart/add/${productId}/`);
  fetch(`/cart/add/${productId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "X-Requested-With": "XMLHttpRequest",
    },
    body: new URLSearchParams({ quantity: 1 }),
  })
    .then((response) => {
      console.log("Response status:", response.status);
      return response.json();
    })
    .then((data) => {
      console.log("Response data:", data);
      if (data.success) {
        // Update cart count in navbar
        const cartCount = document.getElementById("cart-count");
        if (cartCount) {
          cartCount.textContent = data.cart_items_count;
        }
        // Show success message
        alert("Product added to cart successfully!");
      } else {
        alert("Error adding to cart: " + data.error);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error adding to cart");
    });
}

// Document ready
document.addEventListener("DOMContentLoaded", function () {
  // Add event listeners to all "Add to Cart" buttons
  const addToCartButtons = document.querySelectorAll(".btn-cart");
  console.log("Found buttons:", addToCartButtons.length);
  addToCartButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const productId = this.getAttribute("data-product-id");
      console.log("Button clicked, productId:", productId);
      if (productId) {
        addToCart(productId);
      }
    });
  });

  // Add event listeners to quantity inputs for automatic price update
  const quantityInputs = document.querySelectorAll('input[id^="quantity-"]');
  console.log("Found quantity inputs:", quantityInputs.length);
  quantityInputs.forEach((input, index) => {
    console.log(
      `Attaching listener to input ${index}:`,
      input.id,
      "data-product-id:",
      input.getAttribute("data-product-id"),
      "data-unit-price:",
      input.getAttribute("data-unit-price")
    );
    input.addEventListener("input", function () {
      const productId = this.getAttribute("data-product-id");
      const unitPrice = parseFloat(this.getAttribute("data-unit-price"));
      const quantity = this.value;
      console.log("Quantity changed:", productId, quantity, unitPrice);
      updateItemTotal(productId, quantity, unitPrice);
    });
  });

  console.log("Fashion site loaded");
});
