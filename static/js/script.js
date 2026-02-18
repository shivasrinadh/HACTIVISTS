// Enhanced animations and interactions
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card, .metric');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        observer.observe(card);
    });
    
    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Enhanced form validation
    const amountInput = document.querySelector('input[name="claim_amount"]');
    if (amountInput) {
        amountInput.addEventListener("blur", () => {
            const value = Number(amountInput.value);
            if (!Number.isNaN(value) && value > 0) {
                amountInput.value = value.toFixed(2);
            }
        });
        
        // Add animation on focus
        amountInput.addEventListener('focus', function() {
            this.style.transform = 'scale(1.02)';
        });
        
        amountInput.addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
        });
    }

    const claimForm = document.querySelector("#claim-form");
    if (claimForm) {
        claimForm.addEventListener("submit", (event) => {
            const requiredFields = claimForm.querySelectorAll("[data-required='true']");
            let invalid = false;
            requiredFields.forEach((field) => {
                if (!field.value || !field.value.toString().trim()) {
                    invalid = true;
                    field.style.borderColor = "#b91c1c";
                    field.style.animation = 'shake 0.5s ease';
                    setTimeout(() => {
                        field.style.animation = '';
                    }, 500);
                } else {
                    field.style.borderColor = "";
                }
            });
            if (invalid) {
                event.preventDefault();
                // Enhanced error message
                const errorMsg = document.createElement('div');
                errorMsg.className = 'flash flash-danger';
                errorMsg.textContent = 'Please complete all required fields before submitting.';
                errorMsg.style.animation = 'slideInRight 0.5s ease-out';
                claimForm.insertBefore(errorMsg, claimForm.firstChild);
                setTimeout(() => {
                    errorMsg.remove();
                }, 5000);
            }
        });
    }
    
    // Add shake animation for invalid fields
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
    `;
    document.head.appendChild(style);
});
