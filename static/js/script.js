    const audioUploadForm = document.getElementById('audioUploadForm');
        const audioFileInput = document.getElementById('audioFileInput');
        const summarizeCheckbox = document.getElementById('summarizeCheckbox');
        const textarea = document.getElementById('Textarea1'); // Get the textarea
        const downloadLink = document.getElementById('downloadBtn'); // Get the download link

        audioUploadForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
            formData.append('audioFile', audioFileInput.files[0]);
            formData.append('summarize', summarizeCheckbox.checked ? '1' : '0');

            fetch('/upload_audio/', {
                method: 'POST',
                body: formData,
            })
            .then((response) => response.json()) // Parse the response as JSON
            .then((data) => {
                if (summarizeCheckbox.checked) {
                    textarea.value = data.summary; // Set the textarea content to the summary
                } else {
                    textarea.value = data.corrected_text; // Set the textarea content to the corrected text
                }

                // Show the download link
                downloadLink.style.display = 'block';
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });