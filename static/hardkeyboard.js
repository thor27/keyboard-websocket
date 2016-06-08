function HardKeyboard(options) {
    'use strict';
    return this.init(options);
}

(function (window, document) {
  'use strict';

  HardKeyboard.prototype = {

    /**
    Initalizes the HardKeyboard object
    @method init
    **/
    init: function init(options) {
      var self = this;
      if (options.url) {
        this.socket = io.connect(options.url);
      } else {
        this.socket = io.connect('http://' + document.domain + ':' + location.port);
      }
      this.socket.on('key_event', function(msg){
        self.processEvent(msg);
      });
      this.options = options;
      if (options.valid_keys) {
        this.VALID_KEYS = options.valid_keys;
      } else {
        this.VALID_KEYS = [
          'KEY_0','KEY_1', 'KEY_1', 'KEY_2', 'KEY_3', 'KEY_4', 'KEY_5', 'KEY_6',  'KEY_7',  'KEY_8',  'KEY_9',
          'KEY_KP0','KEY_KP1', 'KEY_KP1', 'KEY_KP2', 'KEY_KP3', 'KEY_KP4', 'KEY_KP5', 'KEY_KP6',  'KEY_KP7',  'KEY_KP8',  'KEY_KP9',
        ]
      }
    },

    processEvent: function(msg) {
      if (this.options.textbox) {
        this.simulateKeyboard(this.options.textbox, msg);
      }
    },

    simulateKeyboard: function(box, msg) {
        var element = $(box),
            new_text = '',
            old_text = element.text(),
            char;

        if (msg.type == 'DOWN' || msg.type == 'HOLD') {
          if (this.options.on_key_down && !this.options.on_key_down(msg.data)) {
            return;
          }
          if (msg.data == 'KEY_BACKSPACE') {
            new_text = element.text().slice(0,-1)
            element.text(new_text);
            if (this.options.on_update) {
              this.options.on_update(old_text, new_text);
            }
          }

          if (this.VALID_KEYS.indexOf(msg.data) != -1) {
            if (this.options.on_valid_key_down && !this.options.on_valid_key_down(msg.data)) {
              return;
            }
            char = msg.data.slice(-1);
            element.append(char);
            if (this.options.on_update) {
              this.options.on_update(old_text, element.text(), char);
            }
          }

        }
    }
  };

}(window, document));
