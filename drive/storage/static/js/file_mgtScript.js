function renameItem(oldName, isDir) {  
    var newName = prompt("Enter the new name for " + oldName + ":", oldName);  
    if (newName && newName !== oldName) {  
        var itemType = isDir ? 'folder' : 'file';  
        var path = "{{ current_dir_rel }}" + oldName;  
        var newPath = "{{ current_dir_rel }}" + newName;  
        window.location.href = `{% url 'rename_item' %}?item_type=` + itemType + `&path=` + encodeURIComponent(path) + `&new_name=` + encodeURIComponent(newPath);  
    }  
}  


    
// JavaScript to handle selection and show/hide buttons  
$(document).ready(function() {  
    $('.item-checkbox').change(function() {  
        var selectedFiles = $('.file-checkbox:checked').length;  
        var selectedFolders = $('.folder-checkbox:checked').length;  
        var totalSelected = selectedFiles + selectedFolders;  

        // Show/hide delete button  
        if (totalSelected > 0) {  
            $('#delete-btn').show();  
        } else {  
            $('#delete-btn').hide();  
        }  

        // Show/hide download button  
        if (selectedFiles > 0 && selectedFolders === 0) {  
            $('#download-btn').show();  
        } else {  
            $('#download-btn').hide();  
        }  

        // Show/hide rename button  
        if (totalSelected === 1) {  
            $('#rename-btn').show();  
        } else {  
            $('#rename-btn').hide();  
        }  
    });  
    $('.folder-checkbox').change(function() {  
    var selectedFolders = $('.folder-checkbox:checked').length;  
    // If exactly one folder is selected, show the Download Folder button  
    if (selectedFolders === 1) {  
        $('#download-folder-btn').show();  
    } else {  
        $('#download-folder-btn').hide();  
    }  
});  
});  

    function downloadFolder() {  
var selectedFolders = $('.folder-checkbox:checked');  
if (selectedFolders.length === 1) {  
    var folderPath = selectedFolders.data('name');  
    var url = `{% url 'folder_download' path='PLACEHOLDER' %}`.replace('PLACEHOLDER', encodeURIComponent(folderPath));  
    var form = $('<form>', {  
        'action': url,  
        'method': 'post'  
    }).append('{% csrf_token %}');  
    form.appendTo('body').submit();  
}  
}  


    
    function renameSelected() {  
        // Implement the logic to rename the selected item  
        var selectedItems = $('.item-checkbox:checked');  
        if (selectedItems.length === 1) {  
            var itemName = selectedItems.data('name');  
            var isDir = selectedItems.hasClass('folder-checkbox');  
            renameItem(itemName, isDir);  
        }  
    }  

    function deleteSelected() {  
var selectedItems = $('.item-checkbox:checked');  
var paths = selectedItems.map(function() {  
    return $(this).data('name');  
}).get();  
$('#delete-paths').val(JSON.stringify(paths)); // Convert array to JSON string  
$('#bulk-delete-form').submit();  
}  

function downloadSelected() {  
var selectedItems = $('.item-checkbox:checked');  
var paths = selectedItems.map(function() {  
    return $(this).data('name');  
}).get();  
$('#download-paths').val(JSON.stringify(paths)); // Convert array to JSON string  
$('#bulk-download-form').submit();  
}  

$('#file-upload-form').submit(function(e) {  
e.preventDefault();  
var formData = new FormData(this);  
var xhr = new XMLHttpRequest();  

console.log("Upload started"); // Debugging statement  

// Add an event listener for progress  
xhr.upload.addEventListener('progress', function(e) {  
    if (e.lengthComputable) {  
        var percentComplete = e.loaded / e.total * 100;  
        console.log("Progress: " + percentComplete + "%"); // Debugging statement  
        $('#upload-progress').val(percentComplete);  
        $('#progress-percentage').text(percentComplete.toFixed(2) + '%');  
    }  
}, false);  

// Show the progress bar  
$('#progress-container').show();  

// Update the UI after the upload is complete  
xhr.onreadystatechange = function() {  
    if (xhr.readyState == XMLHttpRequest.DONE) {  
        console.log("Upload finished"); // Debugging statement  
        $('#progress-container').hide();  
        $('#upload-progress').val(0);  
        $('#progress-percentage').text('0%');  
        location.reload(); // or perform other actions like showing a success message  
    }  
};  

// Set up and send the AJAX request  
xhr.open('POST', this.action, true);  
xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');  
xhr.send(formData);  
});  

$('#folder-upload-form').submit(function(e) {  
e.preventDefault();  
var formData = new FormData(this);  
var xhr = new XMLHttpRequest();  

console.log("Folder upload started"); // Debugging statement  

// Add an event listener for progress  
xhr.upload.addEventListener('progress', function(e) {  
    if (e.lengthComputable) {  
        var percentComplete = e.loaded / e.total * 100;  
        console.log("Folder Progress: " + percentComplete + "%"); // Debugging statement  
        $('#upload-progress').val(percentComplete);  
        $('#progress-percentage').text(percentComplete.toFixed(2) + '%');  
    }  
}, false);  

// Show the progress bar  
$('#progress-container').show();  

// Update the UI after the upload is complete  
xhr.onreadystatechange = function() {  
    if (xhr.readyState == XMLHttpRequest.DONE) {  
        console.log("Folder upload finished"); // Debugging statement  
        $('#progress-container').hide();  
        $('#upload-progress').val(0);  
        $('#progress-percentage').text('0%');  
        location.reload(); // or perform other actions like showing a success message  
    }  
};  

// Set up and send the AJAX request  
xhr.open('POST', this.action, true);  
xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');  
xhr.send(formData);  
});  


document.getElementById('execute-command-form').onsubmit = function(e) {  
    e.preventDefault();  
    
    var formData = new FormData(this);  
    fetch("{% url 'execute_command' %}", {  
        method: 'POST',  
        body: formData,  
        headers: {  
            'X-CSRFToken': '{{ csrf_token }}'  
        }  
    })  
    .then(response => response.json())  
    .then(data => {  
        if (data.error) {  
            alert('Error: ' + data.error);  
        } else {  
            alert('Output: ' + data.output);  
        }  
    })  
    .catch(error => {  
        console.error('Error:', error);  
    });  
};  