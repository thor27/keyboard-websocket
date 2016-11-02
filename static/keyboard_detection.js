function KeyboardDetect(options) {
    'use strict';
    return this.init(options);
}

(function (window, document) {
  'use strict';

  KeyboardDetect.prototype = {

    /**
    Initalizes the KeyboardDetect object
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
        self.processKeypress(msg);
      });

      $.get( "/keyboards", function( data ) {
        self.processKeyboards(JSON.parse(data));
      });

      this.socket.on('connected_keyboards', function(msg){
        self.processKeyboards(msg);
      });

      this.options = options;
    },
    humanize: function(key) {
      var splitted = key.split('_'),
          key = splitted.length > 1? splitted[1] : splitted[0],
          key = key.replace(/^KP/,''),
          key = key === 'LEFT'? key : key.replace(/^LEFT/,''),
          key = key === 'RIGHT'? key : key.replace(/^RIGHT/,'');
      return key;
    },
    processKeypress: function(msg) {
      var element = this.getId(msg.device.file);
      if (element && msg.type === 'DOWN') {
        $("#" + element + " span").text(this.humanize(msg.data));
        $("#" + element + " span").css('visibility', 'visible');
      }
    },
    getId: function(file_path) {
      return file_path.replace(/\//g, "_");
    },
    createForm: function(device) {
      var form = "<form method='post'><input type='hidden' name='filename' value='" + device.file + "'>";
      if (this.options.redirect) {
        form += "<input type='hidden' name='redirect' value='" + this.options.redirect + "'>"
      }
      form += "<input type='submit' value='" + this.options.button_label + "'></form>";
      return form;
    },
    processKeyboards: function(msg) {
      var self = this,
          element = $(this.options.boxes);
      element.html("");
      $.each(msg.devices, function(i, device) {
        var device_id = self.getId(device.file),
            form = self.createForm(device);
        element.append("<div class='box' id='" + device_id + "'> <h2>" + device.name + "</h2> <span>X</span>" + form);
      });
    },

  };

}(window, document));
