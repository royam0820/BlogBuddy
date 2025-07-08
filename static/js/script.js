// Blog Magic - JavaScript functionality for kid-friendly interactions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initializeAnimations();
    initializeFormValidation();
    initializeImagePreview();
    initializeShareFunction();
    initializeAccessibility();
});

/**
 * Initialize fun animations for the blog
 */
function initializeAnimations() {
    // Add floating animation to post cards
    const postCards = document.querySelectorAll('.post-card');
    postCards.forEach((card, index) => {
        // Stagger the animation delay
        card.style.animationDelay = `${index * 0.1}s`;
        
        // Add entrance animation
        card.classList.add('animate-entrance');
    });
    
    // Add sparkle effect to magical buttons
    const magicalButtons = document.querySelectorAll('.btn-magical');
    magicalButtons.forEach(button => {
        button.addEventListener('mouseenter', createSparkleEffect);
    });
}

/**
 * Create sparkle effect on magical buttons
 */
function createSparkleEffect(event) {
    const button = event.target;
    const sparkles = ['✨', '⭐', '🌟', '💫'];
    
    for (let i = 0; i < 3; i++) {
        setTimeout(() => {
            const sparkle = document.createElement('span');
            sparkle.textContent = sparkles[Math.floor(Math.random() * sparkles.length)];
            sparkle.className = 'sparkle-effect';
            sparkle.style.cssText = `
                position: absolute;
                pointer-events: none;
                font-size: 1.2rem;
                animation: sparkleFloat 1s ease-out forwards;
                left: ${Math.random() * button.offsetWidth}px;
                top: ${Math.random() * button.offsetHeight}px;
            `;
            
            button.style.position = 'relative';
            button.appendChild(sparkle);
            
            // Remove sparkle after animation
            setTimeout(() => {
                if (sparkle.parentNode) {
                    sparkle.parentNode.removeChild(sparkle);
                }
            }, 1000);
        }, i * 100);
    }
}

/**
 * Enhanced form validation with kid-friendly messages
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!validateForm(this)) {
                event.preventDefault();
                showValidationMessage();
            } else {
                showSubmissionFeedback();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', () => validateField(input));
            input.addEventListener('input', () => clearFieldErrors(input));
        });
    });
}

/**
 * Validate individual form field
 */
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let message = '';
    
    // Custom validation rules
    switch (fieldName) {
        case 'title':
            if (value.length < 3) {
                isValid = false;
                message = 'Ton titre doit avoir au moins 3 caractères! 📝';
            } else if (value.length > 200) {
                isValid = false;
                message = 'Ton titre est trop long! Essaie de le raccourcir. ✂️';
            }
            break;
            
        case 'content':
            if (value.length < 10) {
                isValid = false;
                message = 'Raconte-nous plus de détails! Au moins 10 caractères. ✍️';
            }
            break;
            
        case 'image_url':
            if (value && !isValidUrl(value)) {
                isValid = false;
                message = 'Assure-toi que ton lien d\'image est correct! 🔗';
            }
            break;
    }
    
    if (!isValid) {
        showFieldError(field, message);
    } else {
        clearFieldErrors(field);
    }
    
    return isValid;
}

/**
 * Check if URL is valid
 */
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

/**
 * Show field error message
 */
function showFieldError(field, message) {
    clearFieldErrors(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    
    field.parentNode.appendChild(errorDiv);
}

/**
 * Clear field error messages
 */
function clearFieldErrors(field) {
    field.classList.remove('is-invalid');
    
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

/**
 * Validate entire form
 */
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Show validation message
 */
function showValidationMessage() {
    const existingAlert = document.querySelector('.validation-alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    const alert = document.createElement('div');
    alert.className = 'alert alert-warning validation-alert';
    alert.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        Oups! Vérifie que tu as bien rempli tous les champs obligatoires! 😊
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alert, container.firstChild);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

/**
 * Show submission feedback
 */
function showSubmissionFeedback() {
    const submitButton = document.querySelector('button[type="submit"]');
    if (submitButton) {
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Publication en cours...';
        submitButton.disabled = true;
        
        // Reset button after 3 seconds (in case form doesn't redirect)
        setTimeout(() => {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }, 3000);
    }
}

/**
 * Initialize image preview functionality
 */
function initializeImagePreview() {
    const imageUrlInput = document.querySelector('input[name="image_url"]');
    
    if (imageUrlInput) {
        imageUrlInput.addEventListener('blur', function() {
            const url = this.value.trim();
            if (url && isValidUrl(url)) {
                showImagePreview(url);
            } else {
                hideImagePreview();
            }
        });
    }
}

/**
 * Show image preview
 */
function showImagePreview(url) {
    // Remove existing preview
    hideImagePreview();
    
    const imageUrlInput = document.querySelector('input[name="image_url"]');
    const previewContainer = document.createElement('div');
    previewContainer.className = 'image-preview mt-2';
    previewContainer.innerHTML = `
        <div class="card" style="max-width: 300px;">
            <img src="${url}" class="card-img-top" alt="Aperçu" style="height: 150px; object-fit: cover;" 
                 onerror="this.parentElement.parentElement.innerHTML='<div class=\'text-danger p-2\'><i class=\'fas fa-exclamation-triangle\'></i> Impossible de charger l\'image</div>'">
            <div class="card-body p-2">
                <small class="text-muted">Aperçu de ton image</small>
            </div>
        </div>
    `;
    
    imageUrlInput.parentNode.appendChild(previewContainer);
}

/**
 * Hide image preview
 */
function hideImagePreview() {
    const preview = document.querySelector('.image-preview');
    if (preview) {
        preview.remove();
    }
}

/**
 * Initialize share functionality
 */
function initializeShareFunction() {
    // This function will be called from the template
    window.sharePost = function() {
        const title = document.querySelector('.post-title')?.textContent || 'MiniMonde';
        const url = window.location.href;
        
        if (navigator.share) {
            navigator.share({
                title: title,
                url: url,
                text: 'Découvre cette histoire magique!'
            }).catch(err => console.log('Erreur lors du partage:', err));
        } else {
            // Fallback - copy to clipboard
            navigator.clipboard.writeText(url).then(() => {
                showShareFeedback();
            }).catch(() => {
                // Manual fallback
                const textArea = document.createElement('textarea');
                textArea.value = url;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showShareFeedback();
            });
        }
    };
}

/**
 * Show share feedback
 */
function showShareFeedback() {
    const feedback = document.createElement('div');
    feedback.className = 'alert alert-success position-fixed';
    feedback.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 300px;
    `;
    feedback.innerHTML = `
        <i class="fas fa-check-circle"></i>
        Lien copié! Tu peux maintenant le partager! 🎉
    `;
    
    document.body.appendChild(feedback);
    
    setTimeout(() => {
        if (feedback.parentNode) {
            feedback.remove();
        }
    }, 3000);
}

/**
 * Initialize accessibility features
 */
function initializeAccessibility() {
    // Add keyboard navigation for cards
    const postCards = document.querySelectorAll('.post-card');
    postCards.forEach(card => {
        card.setAttribute('tabindex', '0');
        card.addEventListener('keypress', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                const link = this.querySelector('a[href]');
                if (link) {
                    link.click();
                }
            }
        });
    });
    
    // Add focus indicators
    const focusableElements = document.querySelectorAll('a, button, input, textarea, select');
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '3px solid rgba(255, 107, 107, 0.5)';
            this.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', function() {
            this.style.outline = '';
            this.style.outlineOffset = '';
        });
    });
}

// Add custom CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes sparkleFloat {
        0% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
        100% {
            opacity: 0;
            transform: translateY(-20px) scale(1.5);
        }
    }
    
    @keyframes animateEntrance {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-entrance {
        animation: animateEntrance 0.6s ease-out forwards;
    }
`;
document.head.appendChild(style);

// Add some fun console messages for curious kids!
console.log(`
🌈 Bienvenue sur MiniMonde! 🌈
✨ Tu es un petit curieux qui regarde le code? C'est génial! ✨
🎨 Continue à explorer et à apprendre! 🎨
`);
