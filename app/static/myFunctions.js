function disablePN(p1,p2,p3) {
    const checkbox = document.getElementById(p2);

    if (checkbox.checked) {
        document.getElementById(p1).disabled = true;
        document.getElementById(p3).disabled = false;
    } else {
        document.getElementById(p1).disabled = false;
        document.getElementById(p3).disabled = true;
    }
}

function disableN(p1,p2) {
    const checkbox = document.getElementById(p1);

    if (checkbox.checked) {
        document.getElementById(p2).disabled = false;
    } else {
        document.getElementById(p2).disabled = true;
    }
}

function tdisableN(p1,p2) {
    const selected = document.getElementById(p1);

    if (selected.value=='NONE') {
        document.getElementById(p2).disabled = true;
    } else {
        document.getElementById(p2).disabled = false;
    }
}
