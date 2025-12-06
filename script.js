// ===========================
// CONTACT FORM HANDLER
// ===========================
document.getElementById("contactForm").addEventListener("submit", function(e) {
    e.preventDefault(); 

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();
    const formMessage = document.getElementById("formMessage");

    if (name === "" || email === "" || message === "") {
        formMessage.style.color = "red";
        formMessage.textContent = "Please fill out all fields.";
        return;
    }

    // Success message
    formMessage.style.color = "green";
    formMessage.textContent = "Message Sent Successfully!";

    // Clear form
    document.getElementById("contactForm").reset();
});


// ===========================
// SKILL BAR ANIMATION
// ===========================
const skillBars = document.querySelectorAll(".skill-level");

function showSkills() {
    const trigger = window.innerHeight;

    skillBars.forEach(bar => {
        const top = bar.getBoundingClientRect().top;
        if (top < trigger) {
            bar.style.animation = "fillSkill 2s forwards";
        }
    });
}

window.addEventListener("scroll", showSkills);


// ===========================
// FADE-IN + SLIDE-IN ANIMATION
// ===========================
const sections = document.querySelectorAll("section");

function revealSections() {
    const revealPoint = window.innerHeight - 100;

    sections.forEach(sec => {
        let secTop = sec.getBoundingClientRect().top;

        if (secTop < revealPoint) {
            sec.classList.add("show-section");
        }
    });
}

window.addEventListener("scroll", revealSections);
revealSections();


// ===========================
// ACTIVE NAVBAR HIGHLIGHT
// ===========================
const navLinks = document.querySelectorAll("nav ul li a");

window.addEventListener("scroll", () => {
    let current = "";

    sections.forEach(section => {
        let sectionTop = section.offsetTop - 200;
        if (pageYOffset >= sectionTop) {
            current = section.getAttribute("id");
        }
    });

    navLinks.forEach(link => {
        link.classList.remove("active-link");
        if (link.getAttribute("href").includes(current)) {
            link.classList.add("active-link");
        }
    });
});


// ===========================
// DARK MODE TOGGLE
// ===========================
const toggleBtn = document.createElement("button");
toggleBtn.textContent = "🌙 Dark Mode";
toggleBtn.classList.add("dark-toggle");
document.body.appendChild(toggleBtn);

toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark");

    if (document.body.classList.contains("dark")) {
        toggleBtn.textContent = "☀️ Light Mode";
    } else {
        toggleBtn.textContent = "🌙 Dark Mode";
    }
});
