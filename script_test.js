var fs = require('fs');
eval(fs.readFileSync('static/js/linker.js')+'');

var assert = require('assert');

var actual = null;

actual = linker('<a href="/user/gutomaia">gutomaia</a>');
assert.equal('<a href="/#!/user/gutomaia">gutomaia</a>', actual);

actual = linker('<a href="/learn/python">python</a>');
assert.equal('<a href="/#!/learn/python">python</a>', actual);

actual = linker('<a href="/go_in/Salvador">Salvador</a>');
assert.equal('<a href="/#!/go_in/Salvador">Salvador</a>', actual);

actual = linker('<a class="teste" href="/learn/python">python</a>');
assert.equal('<a class="teste" href="/#!/learn/python">python</a>', actual);


actual = linker('<li>' +
	'<img src="http://a2.twimg.com/profile_images/652584720/avatar_normal.jpg" align="left">' +
	'<p>' + 
	'<a href="/user/gutomaia">gutomaia</a>' +
	' will practice <a href="/learn/python">python</a> ' +
	'at Google in <a href="/go_in/Salvador">Salvador</a>' +
	'</p><a href="/dojo/1">more »</a>'+
	'</li>'
);

expected = '<li>' +
	'<img src="http://a2.twimg.com/profile_images/652584720/avatar_normal.jpg" align="left">' +
	'<p>' + 
	'<a href="/#!/user/gutomaia">gutomaia</a>' +
	' will practice <a href="/#!/learn/python">python</a> ' +
	'at Google in <a href="/#!/go_in/Salvador">Salvador</a>' +
	'</p><a href="/#!/dojo/1">more »</a>'+
	'</li>';

assert.equal(expected, actual)