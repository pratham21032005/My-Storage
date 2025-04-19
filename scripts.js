let userRole = ''; // Will be 'admin' or 'user'

function checkPassword() {
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');

    if (password === 'Pratham') {
        userRole = 'admin';
    } else if (password === '1234') {
        userRole = 'user';
    } else {
        errorMessage.innerText = "Incorrect Password!";
        return;
    }

    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('fileActions').style.display = 'block';
    fetchFiles();
}

function fetchFiles() {
    fetch('/files')
        .then(response => response.json())
        .then(data => {
            const downloadSection = document.getElementById('downloadSection');
            downloadSection.innerHTML = '';

            data.files.forEach(file => {
                const container = document.createElement('div');
                container.classList.add('file-item');

                const fileLink = document.createElement('a');
                fileLink.href = `/download/${file}`;
                fileLink.innerText = file;
                fileLink.setAttribute('target', '_blank');
                container.appendChild(fileLink);

                // Add delete button only for admin
                if (userRole === 'admin') {
                    const deleteBtn = document.createElement('button');
                    deleteBtn.innerText = 'Delete';
                    deleteBtn.classList.add('delete-btn');
                    deleteBtn.onclick = () => deleteFile(file);
                    container.appendChild(deleteBtn);
                }

                downloadSection.appendChild(container);
            });
        });
}

function uploadFile() {
    const fileInput = document.getElementById('fileUpload');
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('File uploaded successfully!');
        fetchFiles();
    })
    .catch(err => {
        alert('Error uploading file!');
    });
}

function deleteFile(filename) {
    fetch(`/delete/${filename}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            alert('File deleted successfully!');
            fetchFiles();
        } else {
            alert('Error deleting file!');
        }
    });
}
