// Function to load and display the dashboard data
async function loadDashboardData() {
    try {
        // Make API calls to fetch competencies, experiences, and projects
        const competenciesResponse = await fetch('http://localhost:8000/competencies');
        const experiencesResponse = await fetch('http://localhost:8000/experiences');
        const educationResponse = await fetch('http://localhost:8000/educations');
        const projectsResponse = await fetch('http://localhost:8000/projects');

        if (competenciesResponse.ok && experiencesResponse.ok && projectsResponse.ok && educationResponse.ok) {
            const competencies = await competenciesResponse.json();
            const experiences = await experiencesResponse.json();
            const educations = await educationResponse.json();
            const projects = await projectsResponse.json();

            // Update the respective lists in the dashboard
            updateList('competencies-list', competencies);
            updateList('experiences-list', experiences);
            updateList('education-list', educations);
            updateList('projects-list', projects);
        } else {
            console.error('Failed to load dashboard data');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to update a list in the dashboard
function updateList(listId, items) {
    const list = document.getElementById(listId);
    
    items.forEach(item => {
        const listItem = document.createElement('li');
        
        // Set the appropriate text content based on the item type
        if (item.name) {
            listItem.textContent = item.name;
        } else if (item.title) {
            listItem.textContent = item.title;
        }
        
        list.appendChild(listItem);
    });
}

// Function to create a new competency
async function createCompetency(competencyData) {
    try {
        const response = await fetch('http://localhost:8000/competencies/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(competencyData)
        });

        if (response.ok) {
            const newCompetency = await response.json();
            // Append the new competency to the existing list
            const competenciesList = document.getElementById('competencies-list');
            const listItem = document.createElement('li');
            listItem.textContent = newCompetency.name;
            competenciesList.appendChild(listItem);
        } else {
            console.error('Failed to create competency');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to create a new experience
async function createExperience(experienceData) {
    try {
        const response = await fetch('http://localhost:8000/experiences/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(experienceData)
        });

        if (response.ok) {
            const newExperience = await response.json();
            // Append the new experience to the existing list
            const experiencesList = document.getElementById('experiences-list');
            const listItem = document.createElement('li');
            listItem.textContent = newExperience.title;
            experiencesList.appendChild(listItem);
        } else {
            console.error('Failed to create experience');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to create a new experience
async function createEducation(educationData) {
    try {
        const response = await fetch('http://localhost:8000/educations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(educationData)
        });

        if (response.ok) {
            const newEducation = await response.json();
            // Append the new experience to the existing list
            const educationsList = document.getElementById('education-list');
            const listItem = document.createElement('li');
            listItem.textContent = newEducation.title;
            educationsList.appendChild(listItem);
        } else {
            console.error('Failed to create experience');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to create a new project
async function createProject(projectData) {
    try {
        const response = await fetch('http://localhost:8000/projects/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(projectData)
        });

        if (response.ok) {
            const newProject = await response.json();
            // Append the new project to the existing list
            const projectsList = document.getElementById('projects-list');
            const listItem = document.createElement('li');
            listItem.textContent = newProject.title;
            projectsList.appendChild(listItem);
        } else {
            console.error('Failed to create project');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Add event listeners to the "Add" buttons
document.getElementById('add-competency').addEventListener('click', () => {
    document.getElementById('competency-form').style.display = 'block';
});

document.getElementById('submit-competency').addEventListener('click', () => {
    const competencyName = document.getElementById('competency-name').value;
    const competencyDescription = document.getElementById('competency-description').value;
    const competencyProficiencyLevel = document.getElementById('competency-proficiency-level').value;

    const competencyData = {
        name: competencyName,
        description: competencyDescription,
        proficiency_level: competencyProficiencyLevel
    };

    createCompetency(competencyData);
    document.getElementById('competency-form').style.display = 'none';
});

document.getElementById('add-experience').addEventListener('click', () => {
    document.getElementById('experience-form').style.display = 'block';
});

document.getElementById('submit-experience').addEventListener('click', () => {
    const experienceTitle = document.getElementById('experience-title').value;
    const experienceCompany = document.getElementById('experience-company').value;
    const experienceLocation = document.getElementById('experience-location').value;
    const experienceStartDate = document.getElementById('experience-start-date').value;
    const experienceEndDate = document.getElementById('experience-end-date').value;
    const experienceDescription = document.getElementById('experience-description').value;

    const experienceData = {
        title: experienceTitle,
        company: experienceCompany,
        location: experienceLocation,
        start_date: experienceStartDate,
        end_date: experienceEndDate,
        description: experienceDescription
    };

    createExperience(experienceData);
    document.getElementById('experience-form').style.display = 'none';
});

document.getElementById('add-education').addEventListener('click', () => {
    document.getElementById('education-form').style.display = 'block';
});

document.getElementById('submit-education').addEventListener('click', () => {
    const educationTitle = document.getElementById('education-title').value;
    const educationInstitute = document.getElementById('education-institute').value;
    const educationLocation = document.getElementById('education-location').value;
    const educationStartDate = document.getElementById('education-start-date').value;
    const educationEndDate = document.getElementById('education-end-date').value;
    const educationDescription = document.getElementById('education-description').value;

    const educationData = {
        title: educationTitle,
        institute: educationInstitute,
        location: educationLocation,
        start_date: educationStartDate,
        end_date: educationEndDate,
        description: educationDescription
    };

    createEducation(educationData);
    document.getElementById('education-form').style.display = 'none';
});

document.getElementById('add-project').addEventListener('click', () => {
    document.getElementById('project-form').style.display = 'block';
});

document.getElementById('submit-project').addEventListener('click', () => {
    const projectTitle = document.getElementById('project-title').value;
    const projectDescription = document.getElementById('project-description').value;
    const projectStartDate = document.getElementById('project-start-date').value;
    const projectEndDate = document.getElementById('project-end-date').value;
    const projectURL = document.getElementById('project-url').value;

    const projectData = {
        title: projectTitle,
        description: projectDescription,
        start_date: projectStartDate,
        end_date: projectEndDate,
        url: projectURL
    };

    createProject(projectData);
    document.getElementById('project-form').style.display = 'none';
});

// Load the dashboard data when the page loads
loadDashboardData();