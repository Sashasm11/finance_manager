// static/js/import.js
document.addEventListener('DOMContentLoaded', function() {
    const importForm = document.getElementById('import-form');

    importForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData();
        const fileInput = document.getElementById('file-input');
        const bankType = document.querySelector('input[name="bank"]:checked').value;
        const accountName = document.getElementById('account-name').value;
        const spinner = document.getElementById('import-spinner');

        formData.append('csv_file', fileInput.files[0]);
        formData.append('bank', bankType);
        formData.append('account_name', accountName);
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

        // Показываем спиннер
        spinner.style.display = 'inline-block';
        document.getElementById('import-button').disabled = true;

        fetch('/import/csv/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showImportResults(data);
            } else {
                alert('Ошибка: ' + data.error);
            }
        })
        .catch(error => {
            alert('Ошибка при импорте: ' + error);
        })
        .finally(() => {
            spinner.style.display = 'none';
            document.getElementById('import-button').disabled = false;
        });
    });
});

function showImportResults(data) {
    document.getElementById('imported-count').textContent = data.imported_count;

    const errorsList = document.getElementById('errors-list');
    errorsList.innerHTML = '';

    if (data.errors && data.errors.length > 0) {
        data.errors.forEach(error => {
            const li = document.createElement('li');
            li.textContent = error;
            errorsList.appendChild(li);
        });
        document.getElementById('import-errors').style.display = 'block';
    } else {
        document.getElementById('import-errors').style.display = 'none';
    }

    document.getElementById('import-result').style.display = 'block';
    document.getElementById('file-import-section').style.display = 'none';
}

function resetImportForm() {
    document.getElementById('import-form').reset();
    document.getElementById('import-result').style.display = 'none';
    document.getElementById('file-import-section').style.display = 'block';
    document.getElementById('import-errors').style.display = 'none';
}
