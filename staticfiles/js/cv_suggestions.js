// ================================================================
//  CV BUILDER SUGGESTIONS
//  Autocomplete for skills, nationality, location, degree, etc.
// ================================================================

const CV_SUGGESTIONS = {

  skills: [
    // IT & Software
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "PHP", "Ruby", "Swift", "Kotlin",
    "React", "Vue.js", "Angular", "Node.js", "Django", "Flask", "FastAPI", "Spring Boot", "Laravel",
    "HTML", "CSS", "Tailwind CSS", "Bootstrap", "REST API", "GraphQL", "Docker", "Kubernetes",
    "Git", "GitHub", "Linux", "AWS", "Azure", "Google Cloud", "PostgreSQL", "MySQL", "MongoDB",
    "Redis", "Firebase", "Machine Learning", "Data Analysis", "TensorFlow", "NumPy", "Pandas",
    "Cybersecurity", "Network Administration", "DevOps", "CI/CD", "Agile", "Scrum",
    // Business & Finance
    "Accounting", "Bookkeeping", "Financial Analysis", "Budgeting", "Auditing", "Tax Preparation",
    "KYC", "eKYC", "AML", "Compliance", "Risk Management", "Customer Service", "CSR",
    "Sales", "Marketing", "Digital Marketing", "SEO", "Social Media Marketing", "Content Creation",
    "Project Management", "Business Analysis", "Data Entry", "Microsoft Excel", "Microsoft Word",
    "Microsoft PowerPoint", "Google Sheets", "Google Slides", "QuickBooks", "SAP",
    "Supply Chain Management", "Logistics", "Procurement", "Inventory Management",
    // Healthcare
    "Nursing", "Patient Care", "Medical Records", "Clinical Research", "Pharmacology",
    "Public Health", "First Aid", "Laboratory Techniques", "Health Education",
    // Engineering
    "AutoCAD", "SolidWorks", "Civil Engineering", "Structural Analysis", "Electrical Engineering",
    "Mechanical Engineering", "Quality Control", "Project Planning", "Construction Management",
    // Education
    "Teaching", "Curriculum Development", "Lesson Planning", "Classroom Management",
    "E-Learning", "Training & Development", "Coaching", "Mentoring",
    // Soft Skills
    "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking",
    "Time Management", "Adaptability", "Creativity", "Attention to Detail", "Negotiation",
    "Conflict Resolution", "Decision Making", "Emotional Intelligence", "Public Speaking",
  ],

  nationalities: [
    "Afghan", "Albanian", "Algerian", "American", "Andorran", "Angolan", "Antiguans",
    "Argentinean", "Armenian", "Australian", "Austrian", "Azerbaijani", "Bahamian",
    "Bahraini", "Bangladeshi", "Barbadian", "Belarusian", "Belgian", "Belizean",
    "Beninese", "Bhutanese", "Bolivian", "Bosnian", "Brazilian", "British", "Bruneian",
    "Bulgarian", "Burkinabe", "Burmese", "Burundian", "Cambodian", "Cameroonian",
    "Canadian", "Central African", "Chadian", "Chilean", "Chinese", "Colombian",
    "Comoran", "Congolese", "Costa Rican", "Croatian", "Cuban", "Cypriot", "Czech",
    "Danish", "Djiboutian", "Dominican", "Dutch", "Ecuadorean", "Egyptian",
    "Eritrean", "Estonian", "Ethiopian", "Fijian", "Filipino", "Finnish", "French",
    "Gabonese", "Gambian", "Georgian", "German", "Ghanaian", "Greek", "Grenadian",
    "Guatemalan", "Guinean", "Guyanese", "Haitian", "Honduran", "Hungarian",
    "I-Kiribati", "Indian", "Indonesian", "Iranian", "Iraqi", "Irish", "Israeli",
    "Italian", "Ivorian", "Jamaican", "Japanese", "Jordanian", "Kazakhstani",
    "Kenyan", "Korean", "Kuwaiti", "Kyrgyz", "Laotian", "Latvian", "Lebanese",
    "Liberian", "Libyan", "Liechtensteiner", "Lithuanian", "Luxembourger",
    "Macedonian", "Malagasy", "Malawian", "Malaysian", "Maldivian", "Malian",
    "Maltese", "Mauritanian", "Mauritian", "Mexican", "Moldovan", "Monacan",
    "Mongolian", "Montenegrin", "Moroccan", "Mozambican", "Namibian", "Nepalese",
    "New Zealander", "Nicaraguan", "Nigerian", "Norwegian", "Omani", "Pakistani",
    "Palauan", "Palestinian", "Panamanian", "Papua New Guinean", "Paraguayan",
    "Peruvian", "Polish", "Portuguese", "Qatari", "Romanian", "Russian", "Rwandan",
    "Saint Lucian", "Salvadoran", "Saudi", "Senegalese", "Serbian", "Sierra Leonean",
    "Singaporean", "Slovak", "Slovenian", "Somali", "South African", "South Sudanese",
    "Spanish", "Sri Lankan", "Sudanese", "Surinamese", "Swazi", "Swedish", "Swiss",
    "Syrian", "Taiwanese", "Tajik", "Tanzanian", "Thai", "Togolese", "Tongan",
    "Trinidadian", "Tunisian", "Turkish", "Turkmen", "Tuvaluan", "Ugandan",
    "Ukrainian", "Emirati", "Uruguayan", "Uzbekistani", "Venezuelan", "Vietnamese",
    "Yemeni", "Zambian", "Zimbabwean",
  ],

  locations: [
    // Ethiopia
    "Addis Ababa, Ethiopia", "Dire Dawa, Ethiopia", "Hawassa, Ethiopia",
    "Mekelle, Ethiopia", "Bahir Dar, Ethiopia", "Gondar, Ethiopia",
    "Jimma, Ethiopia", "Adama, Ethiopia", "Harar, Ethiopia", "Dessie, Ethiopia",
    "Shashamane, Ethiopia", "Bishoftu, Ethiopia", "Arba Minch, Ethiopia",
    // Africa
    "Nairobi, Kenya", "Lagos, Nigeria", "Cairo, Egypt", "Johannesburg, South Africa",
    "Cape Town, South Africa", "Accra, Ghana", "Kampala, Uganda", "Dar es Salaam, Tanzania",
    "Khartoum, Sudan", "Abuja, Nigeria", "Casablanca, Morocco", "Tunis, Tunisia",
    "Kinshasa, DRC", "Dakar, Senegal", "Abidjan, Ivory Coast", "Lusaka, Zambia",
    "Harare, Zimbabwe", "Kigali, Rwanda", "Maputo, Mozambique", "Bamako, Mali",
    // International
    "London, UK", "Paris, France", "Berlin, Germany", "Dubai, UAE", "Riyadh, Saudi Arabia",
    "New York, USA", "Los Angeles, USA", "Toronto, Canada", "Sydney, Australia",
    "Beijing, China", "Tokyo, Japan", "Mumbai, India", "Singapore", "Istanbul, Turkey",
    "Moscow, Russia", "Amsterdam, Netherlands", "Stockholm, Sweden", "Zurich, Switzerland",
  ],

  degrees: [
    "Bachelor of Arts (BA)", "Bachelor of Science (BSc)", "Bachelor of Engineering (BEng)",
    "Bachelor of Commerce (BCom)", "Bachelor of Education (BEd)", "Bachelor of Laws (LLB)",
    "Bachelor of Medicine (MBBS)", "Bachelor of Technology (BTech)",
    "Master of Arts (MA)", "Master of Science (MSc)", "Master of Business Administration (MBA)",
    "Master of Engineering (MEng)", "Master of Education (MEd)", "Master of Laws (LLM)",
    "Master of Public Health (MPH)", "Master of Finance (MFin)",
    "Doctor of Philosophy (PhD)", "Doctor of Medicine (MD)", "Doctor of Education (EdD)",
    "Associate Degree", "Higher National Diploma (HND)", "Diploma", "Certificate",
    "Professional Certificate", "Advanced Diploma",
  ],

  fields: [
    "Computer Science", "Information Technology", "Software Engineering", "Data Science",
    "Artificial Intelligence", "Cybersecurity", "Network Engineering", "Information Systems",
    "Economics", "Business Administration", "Accounting", "Finance", "Marketing",
    "Human Resource Management", "Management", "International Business", "Supply Chain",
    "Civil Engineering", "Mechanical Engineering", "Electrical Engineering",
    "Architecture", "Environmental Science", "Agriculture",
    "Medicine", "Nursing", "Public Health", "Pharmacy", "Dentistry",
    "Law", "Political Science", "Sociology", "Psychology", "Philosophy",
    "Education", "English Literature", "Journalism", "Communication",
    "Mathematics", "Statistics", "Physics", "Chemistry", "Biology",
  ],

  jobTitles: [
    "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Data Scientist", "Data Analyst", "Machine Learning Engineer", "DevOps Engineer",
    "Product Manager", "Project Manager", "Business Analyst", "Systems Analyst",
    "Customer Service Officer", "Call Center Agent", "Sales Representative",
    "Marketing Manager", "Digital Marketing Specialist", "Content Creator",
    "Accountant", "Financial Analyst", "Auditor", "Tax Consultant",
    "HR Manager", "HR Officer", "Recruitment Specialist",
    "Teacher", "Lecturer", "Trainer", "Education Coordinator",
    "Nurse", "Clinical Officer", "Pharmacist", "Lab Technician",
    "Civil Engineer", "Mechanical Engineer", "Electrical Engineer",
    "Graphic Designer", "UI/UX Designer", "Motion Graphics Designer",
    "Logistics Officer", "Supply Chain Manager", "Procurement Officer",
    "Operations Manager", "General Manager", "CEO", "COO", "CTO",
    "Network Administrator", "System Administrator", "IT Support Specialist",
    "Legal Officer", "Compliance Officer", "Risk Analyst", "KYC Officer",
  ],

  companies: [
    "Ethio Telecom", "Commercial Bank of Ethiopia", "Ethiopian Airlines",
    "Safaricom Ethiopia", "Ison BPO", "Nano Technologies", "ALX Africa",
    "Dashen Bank", "Awash Bank", "Bank of Abyssinia", "Zemen Bank",
    "Ethiopian Electric Power", "Ethiopian Railways", "Ethio Post",
    "Google", "Microsoft", "Amazon", "Meta", "Apple", "IBM", "Oracle",
    "Deloitte", "PwC", "KPMG", "Ernst & Young",
    "United Nations", "UNICEF", "World Bank", "IMF", "African Union",
    "USAID", "Save the Children", "Plan International", "Oxfam",
  ],

  certifications: [
    "AWS Certified Solutions Architect", "AWS Certified Developer",
    "Google Cloud Professional", "Microsoft Azure Fundamentals",
    "Certified Information Systems Security Professional (CISSP)",
    "CompTIA Security+", "CompTIA Network+", "CompTIA A+",
    "Project Management Professional (PMP)", "Certified Scrum Master (CSM)",
    "Certified Public Accountant (CPA)", "ACCA", "CFA",
    "Google Analytics Certification", "HubSpot Marketing Certification",
    "Cisco CCNA", "Cisco CCNP",
    "ALX Africa Software Engineering", "ALX Africa Data Science",
    "Coursera Machine Learning", "edX Data Science",
    "Professional Certificate in Python", "Oracle Java Certification",
    "Certified KYC Specialist", "AML Compliance Certification",
    "First Aid Certificate", "Basic Life Support (BLS)",
  ],
};

// ================================================================
//  AUTOCOMPLETE ENGINE
// ================================================================

function createAutocomplete(input, suggestions, multiTag) {
  var wrapper = document.createElement("div");
  wrapper.className = "cvb-autocomplete-wrapper";
  input.parentNode.insertBefore(wrapper, input);
  wrapper.appendChild(input);

  var dropdown = document.createElement("div");
  dropdown.className = "cvb-autocomplete-dropdown";
  wrapper.appendChild(dropdown);

  if (multiTag) {
    var tagContainer = document.createElement("div");
    tagContainer.className = "cvb-tag-container";
    wrapper.insertBefore(tagContainer, input);
  }

  function showSuggestions(val) {
    dropdown.innerHTML = "";
    if (!val || val.length < 1) { dropdown.style.display = "none"; return; }
    var matches = suggestions.filter(function(s) {
      return s.toLowerCase().indexOf(val.toLowerCase()) !== -1;
    }).slice(0, 8);
    if (matches.length === 0) { dropdown.style.display = "none"; return; }
    matches.forEach(function(match) {
      var item = document.createElement("div");
      item.className = "cvb-autocomplete-item";
      item.textContent = match;
      item.addEventListener("mousedown", function(e) {
        e.preventDefault();
        if (multiTag) {
          input.value = "";
          addTag(match, tagContainer, input);
        } else {
          input.value = match;
        }
        dropdown.style.display = "none";
      });
      dropdown.appendChild(item);
    });
    dropdown.style.display = "block";
  }

  input.addEventListener("input", function() {
    showSuggestions(input.value);
  });

  input.addEventListener("focus", function() {
    if (input.value) showSuggestions(input.value);
  });

  input.addEventListener("blur", function() {
    setTimeout(function() { dropdown.style.display = "none"; }, 150);
  });

  input.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && multiTag && input.value.trim()) {
      e.preventDefault();
      addTag(input.value.trim(), tagContainer, input);
      input.value = "";
      dropdown.style.display = "none";
    }
  });
}

function addTag(text, container, input) {
  var tag = document.createElement("span");
  tag.className = "cvb-suggestion-tag";
  tag.textContent = text;
  var remove = document.createElement("button");
  remove.type = "button";
  remove.textContent = "x";
  remove.className = "cvb-suggestion-tag-remove";
  remove.addEventListener("click", function() {
    container.removeChild(tag);
    syncTagsToInput(container, input);
  });
  tag.appendChild(remove);
  container.appendChild(tag);
  syncTagsToInput(container, input);
}

function syncTagsToInput(container, input) {
  var tags = Array.from(container.querySelectorAll(".cvb-suggestion-tag")).map(function(t) {
    return t.textContent.replace("x", "").trim();
  });
  input.value = tags.join(", ");
}

// ================================================================
//  INIT AUTOCOMPLETE ON FIELDS
// ================================================================

function initSuggestions() {
  // Skills
  document.querySelectorAll("input[name='skills[]']").forEach(function(input) {
    createAutocomplete(input, CV_SUGGESTIONS.skills, false);
  });

  // Nationality
  document.querySelectorAll("input[name='nationality']").forEach(function(input) {
    createAutocomplete(input, CV_SUGGESTIONS.nationalities, false);
  });

  // Address / Location
  document.querySelectorAll("input[name='address'], input[name='exp_location[]']").forEach(function(input) {
    createAutocomplete(input, CV_SUGGESTIONS.locations, false);
  });

  // Degree
  document.querySelectorAll("input[name='edu_degree[]']").forEach(function(input) {
    createAutocomplete(input, CV_SUGGESTIONS.degrees, false);
  });

  // Field of Study
  document.querySelectorAll("input[name='edu_field[]']").forEach(function(input) {
    createAutocomplete(input, CV_SUGGESTIONS.fields, false);
  });

  // Job Title
  document.querySelectorAll("input[name='exp_title[]']").forEach(function(input) {
    createAutocomplete(input, CV_SUGGESTIONS.jobTitles, false);
  });

  // Company
  document.querySelectorAll("input[name='exp_company[]']").forEach(function(input) {
    createAutocomplete(input, CV_SUGGESTIONS.companies, false);
  });

  // Certifications
  document.querySelectorAll("input[name='cert_name[]']").forEach(function(input) {
    createAutocomplete(input, CV_SUGGESTIONS.certifications, false);
  });
}

// Re-init when new entries are added
var originalAddSkill = window.addSkill;
window.addSkill = function() {
  if (originalAddSkill) originalAddSkill();
  setTimeout(initSuggestions, 100);
};

var originalAddEducation = window.addEducation;
window.addEducation = function() {
  if (originalAddEducation) originalAddEducation();
  setTimeout(initSuggestions, 100);
};

var originalAddExperience = window.addExperience;
window.addExperience = function() {
  if (originalAddExperience) originalAddExperience();
  setTimeout(initSuggestions, 100);
};

var originalAddCertification = window.addCertification;
window.addCertification = function() {
  if (originalAddCertification) originalAddCertification();
  setTimeout(initSuggestions, 100);
};

document.addEventListener("DOMContentLoaded", function() {
  initSuggestions();
});