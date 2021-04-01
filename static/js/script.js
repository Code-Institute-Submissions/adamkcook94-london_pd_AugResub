$(document).ready(function () {
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('select').formSelect();
    $('.datepicker').datepicker({
        yearRange: [1921, 2013]
    });
});

var modal = document.getElementById('confirm-deletion');


