const dynamicText = document.querySelector("h1 span");
const words = ["Love", "like Art", "the Future", "Everything"];

// Variables to track the position and deletion status of the word
let wordIndex = 0;
let charIndex = 0;
let isDeleting = false;

const typeEffect = () => {
    const currentWord = words[wordIndex];
    const currentChar = currentWord.substring(0, charIndex);
    dynamicText.textContent = currentChar;
    dynamicText.classList.add("stop-blinking");

    if (!isDeleting && charIndex < currentWord.length) {
        // If condition is true, type the next character
        charIndex++;
        setTimeout(typeEffect, 200);
    } else if (isDeleting && charIndex > 0) {
        // If condition is true, remove the previous character
        charIndex--;
        setTimeout(typeEffect, 100);
    } else {
        // If word is deleted then switch to the next word
        isDeleting = !isDeleting;
        dynamicText.classList.remove("stop-blinking");
        wordIndex = !isDeleting ? (wordIndex + 1) % words.length : wordIndex;
        setTimeout(typeEffect, 1200);
    }
}

typeEffect();


const courseData = [
    { id: 1, title: 'Introduction to Programming' },
    { id: 2, title: 'Web Development Fundamentals' },
    { id: 3, title: 'Data Science Essentials' },
    { id: 4, title: 'Machines' },
    // Add more course data as needed
];

const searchInput = document.getElementById('searchInput');
const courseList = document.getElementById('courseList');

searchInput.addEventListener('input', updateCourseList);

function updateCourseList() {
    const searchTerm = searchInput.value.toLowerCase();
    const filteredCourses = courseData.filter(course => course.title.toLowerCase().includes(searchTerm));

    // Clear the course list
    courseList.innerHTML = '';

    if (filteredCourses.length === 0) {
        courseList.innerHTML = '<p>No results found</p>';
    } else {
        filteredCourses.forEach(course => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<a href="course.html?id=${course.id}">${course.title}</a>`;
            courseList.appendChild(listItem);
        });
    }
}