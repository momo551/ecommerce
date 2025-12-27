// ===============================
// Django AJAX Forms + Cart
// ===============================

// ---------- CSRF ----------
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}
// استخدم window.CSRF_TOKEN أولًا لتجنب 403
const csrftoken = window.CSRF_TOKEN || getCookie("csrftoken");

// ---------- Generic AJAX Form Handler ----------
function handleAjaxForm(formId, onSuccess=null) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener("submit", function(e){
        e.preventDefault();
        const formData = new FormData(form);

        fetch(form.action || window.location.href, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            // مسح الأخطاء القديمة
            form.querySelectorAll(".text-danger").forEach(el => el.textContent = "");

            if(data.success) {
                if(onSuccess) onSuccess(data);
                else if(data.redirect_url) window.location.href = data.redirect_url;
                else if(data.message) alert(data.message);
            } else if(data.errors) {
                // عرض الأخطاء لكل حقل
                for(const [field, messages] of Object.entries(data.errors)) {
                    const el = document.getElementById(`error-${field}`);
                    if(el) el.textContent = messages.join(", ");
                }
            }
        })
        .catch(err => console.error(`Form ${formId} error:`, err));
    });
}

// ---------- Cart Functions ----------
function initCart() {
    // تعديل الكميات
    document.querySelectorAll('input[id^="quantity-"]').forEach(input => {
        input.addEventListener("change", function(){
            const productId = this.dataset.productId;
            const unitPrice = this.dataset.unitPrice;
            let quantity = parseInt(this.value);
            if(isNaN(quantity) || quantity < 1) quantity = 1;
            this.value = quantity;
            updateItemTotal(productId, quantity, unitPrice);
            updateCartQuantity(productId, quantity);
        });
    });

    // إضافة إلى السلة
    document.querySelectorAll(".btn-cart").forEach(btn => {
        btn.addEventListener("click", function(e){
            e.preventDefault();
            const form = this.closest("form");
            const productId = this.dataset.productId;
            const formData = new FormData(form);

            fetch(`/cart/add/${productId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData
            })
            .then(res => res.json())
            .then(() => {
                window.location.href="/cart/"; // أو عرض رسالة AJAX بدون إعادة تحميل
            })
            .catch(err => console.error("Add to cart error:", err));
        });
    });
}

// ---------- Cart Total ----------
function updateItemTotal(productId, quantity, unitPrice){
    const total = quantity * parseFloat(unitPrice || 0);
    const itemEl = document.getElementById(`item-total-${productId}`);
    if(itemEl) itemEl.textContent = `$${total.toFixed(2)}`;
    updateOverallTotal();
}

function updateOverallTotal(){
    let overall = 0;
    document.querySelectorAll('[id^="item-total-"]').forEach(item => {
        const val = parseFloat(item.textContent.replace("$",""));
        if(!isNaN(val)) overall += val;
    });
    const overallEl = document.getElementById("overall-total");
    if(overallEl) overallEl.textContent = `$${overall.toFixed(2)}`;
}

function updateCartQuantity(productId, quantity){
    fetch(`/cart/update/${productId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
        },
        body: new URLSearchParams({quantity})
    })
    .then(res => res.json())
    .then(data => {
        if(data.success && data.total_price){
            const overallEl = document.getElementById("overall-total");
            if(overallEl) overallEl.textContent = data.total_price;
        }
    })
    .catch(err => console.error("Update cart error:", err));
}

// ---------- Initialize ----------
document.addEventListener("DOMContentLoaded", function(){
    // AJAX login / register
    handleAjaxForm("login-form", data => window.location.href=data.redirect_url || '/');
    handleAjaxForm("register-form", data => window.location.href=data.redirect_url || '/');
    // AJAX profile update
    handleAjaxForm("profile-form", data => {
        if(data.success) {
            alert('Profile updated successfully!');
            if(data.updated_fields_html) {
                // يمكن تحديث الحقول المعروضة في الصفحة مباشرة إذا أرسل السيرفر HTML
                document.querySelector("#profile-container").innerHTML = data.updated_fields_html;
            }
        }
    });

    // Cart
    initCart();
});
