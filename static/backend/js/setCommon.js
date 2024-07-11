function CheckAll(myform, chkboxname, chkboxname1) {
    var e;
    for (var i = 0; i < eval("" + "document." + myform + ".elements.length"); i++) {
        eval("e =" + "" + "document." + myform + ".elements[i]");
        if ((e.name == eval("'" + chkboxname + "'")) || (e.name == eval("'" + chkboxname1 + "'")) && (e.type == 'checkbox')) {
            // eval("e.checked = " + "" + "document." + myform + "." + chkboxname + ".checked");
            // $('input[type="checkbox"]').prop("checked", true);
        }
    }
}

function CallOperation(value, myform, chkboxname) {

    /*Code for check checkbox is selected or not*/

    var count = 0;
    var frmElement;
    eval("frmElement = document." + myform + "['" + chkboxname + "']");

    var checkcount = 0;

    for (var i = 0; i < eval("" + "document." + myform + ".elements.length"); i++) {
        eval("e =" + "" + "document." + myform + ".elements[i]")
        if (e.type == 'checkbox') {
            checkcount++;
        }
    }

    if (checkcount > 1) {
        if (checkcount == 2 && frmElement.checked !== undefined || checkcount == 3 && frmElement.checked !== undefined) {
            if (frmElement.checked == true) {
                count++;
            }
        } else
            if (frmElement.length) {
                for (var i = 0; i < frmElement.length; i++) {
                    if (frmElement[i].checked == true) {
                        count++;
                    }
                }
            }
    }

    if (count == 0 && checkcount != 1) {
        alert("Please select record(s) to " + value);
        return false;
    } else {
        var message = "";
        if (value == 'Activate') {
            message = "active"
        } else if (value == 'De-Activate') {
            message = "deactive"
        } else if (value == 'Delete') {
            message = "delete"

        } else if (value == 'Set As Header') {
            message = "setHeader"

        } else if (value == 'Unset As Header') {
            message = "unsetHeader"

        } else if (value == 'Set As Footer') {
            message = "setFooter"

        } else if (value == 'Unset As Footer') {
            message = "unsetFooter"

        } else if (value == 'Set As Featured') {
            message = "setFeatured"

        } else if (value == 'Unset As Featured') {
            message = "unsetFeatured"

        } else if (value == 'Customers') {
            message = "customers"
        } else if (value == 'Subscribers') {
            message = "subscribers"
        } else if (value == 'Customerandsubscribers') {
            message = "customerAndSubscribers"
        } else if (value == 'Set As Top') {
            message = "setTop"

        } else if (value == 'Unset As Top') {
            message = "unsetTop"
        } else if (value == 'Set As New') {
            message = "setNew"

        } else if (value == 'Unset As New') {
            message = "unsetNew"
        } else if (value == 'Set As Bottom') {
            message = "setBottom"

        } else if (value == 'Unset As Bottom') {
            message = "unsetBottom"
        } else if (value == 'Verified') {
            message = "verified"

        } else if (value == 'Pending') {
            message = "pending"
        } else if (value == 'NotCancel') {
            message = "notCancel"
        } else if (value == 'Cancel') {
            message = "cancel"
        } else if (value == 'Set As Submenu') {
            message = "setSubmenu"

        } else if (value == 'Unset As Submenu') {
            message = "unsetSubmenu"
        } else {
            message = value
        }


        if (message == 'delete') {
            if (confirm("All checked will be permanently deleted, action cannot be undone.")) {
                eval("" + "" + "document." + myform + ".operationFlag.value=message");
                if (myform == 'frmProducts') {
                    $('#submit').click();
                    $("[name=frmProducts]").submit();
                } else {
                    eval("" + "" + "document." + myform + ".submit()");
                }
            } else {
                return false;
            }
        } else {
            eval("" + "" + "document." + myform + ".operationFlag.value=message");
            if (myform == 'frmProducts') {
                $('#submit').click();
                $("[name=frmProducts]").submit();
            } else {
                eval("" + "" + "document." + myform + ".submit()");
            }
        }


    }

}

function callExport(value, myform, chkboxname) {
    var count = 0;
    var frmElement;
    eval("frmElement = document." + myform + "['" + chkboxname + "']");

    var checkcount = 0;

    for (var i = 0; i < eval("" + "document." + myform + ".elements.length"); i++) {
        eval("e =" + "" + "document." + myform + ".elements[i]")
        if (e.type == 'checkbox') {
            checkcount++;
        }
    }

    if (checkcount > 1) {
        if (checkcount == 2 || checkcount == 3) {
            if (frmElement.checked == true) {
                count++;
            }
        } else if (frmElement.length) {
            for (var i = 0; i < frmElement.length; i++) {
                if (frmElement[i].checked == true) {
                    count++;
                }
            }
        }
    }
    var message = 'export';
    eval("" + "" + "document." + myform + ".operationFlag.value=message");
    eval("" + "" + "document." + myform + ".submit()");


}
