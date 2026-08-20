/**
 * AYL Cart Drawer JS
 * Handles all AJAX cart operations and Drawer UI interactions
 */

class AylCartDrawer {
  constructor() {
    this.drawer = document.getElementById('ayl-cart-drawer');
    this.overlay = document.getElementById('ayl-cart-drawer-overlay');
    this.closeBtn = document.querySelector('.ayl-cart-drawer__close');
    this.itemsContainer = document.getElementById('ayl-cart-drawer-items');
    this.totalPriceElem = document.querySelector('.ayl-cart-total-price');
    this.itemCountElem = document.querySelector('.ayl-cart-item-count');
    
    this.init();
  }

  init() {
    if (!this.drawer) return;

    // Attach Close events
    this.closeBtn.addEventListener('click', () => this.close());
    this.overlay.addEventListener('click', () => this.close());

    // Delegate events for removal and quantity changes
    this.drawer.addEventListener('click', (e) => {
      if (e.target.classList.contains('ayl-cart-item__remove')) {
        this.removeItem(e.target.dataset.id);
      }
      if (e.target.classList.contains('ayl-qty-btn')) {
        const id = e.target.dataset.id;
        const input = e.target.parentElement.querySelector('.ayl-qty-input');
        let val = parseInt(input.value);
        if (e.target.classList.contains('plus')) val++;
        else if (e.target.classList.contains('minus')) val--;
        
        if (val >= 0) this.updateQuantity(id, val);
      }
    });

    // Listen for custom add-to-cart success events
    window.addEventListener('ayl:cart:open', () => this.open());

    // Universal Interceptor for Add to Cart (Desktop Only)
    // Uses capture phase to bypass other scripts
    const interceptATC = (e) => {
      if (window.innerWidth < 992) return;

      let form = null;
      let target = e.target;

      if (e.type === 'submit') {
        form = target;
      } else if (e.type === 'click') {
        const btn = target.closest('.add-cart-btn, .ayl-main-add-btn, .ayl-btn-atc, [name="add"], .btn-add-to-cart, .add-to-cart-btn');
        if (btn) form = btn.closest('form');
      }

      if (form) {
        const action = form.getAttribute('action') || '';
        if (action.includes('/cart/add')) {
          console.log('Intercepting Add to Cart:', action);
          e.preventDefault();
          e.stopPropagation();
          e.stopImmediatePropagation();
          this.handleAjaxSubmit(form);
        }
      }
    };

    document.addEventListener('submit', interceptATC, true);
    document.addEventListener('click', interceptATC, true);
  }

  handleAjaxSubmit(form) {
    const formData = new FormData(form);
    this.setLoading(true);

    fetch('/cart/add.js', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(item => {
      console.log('Item added successfully:', item);
      this.refresh();
      this.open();
      this.setLoading(false);
    })
    .catch(error => {
      console.error('AJAX Add to Cart failed:', error);
      this.setLoading(false);
      // Fallback only if absolutely necessary
      if (!window.location.pathname.includes('/cart')) {
         this.refresh();
         this.open();
      }
    });
  }

  toggle() {
    if (this.drawer.classList.contains('is-visible')) {
      this.close();
    } else {
      this.open();
    }
  }

  open() {
    if (window.innerWidth < 992) return;
    this.refresh();
    this.drawer.classList.add('is-visible');
    this.overlay.classList.add('is-visible');
    document.body.style.overflow = 'hidden';
  }

  close() {
    this.drawer.classList.remove('is-visible');
    this.overlay.classList.remove('is-visible');
    document.body.style.overflow = '';
  }

  refresh() {
    fetch('/cart.js')
      .then(response => response.json())
      .then(cart => {
        this.updateUI(cart);
      });
  }

  updateQuantity(id, qty) {
    this.setLoading(true);
    fetch('/cart/change.js', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: id, quantity: qty })
    })
    .then(response => response.json())
    .then(cart => {
      this.updateUI(cart);
      this.setLoading(false);
    })
    .catch(err => {
      console.error('Error updating quantity:', err);
      this.setLoading(false);
    });
  }

  removeItem(id) {
    this.updateQuantity(id, 0);
  }

  setLoading(state) {
    if (state) this.drawer.classList.add('is-loading');
    else this.drawer.classList.remove('is-loading');
  }

  updateUI(cart) {
    const count = cart.item_count;
    if (this.itemCountElem) this.itemCountElem.innerText = count;
    
    const globalCounts = document.querySelectorAll('.cart-products-count, .ml-cart-count, .site-header__cart-count');
    globalCounts.forEach(el => {
        el.innerText = count;
        el.style.display = count > 0 ? 'flex' : 'none';
    });

    if (this.totalPriceElem) {
      this.totalPriceElem.innerText = Shopify.formatMoney(cart.total_price, window.money_format);
    }

    if (count === 0) {
      this.itemsContainer.innerHTML = '<div class="ayl-cart-drawer__empty"><p>Tu bolsa está vacía.</p><a href="/collections/all" class="btn">Continuar comprando</a></div>';
      const footer = document.querySelector('.ayl-cart-drawer__footer');
      if (footer) footer.style.display = 'none';
      return;
    } else {
      const footer = document.querySelector('.ayl-cart-drawer__footer');
      if (footer) footer.style.display = 'block';
    }

    let itemsHtml = '';
    cart.items.forEach(item => {
      itemsHtml += `
        <div class="ayl-cart-item" data-id="${item.key}">
          <div class="ayl-cart-item__image">
            <a href="${item.url}">
              <img src="${item.image}" alt="${item.title}" loading="lazy">
            </a>
          </div>
          <div class="ayl-cart-item__content">
            <div class="ayl-cart-item__header">
              <div class="ayl-cart-item__tags">NUEVA COLECCIÓN</div>
              <a href="${item.url}" class="ayl-cart-item__title">${item.product_title}</a>
              <button type="button" class="ayl-cart-item__remove" data-id="${item.key}">Eliminar</button>
            </div>
            <div class="ayl-cart-item__details">
              ${item.variant_title ? `<div class="ayl-cart-item__option"><span class="ayl-cart-item__option-value">${item.variant_title}</span></div>` : ''}
            </div>
            <div class="ayl-cart-item__footer">
              <div class="ayl-qty-btn-wrap ayl-cart-item__qty">
                <button type="button" class="ayl-qty-btn minus" data-id="${item.key}">-</button>
                <input type="number" class="ayl-qty-input" value="${item.quantity}" min="0" data-id="${item.key}" readonly>
                <button type="button" class="ayl-qty-btn plus" data-id="${item.key}">+</button>
              </div>
              <div class="ayl-cart-item__price">
                ${Shopify.formatMoney(item.line_price, window.money_format)}
              </div>
            </div>
          </div>
        </div>
      `;
    });
    this.itemsContainer.innerHTML = itemsHtml;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.aylCartDrawer = new AylCartDrawer();
});
