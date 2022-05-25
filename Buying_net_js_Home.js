$(document).ready(function() {
    //datepicker
    $("#start_date_begin").datepicker({ yearRange: "1921:c+3", dateFormat: "yy-mm-dd", changeMonth: true, changeYear: true });
    $("#start_date_final").datepicker({ yearRange: "1921:c+3", dateFormat: "yy-mm-dd", changeMonth: true, changeYear: true });
    $("#end_date_begin").datepicker({ yearRange: "1921:c+3", dateFormat: "yy-mm-dd", changeMonth: true, changeYear: true });
    $("#end_date_final").datepicker({ yearRange: "1921:c+3", dateFormat: "yy-mm-dd", changeMonth: true, changeYear: true });
    //tab section
    $("#content").find("[id^='tab']").hide(); // Hide all content
    $("#tabs li:first").attr("id", "current"); // Activate the first tab
    $("#content #tab1").fadeIn(); // Show first tab's content
    if ($('#tabs input.tab_ref').attr('name') == 'case') {
        $('.tab_company').attr('id', 'current')
        $("#content #tab1").fadeIn(); // Show first tab's content
    } else {
        $("#tabs li:first").attr("id", "current"); // Activate the first tab
        $("#content #tab1").fadeIn(); // Show first tab's content
    }

    $('#tabs a').click(function(e) {
        e.preventDefault();
        if ($(this).closest("li").attr("id") == "current") { //detection for current tab
            return;
        } else {
            $("#content").find("[id^='tab']").hide(); // Hide all content
            $("#tabs li").attr("id", ""); //Reset id's
            $(this).parent().attr("id", "current"); // Activate this
            $('#' + $(this).attr('name')).fadeIn(); // Show content for the current tab
        }
    });

    $('form[name="company_search"]').on('submit', function() {
        if ($('input[type="text"]').val() == '' && $('select').val() == '') {
            alert('至少輸入一個條件');
            return false; //中斷此function進行
        }
    });

    $('form[name="case_search"]').on('submit', function() {
        if ($('input[name="case_search"]').val() == '' && $('input[name="start_date_begin"]').val() == '' && $('input[name="start_date_final"]').val() == '' && $('input[name="end_date_begin"]').val() == '' && $('input[name="end_date_final"]').val() == '' && $('input[name="price_start"]').val() == '' && $('input[name="price_end"]').val() == '' && $('select[name="status"]').val() == '' && $('input[name="company_case_search"]').val() == '' && $('input[name="tender_case_search"]').val() == '') {
            alert('至少輸入一個條件');
            return false; //中斷此function進行
        }
    });

    $('form[name="tender_search"]').on('submit', function() {
        if ($('input[name="tenderer_search"]').val() == '') {
            alert('至少輸入一個條件');
            return false; //中斷此function進行
        }
    });


});

/*function send_page(page) {
    $.ajax({
        type: "POST",
        url: "/company_search",
        data: { 'value': page },
        dataType: "html",
        success: function() {
            console.log(page);
        }
    })
}*/

//extand area
// var extendthebar = document.getElementsByClassName("extend");

// for (var i = 0; i < extendthebar.length; i++) {
//     extendthebar[i].addEventListener("click", function() {
//         this.classList.toggle("active");
//         var content = this.nextElementSibling;
//         if (content.style.display === "block") {
//             content.style.display = "none";
//         } else {
//             content.style.display = "block";
//         }
//     });
// }