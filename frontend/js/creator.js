// creator.js
let competencies = [];
let experiences = [];
let educations = [];
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
        const educationsResponse = await fetch('http://localhost:8000/educations');
        const projectsResponse = await fetch('http://localhost:8000/projects');

        if (competenciesResponse.ok && experiencesResponse.ok && projectsResponse.ok) {
            competencies = await competenciesResponse.json();
            experiences = await experiencesResponse.json();
            educations = await educationsResponse.json();
            projects = await projectsResponse.json();
            console.log(competencies, experiences, educations, projects);

            // Generate the resume preview HTML based on the selected template
            const resumePreviewHTML = generateResumePreview(competencies, experiences, educations, projects);

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
function generateResumePreview(competencies, experiences, educations, projects) {
    const selectedTemplate = document.getElementById('template').value;

    // Generate the HTML based on the selected template
    let resumePreviewHTML = '';
    let resumeTitle = document.getElementById('resume-title').value;
    if (selectedTemplate === 'modern' || selectedTemplate === 'classic') {
        let templateStyles, listItemStyle;
        if (selectedTemplate === 'modern') {
            templateStyles = `
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
            `;
            listItemStyle = 'modern';
        } else if (selectedTemplate === 'classic') {
            templateStyles = `
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
            `;
            listItemStyle = 'classic';
        }

        resumePreviewHTML = `
            <style>
                ${templateStyles}
                .resume-preview.${listItemStyle} .remove-item {
                    margin-left: 10px;
                    color: red;
                    cursor: pointer;
                }
            </style>
            <div class="resume-preview ${listItemStyle}">
                <h1>${resumeTitle}</h1>
                <input id="imageInput" name="photo" type="file" accept="image/*" onchange="document.getElementById('output').src = window.URL.createObjectURL(this.files[0])" style="display: none;">
                <label for="imageInput">
                <img src="/images/placeholder.jpeg" id="output" alt="Image Placeholder" width="200" height="200" style="cursor: pointer;" />
                </label>
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
                <h2>Education & Certificates:</h2>
                <ul>
                ${educations.map(education => `
                    <li>
                        <h3>${education.title} at ${education.institute} - (${education.start_date} - ${education.end_date}) in ${education.location}</h3>
                        <span class="remove-item" data-id="${education.id}" data-type="experience">&times;</span>
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
    } else if (selectedTemplate === 'cypoint') {
        let templateStyles = `
            .resume-preview.cypoint {
                font-family: Arial, sans-serif;
                color: #000;
                background-color: #fff;
                padding: 20px;
                border: 1px solid #ccc;
            }
            .resume-preview.cypoint h1, .resume-preview.cypoint h2, .resume-preview.cypoint h3, .resume-preview.cypoint p {
                margin: 10px 0;
            }
            .resume-preview.cypoint ul {
                list-style-type: none;
                padding-left: 0;
            }
            .resume-preview.cypoint li {
                margin-bottom: 5px;
                font-size: 14px;
                line-height: 1.5;
            }
            .resume-preview.cypoint .remove-item {
                margin-left: 10px;
                color: red;
                cursor: pointer;
            }
            .resume-preview.cypoint .section-title {
                font-weight: bold;
                text-align: center;
                font-size: 3em;
                margin-bottom: 10px;
            }
            .resume-preview.cypoint .section-content {
                margin-left: 20px;
                font-size: 1.2em;
                margin-top: 5%;
            }
            .resume-preview.cypoint .experience-table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            .resume-preview.cypoint .experience-table td {
                padding: 5px;
                vertical-align: top;
            }
            .resume-preview.cypoint .experience-table td:first-child {
                font-weight: bold;
                width: 240px;
            }
            .resume-preview.cypoint .section {
                page-break-inside: avoid;
            }
            .resume-preview.cypoint .page {
                width: 595px; /* A4 width in pixels */
                min-height: 842px; /* A4 height in pixels */
                margin: auto;
                page-break-after: always;
                position: relative;
                box-sizing: border-box;
                padding: 20px;
            }
            .resume-preview.cypoint .page-1-content {
                text-align: center;
                margin-top: 35%;
            }
            .resume-preview.cypoint .page-1 {
                background-image: url('/images/CV_BG_P1.jpg');
                background-size: cover;
                background-repeat: no-repeat;
            }
            .resume-preview.cypoint .page-2 {
                margin-left: 5%;
                margin-top: 5%;
            }
            .page-3 {
                text-align: left;
            }
            div.header-section h1, div.header-section h3, div.section-content p, div.section-content h2 {
                border: none;
                outline: none;
                background: transparent;
            }
            
            div.header-section h1:focus, div.header-section h3:focus, div.section-content p:focus, div.section-content h2:focus {
                outline: none;
                border-bottom: 1px solid #ccc; /* Only show a bottom border when focused */
            }
            
            /* Hide the border when printing or saving to PDF */
            @media print {
                div.header-section h1, div.header-section h3, div.section-content p, div.section-content h2 {
                    border: none;
                }
            }
            #output:hover {
                opacity: 0.8;
            }
        `;
        listItemStyle = 'cypoint';  // Use a consistent class name strategy
        resumePreviewHTML = `
            <style>
                ${templateStyles}
            </style>
            <div class="resume-preview ${listItemStyle}">
                <div class="page page-1">
                    <div class="page-1-content">
                        <input id="imageInput" name="photo" type="file" accept="image/*" onchange="document.getElementById('output').src = window.URL.createObjectURL(this.files[0])" style="display: none;">
                        <label for="imageInput">
                        <img src="/images/placeholder.jpeg" id="output" alt="Image Placeholder" width="200" height="200" style="cursor: pointer;" />
                        </label>
                        <div class="header-section">
                            <h1 contenteditable="true" id="Name">FirstName LastName</h1>
                            <h3 contenteditable="true" id="jobTitle">My Job title/role (DevOps Engineer etc...)</h3>
                        </div>
                        <img style="margin-bottom: 3%;" src="/images/CV_LOGO_P1.png" alt="Logo"><br>
                        <div class="section">
                            <div class="section-content">
                                <p contenteditable="true" id="Summary">summery text here....</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="page">
                    <div class="section page-2">
                        <div class="section-title">EXPERIENCE</div>
                        <div class="section-content">
                            ${experiences.map(experience => `
                                <table class="experience-table">
                                    <tr>
                                        <td>Customer:</td>
                                        <td>${experience.company}</td>
                                    </tr>
                                    <tr>
                                        <td>Role:</td>
                                        <td>${experience.title}</td>
                                    </tr>
                                    <tr>
                                        <td>Period:</td>
                                        <td>${experience.start_date} - ${experience.end_date}</td>
                                    </tr>
                                    <tr>
                                        <td>Tech and Methodology:</td>
                                        <td>DevOps, Agile, Scrum, SAFE, ITIL...</td>
                                    </tr>
                                    <tr>
                                        <td>Description:</td>
                                        <td>${experience.description}</td>
                                    </tr>
                                    <tr>
                                        <td colspan="2">
                                            <span class="remove-item" data-id="${experience.id}" data-type="experience">&times;</span>
                                        </td>
                                    </tr>
                                </table>
                            `).join('')}
                        </div>
                    </div>
                    <img style="margin-left: 35%; margin-top: 5%;" src="/images/CV_LOGO_FOOTER.jpg" alt="Footer Logo" width="200" height="40">
                </div>
                <div class="page">
                    <div class="section">
                        <div class="section-title">Education & Knowledge</div>
                        <div class="section-content page-3">
                            <h2 contenteditable="true" id="jobTitle2">My Job title/role (DevOps Engineer etc...)</h2>
                            <p contenteditable="true" id="jobTitle2Desc">Short description of the role and how I apply it</p>
                            <h2>Education & Certificates:</h2>
                            <ul>
                            ${educations.map(education => `
                                <li>
                                    <h3>${education.title} at ${education.institute} - (${education.start_date} - ${education.end_date}) in ${education.location}</h3>
                                    <span class="remove-item" data-id="${education.id}" data-type="experience">&times;</span>
                                </li>
                            `).join('')}
                            </ul>
                            <h2>Projects:</h2>
                            <ul>
                            ${projects.map(project => `
                                <li>
                                    <h3>${project.title} - ${project.description} - (${project.start_date} - ${project.end_date})</h3>
                                    <span class="remove-item" data-id="${project.id}" data-type="project">&times;</span>
                                </li>
                            `).join('')}
                            </ul>
                            <h2>Competencies</h2>
                            <ul>
                            ${competencies.map(competency => `
                                <li>
                                    <h3>${competency.proficiency_level} ${competency.name} - ${competency.description}</h3>
                                    <span class="remove-item" data-id="${competency.id}" data-type="competency">&times;</span>
                                </li>
                            `).join('')}
                            </ul>
                        </div>
                    </div>
                    <img style="margin-left: 35%; margin-top: 5%;" src="/images/CV_LOGO_FOOTER.jpg" alt="Footer Logo" width="200" height="40">
                </div>
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
        if (event.target.closest('.experience-table')) {
            // If the item is within an experience table (cypoint template), remove the entire table
            event.target.closest('.experience-table').remove();
        } else {
            // For other templates, remove the parent list item
            event.target.parentNode.remove();
        }

        // Update the resume data based on the removed item
        if (itemType === 'competency') {
            // Remove the competency from the competencies array
            competencies = competencies.filter(competency => competency.id !== itemId);
        } else if (itemType === 'experience') {
            // Remove the experience from the experiences array
            experiences = experiences.filter(experience => experience.id !== itemId);
        } else if (itemType === 'education') {
            // Remove the experience from the experiences array
            educations = educations.filter(education => education.id !== itemId);
        } else if (itemType === 'project') {
            // Remove the project from the projects array
            projects = projects.filter(project => project.id !== itemId);
        }
    }
}



// Function to save the resume to the database
async function saveResume() {
    const resumeName = document.getElementById('resume-title').value;
    const resumeDescription = document.getElementById('resume-description').value;

    // Preparing section data
    const sections = [
        ...experiences.map((exp, index) => ({
            section_type: 'experience',
            section_id: exp.id,  // Assuming `id` is provided in the experience objects
            order: index + 1
        })),
        ...educations.map((edu, index) => ({
            section_type: 'education',
            section_id: edu.id,  // Assuming `id` is provided in the education objects
            order: index + 1 + experiences.length  // Continue ordering after experiences
        })),
        ...projects.map((proj, index) => ({
            section_type: 'project',
            section_id: proj.id,  // Assuming `id` is provided in the project objects
            order: index + 1 + experiences.length + educations.length  // Continue ordering after experiences and educations
        }))
    ];

    const resumeData = {
        name: resumeName,
        description: resumeDescription,
        sections: sections
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
            const result = await response.json();
            console.log('Resume saved successfully', result);
            alert('Resume saved successfully!');
        } else {
            console.error('Failed to save resume', response);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}


// Function to populate the dropdown with existing resumes
async function populateResumeDropdown() {
    const dropdown = document.getElementById('existing-resumes');
    try {
        const response = await fetch('http://localhost:8000/resumes/');
        const resumes = await response.json();

        // Clear the dropdown
        dropdown.innerHTML = '';
        // Populate the dropdown with resumes
        resumes.forEach(resume => {
            const option = document.createElement('option');
            option.value = resume.id;
            option.textContent = resume.name;
            dropdown.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching resumes:', error);
    }
}


async function loadSectionDetails(sectionType, sectionId) {
    const response = await fetch(`http://localhost:8000/${sectionType}s/${sectionId}`);
    if (response.ok) {
        return response.json();
    } else {
        throw new Error(`Failed to fetch details for ${sectionType} with ID ${sectionId}`);
    }
}

async function loadResumeIntoPreview(resumeId) {
    try {
        const response = await fetch(`http://localhost:8000/resumes/${resumeId}`);
        if (!response.ok) throw new Error('Failed to fetch resume data');
        const resume = await response.json();

        // Reset the arrays
        competencies = [];
        experiences = [];
        educations = [];
        projects = [];

        // Load details for each section
        for (const section of resume.sections) {
            const details = await loadSectionDetails(section.section_type, section.section_id);

            if (section.section_type === 'competency') {
                competencies.push(details);
            } else if (section.section_type === 'experience') {
                experiences.push(details);
            } else if (section.section_type === 'education') {
                educations.push(details);
            } else if (section.section_type === 'project') {
                projects.push(details);
            }
        }
        console.log(competencies, experiences, educations, projects);
        document.getElementById('resume-title').value = resume.name;
        document.getElementById('resume-description').value = resume.description;

        // Generate the resume preview
        const resumePreviewHTML = generateResumePreview(competencies, experiences, educations, projects);
        document.getElementById('resume-preview').innerHTML = resumePreviewHTML;
    } catch (error) {
        console.error('Error loading resume into preview:', error);
    }
}



// Event listener for when a resume is selected from the dropdown
document.getElementById('existing-resumes').addEventListener('change', function() {
    console.log("Selected resume:", this.value);
    const resumeId = this.value;
    loadResumeIntoPreview(resumeId);
});

// Call this function when the modal is opened to populate the dropdown
populateResumeDropdown();

// Add event listeners
document.getElementById('template').addEventListener('change', loadResumePreview);
document.getElementById('resume-preview').addEventListener('click', removeItemFromPreview);
document.getElementById('save-resume').addEventListener('click', saveResume);

// Load the resume preview when the modal is opened
openModalBtn.addEventListener('click', loadResumePreview);