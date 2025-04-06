// In your script.js
// console.log("this is working");

// Initialize cart
if (localStorage.getItem('cart') == null) {
    var cart = {};
} else {
    cart = JSON.parse(localStorage.getItem('cart'));
    updateCartDisplay();
}

// Add to cart function
$(document).on('click', '.atc', function () {
    let itemId = this.id.toString();

    if (cart[itemId] != null) {
        cart[itemId] += 1;
    } else { 
        cart[itemId] = 1; 
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartDisplay();
});

// Update cart display function
function updateCartDisplay() {
    const cartCount = Object.keys(cart).length;
    const cartButton = document.getElementById("items");
    
    // Update button text
    cartButton.innerHTML = `Cart(${cartCount})`;
    
    // Update popover content
    const popover = bootstrap.Popover.getInstance(cartButton);
    if (popover) {
        popover.setContent({
            '.popover-body': cartCount === 0 
                ? 'Your cart is empty' 
                : `${cartCount} items in cart`
        });
    }
}

// Initialize popovers after DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Initialize cart display
    updateCartDisplay();
});