// document.addEventListener('DOMContentLoaded', function() {
//     // Your initialization code here
// });

function showResultDiv(x, y, z) {
    var Out = document.getElementById('Output');
    Out.style.display = "block";
    var Error = document.getElementById('error');
    Error.style.display = 'none';
    document.getElementById('x').innerText = x;
    document.getElementById('y').innerText = y;
    document.getElementById('z').innerText = z;
}

function block() {
    var path = '/receive_data';
    if (window.location.pathname === path) {
        
        window.location.href = '/';
    }
}

function prin() {
    
    var error_div=document.getElementById('error');
    error_div.style.display = 'none';
    var fileInput = document.getElementById('attachment');
    var x = document.getElementById('input_box');
    x.style.display = 'none';

    var file = fileInput.files[0];
    if (!file) {
        console.error('No file selected.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/received_data', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.res === 1) {
            // console.log('Data received:', data.x, data.y, data.z);
            showResultDiv(data.x, data.y, data.z);
        } else {
            console.log("No result received");
            showErrorDiv();
        }
    })
    .catch(error => {
        console.log("in error");
        showErrorDiv();
    });
}

function showErrorDiv() {
    console.log("There is a error");
    var Out = document.getElementById('input_box');
    Out.style.display = "none";
    var error = document.getElementById('error');
    error.style.display = "block";
}