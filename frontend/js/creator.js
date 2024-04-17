// creator.js
let competencies = [];
let experiences = [];
let projects = [];

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

// Function to load and display the resume preview in the modal
async function loadResumePreview() {
    try {
        // Make API calls to fetch competencies, experiences, and projects
        const competenciesResponse = await fetch('http://localhost:8000/competencies');
        const experiencesResponse = await fetch('http://localhost:8000/experiences');
        const projectsResponse = await fetch('http://localhost:8000/projects');

        if (competenciesResponse.ok && experiencesResponse.ok && projectsResponse.ok) {
            competencies = await competenciesResponse.json();
            experiences = await experiencesResponse.json();
            projects = await projectsResponse.json();
            console.log(competencies, experiences, projects);

            // Generate the resume preview HTML based on the selected template
            const resumePreviewHTML = generateResumePreview(competencies, experiences, projects);

            // Update the resume preview in the modal
            document.getElementById('resume-preview').innerHTML = resumePreviewHTML;
        } else {
            console.error('Failed to load resume data');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to generate the resume preview HTML based on the selected template
function generateResumePreview(competencies, experiences, projects) {
    const selectedTemplate = document.getElementById('template').value;

    // Generate the HTML based on the selected template
    let resumePreviewHTML = '';
    let resumeTitle = document.getElementById('resume-title').value;
    if (selectedTemplate === 'modern') {
        resumePreviewHTML = `
            <style>
                .resume-preview.modern {
                    font-family: 'Arial', sans-serif;
                    color: #333;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .resume-preview.modern h2 {
                    color: #0056b3;
                    border-bottom: 2px solid #0056b3;
                }
                .resume-preview.modern ul {
                    list-style: none;
                    padding: 0;
                }
                .resume-preview.modern li {
                    margin-bottom: 10px;
                    font-size: 16px;
                    line-height: 1.6;
                }
                .resume-preview.modern .remove-item {
                    margin-left: 10px;
                    color: red;
                    cursor: pointer;
                }
            </style>
            <div class="resume-preview modern">
                <h1>${resumeTitle}</h1>
                <h2>Competencies</h2>
                <ul>
                    ${competencies.map(competency => `
                        <li>
                        <h3>${competency.proficiency_level} ${competency.name} - ${competency.description}</h3>
                            <span class="remove-item" data-id="${competency.id}" data-type="competency">&times;</span>
                        </li>
                    `).join('')}
                </ul>
                <h2>Experiences</h2>
                <ul>
                    ${experiences.map(experience => `
                        <li>
                        <h3>${experience.title} at ${experience.company} - (${experience.start_date} - ${experience.end_date}) in ${experience.location}</h3>
                            <span class="remove-item" data-id="${experience.id}" data-type="experience">&times;</span>
                        </li>
                    `).join('')}
                </ul>
                <h2>Projects</h2>
                <ul>
                    ${projects.map(project => `
                        <li>
                        <h3>${project.title} - ${project.description} - (${project.start_date} - ${project.end_date})</h3>
                            <span class="remove-item" data-id="${project.id}" data-type="project">&times;</span>
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
    } else if (selectedTemplate === 'classic') {
        resumePreviewHTML = `
            <style>
                .resume-preview.classic {
                    font-family: 'Times New Roman', serif;
                    color: #000;
                    background-color: #f4f4f9;
                    padding: 20px;
                    border: 1px solid #ccc;
                }
                .resume-preview.classic h2 {
                    color: #000;
                    border-bottom: 1px solid #000;
                }
                .resume-preview.classic ul {
                    list-style-type: square;
                    padding-left: 20px;
                }
                .resume-preview.classic li {
                    margin-bottom: 5px;
                    font-size: 14px;
                    line-height: 1.5;
                }
                .resume-preview.classic .remove-item {
                    margin-left: 10px;
                    color: red;
                    cursor: pointer;
                }
            </style>
            <div class="resume-preview classic">
                <h1>${resumeTitle}</h1>
                <h2>Competencies</h2>
                <ul>
                    ${competencies.map(competency => `
                        <li>
                        <h3>${competency.proficiency_level} ${competency.name} - ${competency.description}</h3>
                            <span class="remove-item" data-id="${competency.id}" data-type="competency">&times;</span>
                        </li>
                    `).join('')}
                </ul>
                <h2>Experiences</h2>
                <ul>
                    ${experiences.map(experience => `
                        <li>
                        <h3>${experience.title} at ${experience.company} - (${experience.start_date} - ${experience.end_date}) in ${experience.location}</h3>
                            <span class="remove-item" data-id="${experience.id}" data-type="experience">&times;</span>
                        </li>
                    `).join('')}
                </ul>
                <h2>Projects</h2>
                <ul>
                    ${projects.map(project => `
                        <li>
                        <h3>${project.title} - ${project.description} - (${project.start_date} - ${project.end_date})</h3>
                            <span class="remove-item" data-id="${project.id}" data-type="project">&times;</span>
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
    }

    return resumePreviewHTML;
}


// Function to handle removing an item from the resume preview
function removeItemFromPreview(event) {
    if (event.target.classList.contains('remove-item')) {
        const itemId = event.target.dataset.id;
        const itemType = event.target.dataset.type;

        // Remove the item from the resume preview
        event.target.parentNode.remove();

        // Update the resume data based on the removed item
        if (itemType === 'competency') {
            // Remove the competency from the competencies array
            competencies = competencies.filter(competency => competency.id !== itemId);
        } else if (itemType === 'experience') {
            // Remove the experience from the experiences array
            experiences = experiences.filter(experience => experience.id !== itemId);
        } else if (itemType === 'project') {
            // Remove the project from the projects array
            projects = projects.filter(project => project.id !== itemId);
        }
    }
}

// Function to save the resume to the database
async function saveResume() {
    const resumeData = {
        name: 'My Resume',
        description: 'A resume created using Flexsume',
        sections: [],
        competencies: competencies,
        experiences: experiences,
        projects: projects
    };

    try {
        const response = await fetch('http://localhost:8000/resumes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(resumeData)
        });

        if (response.ok) {
            console.log('Resume saved successfully');
        } else {
            console.error('Failed to save resume');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Add event listeners
document.getElementById('template').addEventListener('change', loadResumePreview);
document.getElementById('resume-preview').addEventListener('click', removeItemFromPreview);
document.getElementById('save-resume').addEventListener('click', saveResume);

// Load the resume preview when the modal is opened
openModalBtn.addEventListener('click', loadResumePreview);