window.theme = window.theme || {};

/* ================ SLATE ================ */
window.theme = window.theme || {};

theme.Sections = function Sections() {
  this.constructors = {};
  this.instances = [];

  document.addEventListener(
    'shopify:section:load',
    this._onSectionLoad.bind(this)
  );
  document.addEventListener(
    'shopify:section:unload',
    this._onSectionUnload.bind(this)
  );
  document.addEventListener(
    'shopify:section:select',
    this._onSelect.bind(this)
  );
  document.addEventListener(
    'shopify:section:deselect',
    this._onDeselect.bind(this)
  );
  document.addEventListener(
    'shopify:block:select',
    this._onBlockSelect.bind(this)
  );
  document.addEventListener(
    'shopify:block:deselect',
    this._onBlockDeselect.bind(this)
  );
};
theme.Sections.prototype = Object.assign({}, theme.Sections.prototype, {
  _createInstance: function(container, constructor) {
    var id = container.getAttribute('data-section-id');
    var type = container.getAttribute('data-section-type');

    constructor = constructor || this.constructors[type];

    if (typeof constructor === 'undefined') {
      return;
    }

    var instance = Object.assign(new constructor(container), {
      id: id,
      type: type,
      container: container
    });

    this.instances.push(instance);
  },

  _onSectionLoad: function(evt) {
    var container = document.querySelector(
      '[data-section-id="' + evt.detail.sectionId + '"]'
    );

    if (container) {
      this._createInstance(container);
    }
  },

  _onSectionUnload: function(evt) {
    this.instances = this.instances.filter(function(instance) {
      var isEventInstance = instance.id === evt.detail.sectionId;

      if (isEventInstance) {
        if (typeof instance.onUnload === 'function') {
          instance.onUnload(evt);
        }
      }

      return !isEventInstance;
    });
  },

  _onSelect: function(evt) {
    // eslint-disable-next-line no-shadow
    var instance = this.instances.find(function(instance) {
      return instance.id === evt.detail.sectionId;
    });

    if (
      typeof instance !== 'undefined' &&
      typeof instance.onSelect === 'function'
    ) {
      instance.onSelect(evt);
    }
  },

  _onDeselect: function(evt) {
    // eslint-disable-next-line no-shadow
    var instance = this.instances.find(function(instance) {
      return instance.id === evt.detail.sectionId;
    });

    if (
      typeof instance !== 'undefined' &&
      typeof instance.onDeselect === 'function'
    ) {
      instance.onDeselect(evt);
    }
  },

  _onBlockSelect: function(evt) {
    // eslint-disable-next-line no-shadow
    var instance = this.instances.find(function(instance) {
      return instance.id === evt.detail.sectionId;
    });

    if (
      typeof instance !== 'undefined' &&
      typeof instance.onBlockSelect === 'function'
    ) {
      instance.onBlockSelect(evt);
    }
  },

  _onBlockDeselect: function(evt) {
    // eslint-disable-next-line no-shadow
    var instance = this.instances.find(function(instance) {
      return instance.id === evt.detail.sectionId;
    });

    if (
      typeof instance !== 'undefined' &&
      typeof instance.onBlockDeselect === 'function'
    ) {
      instance.onBlockDeselect(evt);
    }
  },

  register: function(type, constructor) {
    this.constructors[type] = constructor;

    document.querySelectorAll('[data-section-type="' + type + '"]').forEach(
      function(container) {
        this._createInstance(container, constructor);
      }.bind(this)
    );
  }
});

window.slate = window.slate || {};

/**
 * Slate utilities
 * -----------------------------------------------------------------------------
 * A collection of useful utilities to help build your theme
 *
 *
 * @namespace utils
 */

slate.utils = {
  /**
   * Get the query params in a Url
   * Ex
   * https://mysite.com/search?q=noodles&b
   * getParameterByName('q') = "noodles"
   * getParameterByName('b') = "" (empty value)
   * getParameterByName('test') = null (absent)
   */
  getParameterByName: function(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
  },

  resizeSelects: function(selects) {
    selects.forEach(function(select) {
      var arrowWidth = 55;

      var test = document.createElement('span');
      test.innerHTML = select.selectedOptions[0].label;

      document.querySelector('.site-footer').appendChild(test);

      var width = test.offsetWidth + arrowWidth;
      test.remove();

      select.style.width = width + 'px';
    });
  },

  keyboardKeys: {
    TAB: 9,
    ENTER: 13,
    ESCAPE: 27,
    LEFTARROW: 37,
    RIGHTARROW: 39
  }
};

window.slate = window.slate || {};

/**
 * iFrames
 * -----------------------------------------------------------------------------
 * Wrap videos in div to force responsive layout.
 *
 * @namespace iframes
 */

slate.rte = {
  /**
   * Wrap tables in a container div to make them scrollable when needed
   *
   * @param {object} options - Options to be used
   * @param {NodeList} options.tables - Elements of the table(s) to wrap
   * @param {string} options.tableWrapperClass - table wrapper class name
   */
  wrapTable: function(options) {
    options.tables.forEach(function(table) {
      var wrapper = document.createElement('div');
      wrapper.classList.add(options.tableWrapperClass);

      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    });
  },

  /**
   * Wrap iframes in a container div to make them responsive
   *
   * @param {object} options - Options to be used
   * @param {NodeList} options.iframes - Elements of the iframe(s) to wrap
   * @param {string} options.iframeWrapperClass - class name used on the wrapping div
   */
  wrapIframe: function(options) {
    options.iframes.forEach(function(iframe) {
      var wrapper = document.createElement('div');
      wrapper.classList.add(options.iframeWrapperClass);

      iframe.parentNode.insertBefore(wrapper, iframe);
      wrapper.appendChild(iframe);

      iframe.src = iframe.src;
    });
  }
};

window.slate = window.slate || {};

/**
 * A11y Helpers
 * -----------------------------------------------------------------------------
 * A collection of useful functions that help make your theme more accessible
 * to users with visual impairments.
 *
 *
 * @namespace a11y
 */

slate.a11y = {
  state: {
    firstFocusable: null,
    lastFocusable: null
  },
  /**
   * For use when focus shifts to a container rather than a link
   * eg for In-page links, after scroll, focus shifts to content area so that
   * next `tab` is where user expects
   *
   * @param {HTMLElement} element - The element to be acted upon
   */
  pageLinkFocus: function(element) {
    if (!element) return;
    var focusClass = 'js-focus-hidden';

    element.setAttribute('tabIndex', '-1');
    element.focus();
    element.classList.add(focusClass);
    element.addEventListener('blur', callback, { once: true });

    function callback() {
      element.classList.remove(focusClass);
      element.removeAttribute('tabindex');
    }
  },

  /**
   * Traps the focus in a particular container
   *
   * @param {object} options - Options to be used
   * @param {HTMLElement} options.container - Container to trap focus within
   * @param {HTMLElement} options.elementToFocus - Element to be focused when focus leaves container
   */
  trapFocus: function(options) {
    var focusableElements = Array.from(
      options.container.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex^="-"])'
      )
    ).filter(function(element) {
      var width = element.offsetWidth;
      var height = element.offsetHeight;

      return (
        width !== 0 &&
        height !== 0 &&
        getComputedStyle(element).getPropertyValue('display') !== 'none'
      );
    });

    this.state.firstFocusable = focusableElements[0];
    this.state.lastFocusable = focusableElements[focusableElements.length - 1];

    if (!options.elementToFocus) {
      options.elementToFocus = options.container;
    }

    options.container.setAttribute('tabindex', '-1');
    options.elementToFocus.focus();

    this._setupHandlers();

    document.addEventListener('focusin', this._onFocusInHandler);
    document.addEventListener('focusout', this._onFocusOutHandler);
  },

  _setupHandlers: function() {
    if (!this._onFocusInHandler) {
      this._onFocusInHandler = this._onFocusIn.bind(this);
    }

    if (!this._onFocusOutHandler) {
      this._onFocusOutHandler = this._onFocusIn.bind(this);
    }

    if (!this._manageFocusHandler) {
      this._manageFocusHandler = this._manageFocus.bind(this);
    }
  },

  _onFocusOut: function() {
    document.removeEventListener('keydown', this._manageFocusHandler);
  },

  _onFocusIn: function(evt) {
    if (
      evt.target !== this.state.lastFocusable &&
      evt.target !== this.state.firstFocusable
    )
      return;

    document.addEventListener('keydown', this._manageFocusHandler);
  },

  _manageFocus: function(evt) {
    if (evt.keyCode !== slate.utils.keyboardKeys.TAB) return;

    /**
     * On the last focusable element and tab forward,
     * focus the first element.
     */
    if (evt.target === this.state.lastFocusable && !evt.shiftKey) {
      evt.preventDefault();
      this.state.firstFocusable.focus();
    }
    /**
     * On the first focusable element and tab backward,
     * focus the last element.
     */
    if (evt.target === this.state.firstFocusable && evt.shiftKey) {
      evt.preventDefault();
      this.state.lastFocusable.focus();
    }
  },

  /**
   * Removes the trap of focus in a particular container
   *
   * @param {object} options - Options to be used
   * @param {HTMLElement} options.container - Container to trap focus within
   */
  removeTrapFocus: function(options) {
    if (options.container) {
      options.container.removeAttribute('tabindex');
    }
    document.removeEventListener('focusin', this._onFocusInHandler);
  },

  /**
   * Add aria-describedby attribute to external and new window links
   *
   * @param {object} options - Options to be used
   * @param {object} options.messages - Custom messages to be used
   * @param {HTMLElement} options.links - Specific links to be targeted
   */
  accessibleLinks: function(options) {
    var body = document.querySelector('body');

    var idSelectors = {
      newWindow: 'a11y-new-window-message',
      external: 'a11y-external-message',
      newWindowExternal: 'a11y-new-window-external-message'
    };

    if (options.links === undefined || !options.links.length) {
      options.links = document.querySelectorAll(
        'a[href]:not([aria-describedby])'
      );
    }

    function generateHTML(customMessages) {
      if (typeof customMessages !== 'object') {
        customMessages = {};
      }

      var messages = Object.assign(
        {
          newWindow: 'Opens in a new window.',
          external: 'Opens external website.',
          newWindowExternal: 'Opens external website in a new window.'
        },
        customMessages
      );

      var container = document.createElement('ul');
      var htmlMessages = '';

      for (var message in messages) {
        htmlMessages +=
          '<li id=' + idSelectors[message] + '>' + messages[message] + '</li>';
      }

      container.setAttribute('hidden', true);
      container.innerHTML = htmlMessages;

      body.appendChild(container);
    }

    function _externalSite(link) {
      var hostname = window.location.hostname;

      return link.hostname !== hostname;
    }

    options.links.forEach(function(link) {
      var target = link.getAttribute('target');
      var rel = link.getAttribute('rel');
      var isExternal = _externalSite(link);
      var isTargetBlank = target === '_blank';

      if (isExternal) {
        link.setAttribute('aria-describedby', idSelectors.external);
      }

      if (isTargetBlank) {
        if (!rel || rel.indexOf('noopener') === -1) {
          var relValue = rel === undefined ? '' : rel + ' ';
          relValue = relValue + 'noopener';
          link.setAttribute('rel', relValue);
        }

        link.setAttribute('aria-describedby', idSelectors.newWindow);
      }

      if (isExternal && isTargetBlank) {
        link.setAttribute('aria-describedby', idSelectors.newWindowExternal);
      }
    });

    generateHTML(options.messages);
  }
};

/**
 * Currency Helpers
 * -----------------------------------------------------------------------------
 * A collection of useful functions that help with currency formatting
 *
 * Current contents
 * - formatMoney - Takes an amount in cents and returns it as a formatted dollar value.
 *
 * Alternatives
 * - Accounting.js - http://openexchangerates.github.io/accounting.js/
 *
 */

theme.Currency = (function() {
  var moneyFormat = '${{amount}}'; // eslint-disable-line camelcase

  function formatMoney(cents, format) {
    if (typeof cents === 'string') {
      cents = cents.replace('.', '');
    }
    var value = '';
    var placeholderRegex = /\{\{\s*(\w+)\s*\}\}/;
    var formatString = format || moneyFormat;

    function formatWithDelimiters(number, precision, thousands, decimal) {
      thousands = thousands || ',';
      decimal = decimal || '.';

      if (isNaN(number) || number === null) {
        return 0;
      }

      number = (number / 100.0).toFixed(precision);

      var parts = number.split('.');
      var dollarsAmount = parts[0].replace(
        /(\d)(?=(\d\d\d)+(?!\d))/g,
        '$1' + thousands
      );
      var centsAmount = parts[1] ? decimal + parts[1] : '';

      return dollarsAmount + centsAmount;
    }

    switch (formatString.match(placeholderRegex)[1]) {
      case 'amount':
        value = formatWithDelimiters(cents, 2);
        break;
      case 'amount_no_decimals':
        value = formatWithDelimiters(cents, 0);
        break;
      case 'amount_with_comma_separator':
        value = formatWithDelimiters(cents, 2, '.', ',');
        break;
      case 'amount_no_decimals_with_comma_separator':
        value = formatWithDelimiters(cents, 0, '.', ',');
        break;
      case 'amount_no_decimals_with_space_separator':
        value = formatWithDelimiters(cents, 0, ' ');
        break;
      case 'amount_with_apostrophe_separator':
        value = formatWithDelimiters(cents, 2, "'");
        break;
    }

    return formatString.replace(placeholderRegex, value);
  }

  return {
    formatMoney: formatMoney
  };
})();

/* ================ MODULES ================ */

window.theme = window.theme || {};

theme.FormStatus = (function() {
  var selectors = {
    statusMessage: '[data-form-status]'
  };

  function init() {
    var statusMessages = document.querySelectorAll(selectors.statusMessage);

    statusMessages.forEach(function(statusMessage) {
      statusMessage.setAttribute('tabindex', -1);
      statusMessage.focus();

      statusMessage.addEventListener(
        'blur',
        function(evt) {
          evt.target.removeAttribute('tabindex');
        },
        { once: true }
      );
    });
  }

  return {
    init: init
  };
})();

// prettier-ignore
window.theme = window.theme || {};

theme.TouchEvents = function TouchEvents(element, options) {
  this.axis;
  this.checkEvents = [];
  this.eventHandlers = {};
  this.eventModel = {};
  this.events = [
    ['touchstart', 'touchmove', 'touchend', 'touchcancel'],
    ['pointerdown', 'pointermove', 'pointerup', 'pointercancel'],
    ['mousedown', 'mousemove', 'mouseup']
  ];
  this.eventType;
  this.difference = {};
  this.direction;
  this.start = {};

  this.element = element;
  this.options = Object.assign(
    {},
    {
      dragThreshold: 10,
      start: function() {}, // eslint-disable-line
      move: function() {}, // eslint-disable-line
      end: function() {} // eslint-disable-line
    },
    options
  );

  this.checkEvents = this._getCheckEvents();
  this.eventModel = this._getEventModel();

  this._setupEventHandlers();
};

theme.TouchEvents.prototype = Object.assign({}, theme.TouchEvents.prototype, {
  destroy: function() {
    this.element.removeEventListener(
      'dragstart',
      this.eventHandlers.preventDefault
    );

    this.element.removeEventListener(
      this.events[this.eventModel][0],
      this.eventHandlers.touchStart
    );

    if (!this.eventModel) {
      this.element.removeEventListener(
        this.events[2][0],
        this.eventHandlers.touchStart
      );
    }

    this.element.removeEventListener('click', this.eventHandlers.preventClick);
  },

  _setupEventHandlers: function() {
    this.eventHandlers.preventDefault = this._preventDefault.bind(this);
    this.eventHandlers.preventClick = this._preventClick.bind(this);
    this.eventHandlers.touchStart = this._touchStart.bind(this);
    this.eventHandlers.touchMove = this._touchMove.bind(this);
    this.eventHandlers.touchEnd = this._touchEnd.bind(this);

    // Prevent element from dragging when using mouse
    this.element.addEventListener(
      'dragstart',
      this.eventHandlers.preventDefault
    );

    // Bind the touchstart/pointerdown event
    this.element.addEventListener(
      this.events[this.eventModel][0],
      this.eventHandlers.touchStart
    );

    // Bind mousedown if necessary
    if (!this.eventModel) {
      this.element.addEventListener(
        this.events[2][0],
        this.eventHandlers.touchStart
      );
    }

    // No clicking during touch
    this.element.addEventListener('click', this.eventHandlers.preventClick);
  },

  _touchStart: function(event) {
    this.eventType = this.eventModel;

    if (event.type === 'mousedown' && !this.eventModel) {
      this.eventType = 2;
    }

    if (this.checkEvents[this.eventType](event)) return;
    if (this.eventType) this._preventDefault(event);

    document.addEventListener(
      this.events[this.eventType][1],
      this.eventHandlers.touchMove
    );

    document.addEventListener(
      this.events[this.eventType][2],
      this.eventHandlers.touchEnd
    );

    if (this.eventType < 2) {
      document.addEventListener(
        this.events[this.eventType][3],
        this.eventHandlers.touchEnd
      );
    }

    this.start = {
      xPosition: this.eventType ? event.clientX : event.touches[0].clientX,
      yPosition: this.eventType ? event.clientY : event.touches[0].clientY,
      time: new Date().getTime()
    };

    // Ensure we empty out the this.difference object
    Object.keys(this.difference).forEach(
      function(key) {
        delete this.difference[key];
      }.bind(this)
    );

    this.options.start(event);
  },

  _touchMove: function(event) {
    this.difference = this._getDifference(event);

    // Prevent document from scrolling during swipe gesture
    document['on' + this.events[this.eventType][1]] = function(event) {
      this._preventDefault(event);
    }.bind(this);

    // Get the direction user is dragging
    if (!this.axis) {
      if (this.options.dragThreshold < Math.abs(this.difference.xPosition)) {
        this.axis = 'xPosition';
      } else if (
        this.options.dragThreshold < Math.abs(this.difference.yPosition)
      ) {
        this.axis = 'yPosition';
      } else {
        this.axis = false;
      }
    } else if (this.axis === 'xPosition') {
      this.direction = this.difference.xPosition < 0 ? 'left' : 'right';
    } else if (this.axis === 'yPosition') {
      this.direction = this.difference.yPosition < 0 ? 'up' : 'down';
    }

    this.options.move(event, this.direction, this.difference);
  },

  _touchEnd: function(event) {
    document.removeEventListener(
      this.events[this.eventType][1],
      this.eventHandlers.touchMove
    );

    document.removeEventListener(
      this.events[this.eventType][2],
      this.eventHandlers.touchEnd
    );

    if (this.eventType < 2) {
      document.removeEventListener(
        this.events[this.eventType][3],
        this.eventHandlers.touchEnd
      );
    }

    // Re-enable document scrolling
    document['on' + this.events[this.eventType][1]] = function() {
      return true;
    };

    this.options.end(event, this.direction, this.difference);
    this.axis = false;
  },

  _getDifference: function(event) {
    return {
      xPosition:
      (this.eventType ? event.clientX : event.touches[0].clientX) -
      this.start.xPosition,
      yPosition:
      (this.eventType ? event.clientY : event.touches[0].clientY) -
      this.start.yPosition,
      time: new Date().getTime() - this.start.time
    };
  },

  _getCheckEvents: function() {
    return [
      // Touch events
      function(event) {
        // Skip the event if it's a multi-touch or pinch move
        return (
          (event.touches && event.touches.length > 1) ||
          (event.scale && event.scale !== 1)
        );
      },
      // Pointer events
      function(event) {
        // Skip it, if:
        // 1. The event is not primary (other pointers during multi-touch),
        // 2. Left mouse button is not pressed,
        // 3. Event is not a touch event
        return (
          !event.isPrimary ||
          (event.buttons && event.buttons !== 1) ||
          (event.pointerType !== 'touch' && event.pointerType !== 'pen')
        );
      },
      // Mouse events
      function(event) {
        // Skip the event if left mouse button is not pressed
        return event.buttons && event.buttons !== 1;
      }
    ];
  },

  _getEventModel: function() {
    return window.navigator.pointerEnabled ? 1 : 0;
  },

  _preventDefault: function(event) {
    event.preventDefault ? event.preventDefault() : (event.returnValue = false);
  },

  _preventClick: function(event) {
    if (Math.abs(this.difference.xPosition) > this.options.dragThreshold) {
      this._preventDefault(event);
    }
  }
});
window.theme = window.theme || {};

theme.Disclosure = (function() {
  var selectors = {
    disclosureForm: '[data-disclosure-form]',
    disclosureList: '[data-disclosure-list]',
    disclosureToggle: '[data-disclosure-toggle]',
    disclosureInput: '[data-disclosure-input]',
    disclosureOptions: '[data-disclosure-option]'
  };

  var classes = {
    listVisible: 'disclosure-list--visible'
  };

  function Disclosure(disclosure) {
    this.container = disclosure;
    this._cacheSelectors();
    this._setupListeners();
  }

  Disclosure.prototype = Object.assign({}, Disclosure.prototype, {
    _cacheSelectors: function() {
      this.cache = {
        disclosureForm: this.container.closest(selectors.disclosureForm),
        disclosureList: this.container.querySelector(selectors.disclosureList),
        disclosureToggle: this.container.querySelector(
          selectors.disclosureToggle
        ),
        disclosureInput: this.container.querySelector(
          selectors.disclosureInput
        ),
        disclosureOptions: this.container.querySelectorAll(
          selectors.disclosureOptions
        )
      };
    },

    _setupListeners: function() {
      this.eventHandlers = this._setupEventHandlers();

      this.cache.disclosureToggle.addEventListener(
        'click',
        this.eventHandlers.toggleList
      );

      this.cache.disclosureOptions.forEach(function(disclosureOption) {
        disclosureOption.addEventListener(
          'click',
          this.eventHandlers.connectOptions
        );
      }, this);

      this.container.addEventListener(
        'keyup',
        this.eventHandlers.onDisclosureKeyUp
      );

      this.cache.disclosureList.addEventListener(
        'focusout',
        this.eventHandlers.onDisclosureListFocusOut
      );

      this.cache.disclosureToggle.addEventListener(
        'focusout',
        this.eventHandlers.onDisclosureToggleFocusOut
      );

      document.body.addEventListener('click', this.eventHandlers.onBodyClick);
    },

    _setupEventHandlers: function() {
      return {
        connectOptions: this._connectOptions.bind(this),
        toggleList: this._toggleList.bind(this),
        onBodyClick: this._onBodyClick.bind(this),
        onDisclosureKeyUp: this._onDisclosureKeyUp.bind(this),
        onDisclosureListFocusOut: this._onDisclosureListFocusOut.bind(this),
        onDisclosureToggleFocusOut: this._onDisclosureToggleFocusOut.bind(this)
      };
    },

    _connectOptions: function(event) {
      event.preventDefault();

      this._submitForm(event.currentTarget.dataset.value);
    },

    _onDisclosureToggleFocusOut: function(event) {
      var disclosureLostFocus =
          this.container.contains(event.relatedTarget) === false;

      if (disclosureLostFocus) {
        this._hideList();
      }
    },

    _onDisclosureListFocusOut: function(event) {
      var childInFocus = event.currentTarget.contains(event.relatedTarget);

      var isVisible = this.cache.disclosureList.classList.contains(
        classes.listVisible
      );

      if (isVisible && !childInFocus) {
        this._hideList();
      }
    },

    _onDisclosureKeyUp: function(event) {
      if (event.which !== slate.utils.keyboardKeys.ESCAPE) return;
      this._hideList();
      this.cache.disclosureToggle.focus();
    },

    _onBodyClick: function(event) {
      var isOption = this.container.contains(event.target);
      var isVisible = this.cache.disclosureList.classList.contains(
        classes.listVisible
      );

      if (isVisible && !isOption) {
        this._hideList();
      }
    },

    _submitForm: function(value) {
      this.cache.disclosureInput.value = value;
      this.cache.disclosureForm.submit();
    },

    _hideList: function() {
      this.cache.disclosureList.classList.remove(classes.listVisible);
      this.cache.disclosureToggle.setAttribute('aria-expanded', false);
    },

    _toggleList: function() {
      var ariaExpanded =
          this.cache.disclosureToggle.getAttribute('aria-expanded') === 'true';
      this.cache.disclosureList.classList.toggle(classes.listVisible);
      this.cache.disclosureToggle.setAttribute('aria-expanded', !ariaExpanded);
    },

    destroy: function() {
      this.cache.disclosureToggle.removeEventListener(
        'click',
        this.eventHandlers.toggleList
      );

      this.cache.disclosureOptions.forEach(function(disclosureOption) {
        disclosureOption.removeEventListener(
          'click',
          this.eventHandlers.connectOptions
        );
      }, this);

      this.container.removeEventListener(
        'keyup',
        this.eventHandlers.onDisclosureKeyUp
      );

      this.cache.disclosureList.removeEventListener(
        'focusout',
        this.eventHandlers.onDisclosureListFocusOut
      );

      this.cache.disclosureToggle.removeEventListener(
        'focusout',
        this.eventHandlers.onDisclosureToggleFocusOut
      );

      document.body.removeEventListener(
        'click',
        this.eventHandlers.onBodyClick
      );
    }
  });

  return Disclosure;
})();

theme.Zoom = (function() {
  var selectors = {
    imageZoom: '[data-image-zoom]'
  };

  var classes = {
    zoomImg: 'zoomImg'
  };

  var attributes = {
    imageZoomTarget: 'data-image-zoom-target'
  };

  function Zoom(container) {
    this.container = container;
    this.cache = {};
    this.url = container.dataset.zoom;

    this._cacheSelectors();

    if (!this.cache.sourceImage) return;

    this._duplicateImage();
  }

  Zoom.prototype = Object.assign({}, Zoom.prototype, {
    _cacheSelectors: function() {
      this.cache = {
        sourceImage: this.container.querySelector(selectors.imageZoom)
      };
    },

    _init: function() {
      var targetWidth = this.cache.targetImage.width;
      var targetHeight = this.cache.targetImage.height;

      if (this.cache.sourceImage === this.cache.targetImage) {
        this.sourceWidth = targetWidth;
        this.sourceHeight = targetHeight;
      } else {
        this.sourceWidth = this.cache.sourceImage.width;
        this.sourceHeight = this.cache.sourceImage.height;
      }

      this.xRatio =
        (this.cache.sourceImage.width - targetWidth) / this.sourceWidth;
      this.yRatio =
        (this.cache.sourceImage.height - targetHeight) / this.sourceHeight;
    },

    _start: function(e) {
      this._init();
      this._move(e);
    },

    _stop: function() {
      this.cache.targetImage.style.opacity = 0;
    },

    /**
     * Sets the correct coordinates top and left position in px
     * It sets a limit within between 0 and the max height of the image
     * So when the mouse leaves the target image, it could
     * never go above or beyond the target image zone
     */
    _setTopLeftMaxValues: function(top, left) {
      return {
        left: Math.max(Math.min(left, this.sourceWidth), 0),
        top: Math.max(Math.min(top, this.sourceHeight), 0)
      };
    },

    _move: function(e) {
      // get left and top position within the "source image" zone
      var left =
          e.pageX -
          (this.cache.sourceImage.getBoundingClientRect().left + window.scrollX);
      var top =
          e.pageY -
          (this.cache.sourceImage.getBoundingClientRect().top + window.scrollY);
      // make sure the left and top position don't go
      // above or beyond the target image zone
      var position = this._setTopLeftMaxValues(top, left);

      top = position.top;
      left = position.left;

      this.cache.targetImage.style.left = -(left * -this.xRatio) + 'px';
      this.cache.targetImage.style.top = -(top * -this.yRatio) + 'px';
      this.cache.targetImage.style.opacity = 1;
    },

    /**
     * This loads a high resolution image
     * via the data attributes url
     * It adds all necessary CSS styles and adds to the container
     */
    _duplicateImage: function() {
      this._loadImage()
      .then(
        function(image) {
          this.cache.targetImage = image;
          image.style.width = image.width + 'px';
          image.style.height = image.height + 'px';
          image.style.position = 'absolute';
          image.style.maxWidth = 'none';
          image.style.maxHeight = 'none';
          image.style.opacity = 0;
          image.style.border = 'none';
          image.style.left = 0;
          image.style.top = 0;

          this.container.appendChild(image);

          this._init();

          this._start = this._start.bind(this);
          this._stop = this._stop.bind(this);
          this._move = this._move.bind(this);

          this.container.addEventListener('mouseenter', this._start);
          this.container.addEventListener('mouseleave', this._stop);
          this.container.addEventListener('mousemove', this._move);

          this.container.style.position = 'relative';
          this.container.style.overflow = 'hidden';
        }.bind(this)
      )
      .catch(function(error) {
        // eslint-disable-next-line no-console
        console.warn('Error fetching image', error);
      });
    },

    _loadImage: function() {
      // eslint-disable-next-line
      return new Promise(function(resolve, reject) {
        var image = new Image();
        image.setAttribute('role', 'presentation');
        image.setAttribute(attributes.imageZoomTarget, true);
        image.classList.add(classes.zoomImg);
        image.src = this.url;

        image.addEventListener('load', function() {
          resolve(image);
        });

        image.addEventListener('error', function(error) {
          reject(error);
        });
      }.bind(this)
                        );
    },

    unload: function() {
      var targetImage = this.container.querySelector(
        '[' + attributes.imageZoomTarget + ']'
      );
      if (targetImage) {
        targetImage.remove();
      }

      this.container.removeEventListener('mouseenter', this._start);
      this.container.removeEventListener('mouseleave', this._stop);
      this.container.removeEventListener('mousemove', this._move);
    }
  });

  return Zoom;
})();

window.theme = theme || {};

theme.Product = (function() {
  function Product(container) {
    this.container = container;
    var sectionId = container.getAttribute('data-section-id');
    this.zoomPictures = [];

    this.settings = {
      mediaQueryMediumUp: 'screen and (min-width: 750px)',
      mediaQuerySmall: 'screen and (max-width: 749px)',
      sectionId: sectionId,
      bpSmall: false,
      zoomEnabled: false
    };

    this.selectors = {    
      imageZoomWrapper: '[data-image-zoom-wrapper]',
      productMediaWrapper: '[data-product-single-media-wrapper]',
      productThumbImages: '.product-single__thumbnail--' + sectionId,
      productThumbs: '.product-single__thumbnails-' + sectionId,
      productThumbListItem: '.product-single__thumbnails-item',
      productThumbsWrapper: '.thumbnails-wrapper',
      Inv: '.items',
      Inv1: '[data-inv]'
    };

    this.classes = {
      hidden: 'hide',
      visibilityHidden: 'visibility-hidden',
      jsZoomEnabled: 'js-zoom-enabled',
      activeClass: 'active-thumb',
      productinstock: 'instock',
      productoutstock: 'outstock'
    };

    this.eventHandlers = {};

    this.Inv1 = container.querySelector(
      this.selectors.Inv1
    );
    this.imageZoomWrapper = container.querySelectorAll(
      this.selectors.imageZoomWrapper
    );

    var productJson = document.getElementById('ProductJson-' + sectionId);
    if (!productJson || !productJson.innerHTML.length) {
      return;
    }
    this.settings.zoomEnabled =
      this.imageZoomWrapper.length > 0
    ? this.imageZoomWrapper[0].classList.contains(
      this.classes.jsZoomEnabled
    )
    : false;

    this.initMobileBreakpoint = this._initMobileBreakpoint.bind(this);
    this.initDesktopBreakpoint = this._initDesktopBreakpoint.bind(this);

    this.mqlMediumUp = window.matchMedia(this.settings.mediaQueryMediumUp);
    this.mqlMediumUp.addListener(this.initDesktopBreakpoint);

    this.initMobileBreakpoint();
    this.initDesktopBreakpoint();
    this._stringOverrides();
    this._initMediaSwitch();
    this._setActiveThumbnail();
  }

  Product.prototype = Object.assign({}, Product.prototype, {
    _stringOverrides: function() {
      theme.productStrings = theme.productStrings || {};
      theme.strings = Object.assign({}, theme.strings, theme.productStrings);
    },

    _initMobileBreakpoint: function() {
      // initialize thumbnail slider on mobile if more than four thumbnails
      // destroy image zooming if enabled
      if (this.settings.zoomEnabled) {
        this.imageZoomWrapper.forEach(
          function(element, index) {
            this._destroyZoom(index);
          }.bind(this)
        );
      }

      this.settings.bpSmall = true;
    },

    _initDesktopBreakpoint: function() {
      if (this.mqlMediumUp.matches && this.settings.zoomEnabled) {
        this.imageZoomWrapper.forEach(
          function(element, index) {
            this._enableZoom(element, index);
          }.bind(this)
        );
      }
    },

    _initMediaSwitch: function() {
      if (!document.querySelector(this.selectors.productThumbImages)) {
        return;
      }

      var self = this;

      var productThumbImages = document.querySelectorAll(
        this.selectors.productThumbImages
      );

      this.eventHandlers.handleMediaFocus = this._handleMediaFocus.bind(this);

      productThumbImages.forEach(function(el) {
        el.addEventListener('click', function(evt) {
          evt.preventDefault();
          var mediaId = el.getAttribute('data-thumbnail-id');

          self._switchMedia(mediaId);
          self._setActiveThumbnail(mediaId);
        });
        el.addEventListener('keyup', self.eventHandlers.handleMediaFocus);
      });
    },

    _setActiveThumbnail: function(mediaId) {
      // If there is no element passed, find it by the current product image
      if (typeof mediaId === 'undefined') {
        var productMediaWrapper = this.container.querySelector(
          this.selectors.productMediaWrapper + ':not(.hide)'
        );

        if (!productMediaWrapper) return;
        mediaId = productMediaWrapper.getAttribute('data-media-id');
      }

      var thumbnailWrappers = this.container.querySelectorAll(
        this.selectors.productThumbListItem + ':not(.slick-cloned)'
      );

      var activeThumbnail;
      thumbnailWrappers.forEach(
        function(el) {
          var current = el.querySelector(
            this.selectors.productThumbImages +
            "[data-thumbnail-id='" +
            mediaId +
            "']"
          );
          if (current) {
            activeThumbnail = current;
          }
        }.bind(this)
      );

      var productThumbImages = document.querySelectorAll(
        this.selectors.productThumbImages
      );
      productThumbImages.forEach(
        function(el) {
          el.classList.remove(this.classes.activeClass);
          el.removeAttribute('aria-current');
        }.bind(this)
      );

      if (activeThumbnail) {
        activeThumbnail.classList.add(this.classes.activeClass);
        activeThumbnail.setAttribute('aria-current', true);
        this._adjustThumbnailSlider(activeThumbnail);
      }
    },

    _adjustThumbnailSlider: function(activeThumbnail) {
      var sliderItem = activeThumbnail.closest('[data-slider-item]');
      if (!sliderItem) return;

      var slideGroupLeaderIndex =
          Math.floor(
            Number(sliderItem.getAttribute('data-slider-slide-index')) / 3
          ) * 3;

      window.setTimeout(
        function() {
          if (!this.slideshow) return;
          this.slideshow.goToSlideByIndex(slideGroupLeaderIndex);
        }.bind(this),
        251
      );
    },

    _switchMedia: function(mediaId) {
      var productMediaWrapper = this.container.querySelector(this.selectors.productMediaWrapper);
      if (productMediaWrapper) {
        var currentMedia = this.container.querySelector(
          this.selectors.productMediaWrapper +
          ':not(.' +
          this.classes.hidden +
          ')'
        );

        var newMedia = this.container.querySelector(
          this.selectors.productMediaWrapper + "[data-media-id='" + mediaId + "']"
        );

        var otherMedia = this.container.querySelectorAll(
          this.selectors.productMediaWrapper +
          ":not([data-media-id='" +
          mediaId +
          "'])"
        );

        currentMedia.dispatchEvent(
          new CustomEvent('mediaHidden', {
            bubbles: true,
            cancelable: true
          })
        );
        newMedia.classList.remove(this.classes.hidden);
        newMedia.dispatchEvent(
          new CustomEvent('mediaVisible', {
            bubbles: true,
            cancelable: true
          })
        );
        otherMedia.forEach(
          function(el) {
            el.classList.add(this.classes.hidden);
          }.bind(this)
        );
      }
    },

    _handleMediaFocus: function(evt) {
      if (evt.keyCode !== slate.utils.keyboardKeys.ENTER) return;

      var mediaId = evt.currentTarget.getAttribute('data-thumbnail-id');

      var productMediaWrapper = this.container.querySelector(
        this.selectors.productMediaWrapper + "[data-media-id='" + mediaId + "']"
      );
      productMediaWrapper.focus();
    },

    _updateMedia: function(evt) {
      var variant = evt.detail.variant;
      var mediaId = variant.featured_media.id;
      var sectionMediaId = this.settings.sectionId + '-' + mediaId;

      this._switchMedia(sectionMediaId);
      this._setActiveThumbnail(sectionMediaId);
    },

    _enableZoom: function(el, index) {
      this.zoomPictures[index] = new theme.Zoom(el);
    },

    _destroyZoom: function(index) {
      if (this.zoomPictures.length === 0) return;
      this.zoomPictures[index].unload();
    },
  });

  return Product;
})();
window.theme = theme || {};

theme.customerTemplates = (function() {
  var selectors = {
    RecoverHeading: '#RecoverHeading',
    RecoverEmail: '#RecoverEmail',
    LoginHeading: '#LoginHeading'
  };

  function initEventListeners() {
    this.recoverHeading = document.querySelector(selectors.RecoverHeading);
    this.recoverEmail = document.querySelector(selectors.RecoverEmail);
    this.loginHeading = document.querySelector(selectors.LoginHeading);
    var recoverPassword = document.getElementById('RecoverPassword');
    var hideRecoverPasswordLink = document.getElementById(
      'HideRecoverPasswordLink'
    );

    // Show reset password form
    if (recoverPassword) {
      recoverPassword.addEventListener(
        'click',
        function(evt) {
          evt.preventDefault();
          showRecoverPasswordForm();
          this.recoverHeading.setAttribute('tabindex', '-1');
          this.recoverHeading.focus();
        }.bind(this)
      );
    }

    // Hide reset password form
    if (hideRecoverPasswordLink) {
      hideRecoverPasswordLink.addEventListener(
        'click',
        function(evt) {
          evt.preventDefault();
          hideRecoverPasswordForm();
          this.loginHeading.setAttribute('tabindex', '-1');
          this.loginHeading.focus();
        }.bind(this)
      );
    }

    if (this.recoverHeading) {
      this.recoverHeading.addEventListener('blur', function(evt) {
        evt.target.removeAttribute('tabindex');
      });
    }

    if (this.loginHeading) {
      this.loginHeading.addEventListener('blur', function(evt) {
        evt.target.removeAttribute('tabindex');
      });
    }
  }

  /**
   *
   *  Show/Hide recover password form
   *
   */

  function showRecoverPasswordForm() {
    document.getElementById('RecoverPasswordForm').classList.remove('hide');
    document.getElementById('CustomerLoginForm').classList.add('hide');

    if (this.recoverEmail.getAttribute('aria-invalid') === 'true') {
      this.recoverEmail.focus();
    }
  }

  function hideRecoverPasswordForm() {
    document.getElementById('RecoverPasswordForm').classList.add('hide');
    document.getElementById('CustomerLoginForm').classList.remove('hide');
  }

  /**
   *
   *  Show reset password success message
   *
   */
  function resetPasswordSuccess() {
    var formState = document.querySelector('.reset-password-success');

    // check if reset password form was successfully submited.
    if (!formState) {
      return;
    }

    // show success message
    var resetSuccess = document.getElementById('ResetSuccess');
    resetSuccess.classList.remove('hide');
    resetSuccess.focus();
  }

  /**
   *
   *  Show/hide customer address forms
   *
   */
  function customerAddressForm() {
    var newAddressForm = document.getElementById('AddressNewForm');
    var newAddressFormButton = document.getElementById('AddressNewButton');

    if (!newAddressForm) {
      return;
    }

    // Initialize observers on address selectors, defined in shopify_common.js
    if (Shopify) {
      // eslint-disable-next-line no-new
      new Shopify.CountryProvinceSelector(
        'AddressCountryNew',
        'AddressProvinceNew',
        {
          hideElement: 'AddressProvinceContainerNew'
        }
      );
    }

    // Initialize each edit form's country/province selector
    document
    .querySelectorAll('.address-country-option')
    .forEach(function(option) {
      var formId = option.dataset.formId;
      var countrySelector = 'AddressCountry_' + formId;
      var provinceSelector = 'AddressProvince_' + formId;
      var containerSelector = 'AddressProvinceContainer_' + formId;

      // eslint-disable-next-line no-new
      new Shopify.CountryProvinceSelector(countrySelector, provinceSelector, {
        hideElement: containerSelector
      });
    });

    // Toggle new/edit address forms
    document.querySelectorAll('.address-new-toggle').forEach(function(button) {
      button.addEventListener('click', function() {
        var isExpanded =
            newAddressFormButton.getAttribute('aria-expanded') === 'true';

        newAddressForm.classList.toggle('hide');
        newAddressFormButton.setAttribute('aria-expanded', !isExpanded);
        newAddressFormButton.focus();
      });
    });

    document.querySelectorAll('.address-edit-toggle').forEach(function(button) {
      button.addEventListener('click', function(evt) {
        var formId = evt.target.dataset.formId;
        var editButton = document.getElementById('EditFormButton_' + formId);
        var editAddress = document.getElementById('EditAddress_' + formId);
        var isExpanded = editButton.getAttribute('aria-expanded') === 'true';

        editAddress.classList.toggle('hide');
        editButton.setAttribute('aria-expanded', !isExpanded);
        editButton.focus();
      });
    });

    document.querySelectorAll('.address-delete').forEach(function(button) {
      button.addEventListener('click', function(evt) {
        var target = evt.target.dataset.target;
        var confirmMessage = evt.target.dataset.confirmMessage;

        // eslint-disable-next-line no-alert
        if (
          confirm(
            confirmMessage || 'Are you sure you wish to delete this address?'
          )
        ) {
          Shopify.postLink(target, {
            parameters: { _method: 'delete' }
          });
        }
      });
    });
  }

  /**
   *
   *  Check URL for reset password hash
   *
   */
  function checkUrlHash() {
    var hash = window.location.hash;

    // Allow deep linking to recover password form
    if (hash === '#recover') {
      showRecoverPasswordForm.bind(this)();
    }
  }

  return {
    init: function() {
      initEventListeners();
      checkUrlHash();
      resetPasswordSuccess();
      customerAddressForm();
    }
  };
})();

  /*================ SECTIONS ================*/
  window.theme = window.theme || {};
  var selectors = {
    disclosureLocale: '[data-disclosure-locale]'
  };
  theme.HeaderSection = (function() {
    function Header(container) {
      //theme.Header.init();
      //theme.MobileNav.init();
      this.container = container;
      this.cache = {};
      this.cacheSelectors();

      if (this.cache.localeDisclosure) {
        this.localeDisclosure = new theme.Disclosure(this.cache.localeDisclosure);
      }
    }

    Header.prototype = Object.assign({}, Header.prototype, {    
      cacheSelectors: function() {
        this.cache = {
          localeDisclosure: this.container.querySelector(
            selectors.disclosureLocale
          )
        };
      },
      onUnload: function() {
        //theme.Header.unload();
        //theme.MobileNav.unload();
        if (this.cache.localeDisclosure) {
          this.localeDisclosure.destroy();
        }
      }
    });

    return Header;
  })();

  document.addEventListener('DOMContentLoaded', function() {
    var sections = new theme.Sections();
    sections.register('product-template', theme.Product);
    sections.register('header-section', theme.HeaderSection);
  });