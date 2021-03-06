(function (exports) {

    function _debug (d) {
        console.log("DEBUG: " + d);
    };

    function WhramiSplashArea (api, $splash_area, $play_area) {
        self.api = api;
        self.$splash_area = $splash_area;
        self.$play_area = $play_area;

        self.init = function () {
            var btn = self.$splash_area.find(".whrami-play-btn");
            btn.on("click", self.play);
        };

        self.show_play_area = function () {
            self.$splash_area
                .removeClass("show")
                .addClass("hidden");
            self.$play_area
                .removeClass("hidden")
                .addClass("show");
        };

        self.play = function () {
            self.show_play_area();
            api.connect();
        };

        self.init();
    }

    function WhramiPublisher (api, $publish_form) {
        var self = this;

        self.api = api;
        self.$publish_form = $publish_form;

        self.init = function () {
            var btn = self.$publish_form.find(".whrami-publish-btn");
            btn.on("click", self.on_publish);
            var input = self.$publish_form.find(".whrami-publish-text");
            input.on("keypress", function (event) {
                if (event.key == "Enter") {
                   self.on_publish();
                }
            });
        };

        self.post = function (msg) {
            self.api.send_msg(msg);
        };

        self.on_publish = function () {
            var text_input = self.$publish_form.find(".whrami-publish-text");

            var text = text_input.val().trim(),
                msg = null;

            if (text) {
                self.post({
                    etype: "user_input",
                    content: text,
                });
            }

            text_input.val("");

            return false;
        };

        self.init();
    }


    function WhramiReceiver (api, $msg_list) {
        var self = this;

        self.api = api;
        self.$msg_list = $msg_list;

        self.init = function () {
            self.$no_msgs_li = $msg_list.find(".whrami-no-messages");
            self.api.add_handler("on_open", self.on_open);
            self.api.add_handler("on_close", self.on_close);
            self.api.add_handler("on_error", self.on_error);
            self.api.add_handler("handle_user_input", self.handle_user_input);
            self.api.add_handler("handle_user_output", self.handle_user_output);
        };

        self.check_msg_overflow = function () {
            var $li = self.$msg_list.find("li:visible").slice(0, -10);
            $li.remove();
        };

        self.check_no_msgs_li = function () {
            msg_count = self.$msg_list.find("li:visible").length;
            if (msg_count == 0) {
                self.$no_msgs_li.show();
            }
            else if (msg_count > 1) {
                self.$no_msgs_li.hide();
            }
        };

        self.append_msg = function (content, opts) {
            opts = opts || {};
            var classes = opts.classes || [];
            classes.push("list-group-item");
            self.$msg_list.append([
              '<li class="', classes.join(" "), '">',
              content,
              '</li>',
            ].join(""));
            self.check_msg_overflow();
            self.check_no_msgs_li();
        };

        self.on_open = function () {
            self.append_msg("Connected.", {
              classes: ["whrami-system-msg"],
            });
        };

        self.on_close = function () {
            self.append_msg("Disconnected.", {
              classes: ["whrami-system-msg"],
            });
        };

        self.on_error = function (msg) {
            self.append_msg("Error " + JSON.stringify(msg), {
              classes: ["whrami-error-msg"],
            });
        };

        self.handle_user_input = function (msg) {
            self.append_msg(msg.content, {
              classes: ["whrami-user-input-msg"],
            });
        };

        self.handle_user_output = function (msg) {
            self.append_msg(msg.content, {
              classes: ["whrami-user-output-msg"],
            });
        };

        self.init();
    }

    function WhramiApi (api_server, opts) {
        var self = this;

        self.api_server = api_server;
        self.opts = opts || {debug: false};
        self.callbacks = {};

        self.socket = null;

        self.init = function () {
        };

        self.debug = function (content) {
            if (self.opts.debug) {
                _debug(content);
            }
        }

        self.connect = function () {
            var socket = new WebSocket("ws://" + self.api_server);
            self.socket = socket;
            socket.onopen = self.ws.on_open;
            socket.onclose = self.ws.on_close;
            socket.onmessage = self.ws.on_message;
            socket.onerror = self.ws.on_error;
        };

        self.add_handler = function (name, handler) {
            if (self.callbacks[name]) {
                return false;
            }
            self.callbacks[name] = handler;
        };

        self.callback = function () {
            var name = Array.prototype.shift.call(arguments);
            if (self.callbacks[name]) {
                self.callbacks[name].apply(self, arguments);
            };
        };

        self.ws = {};

        self.ws.on_open = function () {
            self.debug("Websocket connected.");
            self.callback('on_open');
        };

        self.ws.on_close = function () {
            self.debug("Websocket disconnected.");
            self.callback('on_close');
        };

        self.ws.on_error = function (e) {
            self.debug(e);
            self.callback('on_error', e);
        };

        self.ws.on_message = function (event) {
            self.debug("Websocket message received: " + event.data);
            var msg = JSON.parse(event.data);
            var callback_name = "handle_" + msg.etype;
            self.callback(callback_name, msg);
        };

        self.send_msg = function (msg) {
            self.debug("Websocket message sent: " + JSON.stringify(msg));
            self.socket.send(JSON.stringify(msg));
        };

        self.init();
    }

    exports.WhramiSplashArea = WhramiSplashArea;
    exports.WhramiPublisher = WhramiPublisher;
    exports.WhramiReceiver = WhramiReceiver;
    exports.WhramiApi = WhramiApi;

})(window.whrami = window.whrami || {});
