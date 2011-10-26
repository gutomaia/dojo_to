var fs = require('fs');
eval(fs.readFileSync('static/js/linker.js')+'');

var assert = require('assert');

var actual = null;

actual = linker('<a href="/learn/python">python</a>');
assert.equal('<a href="/#!/learn/python">python</a>', actual);

actual = linker('<a class="teste" href="/learn/python">python</a>');
assert.equal('<a class="teste" href="/#!/learn/python">python</a>', actual);