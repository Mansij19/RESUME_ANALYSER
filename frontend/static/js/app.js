/**
 * Resume Analyzer - Client-Side JavaScript
 * ==========================================
 * Handles: tab switching, drag-and-drop uploads, form submission,
 * loading states, animated counters, and progress rings.
 */

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initDropzone();
    initCharCount();
    initJdToggle();
    initFormSubmit();
    initAnimations();
    initScoreAnimations();
});

/* ========== Tab Switching ========== */
function initTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    if (!tabs.length) return;

    tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.dataset.tab;
            // Update active tab button
            document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
            btn.classList.add('active');
            // Update visible tab content
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.getElementById(`tab-${target}`).classList.add('active');
            // Update hidden input method
            const methodInput = document.getElementById('input-method');
            if (methodInput) methodInput.value = target;
        });
    });
}

/* ========== Drag & Drop File Upload ========== */
function initDropzone() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('resume-file');
    if (!dropzone || !fileInput) return;

    // Click to browse
    dropzone.addEventListener('click', (e) => {
        if (e.target.id === 'file-remove') return;
        fileInput.click();
    });

    // Drag events
    ['dragenter', 'dragover'].forEach(evt => {
        dropzone.addEventListener(evt, (e) => {
            e.preventDefault();
            dropzone.classList.add('dragover');
        });
    });
    ['dragleave', 'drop'].forEach(evt => {
        dropzone.addEventListener(evt, (e) => {
            e.preventDefault();
            dropzone.classList.remove('dragover');
        });
    });

    // Drop handler
    dropzone.addEventListener('drop', (e) => {
        const file = e.dataTransfer.files[0];
        if (file) {
            fileInput.files = e.dataTransfer.files;
            showFileInfo(file.name);
        }
    });

    // File input change
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            showFileInfo(fileInput.files[0].name);
        }
    });

    // Remove file
    const removeBtn = document.getElementById('file-remove');
    if (removeBtn) {
        removeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            fileInput.value = '';
            document.getElementById('file-info').style.display = 'none';
            dropzone.querySelector('.dropzone-icon').style.display = '';
            dropzone.querySelector('.dropzone-text').style.display = '';
            dropzone.querySelector('.dropzone-hint').style.display = '';
        });
    }
}

function showFileInfo(name) {
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const dropzone = document.getElementById('dropzone');
    if (!fileInfo || !fileName) return;

    fileName.textContent = name;
    fileInfo.style.display = 'flex';
    dropzone.querySelector('.dropzone-icon').style.display = 'none';
    dropzone.querySelector('.dropzone-text').style.display = 'none';
    dropzone.querySelector('.dropzone-hint').style.display = 'none';
}

/* ========== Character Count ========== */
function initCharCount() {
    const textarea = document.getElementById('resume-text');
    const counter = document.getElementById('char-count');
    if (!textarea || !counter) return;

    textarea.addEventListener('input', () => {
        const len = textarea.value.length;
        counter.textContent = `${len.toLocaleString()} characters`;
    });
}

/* ========== JD Toggle ========== */
function initJdToggle() {
    const toggle = document.getElementById('jd-toggle');
    const body = document.getElementById('jd-body');
    if (!toggle || !body) return;

    toggle.addEventListener('click', () => {
        const isOpen = body.style.display !== 'none';
        body.style.display = isOpen ? 'none' : 'block';
        toggle.classList.toggle('open', !isOpen);
    });
}

/* ========== Form Submission with Loading ========== */
function initFormSubmit() {
    const form = document.getElementById('analyze-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        const btn = document.getElementById('submit-btn');
        const btnText = btn.querySelector('.btn-text');
        const btnLoader = btn.querySelector('.btn-loader');
        if (btnText && btnLoader) {
            btnText.style.display = 'none';
            btnLoader.style.display = 'flex';
            btn.disabled = true;
        }
    });
}

/* ========== Scroll Animations ========== */
function initAnimations() {
    const animatedEls = document.querySelectorAll(
        '.feature-card, .step-card, .dash-card, .suggestion-item, .correction-item'
    );
    if (!animatedEls.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('animate-in');
                }, index * 80);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    animatedEls.forEach(el => observer.observe(el));
}

/* ========== Score Ring & Bar Animations ========== */
function initScoreAnimations() {
    // Animated score ring
    const scoreRing = document.getElementById('score-ring');
    if (scoreRing) {
        const score = parseInt(scoreRing.dataset.score) || 0;
        const ringFill = document.getElementById('ring-fill');
        const scoreNumber = document.getElementById('score-number');
        const circumference = 2 * Math.PI * 52; // r=52

        if (ringFill) {
            ringFill.style.strokeDasharray = circumference;
            ringFill.style.strokeDashoffset = circumference;

            setTimeout(() => {
                const offset = circumference - (score / 100) * circumference;
                ringFill.style.strokeDashoffset = offset;
            }, 300);
        }

        // Animate counter
        if (scoreNumber) {
            animateCounter(scoreNumber, 0, score, 1200);
        }
    }

    // Animated JD match bar
    const jdBar = document.getElementById('jd-bar-fill');
    if (jdBar) {
        const score = parseFloat(jdBar.dataset.score) || 0;
        setTimeout(() => {
            jdBar.style.width = `${Math.max(score, 5)}%`;
        }, 500);
    }
}

function animateCounter(element, start, end, duration) {
    const range = end - start;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        element.textContent = Math.round(start + range * eased);
        if (progress < 1) requestAnimationFrame(update);
    }

    requestAnimationFrame(update);
}
