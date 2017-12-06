function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([.$?*|{}()\[\]\\\/+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function getBoolCookie(name) {
    var cookie = getCookie(name);
    if (cookie)
        return cookie.toLowerCase() === 'true';
    else
        return false
}

var app = new Vue({
    el: '#app',
    data: {
        using_complex_gravity: getBoolCookie('using_complex_gravity'),
        using_archimedes_force: getBoolCookie('using_archimedes_force'),
        using_environment_resistance: getBoolCookie('using_environment_resistance'),
        using_wind: getBoolCookie('using_wind'),
        water_environment: getBoolCookie('water_environment')
    }
});