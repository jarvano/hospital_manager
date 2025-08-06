// Theme Toggle Functionality
const themeToggle = document.getElementById('theme-toggle');
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

// Load saved theme preference
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
    }
});

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Form validation enhancement
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// Dynamic form fields
function addFormField(containerId, template) {
    const container = document.getElementById(containerId);
    if (container) {
        const newField = template.cloneNode(true);
        newField.querySelectorAll('input, select, textarea').forEach(input => {
            input.value = '';
        });
        container.appendChild(newField);
    }
}

function removeFormField(button) {
    button.closest('.form-field').remove();
}

// Date and time picker initialization
document.addEventListener('DOMContentLoaded', () => {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const timeInputs = document.querySelectorAll('input[type="time"]');
    
    dateInputs.forEach(input => {
        if (!input.value) {
            input.valueAsDate = new Date();
        }
    });
});

// Search functionality
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

const searchInput = document.querySelector('.search-input');
if (searchInput) {
    const performSearch = debounce((query) => {
        // Implement your search logic here
        console.log('Searching for:', query);
    }, 300);

    searchInput.addEventListener('input', (e) => {
        performSearch(e.target.value);
    });
}

// Print functionality
function printContent(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const printWindow = window.open('', '_blank');
        printWindow.document.write('<html><head><title>Print</title>');
        printWindow.document.write('<link rel="stylesheet" href="/static/css/style.css">');
        printWindow.document.write('</head><body>');
        printWindow.document.write(element.innerHTML);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.focus();
        setTimeout(() => {
            printWindow.print();
            printWindow.close();
        }, 250);
    }
}

// File upload preview
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    if (input.files && input.files[0] && preview) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Confirmation dialogs
function confirmAction(message, callback) {
    if (window.confirm(message)) {
        callback();
    }
}

// Format currency
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

// Format date
function formatDate(date, format = 'long') {
    const options = format === 'long' ?
        { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' } :
        { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-US', options);
}

// Handle form submission with AJAX
function handleAjaxForm(formId, successCallback, errorCallback) {
    const form = document.getElementById(formId);
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            try {
                const formData = new FormData(form);
                const response = await fetch(form.action, {
                    method: form.method,
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                const data = await response.json();
                if (response.ok) {
                    successCallback(data);
                } else {
                    errorCallback(data);
                }
            } catch (error) {
                errorCallback({ message: 'An error occurred' });
            }
        });
    }
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', () => {
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));

    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    popovers.forEach(popover => new bootstrap.Popover(popover));
});