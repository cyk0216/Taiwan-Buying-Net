function send_company_id(value) {
    var company_name = value
    $('input[name="company_case_search"]').val(company_name);
    // console.log('company_name:')
    // console.log(company_name)

}

function send_tender_unit_id(value) {
    var tender_unit_name = value
    $('input[name="tender_case_search"]').val(tender_unit_name);
    // console.log('tender_unit_name:')
    // console.log(tender_unit_name)
}

$(function() {
    $('.search_result_company a').click(function() {
        $('.search_result_company a').removeClass('search_result_company_click');
        $(this).addClass('search_result_company_click');
    });
});

$(function() {
    $('.search_result_tender_unit a').click(function() {
        $('.search_result_tender_unit a').removeClass('search_result_tender_unit_click');
        $(this).addClass('search_result_tender_unit_click');
    });
});