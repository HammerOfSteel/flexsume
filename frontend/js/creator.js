// Get the modal element
const modal = document.getElementById('creator-modal');

// Get the button that opens the modal
const openModalBtn = document.getElementById('open-creator-modal');

// Get the <span> element that closes the modal
const closeModalBtn = document.getElementsByClassName('close')[0];

// Open the modal when the button is clicked
openModalBtn.addEventListener('click', () => {
    modal.style.display = 'block';
});

// Close the modal when the close button is clicked
closeModalBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Close the modal when clicking outside of it
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

// Function to load and display the available data in the modal
async function loadAvailableData() {
    try {
        // Make API calls to fetch competencies, experiences, and projects
        const competenciesResponse = await fetch('http://localhost:8000/competencies');
        const experiencesResponse = await fetch('http://localhost:8000/experiences');
        const projectsResponse = await fetch('http://localhost:8000/projects');

        if (competenciesResponse.ok && experiencesResponse.ok && projectsResponse.ok) {
            const competencies = await competenciesResponse.json();
            const experiences = await experiencesResponse.json();
            const projects = await projectsResponse.json();

            // Update the available data list in the modal
            updateList('available-data', [...competencies, ...experiences, ...projects]);
        } else {
            console.error('Failed to load available data');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to update a list in the modal
function updateList(listId, items) {
    const list = document.getElementById(listId);
    list.innerHTML = '';

    items.forEach(item => {
        const listItem = document.createElement('li');
        listItem.textContent = item.name || item.title;
        listItem.addEventListener('click', () => {
            // Toggle selection of the item
            listItem.classList.toggle('selected');
        });
        list.appendChild(listItem);
    });
}

// Function to get the selected data from the modal
function getSelectedData() {
    const selectedItems = document.querySelectorAll('#available-data li.selected');
    const selectedData = Array.from(selectedItems).map(item => item.textContent);
    return selectedData;
}

// Function to create a new resume
// Function to create a new resume
async function createResume(resumeData, selectedTemplate) {
    try {
        // Create the resume first
        const response = await fetch('http://localhost:8000/resumes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(resumeData)
        });

        if (response.ok) {
            const newResume = await response.json();
            console.log('New resume created:', newResume);

            // Send the resume data and selected template to the PDF generation API
            const pdfResponse = await fetch('http://localhost:8000/generate-pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    resumeData: {
                        name: resumeData.name,
                        description: resumeData.description,
                        sections: resumeData.sections.map(section => ({
                            section_type: section.section_type,
                            order: section.order
                        }))
                    },
                    selected_template: selectedTemplate
                })
            });

            if (pdfResponse.ok) {
                const pdfBlob = await pdfResponse.blob();
                const pdfUrl = URL.createObjectURL(pdfBlob);

                // Create a temporary link and trigger the download
                const downloadLink = document.createElement('a');
                downloadLink.href = pdfUrl;
                downloadLink.download = 'resume.pdf';
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);

                console.log('PDF downloaded successfully');
            } else {
                console.error('Failed to generate PDF');
            }
        } else {
            console.error('Failed to create resume');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
// Add event listener to the "Export to PDF" button
document.getElementById('export-pdf').addEventListener('click', () => {
    // Collect selected data and template
    const selectedData = getSelectedData();
    const selectedTemplate = document.getElementById('template').value;

    // Create a new resume with the selected data and template
    const resumeData = {
        name: 'My Resume',
        description: 'A resume created using Flexsume',
        user_id: 1, // Set the appropriate user_id
        created_at: new Date().toISOString().slice(0, 10),
        updated_at: new Date().toISOString().slice(0, 10),
        sections: selectedData.map((item, index) => ({
            section_type: 'custom',
            section_id: index + 1,
            order: index + 1,
            user_id: 1 // Set the appropriate user_id
        }))
    };
    createResume(resumeData, selectedTemplate);
});

// Load the available data when the modal is opened
openModalBtn.addEventListener('click', loadAvailableData);