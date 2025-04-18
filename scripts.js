function checkPassword() {
    var password = document.getElementById('password').value;
    if (password === 'Pratham') {
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('fileActions').style.display = 'block';
        fetchFiles();
    } else {
        document.getElementById('errorMessage').innerText = "Incorrect Password!";
    }
}

function fetchFiles() {
    // Fetching list of files from the server (you will implement the backend)
    fetch('/files')
        .then(response => response.json())
        .then(data => {
            let downloadSection = document.getElementById('downloadSection');
            downloadSection.innerHTML = ''; // Clear any previous files
            data.files.forEach(file => {
                let fileLink = document.createElement('a');
                fileLink.href = `/download/${file}`;
                fileLink.innerText = file;
                downloadSection.appendChild(fileLink);
                downloadSection.appendChild(document.createElement('br'));
            });
        });
}

function uploadFile() {
    let fileInput = document.getElementById('fileUpload');
    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('File uploaded successfully!');
        fetchFiles();  // Refresh the file list
    })
    .catch(err => {
        alert('Error uploading file!');
    });
}
