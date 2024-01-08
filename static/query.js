document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector('form');
  
    form.addEventListener('submit', function (event) {
        event.preventDefault();
  
        var isValid = validateForm();
  
        if (isValid) {
            submitForm();
        } else {
            displayErrorMessage();
        }
    });
  
    function validateForm() {
        // Your validation logic here
        return true;
    }
  
    function submitForm() {
        var formData = new FormData(form);
  
        fetch(form.action, {
          method: 'POST',
          body: formData
      })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                var successMessage = document.querySelector('.u-form-send-success');
                successMessage.style.display = 'block';
                form.reset();
            } else {
                displayErrorMessage();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            displayErrorMessage();
        });
    }
  
    function displayErrorMessage() {
        var errorMessage = document.querySelector('.u-form-send-error');
        errorMessage.style.display = 'block';
    }
  });
  
  
  
  $(document).ready(function(){
    $('.carousel').slick({
    slidesToShow: 3,
    dots:true,
    centerMode: true,
    });
  });
  
  