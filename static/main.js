function editBookModal(ISBN) {
    var modal = document.getElementById('editModal' + ISBN);
    modal.style.display = "block";
}

function closeEditModal(ISBN) {
    var modal = document.getElementById('editModal' + ISBN);
    modal.style.display = "none";
}

function lendBookModal(ISBN) {
    var modal = document.getElementById('lendModal' + ISBN);
    modal.style.display = "block";
}

function closeLendModal(ISBN) {
    var modal = document.getElementById('lendModal' + ISBN);
    modal.style.display = "none";
}

function returnBookModal(ISBN) {
    var modal = document.getElementById('returnModal' + ISBN);
    modal.style.display = "block";
}

function closeReturnModal(ISBN) {
    var modal = document.getElementById('returnModal' + ISBN);
    modal.style.display = "none";
}

function deleteBookButton(param) {
    var form = document.createElement("form");
    form.setAttribute("method", "POST");
    form.setAttribute("action", "/delete");

    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "ISBN");
    hiddenField.setAttribute("value", param);

    form.appendChild(hiddenField);

    document.body.appendChild(form);
    form.submit();
}

function searchISBN() {
    alert("test")

    var form = document.getElementById("srchISBN");
    form.setAttribute("method", "POST");
    form.setAttribute("action", "/search");

    //var isbn = document.getElementById("ISBNfromBox").value;

    //var hiddenField = document.createElement("input");
    //hiddenField.setAttribute("type", "hidden");
    //hiddenField.setAttribute("name", "ISBN");
    //hiddenField.setAttribute("value", isbn);

    //form.appendChild(hiddenField);

    //document.body.appendChild(form);
    form.submit();

}