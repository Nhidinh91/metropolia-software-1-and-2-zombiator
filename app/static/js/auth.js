(() => {
    const gameStart = async () => {
        const emailInput = document.querySelector('.email');
        const passwordInput = document.querySelector('.password');

        if (emailInput.value.length === 0) {
            displayNotification('Email cannot be empty', 'danger');
            return;
        }

        // Validate email
        if (!validateEmail(emailInput.value)) {
            displayNotification('Please enter a valid email address', 'danger');
            return;
        }

        // Validate password
        if (passwordInput.value.length === 0) {
            displayNotification('Password cannot be empty', 'danger');
            return;
        }

        const url = 'http://127.0.0.1:5000/login';
        const data = {
            email: emailInput.value,
            password: passwordInput.value
        };

        const headers = {
            'Content-Type': 'application/json',
        };

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: JSON.stringify(data),
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to authenticate player');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                displayNotification(responseData.message, 'danger');
                return;
            }

            $('#loadingModal').modal('show');

            window.location.href = '/game';
        } catch (error) {
            console.error(error);
        }
    };

    const validateEmail = (email) => {
        const emailRegex = /\S+@\S+\.\S+/;
        return emailRegex.test(email);
    };

    const init = () => {
        const audio = document.querySelector('.background-sounds .audio');
        // Keyup enter event listener
        document.querySelector('.email').addEventListener('keyup', (event) => {
            if (event.keyCode === 13) {
                event.preventDefault();
                gameStart();
            }
        });

        // Keyup enter event listener
        document.querySelector('.password').addEventListener('keyup', (event) => {
            if (event.keyCode === 13) {
                event.preventDefault();
                gameStart();
            }
        });

        // Add event listener to start game button
        document.querySelector('.start-game-button').addEventListener('click', gameStart);

        const gamePlayModal = document.querySelector('.game-play-modal');
        gamePlayModal.addEventListener('hidden.bs.modal', event => {
          audio.play();

          // Stop all playing iframe video
          const videos = document.querySelectorAll('iframe, video');
          Array.prototype.forEach.call(videos, function (video) {
            if (video.tagName.toLowerCase() === 'video') {
              video.pause();
            } else {
              video.src = video.src;
            }
          });
        })

        gamePlayModal.addEventListener('shown.bs.modal', event => {
          audio.pause();
        })
    };

    init();
})();
