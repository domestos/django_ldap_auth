
var cookie_name = "selected";
function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}

function update_selected(varid, check_status) {
    var current_checked = [];
    if (getCookie(cookie_name)) {
        //   alert("cookie is not empty")
        current_checked = getCookie(cookie_name).split(",");
        show_selected_rows()
    }

    if (isNaN(parseInt(varid)) == false && check_status == true) {
        //   alert("need add cooke")
        current_checked.push(varid);
        document.cookie = cookie_name + '=' + Array.from(new Set(current_checked));
        show_selected_rows(current_checked)
    } else if (isNaN(parseInt(varid)) == false && check_status == false) {
        document.cookie = cookie_name + '=' + current_checked.filter(e => e !== varid);
        show_selected_rows()
    }


}

var storage_name = "checkedvars";

function show_selected_rows() {
    if (getCookie(cookie_name)) {
        $(".clearSelected").html("Cencel "+ getCookie(cookie_name).split(",").length + " rows")
        $(".selectAll").html("    Select All")
    }    
}

// toggle button
function toggle(source) {

    checkboxes = document.getElementsByName('selected_rows');
    for (var i in checkboxes) {
        checkboxes[i].checked = source.checked;

        update_selected(checkboxes[i].value, checkboxes[i].checked);
    }
    show_selected_rows()

    
}

function display_checkBoxStatus(){
    var current_checked = [];
    if (getCookie(cookie_name)) {
        current_checked = getCookie(cookie_name).split(",");
        // if cookies isn't empty show sount selected row and buttons
        show_selected_rows()
        checkboxes = document.getElementsByName('selected_rows');
        for (var i in checkboxes) {
            if (current_checked.includes(checkboxes[i].value)) {
                checkboxes[i].checked = true;
            }
        }
    }

}

function cencelSelected(){

}


$(document).ready(function () {
    // display checkboxes according to selected varids in session storage  

    display_checkBoxStatus()
    // save/remove checked/unchecked varid in session storage  
    $(".selected_rows").click(function (event) {
        var varid = event.target.value
        var check_status = event.target.checked
        //   alert(varid)
        //   alert(check_status)   
        update_selected(varid, check_status)
        show_selected_rows()
    });


    $(".selectAll").click(function (event) {
        document.cookie = cookie_name + '=' +'All';
       
    });


    
    $(".clearSelected").click(function (event) {
        // CencelSelected()

        event.preventDefault(); 
        document.cookie = cookie_name + '=' +'';
        $(".clearSelected").html("")
        $(".selectAll").html("")
        show_selected_rows()
        checkboxes = document.getElementsByName('selected_rows');
        
        for (var i in checkboxes) {
            checkboxes[i].checked = false;
        }
        // alert('Clear ')
    });












});