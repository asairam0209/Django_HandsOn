// script.js
console.log("Testing workability");

let cart = JSON.parse(localStorage.getItem('cart')) || {};

// Add to cart function
$(document).on('click', '.atc', function () {
    const itemId = this.id.toString();
    cart[itemId] = (cart[itemId] || 0) + 1;
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartDisplay();
});

// initializing the popover
function initPopover() {
    new bootstrap.Popover(document.getElementById('cart'), {
        html: true, placement: 'bottom', title: 'Your Cart', content: generatePopoverContent(), trigger: 'click'
    });
}

// generating the Popover content
function generatePopoverContent() {
    if (Object.keys(cart).length === 0) return 'Your cart is empty';

    return `
        <div class="cart-items-list">
            ${Object.entries(cart).map(([id, qty], cartIndex) => {
                const productNameElement = document.getElementById(`name-${id}`);
                const productName = productNameElement 
                    ? productNameElement.textContent 
                    : `Item ${id}`;  // Fallback if name not found
                
                
                return `
                    <div class="cart-item d-flex justify-content-between py-2">
                    <span class="text-muted me-2">${cartIndex + 1}.</span>
                        <span>$${productName}</span>
                        <span>Qty: ${qty}</span>

                        
                    </div>  
                `;
            }).join('')}
            <a href="/checkout" class="btn btn-warning" id="checkout">Checkout</a>
        </div>
    `;
}

//updating the popover
function updateCartDisplay() {
    const cartButton = document.getElementById('cart');
    const itemCount = Object.values(cart).reduce((a, b) => a + b, 0)

    // displaying the cart amount
    cartButton.innerHTML = `Cart(${itemCount})`;

    // setting the drop down
    const popover = bootstrap.Popover.getInstance(cartButton);
    if (popover) {
        popover.setContent({
            '.popover-body': generatePopoverContent()
        });
    }
}

// load the popover once the DOM is fully loaded

document.addEventListener('DOMContentLoaded', () => {
    initPopover();
    updateCartDisplay();
})