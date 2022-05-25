var extendthebar = document.getElementsByClassName("extend");

for (var i = 0; i < extendthebar.length; i++) {
    extendthebar[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}

function updateList(type) {
    company_type_filter = 'vendor_' + type;
    console.log(company_type_filter)
    company_name_result = document.getElementsByClassName('search_result')[0].children;
    console.log(company_name_result)

    for (var x = 0; x < company_name_result.length; x++) {
        company_name_result[x].style.display = 'none'; //for迴圈
    }
    select_type = document.getElementsByClassName(company_type_filter); //所有類別

    for (var y = 0; y < select_type.length; y++) {
        select_type[y].style.display = 'block';
    }
    //console.log(select_type);
}

function caseList(id) {
    case_id_choose = 'CaseInfo_' + id;
    console.log(case_id_choose);
    case_info_choose = document.getElementsByClassName('vendor_case_info')[0].children;
    console.log(case_info_choose);

    for (var z = 0; z < case_info_choose.length; z++) {
        case_info_choose[z].style.display = 'none';
    }
    select_case = document.getElementsByClassName(case_id_choose);
    for (var c = 0; c < select_case.length; c++) {
        select_case[c].style.display = 'block';
    }
}

function send_case_id(Case_id) {
    $.ajax({
        type: "POST",
        url: "/vendor_page",
        data: { 'value': Case_id },
        dataType: "html",
        success: function() {
            console.log(Case_id);
        }
    })
    location.reload()
}