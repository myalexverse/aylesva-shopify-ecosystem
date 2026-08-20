(function(e) {   
  e(document).ready(function(){
    initHeaderSticky();
  });
  e(window).resize(function() {
    initHeaderSticky();
  });
  e(window).scroll(function() {
    initHeaderSticky();
  });
  function initHeaderSticky(){
    if(jQuery(document).height() > jQuery(window).height()){
      if (jQuery(window).width() > 1199){
        if(jQuery('.menu-bar').hasClass("sticky_header") || jQuery('.header_3 .full-header').hasClass("sticky_header")){
          if (jQuery(this).scrollTop() > 600)
          {    
            jQuery('.menu-bar,.header_3 .full-header').addClass("fixed");
            jQuery('.header_1 .full-header .myaccount').insertAfter('.header_1 .menu-bar .header-middle');
            
            jQuery('.header_1 .full-header .header-right').insertBefore('.header_1 .menu-bar .myaccount');	  


            jQuery('.header_1 .full-header .header-left').insertBefore('.header_1 .menu-bar .tt-mega-menu');	
            jQuery('.header_2 .full-header .header-left').insertBefore('.header_2 .menu-bar .ttresponsive_menu-wrap');	
            
            jQuery('.header_2 .full-header .wishlist-icon-div').insertAfter('.header_2 .menu-bar .topmenu');              
            jQuery('.header_2 .full-header .compare-icon-div').insertAfter('.header_2 .menu-bar .wishlist-icon-div'); 
            jQuery('.header_2 .full-header .myaccount').insertBefore('.header_2 .menu-bar .wishlist-icon-div');
            jQuery('.header_2 .full-header .header-right').insertBefore('.header_2 .menu-bar .myaccount');
          }else{
            jQuery('.menu-bar,.header_3 .full-header').removeClass("fixed");
            jQuery('.header_1 .menu-bar .myaccount').insertBefore('.header_1 .full-header .topmenu');
            
                        jQuery('.header_1  .sticky_header .header-left').insertBefore('.header_1 .full-header .topmenu');	
                        jQuery('.header_2  .sticky_header .header-left').insertBefore('.header_2 .sticky_header .header-middle');	

            jQuery('.header_1 .menu-bar .header-right').insertBefore('.header_1 .full-header .myaccount');
            jQuery('.header_2 .menu-bar .header-right').insertAfter('.header_2 .full-header .header-middle');
            jQuery('.header_2 .menu-bar .myaccount').insertAfter('.header_2 .full-header .header-right');
            jQuery('.header_2 .menu-bar .wishlist-icon-div').insertAfter('.header_2 .full-header .myaccount');
            jQuery('.header_2 .menu-bar .compare-icon-div').insertAfter('.header_2 .full-header .wishlist-icon-div');
          }
        } else {
          jQuery('.menu-bar,.header_3 .full-header').removeClass("fixed");

                                  jQuery('.header_1  .sticky_header .header-left').insertBefore('.header_1 .full-header  .topmenu');	
                                  jQuery('.header_2  .sticky_header .header-left').insertBefore('.header_2 .sticky_header .header-middle');	


          
          jQuery('.header_1 .menu-bar .myaccount').insertBefore('.header_1 .full-header .topmenu');
          jQuery('.header_1 .menu-bar .header-right').insertBefore('.header_1 .full-header .myaccount');
          jQuery('.header_2 .menu-bar .header-right').insertAfter('.header_2 .full-header .header-middle');
          jQuery('.header_2 .menu-bar .myaccount').insertAfter('.header_2 .full-header .header-right');
          jQuery('.header_2 .menu-bar .wishlist-icon-div').insertAfter('.header_2 .full-header .myaccount');
          jQuery('.header_2 .menu-bar .compare-icon-div').insertAfter('.header_2 .full-header .wishlist-icon-div');
        }

      }else{
        jQuery('.menu-bar,.header_3 .full-header').removeClass('fixed');
      }   
    }
  }

  var cookieName = "ttwishlistList";

   

  

  e(document).ready(function() {
    t.init()
    t.closeQuickViewPopup();
  });


  e(document).on("click", function(n) {   
    var r = e(".quick-view");
    var i = e("#slidedown-cart");
    var s = e(".site-header_cart_link");
    var o = e("#email-modal .modal-window");

    if (!r.is(n.target) && r.has(n.target).length === 0 && !i.is(n.target) && i.has(n.target).length === 0 && !s.is(n.target) && s.has(n.target).length === 0 && !o.is(n.target) && o.has(n.target).length === 0 ) {
      t.closeQuickViewPopup();                             
    }
    if (!r.is(n.target) && r.has(n.target).length === 0 && !i.is(n.target) && i.has(n.target).length === 0 && !s.is(n.target) && s.has(n.target).length === 0 && !o.is(n.target) && o.has(n.target).length === 0 ) {            
      t.closeDropdownCart();
      t.closeEmailModalWindow();

    }
  })


  var t = {
    KidsTimeout: null,
    isSidebarAjaxClick: false,
    init: function() {    
      this.initQuickView();
      this.initAddToCart();
      this.initAddToCarts();
      this.initModal();
      this.initShortcode();
      this.productAccordion();
      this.productCompact();
      this.initProductAddToCart();
      
      this.initWishlist(); 
      this.initcompare();
      this.initProductMoreview();
      this.producteffect();
      this.initSidebar();
      this.initColorSwatchGrid();  
      this.initInfiniteScrolling();
      this.FacetFiltersForm();
    },
    FacetFiltersForm: function() {
      class FacetFiltersForm extends HTMLElement {
        constructor() {
          super();
          this.onActiveFilterClick = this.onActiveFilterClick.bind(this);
          this.debouncedOnSubmit = debounce((event) => {
            this.onSubmitHandler(event);
          }, 500);

          this.querySelector('form').addEventListener('input', this.debouncedOnSubmit.bind(this));

          const facetWrapper = this.querySelector('#FacetsWrapperDesktop');
          if (facetWrapper) facetWrapper.addEventListener('keyup', onKeyUpEscape);
        }

        static setListeners() {
          const onHistoryChange = (event) => {
            const searchParams = event.state ? event.state.searchParams : FacetFiltersForm.searchParamsInitial;
            if (searchParams === FacetFiltersForm.searchParamsPrev) return;
            FacetFiltersForm.renderPage(searchParams, null, false);
          }
          window.addEventListener('popstate', onHistoryChange);
        }

        static toggleActiveFacets(disable = true) {
          document.querySelectorAll('.js-facet-remove').forEach((element) => {
            element.classList.toggle('disabled', disable);
          });
        }

        static renderPage(searchParams, event, updateURLHash = true) {
          FacetFiltersForm.searchParamsPrev = searchParams;
          const sections = FacetFiltersForm.getSections();
          const countContainer = document.getElementById('ProductCount');
          const countContainerDesktop = document.getElementById('ProductCountDesktop');
          document.getElementById('ProductGridContainer').querySelector('.collection_template').classList.add('loading');
          if (countContainer){
            countContainer.classList.add('loading');
          }    
          if (countContainerDesktop){
            countContainerDesktop.classList.add('loading');
          }

          sections.forEach((section) => {
            const url = `${window.location.pathname}?section_id=${section.section}&${searchParams}`;
            const filterDataUrl = element => element.url === url;

            FacetFiltersForm.filterData.some(filterDataUrl) ?
              FacetFiltersForm.renderSectionFromCache(filterDataUrl, event) :
            FacetFiltersForm.renderSectionFromFetch(url, event);
          });

          if (updateURLHash) FacetFiltersForm.updateURLHash(searchParams);
        }

        static renderSectionFromFetch(url, event) {
          fetch(url)
          .then(response => response.text())
          .then((responseText) => {
            const html = responseText;
            FacetFiltersForm.filterData = [...FacetFiltersForm.filterData, { html, url }];
            FacetFiltersForm.renderFilters(html, event);
            FacetFiltersForm.renderProductGridContainer(html);
            //FacetFiltersForm.renderProductCount(html); 
            t.sidebarMapView();
            t.initAddToCart();
            t.sidebarMapShow();
            jQuery(".filter-left").on("click" , function(e){
              e.preventDefault();
              jQuery(this).toggleClass("active");
              jQuery(".off-canvas.position-left").addClass("is-open");
              jQuery(".js-off-canvas-overlay.is-overlay-fixed").addClass("is-visible is-closable");
            });
            jQuery(".filter-right").on("click" , function(e){
              e.preventDefault();
              jQuery(this).toggleClass("active");
              jQuery(".off-canvas.position-right").addClass("is-open");
              jQuery(".js-off-canvas-overlay.is-overlay-fixed").addClass("is-visible is-closable");
            });
            jQuery(".off-canvas .sidebar_close").on("click" , function(e){
              e.preventDefault();
              jQuery(".off-canvas.position-left").removeClass("is-open");
              jQuery(".off-canvas.position-right").removeClass("is-open");
              jQuery(".js-off-canvas-overlay.is-overlay-fixed").removeClass("is-visible is-closable");
            });
            jQuery(".is-overlay-fixed").on("click" , function(e){
              e.preventDefault();
              jQuery(".filter-left").trigger('click');
              jQuery(".filter-right").trigger('click');
              jQuery(".off-canvas.position-left").removeClass("is-open");
              jQuery(".off-canvas.position-right").removeClass("is-open");
              jQuery(".js-off-canvas-overlay.is-overlay-fixed").removeClass("is-visible is-closable");
            });
            jQuery(".filter-toggle").on("click" , function(e){
              e.preventDefault();
              jQuery(this).toggleClass("active");
              jQuery(".filter-toggle-wrap").slideToggle("is-visible");
            })
            if ($(".spr-badges").length > 0) {
              return window.SPR.registerCallbacks(), window.SPR.initRatingHandler(), window.SPR.initDomEls(), window.SPR.loadProducts(), window.SPR.loadBadges()
            };
          });
        }
        static renderSectionFromCache(filterDataUrl, event) {
          const html = FacetFiltersForm.filterData.find(filterDataUrl).html;
          FacetFiltersForm.renderFilters(html, event);
          FacetFiltersForm.renderProductGridContainer(html);
          //FacetFiltersForm.renderProductCount(html);
          t.sidebarMapView();
          t.initAddToCart();
          t.sidebarMapShow();
          jQuery(".filter-left").on("click" , function(e){
            e.preventDefault();
            jQuery(this).toggleClass("active");
            jQuery(".off-canvas.position-left").addClass("is-open");
            jQuery(".js-off-canvas-overlay.is-overlay-fixed").addClass("is-visible is-closable");
          });
          jQuery(".filter-right").on("click" , function(e){
            e.preventDefault();
            jQuery(this).toggleClass("active");
            jQuery(".off-canvas.position-right").addClass("is-open");
            jQuery(".js-off-canvas-overlay.is-overlay-fixed").addClass("is-visible is-closable");
          });
          jQuery(".off-canvas .sidebar_close").on("click" , function(e){
            e.preventDefault();
            jQuery(".off-canvas.position-left").removeClass("is-open");
            jQuery(".off-canvas.position-right").removeClass("is-open");
            jQuery(".js-off-canvas-overlay.is-overlay-fixed").removeClass("is-visible is-closable");
          });
          jQuery(".is-overlay-fixed").on("click" , function(e){
            e.preventDefault();
            jQuery(".filter-left").trigger('click');
            jQuery(".filter-right").trigger('click');
            jQuery(".off-canvas.position-left").removeClass("is-open");
            jQuery(".off-canvas.position-right").removeClass("is-open");
            jQuery(".js-off-canvas-overlay.is-overlay-fixed").removeClass("is-visible is-closable");
          });
          jQuery(".filter-toggle").on("click" , function(e){
            e.preventDefault();
            jQuery(this).toggleClass("active");
            jQuery(".filter-toggle-wrap").slideToggle("is-visible");
          })
          if ($(".spr-badges").length > 0) {
            return window.SPR.registerCallbacks(), window.SPR.initRatingHandler(), window.SPR.initDomEls(), window.SPR.loadProducts(), window.SPR.loadBadges()
          };
        }

        static renderProductGridContainer(html) {
          document.getElementById('ProductGridContainer').innerHTML = new DOMParser().parseFromString(html, 'text/html').getElementById('ProductGridContainer').innerHTML;
        }

        //   static renderProductCount(html) {
        //     const count = new DOMParser().parseFromString(html, 'text/html').getElementById('ProductCount').innerHTML
        //     const container = document.getElementById('ProductCount');
        //     const containerDesktop = document.getElementById('ProductCountDesktop');
        //     container.innerHTML = count;
        //     container.classList.remove('loading');
        //     if (containerDesktop) {
        //       containerDesktop.innerHTML = count;
        //       containerDesktop.classList.remove('loading');
        //     }
        //   }

        static renderFilters(html, event) {
          const parsedHTML = new DOMParser().parseFromString(html, 'text/html');

          const facetDetailsElements =
                parsedHTML.querySelectorAll('#FacetFiltersForm .js-filter, #FacetFiltersFormMobile .js-filter');
          const matchesIndex = (element) => { 
            const jsFilter = event ? event.target.closest('.js-filter') : undefined;
            return jsFilter ? element.dataset.index === jsFilter.dataset.index : false; 
          }
          const facetsToRender = Array.from(facetDetailsElements).filter(element => !matchesIndex(element));
          const countsToRender = Array.from(facetDetailsElements).find(matchesIndex);

          facetsToRender.forEach((element) => {
            document.querySelector(`.js-filter[data-index="${element.dataset.index}"]`).innerHTML = element.innerHTML;
          });

          FacetFiltersForm.renderActiveFacets(parsedHTML);
          FacetFiltersForm.renderAdditionalElements(parsedHTML);

          if (countsToRender) FacetFiltersForm.renderCounts(countsToRender, event.target.closest('.js-filter'));
        }

        static renderActiveFacets(html) {
          const activeFacetElementSelectors = ['.active-facets-mobile', '.active-facets-desktop'];

          activeFacetElementSelectors.forEach((selector) => {
            const activeFacetsElement = html.querySelector(selector);
            if (!activeFacetsElement) return;
            document.querySelector(selector).innerHTML = activeFacetsElement.innerHTML;
          })

          FacetFiltersForm.toggleActiveFacets(false);
        }

        static renderAdditionalElements(html) {
          const mobileElementSelectors = ['.mobile-facets__open', '.mobile-facets__count', '.sorting'];

          mobileElementSelectors.forEach((selector) => {
            if (!html.querySelector(selector)) return;
            document.querySelector(selector).innerHTML = html.querySelector(selector).innerHTML;
          });

          document.getElementById('FacetFiltersFormMobile').closest('menu-drawer').bindEvents();
        }

        static renderCounts(source, target) {
          const targetElement = target.querySelector('.facets__selected');
          const sourceElement = source.querySelector('.facets__selected');

          if (sourceElement && targetElement) {
            target.querySelector('.facets__selected').outerHTML = source.querySelector('.facets__selected').outerHTML;
          }
        }

        static updateURLHash(searchParams) {
          history.pushState({ searchParams }, '', `${window.location.pathname}${searchParams && '?'.concat(searchParams)}`);
        }

        static getSections() {
          return [
            {
              section: document.getElementById('product-grid').dataset.id,
            }
          ]
        }

        onSubmitHandler(event) {
          event.preventDefault();
          const formData = new FormData(event.target.closest('form'));
          const searchParams = new URLSearchParams(formData).toString();
          FacetFiltersForm.renderPage(searchParams, event);
        }

        onActiveFilterClick(event) {
          event.preventDefault();
          FacetFiltersForm.toggleActiveFacets();
          FacetFiltersForm.renderPage(new URL(event.currentTarget.href).searchParams.toString());
          t.sidebarMapView();
          t.initAddToCart();
        }
      }

      FacetFiltersForm.filterData = [];
      FacetFiltersForm.searchParamsInitial = window.location.search.slice(1);
      FacetFiltersForm.searchParamsPrev = window.location.search.slice(1);
      customElements.define('facet-filters-form', FacetFiltersForm);
      FacetFiltersForm.setListeners();

      class PriceRange extends HTMLElement {
        constructor() {
          super();
          this.querySelectorAll('input')
          .forEach(element => element.addEventListener('change', this.onRangeChange.bind(this)));

          this.setMinAndMaxValues();
        }

        onRangeChange(event) {
          this.adjustToValidValues(event.currentTarget);
          this.setMinAndMaxValues();
        }

        setMinAndMaxValues() {
          const inputs = this.querySelectorAll('input');
          const minInput = inputs[0];
          const maxInput = inputs[1];
          if (maxInput.value) minInput.setAttribute('max', maxInput.value);
          if (minInput.value) maxInput.setAttribute('min', minInput.value);
          if (minInput.value === '') maxInput.setAttribute('min', 0);
          if (maxInput.value === '') minInput.setAttribute('max', maxInput.getAttribute('max'));
        }

        adjustToValidValues(input) {
          const value = Number(input.value);
          const min = Number(input.getAttribute('min'));
          const max = Number(input.getAttribute('max'));

          if (value < min) input.value = min;
          if (value > max) input.value = max;
        }
      }

      customElements.define('price-range', PriceRange);

      class FacetRemove extends HTMLElement {
        constructor() {
          super();
          this.querySelector('a').addEventListener('click', (event) => {
            event.preventDefault();
            const form = this.closest('facet-filters-form') || document.querySelector('facet-filters-form');
            form.onActiveFilterClick(event);
          });
        }
      }
      customElements.define('facet-remove', FacetRemove);
    },
          initColorSwatchGrid: function() {
      jQuery('.item-swatch li label,.product-size li label').click(function(){                   
        var newImage = jQuery(this).parent().find('.hidden img').attr('src');
        jQuery(this).closest('ul').find('.active').removeClass('active');
        jQuery(this).parent().addClass('active');
        jQuery(this).closest('.product-wrapper').find('.featured-image').attr({ src: newImage }); 
        return false;
      });

                  jQuery('.item-swatch li label,.product-size li label').on('click', function(e){
        e.preventDefault();    
        jQuery(this).closest('ul').find('.active').removeClass('active');
        jQuery(this).parent().addClass('active');
        var productImage = jQuery(this).parents('.product-wrapper').find('.product-t'); 
        productImage.find('img.featured-image').attr('src', jQuery(this).data('image'));  
      });

 //================================================================================================================================================================= 

      
      jQuery('.item-swatch li label').on('click', function(e){
        e.preventDefault();  
        var productImage = jQuery(this).parents('.product-wrapper').find('.product-t'); 
        productImage.find('img.featured-image').attr('src', jQuery(this).data('image')); 
      });
      jQuery('.item-swatch li label').on('click', function(e){
        e.preventDefault();  
        var productImage = jQuery(this).parents('.product-wrapper').find('.grid-view-item__link'); 
        productImage.find('img.featured-image').attr('src', jQuery(this).data('image')); 
      });
      jQuery('.item-swatch li label').on('click', function(e){
        e.preventDefault();  
        var productPrice = jQuery(this).parents('.product-wrapper').find('.grid-view-item__meta .product-price__sale'); 
        productPrice.find('.money').attr('data-currency-usd', jQuery(this).data('price')); 
      });
    },

    initWishlist: function() {
      t.updateWishlistButtons()
      t.initWishlistButtons()
    },
    initcompare: function() {
      t.initcompareButtons();  
    },
    initWishlistButtons: function() {
      if(e(".add-in-wishlist-js").length == 0) {
        return false;
      }
      e(".add-in-wishlist-js").each(function(){
        e(this).unbind();
        e(this).click(function(event){
          event.preventDefault();
          try
          {
            var id = e(this).attr('href');
            if(e.cookie(cookieName) == null) {
              var str = id;
            } else {
              if(e.cookie(cookieName).indexOf(id) == -1) {
                var str = e.cookie(cookieName) + '__' + id;
              }
            }
            e.cookie(cookieName, str, {expires:14, path:'/'});


            jQuery('.default-wishbutton-'+id).find('i').addClass('mdi-spin mdi-refresh').removeClass('mdi-heart-outline');
            if(e(this).closest('.product-information').length > 0){                 
              setTimeout(function(){
                jQuery('.loadding-wishbutton-'+id).remove(); jQuery('.added-wishbutton-'+id).show();                    
                jQuery('.default-wishbutton-'+id).remove();
              }, 2000);
            }else{
              jQuery('.loadding-wishbutton-'+id).show();
              jQuery('.default-wishbutton-'+id).remove();
              setTimeout(function(){
                jQuery('.loadding-wishbutton-'+id).remove(); jQuery('.added-wishbutton-'+id).show(); 
              }, 2000);
            }
            e(this).unbind();
          }
          catch (err) {} // ignore errors reading cookies
        })
      });
    },


    updateWishlistButtons: function() {
      try
      {
        if(e.cookie(cookieName) != null && e.cookie(cookieName) != '__' && e.cookie(cookieName) != '') {
          var str = String(e.cookie(cookieName)).split("__");
          for (var i=0; i<str.length; i++) {
            if (str[i] != '') {
              jQuery('.added-wishbutton-'+str[i]).show();
              jQuery('.default-wishbutton-'+str[i]).remove();
              jQuery('.loadding-wishbutton-'+str[i]).remove();

            }
          }
        }
      }
      catch (err) {}
    },
    initcompareButtons: function() {
      var compareButtonClass = '.add-in-compare-js',
          compareRemoveButtonClass = '.js-remove-compare',
          $compareCount = e('.compare-count'),
          $comparemsg = e('.max_compare'),
          $compareContainer = e('.js-compare-content'),
          compareObject = JSON.parse(localStorage.getItem('localCompare')) || [];

      function updateCompare(self) {
        var productHandle = e(self).data('comparehandle'),
            alertText = '';
        var isAdded = e.inArray(productHandle,compareObject) !== -1 ? true:false;
        if (isAdded) {
          compareObject.splice(compareObject.indexOf(productHandle), 1);
          alertText = "Item removed to the comparison list!";
          jQuery('#modalCompare1').modal();
          $comparemsg.text(alertText);
        }else{
          if (compareObject.length === 3){
            alertText = "Maximum products to compare. Limit is 3!";
            alertClass = 'error';
            jQuery('#modalCompare1').modal();
            $comparemsg.text(alertText);
          }else{
            alertClass = 'notice';
            compareObject.push(productHandle);
            alertText = "Item added to the comparison list!";
            jQuery('#modalCompare1').modal();
            $comparemsg.text(alertText);
          }
        }
        localStorage.setItem('localCompare', JSON.stringify(compareObject)); 
        if(compareObject.length > 0){$compareCount.text('('+ compareObject.length +')');}
      };

      function loadCompare(){
        var compareGrid;
        $compareContainer.html('');
        //popup compare
        if (compareObject.length > 0){
          compareGrid = compareObject.length === 1? 'col-md-6 col-sm-6' : 'col';
          for (var i = 0; i < compareObject.length; i++) { 
            var productHandle = compareObject[i];
            Shopify.getProduct(productHandle,function(product){
              var htmlProduct = '',
                  productPrice = product.price_varies? 'from ' + Shopify.formatMoney(product.price_min, theme.moneyFormat) : Shopify.formatMoney(product.price, theme.moneyFormat),
                  productComparePrice = product.compare_at_price_min !== 0 ? Shopify.formatMoney(product.compare_at_price_min, theme.moneyFormat) : '',
                  productAvailable = product.available ? 'available' : 'unavailable',
                  productAvailableClass = product.available ? 'alert-success' : 'alert-danger',
                  productTypeHTML = product.type !== "" ? '<a href="/collections/types?q='+ product.type +'">'+ product.type +'</a>' : '<span>none</span>',
                  productVendorHTML = product.vendor !== "" ? '<a href="/collections/vendors?q='+ product.vendor +'">'+ product.vendor +'</a>' : '<span>none</span>';
              htmlProduct += '<div class="compare-item '+compareGrid+' col-xs-6">';
              htmlProduct += '	<a href="'+ product.url +'">';
              htmlProduct += '		<img src="'+ Shopify.resizeImage(product.featured_image,'x300') +'"/>';
              htmlProduct += '	</a>';
              htmlProduct += '	<hr /><h5 >'+ product.title +'</h5>';
              htmlProduct += '	<hr /><s>'+ productComparePrice +'</s>';
              htmlProduct += '	<span> '+ productPrice +'</span>';
              htmlProduct += '	<hr /><span class='+ productAvailableClass +'> '+ productAvailable +'</span>';
              htmlProduct += '	<hr />'+ productTypeHTML;
              htmlProduct += '	<hr />'+ productVendorHTML;
              htmlProduct += '  <hr /><button class="btn js-remove-compare btn-theme gradient-theme" data-handle="'+product.handle+'"><i class="mdi mdi-close-circle"></i></button>';
              htmlProduct += '</div>';
              $compareContainer.append(htmlProduct);
            });
          }
        }else{
          $compareContainer.html('<div class="alert alert-warning d-inline-block">There are no products in the comparison list!</div>');
        }

        //button text
        e(compareButtonClass).each(function(){
          var productHandle = e(this).data('comparehandle');
          var status = e.inArray(productHandle,compareObject) !== -1 ? 'added' : '';
          e(this).removeClass('added').addClass(status);
        });

        //count items
        if(compareObject.length > 0){$compareCount.text('('+ compareObject.length +')');}
      }
      e(document).on('click',compareButtonClass,function (event) {
        event.preventDefault();
        updateCompare(this);
        loadCompare();
      });
      e(document).on('click',compareRemoveButtonClass,function(){
        var productHandle = $(this).data('comparehandle');
        compareObject.splice(compareObject.indexOf(productHandle), 1);
        localStorage.setItem('localCompare', JSON.stringify(compareObject)); 
        loadCompare();
      });

      loadCompare();

    },
    productCompact: function() {
      if($(".product-design-compact .tt-scroll").length > 0){
        $(".product-design-compact .tt-scroll").nanoScroller({
          paneClass: 'tt-scroll-pane',
          sliderClass: 'tt-scroll-slider',
          contentClass: 'tt-scroll-content',
          preventPageScrolling: false
        });
      }
    },
    /*******  Shortcode Faq  *******/
    initShortcode: function() {
      e('.tt-toggle').toggle(function(){ e(this).addClass('active'); },function(){ e(this).removeClass('active'); });
      e('.tt-toggle').click(function(){ e(this).next('.tt-toggle-content').slideToggle(); });
      e('.tt-toggle-frame-set').each(function(){
        var $this = e(this),
            $toggle = $this.find('.tt-toggle-accordion');

        $toggle.click(function(){
          if( e(this).next().is(':hidden') ) {
            $this.find('.tt-toggle-accordion').removeClass('active').next().slideUp();
            e(this).toggleClass('active').next().slideDown();
          }
          return false;
        });

        //Activate First Item always
        $this.find('.tt-toggle-accordion:first').addClass("active");
        $this.find('.tt-toggle-accordion:first').next().slideDown();
      });/* Toggle Shortcode end*/

    },
    /**
             *-------------------------------------------------------------------------------------------------------------------------------------------
             * Product accordion
             *-------------------------------------------------------------------------------------------------------------------------------------------
             */

    productAccordion: function() {
      var $accordion = $('.tabs-layout-accordion');

      var time = 300;

      var hash  = window.location.hash;
      var url   = window.location.href;

      if ( hash.toLowerCase().indexOf( 'comment-' ) >= 0 || hash === '#reviews' || hash === '#tab-reviews' ) {
        $accordion.find('.tab-title-reviews').addClass('active');
      } else if ( url.indexOf( 'comment-page-' ) > 0 || url.indexOf( 'cpage=' ) > 0 ) {
        $accordion.find('.tab-title-reviews').addClass('active');
      } else {
        $accordion.find('.tt-accordion-title').first().addClass('active');
        $accordion.find('.tt-Tabs-panel').first().addClass('active');
      }

      $accordion.on('click', '.tt-accordion-title', function( e ) {
        e.preventDefault();

        var $this = $(this),
            $panel = $this.siblings('.tt-Tabs-panel');

        if( $this.hasClass('active') ) {
          $this.removeClass('active');
          $panel.stop().slideUp(time);
        } else {
          $accordion.find('.tt-accordion-title').removeClass('active');
          $accordion.find('.tt-Tabs-panel').slideUp();
          $this.addClass('active');
          $panel.stop().slideDown(time);
        }

        $(window).resize();

        setTimeout( function() {
          $(window).resize();
        }, time);

      } );
    },

    producteffect: function() {
      $('.product-wrapper').on('mouseover', function() {
        var effect = e(this).parents(".product-layouts.item-row");
        var p = effect.data("id");
        p = p.match(/\d+/g);
        var productload = e("#product-" + p + " .product-wrapper");
        //console.log(productload);
        if (!productload.hasClass('imgloaded')) {
          productload.addClass('loading'); 
          setTimeout(function(){
            productload.removeClass('loading'); 
          }, 1000);
        }
        productload.addClass('imgloaded')
      });
    },

    initProductMoreview: function() {
      e('body:not(.rtl) .design_1 .product-wrapper-owlslider .product-single__thumbs.horizontal_bottom').slick({
        autoplay:false,
        infinite:false,
        autoplaySpeed:1500,
        arrows:true,
        prevArrow:'<button type="button btn" class="slick-prev"><i class="mdi mdi-chevron-left"></i></button>',
        nextArrow:'<button type="button btn" class="slick-next"><i class="mdi mdi-chevron-right"></i></button>',
        slidesToShow: window.number_of_thumb,
        slidesToScroll:1,
        responsive: [
          {
            breakpoint: 1201,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 992,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 768,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 396,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1
            }
          }
        ]
      });

      e('body.rtl .design_1 .product-wrapper-owlslider .product-single__thumbs.horizontal_bottom').slick({
        autoplay:false,
        infinite:false,
        autoplaySpeed:1500,
        arrows:true,
        rtl:true,
        prevArrow:'<button type="button btn" class="slick-prev"><i class="mdi mdi-chevron-left"></i></button>',
        nextArrow:'<button type="button btn" class="slick-next"><i class="mdi mdi-chevron-right"></i></button>',
        slidesToShow: window.number_of_thumb,
        slidesToScroll:1,
        responsive: [
          {
            breakpoint: 992,
            settings: {
              slidesToShow: 4,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 600,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 481,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1
            }
          }
        ]
      });
      e('.design_1 .product-wrapper-owlslider .product-single__thumbs.vertical_left,.design_1 .product-wrapper-owlslider .product-single__thumbs.vertical_right').slick({
        autoplay:false,
        infinite:false,
        autoplaySpeed:1500,
        arrows:true,
        prevArrow:'<button type="button btn" class="slick-prev"><i class="mdi mdi-chevron-left"></i></button>',
        nextArrow:'<button type="button btn" class="slick-next"><i class="mdi mdi-chevron-right"></i></button>',
        vertical: true,
        slidesToShow: window.number_of_thumb,
        slidesToScroll:1,
        responsive: [
          {
            breakpoint: 992,
            settings: {
              slidesToShow: 4,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 600,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 481,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1
            }
          }
        ]
      });
      e('.design_4 .product-wrapper-owlslider .product-single__thumbs.horizontal_bottom').slick({
        autoplay:false,
        autoplaySpeed:1500,
        arrows:true,
        prevArrow:'<button type="button btn" class="slick-prev"><i class="mdi mdi-chevron-left"></i></button>',
        nextArrow:'<button type="button btn" class="slick-next"><i class="mdi mdi-chevron-right"></i></button>',
        centerMode:true,
        slidesToShow: window.number_of_thumb,
        slidesToScroll:1,
        responsive: [
          {
            breakpoint: 992,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 600,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 481,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1
            }
          }
        ]
      });
      e('.design_4 .product-wrapper-owlslider .product-single__thumbs.vertical_left,.design_4 .product-wrapper-owlslider .product-single__thumbs.vertical_right').slick({
        autoplay:false,
        autoplaySpeed:1500,
        arrows:true,
        prevArrow:'<button type="button btn" class="slick-prev"><i class="mdi mdi-chevron-left"></i></button>',
        nextArrow:'<button type="button btn" class="slick-next"><i class="mdi mdi-chevron-right"></i></button>',
        centerMode:true, 
        vertical: true,
        slidesToShow: window.number_of_thumb,
        slidesToScroll:1,
        responsive: [
          {
            breakpoint: 992,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 768,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 481,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1
            }
          }
        ]
      });
    },

    showModal: function(n) {
      e(n).fadeIn(500);
      t.KidsTimeout = setTimeout(function() {
        e(n).fadeOut(500)
      }, 5e3)
    },
    showModalCart: function(n) {
      e(n).fadeIn(500);
    },
    checkItemsInDropdownCart: function() {
      if (e("#slidedown-cart .mini-products-list").children().length > 0) {
        e("#slidedown-cart .no-items").hide();
        e("#slidedown-cart .has-items").show()
      } else {
        e("#slidedown-cart .has-items").hide();
        e("#slidedown-cart .no-items").show()
      }
      if (e("#Sticky-slidedown-cart .mini-products-list").children().length > 0) {
        e("#Sticky-slidedown-cart .no-items").hide();
        e("#Sticky-slidedown-cart .has-items").show()
      } else {
        e("#Sticky-slidedown-cart .has-items").hide();
        e("#Sticky-slidedown-cart .no-items").show()
      }
    },
    initModal: function() {
      e(".continue-shopping").click(function() {
        clearTimeout(t.KidsTimeout);
        e(".ajax-success-modal").fadeOut(500)
      });
      e(".close-modal,.modal .overlay").click(function() {
        clearTimeout(t.KidsTimeout);
        e(".ajax-success-modal").fadeOut(500)
      })
    },
    closeDropdownCart: function() {

      if (e(".site-header:not(.header_2) #slidedown-cart").is(":visible")) {
        e(".site-header:not(.header_2) #slidedown-cart").slideUp("fast")
      }
    },
    initProductAddToCart: function() {
      jQuery("#AddToCart1").click(function(n){
        n.preventDefault();
        jQuery(".template-product #AddToCart").click();
      });
      if (e("#AddToCart").length > 0) {
        e("#AddToCart").click(function(n) {
          n.preventDefault();
          jQuery('body').addClass('cart-open');
          if (e(this).attr("disabled") != "disabled") {
            var r = e(this).parents(".product-block");
            var i = e(r).data("id");
            console.log(i);
            i = i.match(/\d+/g);
            if (!window.ajax_cart) {
              e("form.product-form-" + i).submit()
            } else {
              var r = e(".product-form-" + i + " select[name=id]").val();
              if (!r) {
                r = e(".product-form-" + i + " input[name=id]").val();
                console.log(r);
              }
              var i = e(".product-form-" + i + " input[name=quantity]").val();
              if (!i) {
                i = 1
              }
              if (jQuery('body').hasClass('product_sticky_design_1')) {
                var o = e(".design_1 .product__media #productPhotoImg").attr("src");
              } 
              else if (jQuery('body').hasClass('product_sticky_design_2')) {
                var o = e(".design_2 .product-wrapper-owlslider .product-block .product-single__media-wrapper:first-child .pro_img .product-single__thumb #productPhotoImg").attr("src");
              } 
              else if (jQuery('body').hasClass('product_sticky_design_3')) {
                var o = e(".design_3 .product-wrapper-owlslider .product-block .product-single__media-wrapper:first-child .pro_img .product-single__thumb #productPhotoImg").attr("src");
              }
              else  if (jQuery('body').hasClass('product_sticky_design_4')) {
                var o = e(".design_4 .product__media #productPhotoImg").attr("src");
              } 
              else  if (jQuery('body').hasClass('product_sticky_design_5')) {
                var o = e(".design_5 .product-wrapper-owlslider .product-block .owl-item.center .pro_img #productPhotoImg").attr("src");
              }
              var p = e(".product-single__title").text();
              var amt = e(".product-single__price .price.price--on-sale .sale-price").html();
              var amt1 = e(".product-single__price .price:not(.price--on-sale) .regular-price").html();
              t.doAjaxAddToCart(r, i, o, p, amt, amt1)
            }
          }
          return !1
        })
      }
    },
    initAddToCart: function() {
      if (e(".add-cart-btn").length > 0) {
        e(".add-cart-btn").click(function(n) {
          n.preventDefault();
          if (e(this).attr("disabled") != "disabled") {
            var r = e(this).parents(".item-row");
            var i = e(r).data("id");
            i = i.match(/\d+/g);
            if (!window.ajax_cart) {
              e("form.cart-form-" + i).submit()
            } else {
              var s = e(".cart-form-" + i + " select[name=id]").val();                          
              if (!s) {
                s = e(".cart-form-" + i + " input[name=id]").val()
              }                          
              var o = e(".cart-form-" + i + " select[name=quantity]").val();
              if (!o) {
                o = 1
              }
              console.log(o);
              var a = e(r).find(".featured-image").attr("src");
              var p = e(r).find(".grid-link__title").text();
              var amt = e(r).find(".grid-view-item__meta").html();                         
              t.doAjaxAddToCart(s, o, a, p, amt)
            }
          }
          return false
        })
      }
    },
    initAddToCarts: function() {
      if (e(".add-cart-btns").length > 0) {
        e(".add-cart-btns").click(function(n) {
          n.preventDefault();
          if (e(this).attr("disabled") != "disabled") {
            var r = e(this).parents(".item-row");
            var i = e(r).attr("id");
            i = i.match(/\d+/g);
            if (!window.ajax_cart) {
              e("form.cart-form-" + i).submit()
            } else {
              var s = e(".cart-form-" + i + " select[name=id]").val();                          
              if (!s) {
                s = e(".cart-form-" + i + " input[name=id]").val()
              }                          
              var o = e(".cart-form-" + i + " select[name=quantity]").val();
              if (!o) {
                o = 1
              }
              console.log(o);
              var a = e(r).find(".featured-image").attr("src");
              var p = e(r).find(".grid-link__title").text();
              var amt = e(r).find(".grid-view-item__meta").html();                         
              t.doAjaxAddToCart(s, o, a, p, amt)
            }
          }
          return false
        })
      }
    },
    showLoading: function() {
      e(".loading-modal").show()
    },
    hideLoading: function() {
      e(".loading-modal").hide()
    },
    doAjaxAddToCart: function(n, r, a, p, amt) {
      e.ajax({
        type: "post",
        url: "/cart/add.js",
        data: "quantity=" + r + "&id=" + n,
        dataType: "json",
        beforeSend: function() {
          t.showLoading()
        },
        success: function(n) {
          t.hideLoading();                    
          if (window.innerWidth >= 992 && window.aylCartDrawer) { window.aylCartDrawer.open(); return; } t.showModalCart(".ajax-success-modal");
          e(".ajax-success-modal").find(".ajax-product-image").attr("src", a);
          e(".ajax-success-modal").find(".added-to-wishlist").hide();
          e(".ajax-success-modal").find(".added-to-cart").show();
          e(".ajax-success-modal").find(".ajax-product-title").text(p);
          e(".ajax-success-modal").find(".ajax_price").html(amt);
          t.updateDropdownCart();
          if(window.innerWidth >= 992 && window.aylCartDrawer) {
            window.aylCartDrawer.open();
          }
        },
        error: function(n, r) {
          t.hideLoading();
          e(".ajax-error-message").text(e.parseJSON(n.responseText).description);
          t.showModalCart(".ajax-error-modal")
        }
      })
    },
    initQuickView: function() {
      e(".quick-view-text").click(function() {
        t.showLoading();
        e('.quick-view').addClass('open-in'); 
        var product = e(this).data("id");
        Shopify.getProduct(product, function(product) {
          var quickShopModalBackground = jQuery('.quick-view .quick-shop-modal-bg');

          if(e('.quick-view').hasClass('open-in')){
            quickShopModalBackground.show();
            setTimeout(function() {
              jQuery(".quick-view .quick-shop-modal-bg").hide()
            }, 2000)
          }
          var r = e("#quickview-template").html();
          e(".quick-view").html(r);
          var i = e(".quick-view");

          t.loadQuickViewSlider(product, i);
          var s = product.description.replace(/(<([^>]+)>)/ig, "");
          s = s.split(" ").splice(0, 40).join(" ") + "...";
          i.find(".product-title a").text(product.title);
          i.find(".product-title a").attr("href", product.url);                  
          if (i.find('.product-inventory span').length > 0) {
            var variant = product.variants[0];
            var inventoryInfo = i.find('.product-inventory span');                      
            if(variant.available) {
              inventoryInfo.text(window.in_stock);
              inventoryInfo.addClass("in_stock");
              inventoryInfo.removeClass("many_in_stock out_of_stock");
              jQuery(".qty-box-set").css( 'display', 'inline-block' );
            }
            else {
              inventoryInfo.text(window.out_of_stock);
              inventoryInfo.addClass("out_of_stock");
              inventoryInfo.removeClass("in_stock many_in_stock");
              jQuery(".qty-box-set").css( 'display', 'none' );
            }
          }

          i.find(".product-description").text(s);
          i.find(".price").html(Shopify.formatMoney(product.price, window.money_format));
          i.find(".money").html(Shopify.formatMoney(product.price, window.money_format));
          i.find(".product-item").attr("id", "product-" + product.id);
          i.find(".content").attr("id", "product-" + product.id);
          i.find(".variants").attr("id", "product-actions-" + product.id);
          i.find(".variants select").attr("id", "product-select-" + product.id);
          if (product.compare_at_price > product.price) {
            i.find(".compare-price").html(Shopify.formatMoney(product.compare_at_price_max, window.money_format)).show();
           if (product.compare_at_price > product.price) {
            i.find(".compare-price").html(Shopify.formatMoney(product.compare_at_price_max, window.money_format)).show();
            if (product.compare_at_price > product.price) {
              i.find(".discount-percentage")
                .html(Math.round(((product.compare_at_price - product.price) / product.compare_at_price) * 100) + "%")
                .show();
            } else {
              i.find(".discount-percentage").hide();
            }
          }

            i.find(".price").addClass("on-sale")
          } else {
            i.find(".compare-price").html("");
            i.find(".discount-percentage").html("");

            i.find(".price").removeClass("on-sale")
          }
          if (!product.available) {
            i.find("select, input, .total-price, .dec, .inc, .variants label").remove();
            i.find(".add-to-cart-btn").text("Unavailable").addClass("disabled").attr("disabled", "disabled");                        
          } else {
            i.find(".total-price .price").html(Shopify.formatMoney(product.price, window.money_format));                        
            t.createQuickViewVariants(product, i)

          }     
          $('.quick-view .qtyplus').on('click',function(e){
            e.preventDefault();
            var  input_val = jQuery(this).parents('.qty-box-set').find('.quantity');
            var currentVal = parseInt( jQuery(this).parents('.qty-box-set').find('.quantity').val());

            if (!isNaN(currentVal)) {
              jQuery(this).parents('.qty-box-set').find('.quantity').val(currentVal + 1);
            } else {
              jQuery(this).parents('.qty-box-set').find('.quantity').val(1);
            }

          });

          $(".quick-view .qtyminus").on('click',function(e) {
            e.preventDefault();
            var  input_val = jQuery(this).parents('.qty-box-set').find('.quantity');
            var currentVal = parseInt( jQuery(this).parents('.qty-box-set').find('.quantity').val());
            if (!isNaN(currentVal) && currentVal > 1) {
              jQuery(this).closest('.qty-box-set').find('.quantity').val(currentVal - 1);
            } else {
              jQuery(this).closest('.qty-box-set').find('.quantity').val(1);
            }

          });

          t.initQuickviewAddToCart();
          t.hideLoading();
          e(".quick-view").fadeIn(500);

        });
        return false
      });
      e(".quick-view .overlay, .close-window").on("click", function() {    
        t.closeQuickViewPopup();
        e('.quick-view').removeClass("open-in");
        e('.quick-view').removeClass("option-loader");

        return false
      });

    },
    initQuickviewAddToCart: function() {
      if (e(".quick-view .add-to-cart-btn").length > 0) {
        e(".quick-view .add-to-cart-btn").click(function(event) {
          event.preventDefault();
          if (e(this).attr("disabled") != "disabled") {
            var r = e(this).parents(".content");
            var q = e(r).attr("id");
            q = q.match(/\d+/g);
            if (!window.ajax_cart) {
              e("form#product-actions-" + q ).submit()
            } else {
              var n = e(".quick-view select[name=id]").val();
              if (!n) {
                n = e(".quick-view input[name=id]").val()
              }
              var r = e(".quick-view input[name=quantity]").val();
              if (!r) {
                r = 1
              }
              var p = e('.quick-view .product-title a').html();
              var a = e(".quick-view .quickview-featured-image img").attr("src");                 
              var amt = e(".quick-view .product-price__price").html(); 
              t.doAjaxAddToCart(n, r, a, p, amt);
              t.closeQuickViewPopup();
              e('.quick-view').removeClass("open-in");
              e('.quick-view').removeClass("option-loader");
            }
          }
          return false
        })


      }
    },
    checkNeedToConvertCurrency: function() {
      return window.show_multiple_currencies && Currency.currentCurrency != shopCurrency
    },
    loadQuickViewSlider: function(product, r) {

      var s = Shopify.resizeImage(product.featured_image, "large");
      r.find(".quickview-featured-image").append('<img height="auto" width="480px" src="' + s + '" title="' + product.title + '"/>');
      if (product.images.length > 1) {
        var o = r.find(".more-view-wrapper ul");
        for (i in product.images) {
          var u = Shopify.resizeImage(product.images[i], "large");
          var a = Shopify.resizeImage(product.images[i], "small");
          var f = '<li><a href="javascript:void(0)" data-image="' + u + '"><img height="auto" width="100px" src="' + a + '"  /></a></li>';
          o.append(f)
        }
        o.css('max-height','100px');
        if($("body.rtl").length > 0){
          if (o.hasClass("quickview-more-views-owlslider")) {
            t.initQuickViewMoreviewRtl(o)
          } else {
            t.initQuickViewMoreviewRtl(o)
          }
        }else{
          if (o.hasClass("quickview-more-views-owlslider")) {
            t.initQuickViewMoreview(o)
          } else {
            t.initQuickViewMoreview(o)
          }
        }
        o.find("a").click(function() {
          var t = r.find(".quickview-featured-image img");
          var product = r.find(".quickview-featured-image div");
          if (t.attr("src") != e(this).attr("data-image")) {
            t.attr("src", e(this).attr("data-image"));
            product.show();
            e("a").removeClass('active');
            e(this).addClass('active');
            t.load(function(t) {
              product.hide();
              e(this).unbind("load");                        
              product.hide()
            })
          }
        });


      } else {

        r.find(".more-view-wrapper").remove();

      } 
      e(".quick-view .overlay, .close-window").on("click", function() {    
        t.closeQuickViewPopup();
        e('.quick-view').removeClass("open-in");
        e('.quick-view').removeClass("option-loader");

        return false
      });
    },
    closeEmailModalWindow: function() {
      if (e("#email-modal").length > 0 && e("#email-modal").is(":visible")) {
        e("#email-modal .modal-window").fadeOut(600, function() {
          e("#email-modal .modal-overlay").fadeOut(600, function() {
            e("#email-modal").hide();
            e.cookie("emailSubcribeModal", "closed", {
              expires: 1,
              path: "/"
            })
          })
        })
      }
    },
    initQuickViewMoreview: function(m) {
      if (m) {
        m.owlCarousel({
          nav: true,
          items: 3,
          loop: false,
          rtl: false,
          responsive: {
            0: {
              items: 2
            },
            600: {
              items: 3
            },
            1199: {
              items: 3
            }
          },
          dots: false
        })
        setTimeout(function(){
          $(m).css("visibility", "visible");                    
        }, 500);
      }
      e(".quick-view .overlay, .close-window").on("click", function() {
        t.closeQuickViewPopup();
        e('.quick-view').removeClass("open-in");
        e('.quick-view').removeClass("option-loader");               
        return false
      });
    },
    initQuickViewMoreviewRtl: function(m) {
      if (m) {
        m.owlCarousel({
          nav: true,
          items: 3,
          loop: false,
          rtl: true,
          responsive: {
            0: {
              items: 2
            },
            600: {
              items: 3
            },
            1199: {
              items: 3
            }
          },
          dots: false
        })
        setTimeout(function(){
          $(m).css("visibility", "visible");                    
        }, 500);
      }
      e(".quick-view .overlay, .close-window").on("click", function() {
        t.closeQuickViewPopup();
        e('.quick-view').removeClass("open-in");
        e('.quick-view').removeClass("option-loader");               
        return false
      });
    },


    convertToSlug: function(e) {
      return e.toLowerCase().replace(/[^a-z0-9 -]/g, "").replace(/\s+/g, "-").replace(/-+/g, "-")
    },

    createQuickViewVariants: function(t, product) {
      if (t.variants.length > 1) {
        for (var r = 0; r < t.variants.length; r++) {
          var i = t.variants[r];
          var s = '<option value="' + i.id + '">' + i.title + "</option>";
          product.find("form.variants > select").append(s)
        }
        new Shopify.OptionSelectors("product-select-" + t.id, { product: t,  onVariantSelected: selectCallbackQuickview  });

        if (t.options.length == 1) {
          e(".selector-wrapper:eq(0)").prepend("<label>" + t.options[0].name + "</label>")
        }
        product.find("form.variants .selector-wrapper label").each(function(n, r) {
          e(this).html(t.options[n].name)
        })
      } else {
        product.find("form.variants > select").remove();
        var o = '<input type="hidden" name="id" value="' + t.variants[0].id + '">';
        product.find("form.variants").append(o)
      }
      Currency.convertAll(window.shop_currency, jQuery('.currencies li.active .currencies-a').val(), 'span.money', 'money_format');
    },      
    closeQuickViewPopup: function() {
      e(".quick-view").fadeOut(500);
    },
    initSidebar: function() {
      //if category page then init sidebar
      if (e(".collection_sidebar").length > 0) {
        t.sidebarParams();              
        t.sidebarMapEvents();               
        //t.sidebarInitToggle();
        t.sidebarMapClear();
        t.sidebarMapClearAll();
        t.initSortby();                
        t.sidebarMapPaging();
      }
    },
    
    sidebarMapView: function() {
      // t.sidebarAjaxClick();
      e(".view-mode a.active").removeClass("active");
      e(this).addClass("active");

      jQuery('.products-grid-view  > .product-list .product-thumb').attr('class', 'product-thumb col-xs-5 col-sm-5 col-md-3');
      jQuery('.products-grid-view > .product-list .product-description').attr('class', 'product-description col-xs-7 col-sm-7 col-md-9');

      jQuery('.products-grid-view > div.grid-item.product-list').each(function(){
        var prod_desc = jQuery(this).find('.product-wrapper .product-description .product-description-wrap');
        jQuery(this).find('.grid-view-item__title').prependTo(prod_desc);
      });

      jQuery('.products-grid-view > div.grid-item:not(.style2)').each(function(){
        var prod_des = jQuery(this).find('.grid-view-item__title');
        jQuery(this).find('.grid-view-item__meta').insertAfter(prod_des);
      }); 

      jQuery('.products-grid-view > div.grid-item.product-grid:not(.style2)').each(function(){
        var prod_desc = jQuery(this).find('.grid-view-item__vendor');
        jQuery(this).find('.spr-badges').insertAfter(prod_desc);
      });

      jQuery('.products-grid-view > div.grid-item.product-list').each(function(){
        var prod_desc = jQuery(this).find('.product-description .h4.grid-view-item__title');
        jQuery(this).find('.product-description .spr-badges').insertAfter(prod_desc);
      });

      jQuery('.products-grid-view > div.grid-item.product-grid').each(function(){
        var prod_desc = jQuery(this).find('.product-wrapper .product-description .product-description-wrap');
        jQuery(this).find('.grid-view-item__vendor').prependTo(prod_desc);
      });

      jQuery('.products-grid-view > div.grid-item.product-list').each(function(){
        var prod_color = jQuery(this).find('.product-description .grid-view-item__meta');
        jQuery(this).find('.product-description .item-swatch.color_swatch_Value').insertAfter(prod_color);

      });

      jQuery('.product-short-list .product-wrapper .product-description .product-description-wrap .spr-badges').addClass('grid-item-meta');
      jQuery('.products-grid-view > div.product-short-list').each(function(){
        var prod_ven= jQuery(this).find('.product-wrapper .product-description .product-description-wrap .grid-item-meta');
        jQuery(prod_ven).wrapAll('<div class="short-title col-sm-5"></div>');	
      });

      jQuery('.products-grid-view > .product-grid .product-thumb').attr('class', 'product-thumb col-xs-12 padding_0');
      jQuery('.products-grid-view > .product-grid .product-description').attr('class', 'product-description col-xs-12');

      /* Active class in Product List Grid START */
      jQuery('.products-grid-view > div.grid-item').addClass('product-grid');
            jQuery('#list-view').on('click',function() {
        jQuery('.products-grid-view > div.grid-item').removeClass('product-grid');
        jQuery('.products-grid-view > div.grid-item').removeClass('product-short-list');	
        jQuery('.products-grid-view > div.grid-item').addClass('product-list');
        jQuery('#grid-view').removeClass('active');
        jQuery('#short-list-view').removeClass('active');
        jQuery('#list-view').addClass('active');
        jQuery('.products-grid-view > .product-list .product-thumb').attr('class', 'product-thumb col-xs-5 col-sm-5 col-md-3');
        jQuery('.products-grid-view > .product-list .product-description').attr('class', 'product-description col-xs-7 col-sm-7 col-md-9');
        jQuery('.products-grid-view > div.product-list').each(function(){ 	
          var prod_ven_unwrap= jQuery(this).find('.product-wrapper .product-description .product-description-wrap .short-title');
          jQuery(prod_ven_unwrap).children().unwrap();
        });

        jQuery('.products-grid-view > div.grid-item ').each(function(){
          var thumb = jQuery(this).find('.product-desc');
          jQuery(this).find('.grid-view-item__title').insertBefore(thumb);



          
          

          
        });
        jQuery('.products-grid-view > div.grid-item').each(function(){
          var thumb = jQuery(this).find('.product-description-wrap');
          jQuery(this).find('.grid-view-item__vendor').prependTo(thumb);

          var thumb = jQuery(this).find('.product-description-wrap .product-desc');
          jQuery(this).find('.grid-view-item__meta').insertAfter(thumb);

                              


        });
        jQuery('.products-grid-view > div.grid-item.product-list').each(function(){
          var prod_desc = jQuery(this).find('.product-description .grid-view-item__meta');
          jQuery(this).find('.product-description .item-swatch.color_swatch_Value').insertAfter(prod_desc);
        }); 

        jQuery('.products-grid-view > div.grid-item').each(function() {
          var thumb = jQuery(this).find('.grid-view-item__title');
          jQuery(this).find('.spr-badges').insertAfter(thumb);

          // ====================================================================== ======================================================================
          // add this js
// ====================================================================== ======================================================================

                              var prod_countdown2 = jQuery(this).find('.product-description .product-desc ');
          jQuery(this).find('.product-wrapper .flip-countdown.simple-countdown').insertAfter(prod_countdown2);

          // ====================================================================== ======================================================================
// ====================================================================== ======================================================================
          
        });

        jQuery('.products-grid-view > div.product-list').each(function(){ 	
          var prod_ven_unwrap= jQuery(this).find('.product-wrapper .product-description .product-description-wrap .short-title');
          jQuery(prod_ven_unwrap).children().unwrap();
        });

        localStorage.setItem('display', 'list');
        var paging = e(".filter-show  button span").text();
        Shopify.queryParams.view = paging;
      });


 //       short list view

    jQuery('#short-list-view').on('click',function() {
        jQuery('.products-grid-view > div.grid-item ').removeClass('product-grid');
        jQuery('.products-grid-view > div.grid-item ').removeClass('product-list');
        jQuery('.products-grid-view > div.grid-item ').addClass('product-short-list');
        jQuery('#grid-view').removeClass('active');
        jQuery('#list-view').removeClass('active');
        jQuery('#short-list-view').addClass('active');
        jQuery('.products-grid-view > .product-short-list .product-thumb').attr('class', 'product-thumb col-xs-3 col-sm-3 col-md-2');
        jQuery('.products-grid-view > .product-short-list .product-description').attr('class', 'product-description col-xs-9 col-sm-9 col-md-10');                                                       

        jQuery('.products-grid-view > div.grid-item.product-grid').each(function(){
          var prod_desc = jQuery(this).find('.product-description .product-description-wrap .grid-view-item__title');
          jQuery(this).find('.spr-badges').insertAfter(prod_desc);

          

        });	
        // jQuery('.products-grid-view > div.grid-item').each(function(){
        //   var prod_desc = jQuery(this).find('.product-description .product-description-wrap');
        //   jQuery(this).find('.btn_wrapper').appendTo(prod_desc);
        // }); 

        jQuery('.product-wrapper .product-description .product-description-wrap .spr-badges').addClass('grid-item-meta');
      
        // jQuery('.products-grid-view > div.product-short-list').each(function(){
        //   var prod_ven = jQuery(this).find('.product-wrapper .product-description .product-description-wrap .grid-item-meta');
        //   jQuery(prod_ven).wrapAll('<div class="short-title col-sm-5"></div>');	

        // });
      
// ====================================================================== ======================================================================
// ====================================================================== ======================================================================
          jQuery('.products-grid-view > div.product-short-list').each(function() {
      var prod_ven = jQuery(this).find('.product-wrapper .product-description .product-description-wrap > .grid-item-meta');
      jQuery(prod_ven).wrapAll('<div class="short-title  col-xs-6 col-sm-7"></div>')
    });
// ====================================================================== ======================================================================
// ====================================================================== ======================================================================
      

      
        jQuery('.products-grid-view > div.grid-item').each(function() {
          var prod_desc = jQuery(this).find('.short-title');
          jQuery(this).find('.color_swatch_Value').appendTo(prod_desc);


          // ====================================================================== ======================================================================
          // add this css
// ====================================================================== ======================================================================
          
                          var btnwrap2 = jQuery(this).find('.spr-badges');
          jQuery(this).find('.product-desc').insertAfter(btnwrap2);

          
                    var prod_countdown = jQuery(this).find('.product-description .short-title .product-desc');
          jQuery(this).find('.product-wrapper .flip-countdown.simple-countdown').insertAfter(prod_countdown)

                    // ====================================================================== ======================================================================
// ====================================================================== ======================================================================
          
        });	

        jQuery('.products-grid-view > div.grid-item.product-short-list').each(function(){
          var prod_desc = jQuery(this).find('.product-description-wrap .short-title');
          jQuery(this).find('.grid-view-item__vendor').prependTo(prod_desc);

          var prod_desc = jQuery(this).find('.product-description-wrap .grid-view-item__vendor');
          jQuery(this).find('.grid-view-item__title').insertAfter(prod_desc);

          var prod_desc = jQuery(this).find('.product-description-wrap .grid-view-item__title');
          jQuery(this).find('.spr-badges').insertAfter(prod_desc);

                 var thumb = jQuery(this).find('.product-desc');
          jQuery(this).find('.grid-view-item__title').insertBefore(thumb);

                    var thumb = jQuery(this).find('.grid-view-item__title');
          jQuery(this).find('.spr-badges').insertAfter(thumb);


          // ====================================================================== ======================================================================
          // comment this code
// ====================================================================== ======================================================================

          
          
          // var prod_desc = jQuery(this).find('.product-desc');
          // jQuery(this).find('.grid-view-item__meta').insertAfter(prod_desc);

          // ====================================================================== ======================================================================
          // ====================================================================== ======================================================================
        });    

        localStorage.setItem('display', 'short-list');
        var paging = e(".filter-show  button span").text();
        Shopify.queryParams.view = paging;
      });

  
  // grids view   

      jQuery('#grid-view').on('click',function() {
        jQuery('#list-view').removeClass('active');
        jQuery('#short-list-view').removeClass('active');
        jQuery('#grid-view').addClass('active');
        jQuery('.products-grid-view > div.grid-item ').removeClass('product-list');
        jQuery('.products-grid-view > div.grid-item ').removeClass('product-short-list');
        jQuery('.products-grid-view > div.grid-item ').addClass('product-grid');
        jQuery('.products-grid-view > .product-grid .product-thumb').attr('class', 'product-thumb col-xs-12 padding_0');
        jQuery('.products-grid-view > .product-grid .product-description').attr('class', 'product-description col-xs-12');	
        localStorage.setItem('display', 'grid');

        jQuery('.products-grid-view > div.product-grid').each(function(){ 	
          var prod_ven_unwrap= jQuery(this).find('.product-wrapper .product-description .product-description-wrap .short-title');
          jQuery(prod_ven_unwrap).children().unwrap();



                    // ====================================================================== ======================================================================
          // add this in grid
          // ====================================================================== ======================================================================
          
                    var countt = jQuery(this).find('.product-thumb .product-image');
          jQuery(this).find('.product-description .flip-countdown.simple-countdown').appendTo(countt)

                              // ====================================================================== ======================================================================
          // ====================================================================== ======================================================================
          
        });
        
        jQuery('.products-grid-view > div.grid-item.style3').each(function(){
          var thumb = jQuery(this).find('product-t');
          jQuery(this).find('.main_btn_wrapper').insertAfter(thumb);
        });

        jQuery('.products-grid-view > div.grid-item:not(.style3)').each(function(){
          var thumb = jQuery(this).find('.product-description-wrap');
          jQuery(this).find('.btn_wrapper').appendTo(thumb);
        });

        jQuery('.products-grid-view > div.grid-item.style2').each(function(){
          var thumb = jQuery(this).find('.product-thumb .product-image');
          jQuery(this).find('.grid-view-item__title').prependTo(thumb);

          var thumb = jQuery(this).find('.product-thumb .product-image');
          jQuery(this).find('.grid-view-item__vendor').prependTo(thumb);

          var thumb = jQuery(this).find('.price-btn');
          jQuery(this).find('.grid-view-item__meta').appendTo(thumb);

          var thumb = jQuery(this).find('.product-thumb .grid-view-item__title');
          jQuery(this).find('.spr-badges').insertAfter(thumb);                      
        });

        jQuery('.products-grid-view > div.grid-item.style1').each(function(){
          var title_meta = jQuery(this).find('.spr-badges');
          jQuery(this).find('.grid-view-item__title').insertAfter(title_meta);

        });
        jQuery('.products-grid-view > div.grid-item.style3').each(function(){
          var title_meta = jQuery(this).find('.grid-view-item__vendor');
          jQuery(this).find('.grid-view-item__title').insertAfter(title_meta);

        });
        jQuery('.products-grid-view > div.grid-item.product-grid:not(.style2)').each(function(){
          var prod_desc = jQuery(this).find('.product-wrapper .product-description .product-description-wrap');
          jQuery(this).find('.grid-view-item__vendor').prependTo(prod_desc);

        });
        jQuery('.products-grid-view > div.grid-item.product-grid.style1').each(function(){
          var prod_desc = jQuery(this).find('.grid-view-item__vendor');
          jQuery(this).find('.spr-badges').insertAfter(prod_desc);
        });

        jQuery('.products-grid-view > div.grid-item.product-grid.style3').each(function(){
          var prod_desc = jQuery(this).find('.grid-view-item__title');
          jQuery(this).find('.spr-badges').insertAfter(prod_desc);
        });

        jQuery('.products-grid-view > div.grid-item.product-grid').each(function(){
          var prod_color = jQuery(this).find('.product-description .product-description-wrap');
          jQuery(this).find('.product-description .item-swatch.color_swatch_Value').prependTo(prod_color);
        });

        var paging = e(".filter-show  button span").text();
        Shopify.queryParams.view = paging;
      });
      if(jQuery( window ).width() < 992) {  
        jQuery(".sidebar .widget > h4").addClass( "toggle" );
        jQuery(".sidebar .widget ").children(':nth-child(2)').css( 'display', 'none' );
        jQuery(".sidebar .widget.active").children(':nth-child(2)').css( 'display', 'block' );
        jQuery(".sidebar .widget > h4.toggle").unbind("click");
        jQuery(".sidebar .widget > h4.toggle").on('click',function() {
          jQuery(this).parent().toggleClass('active').children(':nth-child(2)').slideToggle( "fast" );
        });
      }
      /* Active class in Product List Grid END */
      if (localStorage.getItem('display') == 'grid') {
        jQuery('#grid-view').trigger('click');
      } else if (localStorage.getItem('display') == 'list'){
        jQuery('#list-view').trigger('click');
      }
      else if (localStorage.getItem('display') == 'short-list'){
        jQuery('#short-list-view').trigger('click');
      }
      else{
        jQuery('#grid-view').trigger('click');
      }
      countDownIni('.flip-countdown'); 
    },

    

    
    sidebarMapSorting: function(n) {
      e(".filter-sortby a").click(function(n) {
        if (!e(this).parent().hasClass("active")) {
          Shopify.queryParams.sort_by = e(this).attr("href");
          t.sidebarAjaxClick();
          var sortbyText = e(this).text();                  
          e(".filter-sortby  button span").text(sortbyText);
          e(".filter-sortby li.active").removeClass("active");
          e(this).parent().addClass("active");
        }
        n.preventDefault();
      });
    },
    
    sidebarMapShow: function() {
      e(".filter-show a").click(function(n) {
        if (!e(this).parent().hasClass("active")) {
          var thisPaging = e(this).attr('href');
          Shopify.queryParams.view = thisPaging;
          t.sidebarAjaxClick();                  
          e(".filter-show .btn span").text(thisPaging);
          e(".filter-show li.active").removeClass("active");
          e(this).parent().addClass("active");

        }
        n.preventDefault();

      });
    },
    initSortby: function() {
      //sort by filter
      if (Shopify.queryParams.sort_by) {
        var sortby = Shopify.queryParams.sort_by;
        var sortbyText = e(".filter-sortby a[href='" + sortby + "']").text();
        e(".filter-sortby  button span").text(sortbyText);
        e(".filter-sortby li.active").removeClass("active");
        e(".filter-sortby a[href='" + sortby + "']").parent().addClass("active");
      }
    },
    sidebarMapPaging: function() {
      e(".pagination-custom a").click(function(n) {
        var page = e(this).attr("href").match(/page=\d+/g);
        if (page) {
          Shopify.queryParams.page = parseInt(page[0].match(/\d+/g));
          if (Shopify.queryParams.page) {
            var newurl = t.sidebarCreateUrl();
            t.isSidebarAjaxClick = true;
            History.pushState({
              param: Shopify.queryParams
            }, newurl, newurl);
            t.sidebarGetContent(newurl);
            //go to top
            e('body,html').animate({
              scrollTop: 500
            }, 600);
          }
        }
        n.preventDefault();
      });
    },
    sidebarMapTagEvents: function() {
      if(jQuery( window ).width() < 992) {  
        jQuery(".sidebar .widget > h4").addClass( "toggle" );
        jQuery(".sidebar .widget ").children(':nth-child(2)').css( 'display', 'none' );
        jQuery(".sidebar .widget.active").children(':nth-child(2)').css( 'display', 'block' );
        jQuery(".sidebar .widget > h4.toggle").unbind("click");
        jQuery(".sidebar .widget > h4.toggle").on('click',function() {
          jQuery(this).parent().toggleClass('active').children(':nth-child(2)').slideToggle( "fast" );
        });
      }
      if(jQuery( window ).width() < 992) { 
        jQuery(".sidebar-block .widget > h4").addClass( "toggle" );
        jQuery(".sidebar-block .widget ").children(':nth-child(2)').css( 'display', 'none' );
        jQuery(".sidebar-block .widget.active").children(':nth-child(2)').css( 'display', 'block' );
        jQuery(".sidebar-block .widget > h4.toggle").unbind("click");
        jQuery(".sidebar-block .widget > h4.toggle").on('click',function() {
          jQuery(this).parent().toggleClass('active').children(':nth-child(2)').slideToggle( "fast" );
        }); 
      }
      if (jQuery(window).width() < 1200) {
        jQuery(".both-sidebar .sidebar .widget > h4").addClass("toggle");
        jQuery(".both-sidebar .sidebar .widget ").children(':nth-child(2)').css('display', 'none');
        jQuery(".both-sidebar .sidebar .widget.active").children(':nth-child(2)').css('display', 'block');
        jQuery(".both-sidebar .sidebar .widget > h4.toggle").unbind("click");
        jQuery(".both-sidebar .sidebar .widget > h4.toggle").on('click', function() {
          jQuery(this).parent().toggleClass('active').children(':nth-child(2)').slideToggle("fast")
        });
        jQuery(".both-sidebar .right-sidebar .sidebar-block .widget > h4,.both-sidebar .collection_right .sidebar-block .widget > h4,.both-sidebar .collection_left .sidebar-block .widget > h4,.both-sidebar .filter-toggle-wrap .sidebar-block .widget > h4,.both-sidebar .content-right .sidebar-block .widget > h4").addClass( "toggle" );
        jQuery(".both-sidebar .right-sidebar .sidebar-block .widget,.both-sidebar .collection_right .sidebar-block .widget,.both-sidebar .collection_left .sidebar-block .widget,.both-sidebar .filter-toggle-wrap .sidebar-block .widget,.both-sidebar .content-right .sidebar-block .widget ").children(':nth-child(2)').css( 'display', 'none' );
        jQuery(".both-sidebar .right-sidebar .sidebar-block .widget.active,.both-sidebar .collection_right .sidebar-block .widget.active,.both-sidebar .collection_left .sidebar-block .widget.active,.both-sidebar .filter-toggle-wrap .sidebar-block .widget.active,.both-sidebar .content-right .sidebar-block .widget.active").children(':nth-child(2)').css( 'display', 'block' );
        jQuery(".both-sidebar .right-sidebar .sidebar-block .widget > h4.toggle,.both-sidebar .collection_right .sidebar-block .widget > h4.toggle,.both-sidebar .collection_left .sidebar-block .widget > h4.toggle,.both-sidebar .filter-toggle-wrap .sidebar-block .widget > h4.toggle,.both-sidebar .content-right .sidebar-block .widget > h4.toggle").unbind("click");
        jQuery(".both-sidebar .right-sidebar .sidebar-block .widget > h4.toggle,.both-sidebar .collection_right .sidebar-block .widget > h4.toggle,.both-sidebar .collection_left .sidebar-block .widget > h4.toggle,.both-sidebar .filter-toggle-wrap .sidebar-block .widget > h4.toggle,.both-sidebar .content-right .sidebar-block .widget > h4.toggle").on('click',function() {
          jQuery(this).parent().toggleClass('active').children(':nth-child(2)').slideToggle( "fast" );
        });     
      }
      e('.sidebar-tag a:not(".clear"), .sidebar-tag label').click(function(n) {
        e(this).addClass('active');
        var currentTags = [];
        if (Shopify.queryParams.constraint) {
          currentTags = Shopify.queryParams.constraint.split('+');
        }

        //one selection or multi selection
        if (!window.enable_sidebar_multiple_choice && !e(this).prev().is(":checked")) {
          //remove other selection first                  
          var otherTag = e(this).parents('.sidebar-tag').find("input:checked");
          if (otherTag.length > 0) {
            var tagName = otherTag.val();
            if (tagName) {
              var tagPos = currentTags.indexOf(tagName);
              if (tagPos >= 0) {
                //remove tag
                currentTags.splice(tagPos, 1);
              }
            }
          }
        }

        var tagName = e(this).prev().val();
        if (tagName) {
          var tagPos = currentTags.indexOf(tagName);
          if (tagPos >= 0) {
            //tag already existed, remove tag
            currentTags.splice(tagPos, 1);
          } else {
            //tag not existed
            currentTags.push(tagName);
          }
        }
        if (currentTags.length) {
          Shopify.queryParams.constraint = currentTags.join('+');
        } else {
          delete Shopify.queryParams.constraint;
        }
        t.sidebarAjaxClick();
        n.preventDefault();
      });
    },



    sidebarInitToggle: function() {
      if (e(".sidebar-tag").length > 0) {
        e(".sidebar-tag .widget span").click(function() {
          var $title = e(this).parents('.widget');
          if ($title.hasClass('click')) {
            $title.removeClass('click');
          } else {
            $title.addClass('click');
          }

          e(this).parents(".sidebar-tag").find(".widget-content").slideToggle();
        });
      }
    },


    sidebarMapClearAll: function() {
      //clear all selection
      e('.refined-widgets a.clear-all').click(function(n) {
        delete Shopify.queryParams.constraint;
        delete Shopify.queryParams.q;
        t.sidebarAjaxClick();
        n.preventDefault();
      });
    },
    sidebarMapClear: function() {
      e(".sidebar-tag").each(function() {
        var sidebarTag = e(this);
        if (sidebarTag.find("input:checked").length > 0) {
          //has active tag
          sidebarTag.find(".clear").show().click(function(n) {                     
            var currentTags = [];
            if (Shopify.queryParams.constraint) {
              currentTags = Shopify.queryParams.constraint.split('+');
            }
            sidebarTag.find("input:checked").each(function() {
              var selectedTag = e(this);
              var tagName = selectedTag.val();
              if (tagName) {
                var tagPos = currentTags.indexOf(tagName);
                if (tagPos >= 0) {
                  //remove tag
                  currentTags.splice(tagPos, 1);
                }
              }
            });
            if (currentTags.length) {
              Shopify.queryParams.constraint = currentTags.join('+');
            } else {
              delete Shopify.queryParams.constraint;
            }
            t.sidebarAjaxClick();
            n.preventDefault();
          });
        }
      });
    },
    sidebarMapEvents: function() {
      t.sidebarMapTagEvents();
      
      t.sidebarMapView();            
      
      t.sidebarMapSorting();
      t.sidebarMapShow();
    },
    reActivateSidebar: function() {
      e(".sidebar-tag .active").removeClass("active");
      e(".sidebar-tag input:checked").attr("checked", false);

      //view mode and show filter
      if (Shopify.queryParams.view) {
        e(".view-mode .active").removeClass("active");
        var view = Shopify.queryParams.view;
        if (view.indexOf("list") >= 0) {
          e(".view-mode .list").addClass("active");
          //paging
          view = view.replace("list", "");
        } else {
          e(".view-mode .grid").addClass("active");
        }
        e(".filter-show  button span").text(view);
        e(".filter-show li.active").removeClass("active");
        e(".filter-show a[href='" + view + "']").parent().addClass("active");
      }
      t.initSortby();
    },
    sidebarMapData: function(data) {

      var currentList = e(".col-main .products-grid-view");

      var productList = e(data).find(".col-main .products-grid-view");
      currentList.replaceWith(productList);

      //convert currency
      if (t.checkNeedToConvertCurrency()) {
        Currency.convertAll(window.shop_currency, jQuery('.currencies li.active .currencies-a').val(), 'span.money', 'money_format');
      }

      //replace refined
      e(".refined-widgets").replaceWith(e(data).find(".refined-widgets"));

      //replace tags

      e(".sidebar .refined-widgets").replaceWith(e(data).find(".sidebar .refined-widgets"));
      e(".filter-toggle-wrap .refined-widgets").replaceWith(e(data).find(".filter-toggle-wrap .refined-widgets"));

      //replace tags
      e(".sidebar .sidebar-block").replaceWith(e(data).find(".sidebar .sidebar-block"));
      e(".filter-toggle-wrap .sidebar-block").replaceWith(e(data).find(".filter-toggle-wrap .sidebar-block"));
      countDownIni('.flip-countdown'); 
      //replace paging
      if (e(".pagination-wrap").length > 0) {
        e(".pagination-wrap").replaceWith(e(data).find(".pagination-wrap"));
      } else {
        e(e(data).find(".pagination-wrap")).insertAfter(".col-main");
      }
      if (localStorage.getItem('display') == 'grid') {
        jQuery('#grid-view').trigger('click');
      } else if (localStorage.getItem('display') == 'list'){
        jQuery('#list-view').trigger('click');
      }
      else if (localStorage.getItem('display') == 'short-list'){
        jQuery('#short-list-view').trigger('click');
      }
      else{
        jQuery('#grid-view').trigger('click');
      }   
      t.initInfiniteScrolling();
      if ($(".spr-badges").length > 0) {
        return window.SPR.registerCallbacks(), window.SPR.initRatingHandler(), window.SPR.initDomEls(), window.SPR.loadProducts(), window.SPR.loadBadges();
      }


    },
    sidebarCreateUrl: function(baseLink) {
      var newQuery = e.param(Shopify.queryParams).replace(/%2B/g, '+');
      if (baseLink) {
        location.href = baseLink + "?" + newQuery;
        if (newQuery != "")
          return baseLink + "?" + newQuery;
        else
          return baseLink;
      }
      return location.pathname + "?" + newQuery;
    },
    sidebarAjaxClick: function(baseLink) {
      delete Shopify.queryParams.page;
      var newurl = t.sidebarCreateUrl(baseLink);
      t.isSidebarAjaxClick = true;
      History.pushState({
        param: Shopify.queryParams
      }, newurl, newurl);
      t.sidebarGetContent(newurl);
    },
    sidebarGetContent: function(newurl) {
      //alert(newurl)
      $.ajax({
        type: 'get',
        url: newurl,
        beforeSend: function() {
          t.showLoading();
        },
        success: function(data) {
          t.sidebarMapData(data);
          t.sidebarMapTagEvents();
          //t.sidebarInitToggle();
          t.sidebarMapClear();
          t.sidebarMapClearAll();
          t.hideLoading();
          t.initQuickView();
          t.initAddToCart();
          t.initAddToCarts();
          t.initWishlist();
          t.sidebarMapPaging()
          countDownIni('.flip-countdown'); 
          var $container = $(".shop_masonry");
          if($container.length > 0){
            $container.imagesLoaded( function() {
              $container.masonry({ itemSelector : ".ms-item" , columnWidth: ".ms-item",percentPosition: true
                                 }); 
            });
            t.initInfiniteScrolling();


          }
        },
        error: function(xhr, text) {
          t.hideLoading();
          e('.loading-modal').hide();
          e('.ajax-error-message').text($.parseJSON(xhr.responseText).description);
          t.showModal('.ajax-error-modal');
        }
      });
    },
    sidebarParams: function() {
      Shopify.queryParams = {};
      //get after ?...=> Object {q: "Acme"} 
      if (location.search.length) {
        for (var aKeyValue, i = 0, aCouples = location.search.substr(1).split('&'); i < aCouples.length; i++) {
          aKeyValue = aCouples[i].split('=');
          if (aKeyValue.length > 1) {
            Shopify.queryParams[decodeURIComponent(aKeyValue[0])] = decodeURIComponent(aKeyValue[1]);
          }
        }
      }
    },
    initInfiniteScrolling: function() {
      var tt_is_loading = false
      e(".infinite-scrolling").length > 0 && e(".infinite-scrolling a.next").click(function(i) {
        i.preventDefault(), e(this).hasClass("disabled") || t.doInfiniteScrolling()
      })

    },
    doInfiniteScrolling: function() {
      var currentList = $('.col-main .products-grid-view');

      if (currentList) {
        var showMoreButton = $('.infinite-scrolling a.next').first();
        $.ajax({
          type: 'GET',
          url: showMoreButton.attr("href"),
          beforeSend: function() {
            t.showLoading();
            $('.loading-modal').show();
            tt_is_loading = true;
          },
          success: function(data) {
            t.hideLoading();
            var $container = $(".products-grid-view");
            var products = $(data).find(".col-main .products-grid-view");
            tt_is_loading = false;
            //get link of Show more
            if ($(data).find('.infinite-scrolling').length > 0) {
              showMoreButton.attr('href', $(data).find('.infinite-scrolling a.next').attr('href'));
            } else {
              //no more products
              showMoreButton.removeClass('next');
              showMoreButton.hide();
              showMoreButton.next().show();
            }

            if (products.length) {

              jQuery('.products-grid-view > div.product-short-list').each(function(){ 	
                var prod_ven_unwrap= jQuery(this).find('.product-wrapper .product-description .product-description-wrap .short-title');
                jQuery(prod_ven_unwrap).children().unwrap();
              });

              
              currentList.append(products.children());
              

              t.initQuickView();
              t.initAddToCart();
              t.initAddToCarts();
              t.initWishlist();
              countDownIni('.flip-countdown'); 
              if (localStorage.getItem('display') == 'grid') {
                jQuery('#grid-view').trigger('click');
              } else if (localStorage.getItem('display') == 'list'){
                jQuery('#list-view').trigger('click');
              }
              else if (localStorage.getItem('display') == 'short-list'){
                jQuery('#short-list-view').trigger('click');
              }
              else{
                jQuery('#grid-view').trigger('click');
              } 
              


              //currency
              if (window.show_multiple_currencies && window.shop_currency != jQuery(".currencies li.active .currencies-a").val())
              {
                Currency.convertAll(window.shop_currency, jQuery('.currencies li.active .currencies-a').val(), "span.money", "money_format")
              }

              t.initColorSwatchGrid();
              //product review
              if ($(".spr-badges").length > 0) {
                return window.SPR.registerCallbacks(), window.SPR.initRatingHandler(), window.SPR.initDomEls(), window.SPR.loadProducts(), window.SPR.loadBadges();
              }

            }

          },
          error: function(xhr, text) {
            t.hideLoading();
            $('.loading-modal').hide();
            $('.ajax-error-message').text($.parseJSON(xhr.responseText).description);
            t.showModal('.ajax-error-modal');
          },
          dataType: "html"
        });
      }
    }

  }    

  })(jQuery);