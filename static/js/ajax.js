function createXMLHttpRequest() {
	try {
		return new ActiveXObject("Msxml2.XMLHTTP");
	} catch (e) {
	}

	try {
		return new ActiveXObject("Microsoft.XMLHTTP");
	} catch (e) {
	}

	try {
		return new XMLHttpRequest();
	} catch (e) {
	}

	alert("XMLHttpRequest not supported");
	return null;
};

var ajax = {
	callServer : function(url, callback, callingContext, method, body, bodyType, headers) {
		url = url.replace('&amp;', '&');
		var request = createXMLHttpRequest();
		request.onreadystatechange = function() {
			ajax._onStateChange(call);
		};
		var call = {
			request : request,
			callback : callback,
			callingContext : callingContext,
			url : url
		};
		request.open(method, url, true);
		if (headers != null){
			for (index in headers){
				request.setRequestHeader(index, headers[index]);
			}
		}
		if (method == "GET" || method == "HEAD" || method == "DELETE") {
			request.send(null);
		} else if (method == "POST" || method == "PUT" || method == "OPTIONS"
				|| method == "TRACE") {
			bodyType = (bodyType == null) ? 'application/x-www-form-urlencoded; charset=UTF-8'
					: bodyType;
			request.setRequestHeader('Content-Type', bodyType);
			request.send(body);
		};
	},
	_onStateChange : function(call) {
		if (call.request.readyState < 4) {
			return;
		} else if (call.request.readyState == 4) {
			var content = call.request.responseText;
			var responseHeaders = call.request.getAllResponseHeaders();
			call.callback(content, responseHeaders, call.callingContext, call.request);
		};
		call = null;
	}
};
