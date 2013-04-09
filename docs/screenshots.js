/// @export "setup"
var casper = require('casper').create({
    viewportSize : {width : 800, height : 300}
});

var system = require('system');
var PORT = system.env.DEXY_PORT;

/// @export "initial"
casper.start("http://localhost:" + PORT, function() {
    this.wait(500);
    this.capture("dexy-serve-index.pdf");
    this.capture("dexy-serve-index.png");
});

/// @export "run"
casper.run();
