document.addEventListener("DOMContentLoaded", function() {

  // ══════════════════════════════════════════
  //  TOGGLE SECTION
  // ══════════════════════════════════════════
  window.toggleSection = function(name) {
    var form = document.getElementById("form-" + name);
    var view = document.getElementById("view-" + name);
    if (!form) return;
    var isOpen = form.style.display !== "none";
    form.style.display = isOpen ? "none" : "block";
    if (view) view.style.display = isOpen ? "" : "none";
  };

  // ══════════════════════════════════════════
  //  REMOVE BUTTONS
  // ══════════════════════════════════════════
  document.addEventListener("click", function(e) {
    if (e.target.classList.contains("remove")) {
      var parent = e.target.closest(".cvb-entry-block, .cvb-skill-row, .cvb-tag-row");
      if (parent) parent.remove();
    }
  });

  // ══════════════════════════════════════════
  //  ADD SKILL
  // ══════════════════════════════════════════
  window.addSkill = function() {
    var c = document.getElementById("skills-container");
    if (!c) return;
    var div = document.createElement("div");
    div.className = "cvb-skill-row";
    div.innerHTML = '<input name="skills[]" placeholder="e.g. Python">'
      + '<select name="skill_level[]">'
      + '<option value="">Level</option>'
      + '<option value="beginner">Beginner</option>'
      + '<option value="intermediate">Intermediate</option>'
      + '<option value="advanced">Advanced</option>'
      + '<option value="expert">Expert</option>'
      + '</select>'
      + '<button type="button" class="remove cvb-row-remove">x</button>';
    c.appendChild(div);
  };

  window.addSkillConfirm = function() {
    var c = document.getElementById("skills-confirm-container");
    if (!c) return;
    var div = document.createElement("div");
    div.className = "cvb-tag-row";
    div.innerHTML = '<input name="skills[]" placeholder="Add a skill">'
      + '<button type="button" class="remove cvb-tag-remove">x</button>';
    c.appendChild(div);
  };

  // ══════════════════════════════════════════
  //  ADD EDUCATION
  // ══════════════════════════════════════════
  window.addEducation = function() {
    var c = document.getElementById("edu-container");
    if (!c) return;
    var div = document.createElement("div");
    div.className = "cvb-entry-block";
    div.innerHTML = '<button type="button" class="remove cvb-entry-remove">x</button>'
      + '<div class="cvb-grid-2">'
      + '<div class="cvb-field"><label>School</label><input name="edu_school[]" placeholder="University name"></div>'
      + '<div class="cvb-field"><label>Degree</label><input name="edu_degree[]" placeholder="Bachelors"></div>'
      + '<div class="cvb-field"><label>Field of Study</label><input name="edu_field[]" placeholder="Computer Science"></div>'
      + '<div class="cvb-field"></div>'
      + '<div class="cvb-field"><label>Start Year</label><input name="edu_start[]" placeholder="2019"></div>'
      + '<div class="cvb-field"><label>End Year</label><input name="edu_end[]" placeholder="2023"></div>'
      + '</div>'
      + '<div class="cvb-field"><label>Description</label><textarea name="edu_desc[]" rows="2" placeholder="Achievements, GPA..."></textarea></div>';
    c.appendChild(div);
  };

  // ══════════════════════════════════════════
  //  ADD EXPERIENCE
  // ══════════════════════════════════════════
  window.addExperience = function() {
    var c = document.getElementById("exp-container");
    if (!c) return;
    var idx = c.querySelectorAll(".cvb-entry-block").length;
    var div = document.createElement("div");
    div.className = "cvb-entry-block";
    div.innerHTML = '<button type="button" class="remove cvb-entry-remove">x</button>'
      + '<div class="cvb-grid-2">'
      + '<div class="cvb-field"><label>Job Title</label><input name="exp_title[]" placeholder="Software Engineer"></div>'
      + '<div class="cvb-field"><label>Company</label><input name="exp_company[]" placeholder="Acme Corp"></div>'
      + '<div class="cvb-field"><label>Location</label><input name="exp_location[]" placeholder="Addis Ababa"></div>'
      + '<div class="cvb-field"></div>'
      + '<div class="cvb-field"><label>Start Date</label><input name="exp_start[]" placeholder="Jan 2022"></div>'
      + '<div class="cvb-field"><label>End Date</label><input name="exp_end[]" placeholder="Dec 2024"></div>'
      + '</div>'
      + '<label class="cvb-checkbox"><input type="checkbox" name="exp_current[]" value="' + idx + '" onchange="toggleCurrentJob(this)"> I currently work here</label>'
      + '<div class="cvb-field"><label>Description</label><textarea name="exp_desc[]" rows="3" placeholder="Key responsibilities..."></textarea></div>';
    c.appendChild(div);
  };

  // ══════════════════════════════════════════
  //  ADD LANGUAGE
  // ══════════════════════════════════════════
  window.addLanguage = function() {
    var c = document.getElementById("lang-container");
    if (!c) return;
    var opts = '<option value="">-</option><option>A1</option><option>A2</option><option>B1</option><option>B2</option><option>C1</option><option>C2</option><option value="native">Native</option>';
    var div = document.createElement("div");
    div.className = "cvb-entry-block";
    div.innerHTML = '<button type="button" class="remove cvb-entry-remove">x</button>'
      + '<div class="cvb-field" style="margin-bottom:10px"><label>Language</label><input name="lang_name[]" placeholder="English"></div>'
      + '<div class="cvb-lang-grid">'
      + '<div class="cvb-field"><label>Listening</label><select name="lang_listening[]">' + opts + '</select></div>'
      + '<div class="cvb-field"><label>Reading</label><select name="lang_reading[]">' + opts + '</select></div>'
      + '<div class="cvb-field"><label>Writing</label><select name="lang_writing[]">' + opts + '</select></div>'
      + '<div class="cvb-field"><label>Speaking</label><select name="lang_speaking[]">' + opts + '</select></div>'
      + '</div>';
    c.appendChild(div);
  };

  // ══════════════════════════════════════════
  //  ADD PROJECT
  // ══════════════════════════════════════════
  window.addProject = function() {
    var c = document.getElementById("proj-container");
    if (!c) return;
    var div = document.createElement("div");
    div.className = "cvb-entry-block";
    div.innerHTML = '<button type="button" class="remove cvb-entry-remove">x</button>'
      + '<div class="cvb-grid-2">'
      + '<div class="cvb-field"><label>Title</label><input name="proj_title[]" placeholder="My Project"></div>'
      + '<div class="cvb-field"><label>Link</label><input name="proj_link[]" placeholder="https://github.com/..."></div>'
      + '<div class="cvb-field"><label>Start</label><input name="proj_start[]" placeholder="Jan 2023"></div>'
      + '<div class="cvb-field"><label>End</label><input name="proj_end[]" placeholder="Mar 2023"></div>'
      + '</div>'
      + '<div class="cvb-field"><label>Description</label><textarea name="proj_desc[]" rows="2" placeholder="What did you build?"></textarea></div>';
    c.appendChild(div);
  };

  // ══════════════════════════════════════════
  //  ADD CERTIFICATION
  // ══════════════════════════════════════════
  window.addCertification = function() {
    var c = document.getElementById("cert-container");
    if (!c) return;
    var div = document.createElement("div");
    div.className = "cvb-entry-block";
    div.innerHTML = '<button type="button" class="remove cvb-entry-remove">x</button>'
      + '<div class="cvb-grid-2">'
      + '<div class="cvb-field"><label>Name</label><input name="cert_name[]" placeholder="AWS Solutions Architect"></div>'
      + '<div class="cvb-field"><label>Organization</label><input name="cert_org[]" placeholder="Amazon"></div>'
      + '<div class="cvb-field"><label>Year</label><input name="cert_year[]" placeholder="2024"></div>'
      + '<div class="cvb-field"><label>Link</label><input name="cert_link[]" placeholder="https://..."></div>'
      + '</div>';
    c.appendChild(div);
  };

  // ══════════════════════════════════════════
  //  ADD REFERENCE
  // ══════════════════════════════════════════
  window.addReference = function() {
    var c = document.getElementById("ref-container");
    if (!c) return;
    var div = document.createElement("div");
    div.className = "cvb-entry-block";
    div.innerHTML = '<button type="button" class="remove cvb-entry-remove">x</button>'
      + '<div class="cvb-grid-2">'
      + '<div class="cvb-field"><label>Name</label><input name="ref_name[]" placeholder="Jane Smith"></div>'
      + '<div class="cvb-field"><label>Position</label><input name="ref_position[]" placeholder="Senior Manager"></div>'
      + '<div class="cvb-field"><label>Company</label><input name="ref_company[]" placeholder="Acme Corp"></div>'
      + '<div class="cvb-field"><label>Email</label><input name="ref_email[]" placeholder="jane@acme.com"></div>'
      + '<div class="cvb-field"><label>Phone</label><input name="ref_phone[]" placeholder="+251 91 234 5678"></div>'
      + '</div>';
    c.appendChild(div);
  };

  // ══════════════════════════════════════════
  //  TOGGLE CURRENT JOB
  // ══════════════════════════════════════════
  window.toggleCurrentJob = function(checkbox) {
    var block = checkbox.closest(".cvb-entry-block");
    if (!block) return;
    var endInput = block.querySelector("input[name='exp_end[]']");
    if (endInput) {
      endInput.disabled = checkbox.checked;
      if (checkbox.checked) endInput.value = "";
    }
  };

  // ══════════════════════════════════════════
  //  DRAG AND DROP (Step 1)
  // ══════════════════════════════════════════
  var dropzone = document.getElementById("dropzone");
  var fileInput = document.getElementById("cv_pdf_input");
  var uploadBtn = document.getElementById("upload-btn");
  var dropFname = document.getElementById("drop-fname");

  if (dropzone && fileInput) {
    dropzone.addEventListener("click", function() { fileInput.click(); });

    dropzone.addEventListener("dragover", function(e) {
      e.preventDefault();
      dropzone.classList.add("drag-over");
    });
    dropzone.addEventListener("dragleave", function() {
      dropzone.classList.remove("drag-over");
    });
    dropzone.addEventListener("drop", function(e) {
      e.preventDefault();
      dropzone.classList.remove("drag-over");
      var file = e.dataTransfer.files[0];
      if (file && file.type === "application/pdf") setFile(file);
    });

    fileInput.addEventListener("change", function() {
      if (fileInput.files[0]) setFile(fileInput.files[0]);
    });

    function setFile(file) {
      var dt = new DataTransfer();
      dt.items.add(file);
      fileInput.files = dt.files;
      if (dropFname) dropFname.textContent = "📎 " + file.name;
      if (uploadBtn) uploadBtn.disabled = false;
    }
  }

  // ══════════════════════════════════════════
  //  TOAST
  // ══════════════════════════════════════════
  var toast = document.getElementById("autosave-toast");
  window.showToast = function(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("show");
    clearTimeout(toast._t);
    toast._t = setTimeout(function() { toast.classList.remove("show"); }, 2500);
  };

  // ══════════════════════════════════════════
  //  SAVE SECTION VIA AJAX
  // ══════════════════════════════════════════
  document.addEventListener("click", function(e) {
    var saveBtn = e.target.closest(".cvb-btn-save");
    if (!saveBtn) return;

    e.preventDefault();
    e.stopPropagation();

    var form = document.getElementById("cv-form");
    if (!form) return;

    var formData = new FormData(form);
    var csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;

    showToast("Saving...");

    fetch(window.location.pathname + "?step=2", {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
    .then(function(response) { return response.json(); })
    .then(function(data) {
      if (data.status === "ok") {
        showToast("Saved!");
        var inlineForm = saveBtn.closest(".cvb-inline-form");
        if (inlineForm) {
          var sectionId = inlineForm.id.replace("form-", "");
          toggleSection(sectionId);
        }
      }
    })
    .catch(function() {
      showToast("Save failed. Try again.");
    });
  });

  // ══════════════════════════════════════════
  //  COLOR PICKER (Step 3)
  // ══════════════════════════════════════════
  var colorPicker = document.getElementById("color-picker");
  var colorHex = document.getElementById("color-hex");
  var swatches = document.querySelectorAll(".cvb-swatch");

  if (colorPicker) {
    colorPicker.addEventListener("input", function() {
      if (colorHex) colorHex.textContent = colorPicker.value;
      swatches.forEach(function(s) { s.classList.remove("selected"); });
    });
  }

  swatches.forEach(function(swatch) {
    swatch.addEventListener("click", function() {
      swatches.forEach(function(s) { s.classList.remove("selected"); });
      swatch.classList.add("selected");
      var val = swatch.querySelector("input").value;
      if (colorPicker) colorPicker.value = val;
      if (colorHex) colorHex.textContent = val;
    });
  });

  // ══════════════════════════════════════════
  //  TEMPLATE CARDS (Step 3)
  // ══════════════════════════════════════════
  document.querySelectorAll(".cvb-tpl-card").forEach(function(card) {
    card.addEventListener("click", function() {
      document.querySelectorAll(".cvb-tpl-card").forEach(function(c) {
        c.classList.remove("selected");
      });
      card.classList.add("selected");
    });
  });

  // ══════════════════════════════════════════
  //  FONT OPTIONS (Step 3)
  // ══════════════════════════════════════════
  document.querySelectorAll(".cvb-font-opt").forEach(function(opt) {
    opt.addEventListener("click", function() {
      document.querySelectorAll(".cvb-font-opt").forEach(function(o) {
        o.classList.remove("selected");
      });
      opt.classList.add("selected");
    });
  });

  // Show toast on full form submit
  var cvForm = document.getElementById("cv-form");
  if (cvForm) {
    cvForm.addEventListener("submit", function() { showToast("Saving..."); });
  }

}); // end DOMContentLoaded