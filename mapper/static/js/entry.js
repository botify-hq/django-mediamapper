$(document).ready(function() {
    var preview_opened = false;

    $("#main_2").css("left",$(window).width());
    $("#main_2").hide();

    $("#enable_sort .sort").hide();
    $("#enable_sort .savesort").hide();

    $(".services_type.video").hide();
    $("#services_type .photos").click(function() {
        $("#services_type a").removeClass("active");
        $(this).addClass("active");
        $(".services_type .s_item").removeClass("active");
        $(".services_type .imported").addClass("active");

        $(".services_type.video").hide();
        $(".services_type.photo").show();
        load_imported('photo');
        return false;
    });
    $("#services_type .videos").click(function() {
        $("#services_type a").removeClass("active");
        $(this).addClass("active");
        $(".services_type .s_item").removeClass("active");
        $(".services_type .imported").addClass("active");

        $(".services_type.photo").hide();
        $(".services_type.video").show();
        load_imported('video');
        return false;
    });

    //Liste des services disponibles

    $(".services_type .s_item").click(function() {
        $(".services_type .s_item").removeClass("active");
        $(this).addClass("active");
    });

    $(".services_type .s_item.service").click(function() {
        if ($("#service_" + $(this).attr('slug')).is(":visible")) {
            $("#service_" + $(this).attr('slug')).slideUp('slow');
        }
        else {
            $(".service_item").hide();
            $("#service_" + $(this).attr('slug')).slideToggle('slow');
            load_imported_service($(this).attr('slug'), $(this).attr('service_id'));
        }
    });

    var load_imported_service = function(slug) {
        $.post(entry, { 'slug':slug }, function(data) {
            $("#results").hide();
            $("#imported").html(data).show();
            reload_actions();
        });
    }


    //Liste des services importés
    $(".services_type .imported").click(function() {
        $(".service_item").slideUp('slow');
        console.log("load_imported");
        load_imported($(this).parent().attr("type"));
    });

    var load_imported = function(type) {
        $("#enable_sort .sort").show();
        $.post(entry, { 'service_type':type }, function(data) {
            $("#results").hide();
            $("#imported").html(data).show();
            reload_actions();
        });
    }


    //Fonction ajout media
    var add_media_func = function () {
        var _this = $(this);
        $.get($(this).attr('href'), function(data) {
            $(_this)
                .html("REMOVE")
                .unbind()
                .parent()
                .removeClass("add_media")
                .addClass("remove_media")
                .end()
                .click(remove_media_func);
        });

        return false;
    }


    //Fonction suppression media
    var remove_media_func = function () {
        var _this = this;
        $.get($(this).attr('href'), function(data) {
            $(_this)
                .html("ADD")
                .unbind()
                .parent()
                .removeClass("remove_media")
                .addClass("add_media")
                .end()
                .click(add_media_func);
        });

        return false;
    }


    /*var order = new Array;
    var params;
    function sort(){
        $(".sortable").sortable({
            update : function () { 
                $(".sortable .res_item").each(function(index) {
                    console.log($(this).attr('id'));
                    order.push($(this).attr('id'));
                });
                console.log(order);
                
                //$(this).attr('order', order);
                //$("#info").load("process-sortable.php?"+order); 
            }
        });
        return false;
    }
    function sortreset(){
        $(".sortable").sortable('disable');
        var getstr = JSON.stringify(order);
        $.post($(this).attr('href'), {'order':getstr}, function(data) {

        });
        return false;
    }*/

    var order = "";
    var last_order = "";
    var params;
    function sort(){
        $("#enable_sort .sort").hide();
        $("#enable_sort .savesort").show();
        $(".videos_list .res_item_clickable a").unbind('click',preview);
        $(".videos_list .res_item_clickable a").click(function(){
            return false;            
        });
        $(".sortable").sortable('enable');
        $(".sortable").sortable({
            update : function () { 
                $(".sortable .res_item").each(function(index) {
                    order = order + "-" +($(this).attr('id'));
                });
                $("#imported #alignimagesclear").remove();
                alignImages();
            }
        });
        return false;
    }
    function sortreset(){
        $(".videos_list .res_item_clickable a").bind('click', preview);
        if(order != last_order){
            $(".sortable").sortable('disable');
            $.post($(this).attr('href'), {'order':order}, function(data) {
                last_order = order;
                order = "";
                $("#enable_sort .savesort").hide();
                $("#enable_sort .sort").show();
            });
        }
        else{
            $("#enable_sort .savesort").hide();
            $("#enable_sort .sort").show();
        }
        return false;
    }

    function save(enteredText, edit_type) {
            $.post(edit_media_field_url, {text:enteredText, edit_type:edit_type}, function(data) {
                if (edit_type == "edit_title") {
                    $("#preview .original_content .title").show();
                }
                else if (edit_type == "edit_description") {
                    $("#preview .original_content .description").show();
                }
                //$("#results").hide();
                reload_actions();
            });
        }

    function reload_actions() {

        if( $(".services_type .imported").hasClass('active') ){
            $("#enable_sort .sort").show();
            $('#enable_sort .sort').bind('click', sort);
            $('#enable_sort .savesort').bind('click',sortreset);
            $("#enable_sort .savesort").hide();
        }
        else{
            $("#enable_sort .sort").hide();
            $("#enable_sort .savesort").hide();
        }

        $('.search').hide();
     

        //Chargement Preview / Chargement photos d'albums
        $(".videos_list .res_item_clickable a").click(preview);

        
        reload_media_btn();
        $(".page_btn").click(function() {
            $(this).next("form").ajaxForm(
                function(data) {
                    $("#results").html(data).show();
                    $("#imported").hide();
                    reload_actions();
                }).submit();
        });

        var max_size = 140;

        $(".videos_list img").bind('load', function(i) {
            if ($(this).height() > $(this).width()) {
                var h = max_size;
                var w = Math.ceil($(this).width() / $(this).height() * max_size);
                var t = 0;
                var l = Math.ceil((max_size - w) / 2);
            } else {
                var w = max_size;
                var h = Math.ceil($(this).height() / $(this).width() * max_size);
                var t = Math.ceil((max_size - h) / 2);
                var l = 0;
            }
            $(this).css({ height: h, width: w, "margin-top": t, "margin-left": l });
        });

        alignImages();
    }


    function preview(){
        var media_id = $(this).attr('media_id'),
            outer_width = $("#main_2").outerWidth()+30,
            _this = $(this),
            panel = $("#main_2"),
            container = $('#main_1');

        
        if ( !($(this).attr('title') == "albums" && !preview_opened) ){
            if( panel.hasClass("hidden") && !container.is(':animated') ){
                $(".videos_list .res_item_clickable a").removeClass("active");
                _this.addClass("active");
                container.animate({width: "-=" + outer_width}, "slow", 'linear', function() {
                    panel
                        .show()
                        .removeClass("hidden")
                        .addClass("visible");
                    alignImages();
                });
            }

            if( panel.hasClass("visible") && _this.hasClass("active") && !container.is(':animated') ){
                _this.removeClass("active");
                panel
                    .hide()
                    .removeClass("visible")
                    .addClass("hidden");
                container.animate({width: "+=" + outer_width}, "slow", 'linear', function() {
                    alignImages();
                });
            }

            if( panel.hasClass("visible") && !(_this.hasClass("active")) ){
                $(".videos_list .res_item_clickable a").removeClass("active");
                _this.addClass("active");
            }
        }


        if ( ($(this).attr('title') == "albums") && ($('#imported').is(":visible")) ) {
            $('#imported').hide();
            $('#results').hide(); 
            $('.search').show();      
        }
        else if( ($(this).attr('title') == "albums") && ($('#imported').is(":hidden")) ) {
            $('#results').hide();
            $('.searching').show();
        }


        $.get($(this).attr('href'), function(data) {

            if (_this.attr('title') == "albums") {
                $('.searching').hide();
                $('#results').show();
                $("#results").html(data);
                reload_media_btn();
                reload_actions();
            } 
            else {
                $("#preview").html(data);

                if (!($('#preview .original_content .title').hasClass('modified'))) {
                    $("#preview .original_content .title").hide();
                }
                if (!($('#preview .original_content .description').hasClass('modified'))) {
                    $("#preview .original_content .description").hide();
                }

                $("#choices").hide();
                $("#media_type_choice").editInPlace({
                    callback: function(unused, enteredText) { 
                        save(enteredText, $(this).attr('type'), media_id);
                        return enteredText;
                    },
                    field_type: "select",
                    bg_over: '#3eba1c',
                    bg_out: '#3eba1c',
                    select_options: $("#choices").text()
                });

                var edit_in_place_options = {
                    callback: function(unused, enteredText) {
                        save(enteredText, $(this).attr('type'));
                        return enteredText;
                    },
                    bg_over: '#BB81D1',
                    show_buttons: true
                };


                $("#preview h2").editInPlace($.extend({}, edit_in_place_options, {default_text: "click to set title"}));
                $("#preview .edit_description").editInPlace($.extend({}, edit_in_place_options, { field_type: "textarea",
                    textarea_rows: "5",
                    textarea_cols: "45",
		    default_text: "Click to set description"})
                );

                $(".original_content a").click(function(){
                    var _this = $(this);
                    $.post(rollback_media_field_url, {'original':$(this).attr("href")}, function(data) {
                        if(_this.attr("href")=="original_title"){
                            $("#preview h2").html($(".original_content .title .content").text());
                            $("#preview .original_content .title").hide();
                        }
                        else if(_this.attr("href")=="original_description"){
                            $("#preview .edit_description").html($(".original_content .description .content").text());
                            $("#preview .original_content .description").hide();
                        }
                    });
                    return false;
                });

                reload_media_btn();
            }
	    alignImages();

            
        });
	preview_opened = true;
        return false;
    }


    function alignImages(){
        $("div#alignimagesclear").remove();
        var results_width = $("#main_1").width();
	if ($('#imported').is(':visible')) {
	  var el = '#imported';
	} else {
	  var el = '#results';
	}
        if ($(el+' .res_item:first').outerWidth() > 0) {
            var nb_by_line = Math.floor((results_width - 50) / $('.res_item:first').outerWidth());
	    $(el+' .res_item').each(function(i) {
                if (((i+1) % nb_by_line) == 0) {
                    $(this).after('<div id="alignimagesclear" style="clear:both"></div>');
                }
            });
        }
    }

    function reload_media_btn() {
        $(".add_media a").click(add_media_func);
        $(".remove_media a").click(remove_media_func);
    }

    load_imported('photo');
    reload_actions();


    $('input[type=submit]').click(function() {
        $('.searching').show();
        $('#imported').hide();
        $('#results').hide();
    });

    $('form.search_entry').ajaxForm(function(data) {
        $("#results").html(data).show();
        $('.searching').hide();
        $("#imported").hide();
        reload_actions();
    });

});
