document.addEventListener('DOMContentLoaded', function() {
    let fileInput = document.getElementById('id_image');

    if(!fileInput) {
        fileInput = document.getElementById('id_video_file');
    }

    if(!fileInput) {
        fileInput = document.getElementById('id_audio_file');
    }

    const fileNameDisplay = document.getElementById('file-name');
    const fileTrigger = document.querySelector('.protocol-file-trigger'); 

    if (fileInput && fileNameDisplay && fileTrigger) {
        fileTrigger.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                fileInput.click();
            }
        });
        
        fileInput.addEventListener('change', function() {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = fileInput.files[0].name;
            } else {
                fileNameDisplay.textContent = '[...NO FILE SELECTED...]';
            }
        });
    }
});
