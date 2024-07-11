$(document).ready(function () {

    $('.srchWrp a.srch').click(function () {
        $('.srchWrp span').addClass('show');
    });

    $('.srchWrp a.close').click(function () {
        $('.srchWrp span').removeClass('show');
    });



    $(".mob-menu").click(function (e) {
        if ($(".dropdown").hasClass("show")) {
            $(".dropdown").removeClass("show");
            $(".mob-menu").removeClass("show");
        } else {
            $(".dropdown").addClass("show");
            $(".mob-menu").addClass("show");
            $(".left_panel").removeClass("show");
        }
    });

    if ($(window).innerWidth() < 820) {
        $('.bg').click(function (e) {
            e.stopPropagation();
            if ($(this).find('.submenu').hasClass('show')) {
                $(this).find('.submenu').removeClass('show')
                $(this).find('.submenu').hide();
            } else {
                $('.bg').find('.submenu').removeClass('show');
                $('.bg').find('.submenu').hide();
                $(this).find('.submenu').addClass('show')
                $(this).find('.submenu').slideDown('fast');
            }
        });
        $('.submenu > li').click(function (e) {
            e.stopPropagation();
            if ($(this).find('.sub-submenu').hasClass('show')) {
                $(this).find('.sub-submenu').removeClass('show')
                $(this).find('.sub-submenu').hide();
            } else {
                $('.submenu > li').find('.sub-submenu').hide();
                $('.submenu > li').find('.sub-submenu').removeClass('show');
                $(this).find('.sub-submenu').addClass('show')
                $(this).find('.sub-submenu').slideDown('fast');
            }
        });

        $('.sub-submenu > li').click(function (e) {
            e.stopPropagation();
        });
    }

    if (navigator.userAgent.match(/Trident\/7\./)) { // if IE
        $('body').on("mousewheel", function () {
            // remove default behavior
            event.preventDefault();

            //scroll without smoothing
            var wheelDelta = event.wheelDelta;
            var currentScrollPosition = window.pageYOffset;
            window.scrollTo(0, currentScrollPosition - wheelDelta);
        });
    }


    // -----------
    // Debugger that shows view port width. Helps when making responsive designs.
    // -----------
    function showViewPortWidth(display) {
        if (display) {
            var width = jQuery(window).width();
            jQuery('body').prepend('<div id="viewportsize" style="z-index:9999;position:fixed;top:40px;left:5px;color:#fff;background:#000;padding:10px">Width: ' + width + '</div>');
            jQuery(window).resize(function () {
                width = jQuery(window).width();
                jQuery('#viewportsize').html('Width: ' + width);
            });
        }
    }

    showViewPortWidth(true);

    //banner Owl Carousel
    $("#owl-demo").owlCarousel({
        navigation: true, // Show next and prev buttons
        slideSpeed: 300,
        paginationSpeed: 400,
        singleItem: true,        
        autoPlay : true,
	  	autoPlaySpeed: 5000,
        autoPlayTimeout: 5000,
        itemsDesktop: false,
        itemsDesktopSmall: false,
        itemsTablet: false,
        itemsMobile: false
    });

    if (window.matchMedia("(max-width: 767px)").matches) {
        $("#mainBox .banner").css({"height": "calc(100vh - " + ($("#header").outerHeight() + 50) + "px)"});
    } else {
        $("#mainBox .banner").css({"height": "calc(100vh - " + $("#header").outerHeight() + "px)"});
    }

    var isiPhone = /iphone/i.test(navigator.userAgent.toLowerCase());
    // alert(isiPhone);
    if (isiPhone) {
        $("#mainBox .banner").css({"height": "calc(100vh - " + ($("#header").outerHeight() + 50) + "px)"});
    }
    
});