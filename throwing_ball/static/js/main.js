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
        water_environment: getBoolCookie('water_environment'),
        ball_animation: {
            coordinates: null,
            flying: false,
            curr_coordinates: {
                x: 'undefined',
                y: 'undefined'
            }
        }
    },
    methods: {
        animate_ball: function (id) {
            if (this.ball_animation.flying) {
                return;
            }

            var ball = document.getElementById(id);
            const h = (this.ball_animation.coordinates[0][1] - this.ball_animation.coordinates[0][0]) * 1000;
            const max_w = Math.max.apply(null, this.ball_animation.coordinates[1]);
            const max_h = Math.max.apply(null, this.ball_animation.coordinates[2]);

            var step = function step(that) {
                that.ball_animation.flying = true;

                if (i < that.ball_animation.coordinates[0].length) {

                    const xi_real = that.ball_animation.coordinates[1][i];
                    const yi_real = that.ball_animation.coordinates[2][i];
                    const xi = xi_real * 100 / max_w;
                    const yi = 75 - yi_real * 75 / max_h;

                    const xi_1_real = that.ball_animation.coordinates[1][i - 1];
                    const yi_1_real = that.ball_animation.coordinates[2][i - 1];
                    const xi_1 = xi_1_real * 100 / max_w;
                    const yi_1 = 75 - yi_1_real * 75 / max_h;

                    animate(function (dt) {
                        const x = xi_1 + (xi - xi_1) / h * dt;
                        const y = yi_1 + (yi - yi_1) / h * dt;

                        that.ball_animation.curr_coordinates.x = xi_1_real + (xi_real - xi_1_real) / h * dt;
                        that.ball_animation.curr_coordinates.y = yi_1_real + (yi_real - yi_1_real) / h * dt;

                        ball.style.marginLeft = 'calc(' + x + '% - 50px)';
                        ball.style.marginTop = 'calc(' + y + 'vh - 50px)';
                    }, h);

                    i++;
                    setTimeout(step, h, that);
                } else {
                    that.ball_animation.flying = false;
                }
            };

            var i = 1;
            step(this);
        }
    }
});

function animate(draw_callback, duration) {
    const start = performance.now();

    requestAnimationFrame(function animate(time) {
        var timePassed = time - start;

        if (timePassed > duration) {
            timePassed = duration;
        }

        draw_callback(timePassed);

        if (timePassed < duration) {
            requestAnimationFrame(animate);
        }
    });
}