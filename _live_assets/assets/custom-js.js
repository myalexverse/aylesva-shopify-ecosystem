$(document).ready(function() {

  jQuery(".filter-toggle").on("click" , function(e){
    e.preventDefault();
    jQuery(this).toggleClass("active");
    jQuery(".filter-toggle-wrap").slideToggle("is-visible");
  })
  var filter = jQuery(this).find('.full_width .sorting_wrapper');
  jQuery(this).find('.filter-toggle').insertBefore(filter);

  jQuery('#shopify-section-footer-style-3,#shopify-section-footer-style-2, #shopify-section-footer-style-1').appendTo('.site-inner');
  jQuery('.tt-flexslider').prependTo('.site-inner .main-content');

  jQuery("#tt-megamenu .tt-mega_menu").hover(
    function () {
      jQuery('body').addClass("menu_hover");
    },
    function () {
      jQuery('body').removeClass("menu_hover");
    }
  );
  jQuery("#tt-megamenu .tt_menu_item.left_more_menu.active").each(function(){
    jQuery('body').removeClass("menu_hover");
  });
  jQuery("#accessibleNav li.menu-item-depth-0").hover(
    function () {
      jQuery('body').addClass("menu-open");
    },
    function () {
      jQuery('body').removeClass("menu-open");
    }
  );

  jQuery('.category-slider .product-wrapper').each(function(){    
    var prod_review = jQuery(this).find('.product-description .product-description-wrap');
    jQuery(this).find('.spr-badges').prependTo(prod_review);

    var prod_desc = jQuery(this).find('.product-description .product-description-wrap');
    jQuery(this).find('.h4.grid-view-item__title').prependTo(prod_desc);

    var prod_ven = jQuery(this).find('.product-description .product-description-wrap');
    jQuery(this).find('.grid-view-item__vendor').prependTo(prod_desc);
  });

  jQuery(".tt-mega-menu #tt-megamenu .tt-mega_menu").on("click", function(event) {
    event.stopPropagation();
  });


  if(jQuery('.header_1 .wrapper-wrap').hasClass('logo_center'))  {
    jQuery('body').addClass('logo_center');
  }
  var w_width = $(window).width();
  $('.slider-content-main-wrap').css('width',w_width);
  if($('.site-header').hasClass('header_transaparent')){
    $('body.template-index').addClass('header_transaparent')
  }

  var img_id = jQuery('.product-single__thumbs .slick-active.slick-current').find('.product-single__thumb').data('id');
  if(jQuery('.product-lightbox-btn').hasClass(img_id)){
    jQuery('.product-lightbox-btn.'+img_id).show();
  }

  //video
  var p = jQuery(".popup_overlay");

  jQuery(".play-icone").click(function() {
    jQuery("body").addClass("popup-toggle");
    p.css("display", "block");

  });
  p.click(function(event) {
    e = event || window.event;
    if (e.target == this) {
      jQuery(p).css("display", "none");
      jQuery('body').removeClass('popup-toggle'); 
    }
  });
  jQuery(".popup_close,.flex-direction-nav li a").click(function() {
    p.css("display", "none");
    jQuery('body').removeClass('popup-toggle'); 
  });

  //video popup
  function toggleVideo(state) {
    // if state == 'hide', hide. Else: show video
    e = state || window.event;
    if (e.target == this) {
      var div = document.getElementById("popupVid");
      var iframe = div.getElementsByTagName("iframe")[0].contentWindow;
      //div.style.display = state == 'hide' ? 'none' : '';
      func = state == "hide" ? "pauseVideo" : "playVideo";
      iframe.postMessage(
        '{"event":"command","func":"' + func + '","args":""}',
        "*"
      );
    }
  }

  jQuery("#popup_toggle").click(function() {
    p.css("visibility", "visible").css("opacity", "1");
  });

  p.click(function(event) {
    e = event || window.event;
    if (e.target == this) {
      jQuery(p)
      .css("visibility", "hidden")
      .css("opacity", "0");
      toggleVideo("hide");
    }
  });

  jQuery(".popup_close,.flex-direction-nav li a").click(function() {
    p.css("visibility", "hidden").css("opacity", "0");
    toggleVideo("hide");
  });

  var iframe = jQuery("iframe")[0];

  jQuery(".filter-left").on("click" , function(e){
    e.preventDefault();
    jQuery(this).toggleClass("active");
    jQuery(".off-canvas.position-left").toggleClass("is-open");
    jQuery(".js-off-canvas-overlay.is-overlay-fixed").toggleClass("is-visible is-closable");
  });
  jQuery(".is-overlay-fixed").on("click" , function(e){
    e.preventDefault();
    jQuery(".filter-left").trigger('click');
    jQuery(".filter-right").trigger('click');
  });
  jQuery(".filter-right").on("click" , function(e){
    e.preventDefault();
    jQuery(this).toggleClass("active");
    jQuery(".off-canvas.position-right").toggleClass("is-open");
    jQuery(".js-off-canvas-overlay.is-overlay-fixed").toggleClass("is-visible is-closable");
  });
  $('.product-360-button a').magnificPopup({
    type: 'inline',
    mainClass: 'mfp-fade',
    removalDelay: 160,
    disableOn: false,
    preloader: false,
    fixedContentPos: false,
    callbacks: {
      open: function() {
        $(window).resize()
      }
    }
  });



  /* coundown js */
  //countDownProductIni('.js-flip-countdown');
  /* simple countdown */
  countDownIni('.flip-countdown,.js-flip-countdown'); 
  /***/
  /** popup Video **/

  $('.popup-video').magnificPopup({
    disableOn: 300,
    type: 'iframe',
    mainClass: 'mfp-fade',
    removalDelay: 160,
    preloader: false,
    fixedContentPos: false
  });

  /***/

  if ($('a.product-lightbox-btn').length > 0 || $('a.product-video-popup').length > 0) {
    $('.product-single__photos .gallery,.design_2 .product-img').magnificPopup({
      delegate: 'a', // child items selector, by clicking on it popup will open
      type: 'image',
      tLoading: '<div class="please-wait dark"><span></span><span></span><span></span></div>',
      removalDelay: 300,
      closeOnContentClick: true,
      gallery: {
        enabled: true,
        navigateByImgClick: false,
        preload: [0, 1]
      },
      image: {
        verticalFit: false,
        tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
      },
      callbacks: {
        beforeOpen: function() {
          var productVideo = $('.product-video-popup').attr('href');
          if (productVideo) {
            this.st.mainClass = 'has-product-video';
            var galeryPopup = $.magnificPopup.instance;
            galeryPopup.items.push({
              src: productVideo,
              type: 'iframe'
            });
            galeryPopup.updateItemHTML();
          }
        },
        open: function() {}
      }
      // other options
    });
  }
  $('.design_3 .product-img,.design_5 .pro_img').magnificPopup({
    delegate: 'a', // child items selector, by clicking on it popup will open
    type: 'image',
    tLoading: '<div class="please-wait dark"><span></span><span></span><span></span></div>',
    removalDelay: 300,
    closeOnContentClick: true,
    gallery: {
      enabled: true,
      navigateByImgClick: false,
      preload: [0, 1]
    },
    image: {
      verticalFit: false,
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    },
    callbacks: {
      beforeOpen: function() {
        var productVideo = $('.product-video-popup').attr('href');
        if (productVideo) {
          this.st.mainClass = 'has-product-video';
          var galeryPopup = $.magnificPopup.instance;
          galeryPopup.items.push({
            src: productVideo,
            type: 'iframe'
          });
          galeryPopup.updateItemHTML();
        }
      },
      open: function() {}
    }
    // other options
  });
  $('body').on('click', '.product-lightbox-btn', function(e) {
    $('.product-wrapper-owlslider').find('.owl-item.active a').click();
    e.preventDefault();
  });
  $('.product-layouts .qtyplus').on('click', function(e) {
    e.preventDefault();
    var input_val = jQuery(this).parents('.qty-box-set').find('.quantity');
    var currentVal = parseInt(jQuery(this).parents('.qty-box-set').find('.quantity').val());
    if (!isNaN(currentVal)) {
      jQuery(this).parents('.qty-box-set').find('.quantity').val(currentVal + 1)
    } else {
      jQuery(this).parents('.qty-box-set').find('.quantity').val(1)
    }
  });
  $(".product-layouts .qtyminus").on('click', function(e) {
    e.preventDefault();
    var input_val = jQuery(this).parents('.qty-box-set').find('.quantity');
    var currentVal = parseInt(jQuery(this).parents('.qty-box-set').find('.quantity').val());
    if (!isNaN(currentVal) && currentVal > 1) {
      jQuery(this).closest('.qty-box-set').find('.quantity').val(currentVal - 1)
    } else {
      jQuery(this).closest('.qty-box-set').find('.quantity').val(1)
    }
  });
  jQuery(".fullscreen_header_toggle").on("click" , function(e){
    e.preventDefault();
    jQuery(this).toggleClass("active");
    jQuery(".fullscreen_header").toggleClass("nav-open");
    jQuery("body").toggleClass("fullnav-open header_2");
  });

  /* start vertical js*/	
  if(jQuery(".leftmenu_header").length > 0){
    if(jQuery(".leftmenu_header_fixed.leftmenu_header").length > 0){
      if(jQuery(".leftmenu_header_fixed.leftmenu_header").hasClass('menu_left')){
        jQuery("body").addClass("menu_left");
      } 
      if(jQuery(".leftmenu_header_fixed.leftmenu_header").hasClass('menu_right')){
        jQuery("body").addClass("menu_right");
      }
    }
    jQuery(".leftmenu_header").on("click" , function(e){
      e.preventDefault();
      jQuery(this).toggleClass("active");
      jQuery("body").toggleClass("nav-open");
    });

  }

  /* end vertical js*/

  /* special product thumb js*/
  jQuery('.slider-newproduct .product-single__thumbs a').on('click', function () {
    var src = jQuery(this).data("fullsrc");
    if (src != '') {
      jQuery(this).closest('.product-wrapper').find('img.grid-view-item__image').first().attr('src', src);
    }
    jQuery(this).parent('.grid-item').addClass('open').siblings('.grid-item').removeClass('open');
  });


  $('.qtyplus').on('click',function(e){
    e.preventDefault();     
    var  input_val = jQuery(this).parents('.qty-box-set').find('.quantity');
    var currentVal = parseInt( jQuery(this).parents('.qty-box-set').find('.quantity').val());
    if (!isNaN(currentVal)) {
      jQuery(this).parents('.qty-box-set').find('.quantity').val(currentVal + 1);
    } else {
      jQuery(this).parents('.qty-box-set').find('.quantity').val(1);
    }

  });

  $(".qtyminus").on('click',function(e) {
    e.preventDefault();
    var  input_val = jQuery(this).parents('.qty-box-set').find('.quantity');
    var currentVal = parseInt( jQuery(this).parents('.qty-box-set').find('.quantity').val());
    if (!isNaN(currentVal) && currentVal > 1) {
      jQuery(this).parents('.qty-box-set').find('.quantity').val(currentVal - 1);
    } else {
      jQuery(this).parents('.qty-box-set').find('.quantity').val(1);
    }

  });
  $("#navToggle").on('click',function(e) {
    jQuery(this).next('.Site-navigation').slideToggle(500);
  });
  $(".menu_toggle_wrap #navToggle").on('click',function(e) {
    jQuery(this).parent().next('.Site-navigation').slideToggle(500);
  });


  /*Scroll to top js*/
  jQuery("#GotoTop").on('click',function () {
    jQuery("html, body").animate({
      scrollTop: 0
    }, '1000');
    return false;
  });

  jQuery(".site-header__search.search-full .serach_icon").on('click',function(e){
    e.preventDefault();
    jQuery(this).toggleClass('active'); 
    jQuery('body').toggleClass('search_full_active'); 
    jQuery('.full-search-wrapper').addClass('search-overlap');
    jQuery(".search-bar > input").focus();
  });
  jQuery(".site-header__search.search-full .close-search").on('click',function(){
    jQuery('.site-header__search.search-full .serach_icon').removeClass('active');   
    jQuery('.full-search-wrapper').removeClass('search-overlap');   
    jQuery('body').removeClass('search_full_active'); 
  });

  jQuery(".site-header__search:not(.search-full) .serach_icon").on('click',function(){    
    jQuery( ".search_wrapper" ).slideToggle( "fast" );
    jQuery( ".search-bar > input" ).focus();
    jQuery(this).toggleClass('active');
    jQuery( ".customer_account" ).slideUp( "fast" );  
    jQuery('body').removeClass('currency-open');
    jQuery('body').removeClass('language-open');
    jQuery('body').removeClass('myaccount_active');

    jQuery( "#slidedown-cart" ).slideUp( "fast" );
    jQuery( "#Sticky-slidedown-cart" ).slideUp( "fast" );
  });
  jQuery(".myaccount  .dropdown-toggle").on('click', function(event) {
    event.preventDefault();
    jQuery(".customer_account").slideToggle("fast");
    jQuery('.site-header__search:not(.search-full) .serach_icon').removeClass('active');
    jQuery('body').removeClass('search_full_active');
    jQuery('.site-header_cart_link').removeClass('active');
    jQuery(".site-header .search_wrapper").slideUp("fast");
    jQuery('body').toggleClass('myaccount_active');
    jQuery('body').removeClass('cart_active');
    jQuery('body').removeClass('currency-open');
    jQuery('body').removeClass('language-open');
    jQuery("#slidedown-cart").slideUp("fast");
                                    jQuery( ".language.flag-dropdown-menu" ).slideUp( "fast" );
        jQuery( ".currencies.flag-dropdown-menu" ).slideUp( "fast" );
    jQuery("#Sticky-slidedown-cart").slideUp("fast")
  });
  $(".header_currency .currency_wrapper.dropdown-toggle").on("click", function (event) {     
    event.preventDefault();
    jQuery(".customer_account").stop(); 
    jQuery( ".currencies.flag-dropdown-menu" ).slideToggle( "fast" );
    $(this).toggleClass('active');   
    jQuery('body').toggleClass('currency-open');
    jQuery('body').removeClass('language-open');
    jQuery('body').removeClass('myaccount_active');
    jQuery('body').removeClass('cart_active');
    jQuery( ".language.flag-dropdown-menu" ).slideUp( "fast" );
    jQuery("#slidedown-cart").slideUp("fast");
    jQuery("#Sticky-slidedown-cart").slideUp("fast");
    $(".header_language .language-block .language_wrapper.dropdown-toggle").removeClass('active');
  });
  /*---------------- Language ---------------*/
  $(".header_language .language-block .language_wrapper.dropdown-toggle").on("click", function (event) {     
    event.preventDefault();
    jQuery(".customer_account").stop();      
    jQuery( ".language.flag-dropdown-menu" ).slideToggle( "fast" );
    $(this).toggleClass('active');  
    jQuery('body').toggleClass('language-open');
    jQuery('body').removeClass('cart_active');
    jQuery('body').removeClass('currency-open');
    jQuery('body').removeClass('myaccount_active');
    jQuery( ".currencies.flag-dropdown-menu" ).slideUp( "fast" );
    jQuery("#slidedown-cart").slideUp("fast");
    jQuery("#Sticky-slidedown-cart").slideUp("fast");
    jQuery( ".customer_account" ).slideUp( "fast" );
    $(".header_currency .currency_wrapper.dropdown-toggle").removeClass('active');
  });


           /*-------------------- END -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*/



  function stickymenu() {
      if($('.toggle_menu').hasClass('current-open') && $('.sticky_header').hasClass('fixed')) {
      $('.toggle_menu').addClass("current-close");
      $('body').removeClass("menu-current-open");
      $('.toggle_menu').removeClass("current-open");
      $('.tt-mega_menu').slideToggle("2000");
    }
  }
  
  $(document).ready(function() {
    stickymenu()
  });
  $(window).resize(function() {
    stickymenu()
  });
  $(window).scroll(function() {
    stickymenu()
  });
  

  

    jQuery(".header_currency .flag-dropdown-menu>li").click(function(){
    jQuery(".currencies").slideUp();
    jQuery("body").removeClass("currency-open");
    jQuery(".currency_wrapper").removeClass("active");
});
  
  
    jQuery(document).on("click", function(event) {
  
  var myacc = jQuery(".myaccount")[0];
  var myaccont = jQuery(".myaccount");

  if (
    myaccont !== event.target &&
    !myaccont.has(event.target).length &&
    myacc !== event.target
  ) {
    jQuery(".customer_account").slideUp("fast");
    jQuery("body").removeClass("myaccount_active");
    jQuery(".myaccount").removeClass("open");
  }

        var car = jQuery(".site-header__cart")[0];
  var cart = jQuery(".site-header__cart");
  if (
    cart !== event.target &&
    !cart.has(event.target).length &&
    car !== event.target
  ) {
    jQuery("#Sticky-slidedown-cart").slideUp("slow");
    jQuery("body").removeClass("cart_active");
    jQuery(".site-header_cart_link").removeClass("active");
  }
      

var langu = jQuery(".language")[0];
var language = jQuery(".language");

if (language !== event.target && !language.has(event.target).length && langu !== event.target) {
			jQuery('.language.flag-dropdown-menu').slideUp("fast");
			jQuery('body').removeClass("language-open");
            jQuery('.language_wrapper').removeClass("active");
}

var curr = jQuery(".currency")[0];
var currency = jQuery(".currency");

if (currency !== event.target && !currency.has(event.target).length && curr !== event.target) {
			jQuery('.currencies').slideUp("fast");
			jQuery('body').removeClass("currency-open");
            jQuery('.currency_wrapper').removeClass("active");
} 
});
  // /*-------------------- END ------------------------------------------
  
  

  $('.mobile-nav__sublist-trigger').on('click', function(evt) {
    evt.preventDefault();
    var $el = $(this);
    $el.toggleClass('is-active');
    $el.parent().find('.tt_sub_menu_wrap').slideToggle(200);
  });

  /*$(".Site-navigation .header-icons-wrap").append($(".menu_toggle_wrap"));*/
  $('.slider-bestproduct .product-wrapper').each(function(){
    var $desc = $(this).find('.product-description .progress');
    var $qty = $(this).find('.quantity');
    var $pbar = $(this).find('.progress-bar');
    var $progress = $desc;
    var $progressBar = $pbar;
    var $quantity = $qty.html();
    var currentWidth = parseInt($progressBar.css('width'));
    var allowedWidth = parseInt($progress.css('width'));
    var addedWidth = currentWidth + parseInt($quantity);
    if (addedWidth > allowedWidth) {
      addedWidth = allowedWidth;
    }
    var progress = (addedWidth / allowedWidth) * 100;
    $progressBar.animate({width: progress + '%' }, 100);
  });



  var p_col = jQuery('.slider-bestproduct').data('col');
  $('body:not(.rtl) .slider-bestproduct').owlCarousel({
    items : p_col, //10 items above 1000px browser width
    nav : true,
    autoplay:true,
    autoplaySpeed:1500,	
    dots : false,
    responsive: {
      100: {
        items: 1
      },
      543: {
        items: 2
      },
      768: {
        items: 2
      },
      992: {
        items:2
      },
      1200: {
        items: 3
      },
      1660: {
        items: 4
      },
      1700: {
        items: p_col
      }
    }
  });

  $('body.rtl .slider-bestproduct').owlCarousel({
    items : p_col, //10 items above 1000px browser width
    nav : true,
    dots : false,
    autoplay:true,
    autoplaySpeed:1500,	
    responsive: {
      100: {
        items: 1
      },
      543: {
        items: 2
      },
      768: {
        items: 2
      },
      992: {
        items: 2
      },
      1200: {
        items: 3
      },
      1660: {
        items: 4
      },
      1700: {
        items: p_col
      }
    }
  });

    var prevScrollpos = window.pageYOffset;
  window.onscroll = function(e) {
    var currentScrollPos = window.pageYOffset;
    var stickyHeader = document.getElementById("header-sticky");
    
    if (stickyHeader) {
      if (prevScrollpos > currentScrollPos) {
        stickyHeader.style.top = "0";
      } 
      else if ( $('body').hasClass('account-toggle') || $('body').hasClass('menu_hover') || $('body').hasClass('cart_toggle') || $('body').hasClass('search_toggle')) {
        stickyHeader.style.top = "0";
        e.stopPropagation();
      }
      else {
        stickyHeader.style.top = "-100px";
      }
    }
    prevScrollpos = currentScrollPos;
  }

  $('.slider-bestproduct-wrap').each(function () { 
    if($(this).find('.owl-nav').hasClass('disabled')){
      $(this).find('.customNavigation').hide();
    }else{
      $(this).find('.customNavigation').show();
    }
  });
  $(".slider-bestproduct-wrap .customNavigation .next").click(function(){
    var wrap = $(this).closest('.slider-bestproduct-wrap');
    $(wrap).find('.slider-bestproduct').trigger('next.owl');
  });
  $(".slider-bestproduct-wrap .customNavigation .prev").click(function(){
    var wrap = $(this).closest('.slider-bestproduct-wrap');
    $(wrap).find('.slider-bestproduct').trigger('prev.owl');
  });

  $('body:not(.rtl) #ttcmsfooter-services .block_content').owlCarousel({
    items :5, //1 items above 1000px browser width
    nav : true,
    dots : true,
    loop: false,
    autoplay:true,
    rtl:false,
    responsive: {
      1430: {
        items: 5
      },
      1200: {
        items: 4
      },
      992: {
        items: 3
      },
      768: {
        items: 2
      },
      100: {
        items:2
      }
    }
  });
  $('body.rtl #ttcmsfooter-services .block_content').owlCarousel({
    items : 5, //1 items above 1000px browser width
    nav : true,
    dots : true,
    loop: false,
    autoplay:true,				
    rtl:true,
    responsive: {
      1430: {
        items: 5
      },
      1200: {
        items: 4
      },
      992: {
        items: 3
      },
      768: {
        items: 2
      },
      100: {
        items: 2
      }
    }
  });

  $('body:not(.rtl) .slider-newproduct .product-single__thumbs').owlCarousel({
    items :2, //1 items above 1000px browser width
    nav : true,
    dots : false,
    loop: false,
    autoplay:false,
    slideTransition: 'linear',
    rtl:false,
    responsive: {
      1279: {
        items: 2
      },
      600: {
        items:2
      }
    }
  });
  $('body.rtl .slider-newproduct .product-single__thumbs').owlCarousel({
    items : 2, //1 items above 1000px browser width
    nav : true,
    dots : false,
    loop: false,
    autoplay:false,
    slideTransition: 'linear',
    rtl:true,
    responsive: {
      1279: {
        items: 2
      },
      600: {
        items: 2
      }
    }
  });


  $('body:not(.rtl) .widget_top_rated_products .top-products').owlCarousel({
    items : 1, //1 items above 1000px browser width
    nav : true,
    dots : true,
    loop: false,
    autoplay:true,
    rtl:false,
    responsive: {
      1279: {
        items: 1
      },
      1250: {
        items: 1
      },
      600: {
        items: 1
      }
    }
  });
  $('body.rtl .widget_top_rated_products .top-products').owlCarousel({
    items : 1, //1 items above 1000px browser width
    nav : true,
    dots : true,
    loop: false,
    autoplay:true,				
    rtl:true,
    responsive: {
      1279: {
        items: 1
      },
      1250: {
        items: 1
      },
      600: {
        items: 1
      }
    }
  });

  $('body:not(.rtl) .ttleft-testimonial-wrap .testimonials_wrap').owlCarousel({
    items : 1, //1 items above 1000px browser width
    nav : true,
    dots : true,
    loop: false,
    autoplay:true,
    rtl:false,
    responsive: {
      1279: {
        items: 1
      },
      1250: {
        items: 1
      },
      600: {
        items: 1
      }
    }
  });
  $('body.rtl .ttleft-testimonial-wrap .testimonials_wrap').owlCarousel({
    items : 1, //1 items above 1000px browser width
    nav : true,
    dots : true,
    loop: false,
    autoplay:true,				
    rtl:true,
    responsive: {
      1279: {
        items: 1
      },
      1250: {
        items: 1
      },
      600: {
        items: 1
      }
    }
  });
  $('body:not(.rtl) .testimonial-wrap .testimonials_wrap').owlCarousel({
    items : 1, //1 items above 1000px browser width
    nav : true,
    dots : true,
    loop: false,
    autoplay:true,
    rtl:false,
    responsive: {
      1279: {
        items: 1
      },
      1250: {
        items: 1
      },
      600: {
        items: 1
      }
    }
  });
  $('body.rtl .testimonial-wrap .testimonials_wrap').owlCarousel({
    items : 1, //1 items above 1000px browser width
    nav : true,
    dots : true,
    loop: false,
    autoplay:true,				
    rtl:true,
    responsive: {
      1279: {
        items: 1
      },
      1250: {
        items: 1
      },
      600: {
        items: 1
      }
    }
  });

  $('body:not(.rtl) #ttcmsservices .block_content').owlCarousel({
    items :4, //1 items above 1000px browser width
    nav : true,
    dots : true,
    loop: true,
    autoplay:true,
    rtl:false,
    responsive: {
      1279: {
        items: 4
      },
      992: {
        items: 4
      },
      481: {
        items: 3
      },
      100: {
        items:1
      }
    }
  });
  $('body.rtl #ttcmsservices .block_content').owlCarousel({
    items : 4, //1 items above 1000px browser width
    nav : true,
    dots : true,
    loop: true,
    autoplay:true,				
    rtl:true,
    responsive: {
      1279: {
        items: 4
      },
      992: {
        items: 4
      },
      481: {
        items: 3
      },
      100: {
        items: 1
      }
    }
  });



  $('body:not(.rtl) #tt-megamenu .list_product_menu_content').owlCarousel({
    items : 3, //1 items above 1000px browser width
    nav : true,
    autoPlay:true,
    autoplaySpeed:1000,
    stopOnHover: false,
    loop: false,
    dots : true,
    responsive: {
      992: {
        items: 3
      },
      481: {
        items: 2
      },
      100: {
        items: 1
      }
    }
  });
  $('body.rtl #tt-megamenu .list_product_menu_content').owlCarousel({
    items : 3, //1 items above 1000px browser width
    nav : true,
    autoPlay:true,
    autoplaySpeed:1000,
    rtl: true,
    stopOnHover: false,
    loop: false,
    dots : true,
    responsive: {
      992: {
        items: 3
      },
      481: {
        items: 2
      },
      100: {
        items: 1
      }
    }
  });



  var blogowlrtl = $("body.rtl .grid-blog-slider");
  $("body.rtl .grid-blog-slider").owlCarousel({
    items : 3 , //10 items above 1000px browser width
    loop: false,
    nav: true,  
    rtl: true, 
    dots: false,
    autoplayHoverPause: true,
    responsive: {
      100: {
        items: 1
      },
      543: {
        items: 2
      },
      992: {
        items: 2
      },
      1200: {
        items: 3
      },
      1460: {
        items: 4
      }
    }
  });

  var blogowl = $("body:not(.rtl) .grid-blog-slider");
  $("body:not(.rtl) .grid-blog-slider").owlCarousel({
    items : 3 , //10 items above 1000px browser width
    loop: false,
    nav: true,  
    rtl: false,  
    dots: false,
    autoplayHoverPause: true,
    responsive: {
      100: {
        items: 1
      },
      543: {
        items: 2
      },
      992: {
        items: 2
      },
      1200: {
        items: 3
      },
      1460: {
        items: 4
      }
    }
  });
  $('.grid--blog').each(function () { 
    if($(this).find('.owl-nav').hasClass('disabled')){
      $(this).find('.customNavigation').hide();
    }else{
      $(this).find('.customNavigation').show();
    }
  });
  $(".blog_next").click(function(){
    $(".grid-blog-slider").trigger('next.owl');
  });
  $(".blog_prev").click(function(){
    $(".grid-blog-slider").trigger('prev.owl');
  });


  $('.brand-bar').each(function () { 
    if($(this).find('.owl-nav').hasClass('disabled')){
      $(this).find('.customNavigation').hide();
    }else{
      $(this).find('.customNavigation').show();
    }
  });
  $(".brand_next").click(function(){
    $(".tt-brand_slider").trigger('next.owl');
  });
  $(".brand_prev").click(function(){
    $(".tt-brand_slider").trigger('prev.owl');
  });

  if($('body:not(#index) .toggle_menu').hasClass('current-close')) {
    $('.tt-mega_menu').slideUp("2000");
  }
  $('.toggle_menu').click(function() {
    if($(this).hasClass('default-open') && $(window).width() < 992){
      if($(this).hasClass('current-close')) {
        $(this).addClass("current-open");
        $('body').addClass("menu-current-open");
        $(this).removeClass("current-close");
        $('.tt-mega_menu').slideToggle("2000");
      } else {
        $(this).removeClass("default-open");
        $(this).addClass("current-open");
        $('body').addClass("menu-current-open");
        $(this).removeClass("current-close");
        $('.tt-mega_menu').slideToggle("2000");
      }    
    }else if($(this).hasClass('default-open')){
      if($(this).hasClass('current-close')) {
        $(this).addClass("current-open");
        $('body').addClass("menu-current-open");
        $(this).removeClass("current-close");
        $('.tt-mega_menu').slideToggle("2000");
      } else if($(this).hasClass('current-open')) {
        $(this).addClass("current-close");
        $(this).removeClass("current-open");
        $('body').removeClass("menu-current-open");
        $('.tt-mega_menu').slideToggle("2000");
      }
    }
    else{
      if($(this).hasClass('current-open')) {
        $(this).addClass("current-close");
        $('body').removeClass("menu-current-open");
        $(this).removeClass("current-open");
        $('.tt-mega_menu').slideToggle("2000");
      } else{
        $(this).addClass("current-open");
        $(this).removeClass("current-close");
        $('body').addClass("menu-current-open");
        $('.tt-mega_menu').slideToggle("2000");
      }
    }

    if($(this).hasClass('default-open') && !$('.sticky_header').hasClass('fixed')) {
      $(this).addClass("current-close");
      $(this).removeClass("default-open");
      $('.tt-mega_menu').slideToggle("2000");
    }	
    if($(this).hasClass('default-open') && $('.sticky_header').hasClass('fixed')) {
      $(this).addClass("current-open");
      $('body').addClass("menu-current-open");
      $(this).removeClass("default-open");
      $('.tt-mega_menu').slideDown("2000");
    }
  });
});



jQuery(window).scroll(function () {
  if(jQuery(document).height() > jQuery(window).height()){
    var scroll = jQuery(window).scrollTop();
    if (scroll > 100) {
      jQuery("#GotoTop").fadeIn();
    } else {
      jQuery("#GotoTop").fadeOut();
    }
  }
});

function responsiveMenu(){
  if(jQuery(window).width() < 992) {

    jQuery(".Site-navigation").insertAfter( ".nav-toggle" );
    jQuery('.sub-nav__dropdown').css('display','none');   

  }else{
    jQuery(".Site-navigation").appendTo( ".menu_wrapper" );

  } 

  if(jQuery(window).width() < 992) {
    $('#shopify-section-TT-mega_menu').appendTo('.menu-bar .ttresponsive_menu');	
    $('#accessibleNav').appendTo('#tt-megamenu .tt_menus_ul');
    // $("#top .header-top-right").insertAfter('#tt-megamenu #accessibleNav');
    $(".header_1 .header-right-cms").appendTo('#tt-megamenu .tt_menus_ul');
    $(".header_2 .cms-contactus").appendTo('#tt-megamenu .tt_menus_ul');
    $(".header_1 .header-middle").insertBefore('.ttresponsive_menu-wrap');
    $(".header_1 .myaccount").insertAfter('.header-middle');
    $(".header_1 .ttcmsheader").insertBefore('.header-right-cms');
  }
  else{
    $(".header_style_1 #shopify-section-TT-mega_menu").insertBefore('.menu-bar .header-middle');
    $(".header_style_3 #shopify-section-TT-mega_menu").insertBefore('.full-header .header-middle');
    $('.header_style_3 .header-right').insertAfter('.header_style_3 .header-middle');
    $("#tt-megamenu .tt_menus_ul .header-right-cms").insertBefore('.full-header .header-middle');
    $('#tt-megamenu .tt_menus_ul #accessibleNav').appendTo('.topmenu');
    $(".header_style_2 #tt-megamenu .tt_menus_ul .cms-contactus").insertAfter('.header_2 .topmenu');
    // $("#tt-megamenu .tt_menus_ul .header-top-right").insertAfter('#top .header-top-left');
    $(".header_style_1 .menu-bar .myaccount").insertBefore('.header_style_1 .full-header .topmenu');
    $(".header_style_1 #tt-megamenu .ttcmsheader").insertBefore('.header_style_1 .full-header .topmenu'); 
  }
}
jQuery(document).ready(function() {
  responsiveMenu();

  jQuery(".product-write-review").on('click',function(e) {
    e.preventDefault();
    $('a[href=\'#tab-2\']').trigger('click');
    jQuery('html, body').animate({
      scrollTop: jQuery(".product_tab_wrapper").offset().top-150
    }, 1000);
  });
});
jQuery(document).load(function() { 
  //var menu_wrapper = jQuery('.menu_wrapper.logo_left').height();

});
jQuery(window).resize(function() {
  responsiveMenu();
  var w_width = $(window).width();
  $('.slider-content-main-wrap').css('width',w_width);
});


function footerToggle() {
  if(jQuery( window ).width() < 992) { 
    jQuery('.header-right').appendTo('.ttresponsive_menu');

  }else{
    jQuery('.ttresponsive_menu .header-right').insertAfter('.header-left');
  }
  if(jQuery( window ).width() < 992) { 
    if($('.left-sidebar-menu').length > 0){
      jQuery('.left-sidebar-menu').appendTo('.ttresponsive_menu');
      jQuery('.header-right').appendTo('.ttresponsive_menu');

      jQuery(".ttresponsive_menu h4.widget-title").unbind("click");
      jQuery(".ttresponsive_menu  h4.widget-title").on('click',function() {
        jQuery(this).parent().toggleClass('active').children(':nth-child(2)').slideToggle( "fast" );
      }); 
    }else{

      jQuery('nav#menu .nav-menu-wrapper').appendTo('.ttresponsive_menu');
      jQuery(".nav-menu-wrapper h4.widget-title").unbind("click");
      jQuery(".nav-menu-wrapper h4.widget-title").on('click',function() {
        jQuery(this).parent().toggleClass('active').children(':nth-child(2)').slideToggle( "fast" );
      }); 
    }

    jQuery('#column-left').insertAfter('#content');
    if(jQuery('.site-footer').hasClass('fixed_footer'))  {
      jQuery('.page-wrapper').css('margin-bottom','0px');
    }
    jQuery('.left-sidebar.sidebar').insertAfter('.collection_wrapper, .content-wrapper');
    jQuery('.sidebar .sidebar-block').insertAfter('.filter-wrapper');
    jQuery('.both_sidebar .sidebar#column-left .collection_sidebar').insertAfter('.filter-wrapper');
    jQuery(".site-footer .footer-column h5").addClass( "toggle" );
    jQuery(".site-footer .footer-column").children(':nth-child(2)').css( 'display', 'none' );
    jQuery(".site-footer .footer-column.active").children(':nth-child(2)').css( 'display', 'block' );
    jQuery(".site-footer .footer-column h5.toggle").unbind("click");
    jQuery(".site-footer .footer-column h5.toggle").on('click',function() {
      jQuery(this).parent().toggleClass('active').children(':nth-child(2)').slideToggle( "fast" );
    });   
    jQuery(".site-footer .widget h5").addClass( "toggle" );
    jQuery(".site-footer .widget").children(':nth-child(2)').css( 'display', 'none' );
    jQuery(".site-footer .widget.active").children(':nth-child(2)').css( 'display', 'block' );
    jQuery(".site-footer .widget h5.toggle").unbind("click");
    jQuery(".site-footer .widget h5.toggle").on('click',function() {
      jQuery(this).parent().toggleClass('active').children(':nth-child(2)').slideToggle( "fast" );
    });   
    jQuery(".sidebar .widget > h4").addClass( "toggle" );
    jQuery(".sidebar .widget ").children(':nth-child(2)').css( 'display', 'none' );
    jQuery(".sidebar .widget.active").children(':nth-child(2)').css( 'display', 'block' );
    jQuery(".sidebar .widget > h4.toggle").unbind("click");
    jQuery(".sidebar .widget > h4.toggle").on('click',function() {
      jQuery(this).parent().toggleClass('active').children(':nth-child(2)').slideToggle( "fast" );
    });   
    jQuery(".sidebar-block .widget > h4").addClass( "toggle" );
    jQuery(".sidebar-block .widget ").children(':nth-child(2)').css( 'display', 'none' );
    jQuery(".sidebar-block .widget.active").children(':nth-child(2)').css( 'display', 'block' );
    jQuery(".sidebar-block .widget > h4.toggle").unbind("click");
    jQuery(".sidebar-block .widget > h4.toggle").on('click',function() {
      jQuery(this).parent().toggleClass('active').children(':nth-child(2)').slideToggle( "fast" );
    });  
  }else{
    if($('.left-sidebar-menu').length > 0){
      jQuery('#accessibleNav').appendTo('.nav-menu-wrapper .navbar-collapse');
    }else{
      jQuery('.ttresponsive_menu .nav-menu-wrapper').appendTo('nav#menu');
    }
    jQuery('.left-sidebar-menu').appendTo('#shopify-section-left-col-menu');
    jQuery('#column-left').insertBefore('#content');
    jQuery('.sidebar .sidebar-block').insertAfter('#shopify-section-left-col-menu');
    jQuery('.both_sidebar .sidebar#column-left .sidebar-block').prependTo('.collection_sidebar');
    jQuery('.section-header .sidebar-block').prependTo('.collection_sidebar');
    if(jQuery('.site-footer').hasClass('fixed_footer'))  {
      var footer_h = jQuery('.site-footer.fixed_footer').height();
      jQuery('.page-wrapper').css('margin-bottom',footer_h+'px');
    }
    jQuery('.left-sidebar.sidebar').insertBefore('.collection_wrapper, .content-wrapper');
    jQuery(".sidebar .widget h4.widget-title").addClass( "toggle" );
    jQuery(".sidebar .widget .product-categories, .sidebar .widget .facets-filter").css( 'display', 'none' );
    jQuery(".sidebar .widget.active .product-categories, .sidebar .widget.active .facets-filter").css( 'display', 'block' );
    jQuery(".sidebar .widget h4.widget-title").unbind("click");
    jQuery(".sidebar .widget h4.widget-title").on('click',function() {
      var $widget = jQuery(this).closest('.widget');
      $widget.toggleClass('active');
      $widget.find('.product-categories, .facets-filter').slideToggle( "fast" );
    });

    jQuery(".site-footer .footer-column h5").unbind("click");
    jQuery(".site-footer .footer-column h5").removeClass( "toggle" );
    jQuery(".site-footer .footer-column").children(':nth-child(2)').css( 'display', 'block' );
    jQuery(".site-footer .widget h5").unbind("click");
    jQuery(".site-footer .widget h5").removeClass( "toggle" );
    jQuery(".site-footer .widget").children(':nth-child(2)').css( 'display', 'block' );

  }

  if (jQuery(window).width() < 1200) {
    jQuery('.both-sidebar .left-sidebar.sidebar').insertAfter('.collection_wrapper, .content-wrapper');
    jQuery('.both-sidebar .sidebar .sidebar-block').insertAfter('.filter-wrapper');
    jQuery('.both-sidebar #column-left').insertAfter('#content');
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
  } else {
    jQuery('.both-sidebar .left-sidebar.sidebar').insertBefore('.collection_wrapper, .content-wrapper');
    jQuery('.both-sidebar #column-left').insertBefore('#content');
    jQuery('.both-sidebar .sidebar .sidebar-block').insertAfter('#shopify-section-left-col-menu');
    jQuery('.both-sidebar .section-header .sidebar-block').prependTo('.collection_sidebar');
    jQuery(".both-sidebar .sidebar .widget > h4").unbind("click");
    jQuery(".both-sidebar .sidebar .widget > h4").removeClass("toggle");
    jQuery(".both-sidebar .sidebar .widget").children(':nth-child(2)').css('display', 'block');
  }

}
jQuery(document).ready(function() {
  footerToggle();
  sidebarsticky();  
});
jQuery(window).load(function() {
  var h = $('.design_4 .product-wrapper-owlslider').height();
  $('.design_4 .product-information-inner.tt-scroll').css('min-height', h+"px");
});
jQuery(window).resize(function() {
  footerToggle();
  var h = $('.design_4 .product-wrapper-owlslider').height();
  $('.design_4 .product-information-inner.tt-scroll').css('min-height', h+"px");
});

function splitStr(string,seperator){
  return string.split(seperator);
}

function countDownIni(countdown) {
  $(countdown).each(function () {
    var countdown = $(this);
    var promoperiod;
    if (countdown.attr('data-promoperiod')) {
      promoperiod = new Date().getTime() + parseInt(countdown.attr('data-promoperiod'), 10);
    } else if (countdown.attr('data-countdown')) {
      promoperiod = countdown.attr('data-countdown');
    }
    if (Date.parse(promoperiod) - Date.parse(new Date()) > 0) {
      $(this).parent(".simple-countdown").addClass("countdown-block");
      $(this).parent().addClass('countdown-enable');
      countdown.countdown(promoperiod, function (event) {
        // countdown.html(event.strftime('%-w weeks %-d days %Hh %Mm %Ss'));
        countdown.html(event.strftime('<span><span class="left-txt">LEFT</span><span>%D</span><span class="time-txt">days</span></span>' + '<span><span>%H</span><span class="time-txt">hours</span></span>' + '<span><span>%M</span><span class="time-txt">min</span></span>' + '<span><span class="second">%S</span><span class="time-txt">sec</span></span>'));
      });
    }

  });
}

function sidebarsticky() { 
  if ($(document).width() > 992 && $(document).width() < 1199) {
    jQuery('#column-left,.no_sidebar .left-sidebar.sidebar,.no_sidebar .right-sidebar.sidebar').theiaStickySidebar({
      additionalMarginBottom: 30,
      additionalMarginTop: 30
    });
  } 
  else if ($(document).width() >= 1200) {
    jQuery('#column-left,.no_sidebar .left-sidebar.sidebar,.no_sidebar .right-sidebar.sidebar').theiaStickySidebar({
      additionalMarginBottom: 30,
      additionalMarginTop: 130
    });
  }
}
jQuery(window).resize(function() {
  sidebarsticky();
});





function bindgrid() {
  
if (localStorage.getItem('display') == 'grid') {
    
jQuery('#grid-view').trigger('click')
  
} 
else if (localStorage.getItem('display') == 'grids') 
{
    
jQuery('#grid-views').trigger('click')
  
} 
else if (localStorage.getItem('display') == 'list') 
{
   
 jQuery('#list-view').trigger('click')
  
} 
else if (localStorage.getItem('display') == 'short-list') 
{
    
jQuery('#short-list-view').trigger('click')
  
} 
else 
{
    
jQuery('#grid-view').trigger('click')
  
}

		
if(jQuery(window).width() < 768) 
{
			
if(jQuery("#grid-view").hasClass("active")) 
{
			
jQuery("#grid-views").toggleClass("active");
			
			
}
		
}
		
if(jQuery(window).width() < 481) 
{
			
if(jQuery("#list-view").hasClass("active")) 
{
			
jQuery("#short-list-view").toggleClass("active");
			
jQuery("#list-view").removeClass("active");
			
}
		
}
 
}

$(document).ready(function(){
	
bindgrid();
});

$(window).load(function(){
	
bindgrid();
});

$(window).resize(function() {
	
bindgrid();
});	


