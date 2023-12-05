(() => {
    let gameTimerInterval = null;
    let checkingInventoryInterval = null;
    let airportList = [];
    let markerList = [];
    let completed_airports = [];
    let password_collected = [];
    const difficultyLevel = {
        'easy': 1,
        'normal': 3,
        'hard': 5,
    };

    const gameResult = async () => {
        clearInterval(gameTimerInterval);
        $('.modal:visible').modal('hide'); // Hide the visible modal

        const url = 'http://127.0.0.1:5000/game/result';
        const headers = {
            'Content-Type': 'application/json',
        };

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to get the game result');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                alert('Failed to get the game result');
            }

            const minutes = Math.floor(responseData.game_duration / 60);
            const seconds = responseData.game_duration % 60;
            const gameDuration = `${minutes.toString().padStart(2, '0')} : ${seconds.toString().padStart(2, '0')}`;

            if (responseData.player.game_status === "completed") {
                document.querySelector('.game-result-modal .game-result.game-win .game-result-score .score-value').innerHTML = responseData.calculated_score;
                document.querySelector('.game-result-modal .game-result.game-win .result-item .time').innerHTML = gameDuration
                document.querySelector('.game-result-modal .game-result.game-win .result-item .weapon').innerHTML = responseData.weapons_remaining;
                document.querySelector('.game-result-modal .game-result.game-win .result-item .energy').innerHTML = responseData.energy_remaining;
                document.querySelector('.game-result-modal .game-result.game-win').classList.remove('d-none');
                document.querySelector('.game-result-modal .game-result.game-lose').classList.add('d-none');
            } else {
                document.querySelector('.game-result-modal .game-result.game-lose .result-item .time').innerHTML = gameDuration
                document.querySelector('.game-result-modal .game-result.game-lose .result-item .weapon').innerHTML = responseData.weapons_remaining;
                document.querySelector('.game-result-modal .game-result.game-lose .result-item .energy').innerHTML = responseData.energy_remaining;
                document.querySelector('.game-result-modal .game-result.game-win').classList.add('d-none');
                document.querySelector('.game-result-modal .game-result.game-lose').classList.remove('d-none');
            }

            $('.game-result-modal').modal('show');
        } catch (error) {
            console.error(error);
        }
    }

    const startGameTimer = () => {
        const countdownElement = document.getElementsByClassName('countdown')[0];
        if (game_status === "completed" || game_status === "failed") {
            countdownElement.innerHTML = 'GAME OVER!';
            return;
        }

        const gameEndAt = game_end_at;

        if (gameEndAt === undefined || gameEndAt === null) {
            return;
        }

        document.querySelector('.game-timer-container .resume-timer-button').classList.add('d-none');
        document.querySelector('.game-timer-container .pause-timer-button').classList.remove('d-none');

        // Calculate the total seconds
        let totalSeconds = Math.floor((new Date(gameEndAt) - new Date()) / 1000);

        // Update the count down every 1 second
        gameTimerInterval = setInterval(() => {
            // Calculate the minutes and seconds
            const minutes = Math.floor(totalSeconds / 60);
            const seconds = totalSeconds % 60;

            // display 2 digits for minutes and seconds
            countdownElement.innerHTML = `${minutes.toString().padStart(2, '0')} : ${seconds.toString().padStart(2, '0')}`;

            // If the count down is finished, write some text
            if (totalSeconds <= 0) {
                clearInterval(gameTimerInterval);
                countdownElement.innerHTML = 'TIME UP!';
                document.querySelector('.game-timer-container .pause-timer-button').classList.add('d-none');
                document.querySelector('.game-timer-container .resume-timer-button').classList.add('d-none');

                gameEnd("failed", () => {
                    gameResult();
                });
            }
            totalSeconds--;
        }, 1000);
    }

    const setUpGame = async () => {
        const url = 'http://127.0.0.1:5000/game/set-up';
        const data = {
            email: current_user_email
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
                throw new Error('Failed to start the game');
            }

            const responseData = await response.json();

            if (responseData.status === -1) {
                alert('Failed to start the game');
                return;
            }

            getAirportList();

        } catch (error) {
            console.error(error);
        }
    }

    const startGame = async () => {
        const url = 'http://127.0.0.1:5000/game/start';
        const data = {
            email: current_user_email
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
                throw new Error('Failed to start the game');
            }

            const responseData = await response.json();

            if (responseData.status === -1) {
                alert('Failed to start the game');
                return;
            }

            // Update the variables which are located in the global scope
            game_status = responseData.player.game_status;
            game_end_at = responseData.player.game_end_at;
            inventory_weapon = responseData.player.inventory_weapon;
            inventory_energy = responseData.player.inventory_energy;
            current_location = responseData.player.location;
            game_completed_airports = responseData.player.game_completed_airports;
            game_password_collected = responseData.player.game_password_collected;

            document.querySelector('.inventory-item.weapon .item-quantity').innerHTML = inventory_weapon;
            document.querySelector('.inventory-item.energy .item-quantity').innerHTML = inventory_energy;

            if (game_status === "paused") {
                document.querySelector('.game-timer-container .resume-timer-button').classList.remove('d-none');
                let totalSeconds = Math.floor((new Date(game_end_at) - new Date()) / 1000);
                const minutes = Math.floor(totalSeconds / 60);
                const seconds = totalSeconds % 60;
                document.querySelector('.game-timer-container .countdown').innerHTML = `${minutes.toString().padStart(2, '0')} : ${seconds.toString().padStart(2, '0')}`;
                return;
            }

            // Start the game timer
            startGameTimer();
        } catch (error) {
            console.error(error);
        }
    }

    const isCompleted = (airport) => {
        return completed_airports.find((a) => {
            return a.name === airport.name;
        });
    }

    const buildGoogleMap = (airportList) => {
        // Check if Google Maps API is loaded
        if (typeof google === 'undefined') {
            console.error('Google Maps API is not loaded.');
            return;
        }

        // get the current location latitude and longitude
        const currentLocation = airportList.find((airport) => {
            return airport.country === current_location;
        });

        document.querySelector('#map').classList.remove('is-loading');
        // Create a new map centered at a default location (you can set your desired default coordinates)
        const map = new google.maps.Map(document.getElementById('map'), {
            center: { lat: currentLocation.latitude_deg, lng: currentLocation.longitude_deg },
            zoom: 6,
        });

        // Loop through the airportList and add markers to the map
        airportList.forEach((airport) => {
            if (airport.latitude_deg === null || airport.longitude_deg === null) {
                return;
            }

            let marker = null;
            let infoContent = '';
            if (airport.country === current_location) {
                marker = new google.maps.Marker({
                    position: { lat: airport.latitude_deg, lng: airport.longitude_deg }, // Use the actual latitude and longitude of each airport
                    map: map,
                    title: airport.name,
                    icon: {
                        url: 'static/images/current_location.png',
                        scaledSize: new google.maps.Size(100, 100),
                    },
                    animation: google.maps.Animation.DROP,
                });

                // Render font awesome stars based on the difficulty level
                let difficultyLevelStars = '';
                for (let i = 0; i < difficultyLevel[airport.difficulty_level]; i++) {
                    difficultyLevelStars += '<i class="fas fa-star"></i>';
                }

                let ariportInfo = `
                        <div class="airport-info">
                            <div class="d-flex align-items-center gap-1">
                                Difficulty Level:
                                <span class="difficulty-level">${difficultyLevelStars}</span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                Needed Weapon:
                                <span class="needed-weapon item-value d-flex align-items-center gap-1">
                                    ${airport.needed_weapon} <img src="static/images/weapon.png" class="img-fluid" />
                                </span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                Earned Weapon:
                                <span class="earned-weapon item-value d-flex align-items-center gap-1">
                                    ${airport.rewards_weapon} <img src="static/images/weapon.png" class="img-fluid" />
                                </span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                Needed Energy:
                                <span class="earned-energy item-value d-flex align-items-center gap-1">
                                    ${airport.rewards_energy} <img src="static/images/batery.png" class="img-fluid" />
                                </span>
                            </div>
                        </div>`;

                if (current_location === 'Finland') {
                    ariportInfo = '';
                }

                // Customize the content of the info window
                infoContent = `
                    <div class="info-window completed" data-airport-id="${airport.id}">
                        <div class="airport-header">    
                            <div class="airport-name">${airport.name} <i class="fas fa-check-circle"></i></div>
                            <div class="airport-weather-info">
                                <div class="pollution-level ${airport.pollution_level.toLowerCase().replace(' ', '-')}"><i class="fas fa-smog"></i> ${airport.pollution_level} </div>
                                <div class="temperature"><i class="fas fa-thermometer-half"></i> ${airport.temperature}°C</div>
                                <div class="wind-speed"><i class="fas fa-wind"></i> ${airport.wind_speed} meter/sec</div>
                            </div>
                        </div>
                        ${ariportInfo}
                    </div>`;
            } else if (airport.country === 'Finland') {
                marker = new google.maps.Marker({
                    position: { lat: airport.latitude_deg, lng: airport.longitude_deg }, // Use the actual latitude and longitude of each airport
                    map: map,
                    title: airport.name,
                    icon: {
                        url: 'static/images/based_location.png',
                        scaledSize: new google.maps.Size(60, 60),
                    },
                    animation: google.maps.Animation.DROP,
                });

                // Customize the content of the info window
                infoContent = `
                    <div class="info-window completed" data-airport-id="${airport.id}">
                        <div class="airport-header">    
                            <div class="airport-name">${airport.name} <i class="fas fa-check-circle"></i></div>
                            <div class="airport-weather-info">
                                <div class="pollution-level ${airport.pollution_level.toLowerCase().replace(' ', '-')}"><i class="fas fa-smog"></i> ${airport.pollution_level} </div>  
                                <div class="temperature"><i class="fas fa-thermometer-half"></i> ${airport.temperature}°C</div>
                                <div class="wind-speed"><i class="fas fa-wind"></i> ${airport.wind_speed} meter/sec</div>
                            </div>
                        </div>
                    </div>`;
            } else if (isCompleted(airport)) {
                marker = new google.maps.Marker({
                    position: { lat: airport.latitude_deg, lng: airport.longitude_deg }, // Use the actual latitude and longitude of each airport
                    map: map,
                    title: airport.name,
                    icon: {
                        url: 'static/images/completed_location.png',
                        scaledSize: new google.maps.Size(60, 60),
                    },
                    animation: google.maps.Animation.DROP,
                });

                // Render font awesome stars based on the difficulty level
                let difficultyLevelStars = '';
                for (let i = 0; i < difficultyLevel[airport.difficulty_level]; i++) {
                    difficultyLevelStars += '<i class="fas fa-star"></i>';
                }

                // Customize the content of the info window
                infoContent = `
                    <div class="info-window completed" data-airport-id="${airport.id}">
                        <div class="airport-header">    
                            <div class="airport-name">${airport.name} <i class="fas fa-check-circle"></i></div>
                            <div class="airport-weather-info">
                                <div class="pollution-level ${airport.pollution_level.toLowerCase().replace(' ', '-')}"><i class="fas fa-smog"></i> ${airport.pollution_level} </div>
                                <div class="temperature"><i class="fas fa-thermometer-half"></i> ${airport.temperature}°C</div>
                                <div class="wind-speed"><i class="fas fa-wind"></i> ${airport.wind_speed} meter/sec</div>
                            </div>
                        </div>
                        <div class="airport-info">
                            <div class="d-flex align-items-center gap-1">
                                Difficulty Level:
                                <span class="difficulty-level">${difficultyLevelStars}</span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                Needed Weapon:
                                <span class="needed-weapon item-value d-flex align-items-center gap-1">
                                    ${airport.needed_weapon} <img src="static/images/weapon.png" class="img-fluid" />
                                </span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                Earned Weapon:
                                <span class="earned-weapon item-value d-flex align-items-center gap-1">
                                    ${airport.rewards_weapon} <img src="static/images/weapon.png" class="img-fluid" />
                                </span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                Needed Energy:
                                <span class="earned-energy item-value d-flex align-items-center gap-1">
                                    ${airport.rewards_energy} <img src="static/images/batery.png" class="img-fluid" />
                                </span>
                            </div>
                        </div>
                    </div>`;
            } else if (airport.country == "Spain") {
                marker = new google.maps.Marker({
                    position: { lat: airport.latitude_deg, lng: airport.longitude_deg }, // Use the actual latitude and longitude of each airport
                    map: map,
                    title: airport.name,
                    icon: {
                        url: 'static/images/final_location.png',
                        scaledSize: new google.maps.Size(50, 50),
                    },
                    animation: google.maps.Animation.DROP,
                });

                // Customize the content of the info window
                infoContent = `
                    <div class="info-window" data-airport-id="${airport.id}">
                        <div class="airport-header">    
                            <div class="airport-name">${airport.name}</div>
                            <div class="airport-weather-info">
                                <div class="pollution-level ${airport.pollution_level.toLowerCase().replace(' ', '-')}"><i class="fas fa-smog"></i> ${airport.pollution_level} </div> 
                                <div class="temperature"><i class="fas fa-thermometer-half"></i> ${airport.temperature}°C</div>
                                <div class="wind-speed"><i class="fas fa-wind"></i> ${airport.wind_speed} meter/sec</div>
                            </div>
                        </div>
                        <div class="airport-info">
                            <div class="d-flex align-items-center gap-1">
                                Difficulty Level:
                                <span class="difficulty-level">
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                </span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                Needed Weapon:
                                <span class="needed-weapon item-value d-flex align-items-center gap-1">
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                </span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                <span class="earned-weapon-text">Earning Weapon:</span>
                                <span class="earned-weapon item-value d-flex align-items-center gap-1">
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                </span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                <span class="earned-energy-text">Earning Energy:</span>
                                <span class="earned-energy item-value d-flex align-items-center gap-1">
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                </span>
                            </div>
                        </div>
                        <div class="stage-fighting text-center d-none">
                            <div class="fight-win-loading d-none">
                                <img src="static/images/win-fight.gif" class="img-fluid" />
                            </div>
                            <div class="fight-lose-loading d-none">
                                <img src="static/images/lose-fight.gif" class="img-fluid" />
                            </div>
                        </div>
                        <div class="mission-result text-center d-none"></div>
                        <button class="btn btn-success" onclick="checkNeededEnergyAndStartRescue('${airport.id}')">Rescue</button>
                    </div>`;
            } else {
                marker = new google.maps.Marker({
                    position: { lat: airport.latitude_deg, lng: airport.longitude_deg }, // Use the actual latitude and longitude of each airport
                    map: map,
                    title: airport.name,
                    animation: google.maps.Animation.DROP,
                });

                // Customize the content of the info window
                infoContent = `
                    <div class="info-window" data-airport-id="${airport.id}">
                        <div class="airport-header">    
                            <div class="airport-name">${airport.name}</div>
                            <div class="airport-weather-info">
                                <div class="pollution-level ${airport.pollution_level.toLowerCase().replace(' ', '-')}"><i class="fas fa-smog"></i> ${airport.pollution_level} </div>
                                <div class="temperature"><i class="fas fa-thermometer-half"></i> ${airport.temperature}°C</div>
                                <div class="wind-speed"><i class="fas fa-wind"></i> ${airport.wind_speed} meter/sec</div>
                            </div>
                        </div>
                        <div class="airport-info">
                            <div class="d-flex align-items-center gap-1">
                                Difficulty Level:
                                <span class="difficulty-level">
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                </span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                Needed Weapon:
                                <span class="needed-weapon item-value d-flex align-items-center gap-1">
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                </span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                <span class="earned-weapon-text">Earning Weapon:</span>
                                <span class="earned-weapon item-value d-flex align-items-center gap-1">
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                </span>
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                <span class="earned-energy-text">Earning Energy:</span>
                                <span class="earned-energy item-value d-flex align-items-center gap-1">
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                    <i class="fas fa-question"></i>
                                </span>
                            </div>
                        </div>
                        <div class="stage-fighting text-center d-none">
                            <div class="fight-win-loading d-none">
                                <img src="static/images/win-fight.gif" class="img-fluid" />
                            </div>
                            <div class="fight-lose-loading d-none">
                                <img src="static/images/lose-fight.gif" class="img-fluid" />
                            </div>
                        </div>
                        <div class="mission-result text-center d-none"></div>
                        <button class="btn btn-success" onclick="checkNeededEnergyAndStartRescue('${airport.id}')">Rescue</button>
                    </div>`;
            }

            const infoWindow = new google.maps.InfoWindow({
                content: infoContent,
            });

            // Show the info window when the marker is clicked
            marker.addListener('click', () => {
                infoWindow.open(map, marker);
            });

            // Add the marker to the marker list
            markerList.push(marker);
        });
    };

    const buildCompletedAirportsList = (airportList) => {
        completed_airports = [];
        game_completed_airports.split(',').forEach((country) => {
            if (country !== '') {
                airportList.forEach((airport) => {
                    if (airport.country === country) {
                        completed_airports.push(airport);
                    }
                });
            }
        });
    }

    const buildPasswordCollectedList = () => {
        password_collected = [];
        game_password_collected.split(',').forEach((password, i) => {
            if (password !== '') {
                password_collected.push(password);
                document.querySelector(`.password-items .password-number-${i + 1} img`).src = 'static/images/number-' + password + '.png';
                document.querySelector(`.final-password-modal .password-items .password-number-${i + 1} img`).src = 'static/images/number-' + password + '.png';
            }
        });
    }

    const getAirportList = async () => {
        const url = 'http://127.0.0.1:5000/game/airports';

        const headers = {
            'Content-Type': 'application/json',
        };

        try {

            const response = await fetch(url, {
                method: 'GET',
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to load airport list');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                alert('Failed to load airport list');
            }

            airportList = responseData.airports;

            buildCompletedAirportsList(airportList);
            buildPasswordCollectedList();
            buildGoogleMap(airportList);

            startGame();
        } catch (error) {
            console.error(error);
        }
    }

    const rescueAirport = async (data) => {
        const url = 'http://127.0.0.1:5000/game/rescue-airport';

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
                throw new Error('Failed to start the game');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                alert('Failed to start the game');
            }

            game_completed_airports = responseData.player.game_completed_airports;
            game_password_collected = responseData.player.game_password_collected;
            game_status = responseData.player.game_status;

            buildCompletedAirportsList(airportList);
            buildPasswordCollectedList();

            if (game_status === 'need_master_password') {
                $('.final-password-modal').modal('show');
            }
        } catch (error) {
            console.error(error);
        }
    }

    const checkNeededEnergyAndStartRescue = async (airportId) => {
        const airport = airportList.find((a) => {
            return a.id === airportId || a.id === parseInt(airportId);
        });

        const url = `http://127.0.0.1:5000/game/check-needed-energy/${current_location}/${airport.country}`;

        const headers = {
            'Content-Type': 'application/json',
        };

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to check the needed energy');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                alert(responseData.message);
                return;
            }

            const neededEnergy = responseData.needed_energy;
            if (inventory_energy < neededEnergy) {
                alert(`You need ${neededEnergy} energy to rescue this airport.`)
                return;
            }
            startRescue(airportId, neededEnergy);
        } catch (error) {
            console.error(error);
        }
    }

    const startRescue = (airportId, neededEnergy) => {
        const infoWindow = document.querySelector(`.info-window[data-airport-id="${airportId}"]`);
        const stageFighting = infoWindow.querySelector('.stage-fighting');
        const airportInfo = infoWindow.querySelector('.airport-info');
        const fightWinLoading = infoWindow.querySelector('.fight-win-loading');
        const fightLoseLoading = infoWindow.querySelector('.fight-lose-loading');

        const airport = airportList.find((a) => {
            return a.id === airportId || a.id === parseInt(airportId);
        });

        infoWindow.querySelector('button').classList.add('d-none');

        // Render font awesome stars based on the difficulty level
        let difficultyLevelStars = '';
        for (let i = 0; i < difficultyLevel[airport.difficulty_level]; i++) {
            difficultyLevelStars += '<i class="fas fa-star"></i>';
        }
        infoWindow.querySelector('.difficulty-level').innerHTML = difficultyLevelStars;
        infoWindow.querySelector('.needed-weapon').innerHTML = `${airport.needed_weapon} <img src="static/images/weapon.png" class="img-fluid" />`

        airportInfo.classList.add('d-none');
        stageFighting.classList.remove('d-none');

        if (inventory_weapon >= airport.needed_weapon) {
            fightWinLoading.classList.remove('d-none');
            fightLoseLoading.classList.add('d-none');
            setTimeout(() => {
                stageFighting.classList.add('d-none');
                fightWinLoading.classList.add('d-none');
                infoWindow.querySelector('.mission-result').classList.remove('d-none');
                infoWindow.classList.add('completed');
                infoWindow.querySelector('.airport-name').innerHTML = `${airport.name} <i class="fas fa-check-circle"></i>`;
                infoWindow.querySelector('.mission-result').innerHTML = `<div class="win-fight">
                    <div class="alert alert-success" role="alert">
                        <strong>Mission Completed!</strong>
                    </div>
                    <div>
                        <span><strong>Here are your rewards for this mission</strong></span>
                        <div class="rewards d-flex align-items-center gap-2 mt-2">
                            <div class="reward-item d-flex align-items-center gap-2">
                                <span class="reward-value">+${airport.rewards_weapon}</span>
                                <img src="static/images/weapon.png" class="img-fluid" />
                            </div>
                            <div class="reward-item d-flex align-items-center gap-2">
                                <span class="reward-value">+${airport.rewards_energy}</span>
                                <img src="static/images/batery.png" class="img-fluid" />
                            </div>
                        </div>
                    </div>
                `
                setTimeout(() => {
                    infoWindow.querySelector('.mission-result').classList.add('d-none');
                    infoWindow.querySelector('.earned-weapon-text').innerHTML = 'Earned Weapon:';
                    infoWindow.querySelector('.earned-weapon').innerHTML = `${airport.rewards_weapon} <img src="static/images/weapon.png" class="img-fluid" />`;
                    infoWindow.querySelector('.earned-energy-text').innerHTML = 'Earned Energy:';
                    infoWindow.querySelector('.earned-energy').innerHTML = `${airport.rewards_energy} <img src="static/images/batery.png" class="img-fluid" />`;

                    airportInfo.classList.remove('d-none');
                }, 5000);

                const new_inventory_weapon = parseInt(inventory_weapon) - parseInt(airport.needed_weapon) + parseInt(airport.rewards_weapon);
                const new_inventory_energy = parseInt(inventory_energy) - parseInt(neededEnergy) + parseInt(airport.rewards_energy);

                document.querySelector('.inventory-item.weapon .item-quantity').innerHTML = new_inventory_weapon;
                inventory_weapon = new_inventory_weapon;
                document.querySelector('.inventory-item.energy .item-quantity').innerHTML = new_inventory_energy;
                inventory_energy = new_inventory_energy;

                // Put the current location to game_completed_airports
                completed_airports.push(airport);
                // If the password_collected does not contain the password piece, add it
                if (!password_collected.includes(airport.password_piece)) {
                    password_collected.push(airport.password_piece);
                }
                current_location = airport.country;

                // Call api to update the game info
                const updateData = {
                    rescue_status: 1,
                    email: current_user_email,
                    new_location: airport.country,
                    inventory_weapon: new_inventory_weapon,
                    inventory_energy: new_inventory_energy,
                    completed_airports: completed_airports.map((a) => {
                        return a.country;
                    }).join(','),
                    password_collected: password_collected.join(','),
                    airport_stage: airport.stage,
                };
                rescueAirport(updateData);

                markerList.forEach((marker) => {
                    if (completed_airports.find((a) => {
                        return a.name === marker.title;
                    })) {
                        marker.setIcon({
                            url: 'static/images/completed_location.png',
                            scaledSize: new google.maps.Size(60, 60),
                        });
                    }
                });

                const finlandMarker = markerList.find((m) => {
                    return m.title === 'Helsinki Vantaa Airport';
                });
                finlandMarker.setIcon({
                    url: 'static/images/based_location.png',
                    scaledSize: new google.maps.Size(60, 60),
                });

                // Change the marker icon to current location icon
                const marker = markerList.find((m) => {
                    return m.title === airport.name;
                });

                marker.setIcon({
                    url: 'static/images/current_location.png',
                    scaledSize: new google.maps.Size(60, 60),
                });

            }, 4000);
        } else {
            fightWinLoading.classList.add('d-none');
            fightLoseLoading.classList.remove('d-none');
            setTimeout(() => {
                // Reduce the inventory_weapon and inventory_energy by the airport.needed_weapon and neededEnergy to fly there
                let new_inventory_weapon = parseInt(inventory_weapon) - parseInt(airport.needed_weapon);
                let new_inventory_energy = parseInt(inventory_energy) - parseInt(neededEnergy);

                // Punish the player by reducing the inventory_weapon and inventory_energy by 10% of the original value
                const punish_inventory_weapon = Math.ceil(0.1 * parseInt(new_inventory_weapon));
                const punish_inventory_energy = Math.ceil(0.1 * parseInt(new_inventory_energy));

                stageFighting.classList.add('d-none');
                fightLoseLoading.classList.add('d-none');
                infoWindow.querySelector('.mission-result').classList.remove('d-none');
                infoWindow.querySelector('.mission-result').innerHTML = `<div class="lose-fight">
                    <div class="alert alert-danger" role="alert">
                        <strong>Mission Failed!!!!</strong>
                    </div>
                    <div>
                        <span><strong>Punishment for this mission</strong></span>
                        <div class="punishment d-flex align-items-center gap-2 mt-2">
                            <div class="punishment-item d-flex align-items-center gap-2">
                                <span class="punishment-value">-${punish_inventory_weapon}</span>
                                <img src="static/images/weapon.png" class="img-fluid" />
                            </div>
                            <div class="punishment-item d-flex align-items-center gap-2">
                                <span class="punishment-value">-${punish_inventory_energy}</span>
                                <img src="static/images/batery.png" class="img-fluid" />
                            </div>
                        </div>
                    </div>
                `
                const final_inventory_weapon = new_inventory_weapon - punish_inventory_weapon;
                document.querySelector('.inventory-item.weapon .item-quantity').innerHTML = final_inventory_weapon;
                inventory_weapon = final_inventory_weapon;

                const final_inventory_energy = new_inventory_energy - punish_inventory_energy;
                document.querySelector('.inventory-item.energy .item-quantity').innerHTML = final_inventory_energy;
                inventory_energy = final_inventory_energy;

                setTimeout(() => {
                    infoWindow.querySelector('button').classList.remove('d-none');
                    infoWindow.querySelector('.mission-result').classList.add('d-none');
                    airportInfo.classList.remove('d-none');
                }, 5000);

                const updateData = {
                    rescue_status: 0,
                    inventory_weapon: new_inventory_weapon,
                    inventory_energy: new_inventory_energy,
                };
                rescueAirport(updateData);

            }, 5000);
        }
    }

    const logOut = async () => {
        const url = 'http://127.0.0.1:5000/logout';

        const headers = {
            'Content-Type': 'application/json',
        };
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to log out');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                alert('Failed to log out');
            }

            window.location.href = '/';
        } catch (error) {
            console.error(error);
        }
    }

    const gameEnd = async (status, callback = null) => {
        const url = 'http://127.0.0.1:5000/game/end';
        const headers = {
            'Content-Type': 'application/json',
        };
        try {
            const response = await fetch(url, {
                method: 'POST',
                body: JSON.stringify({
                    game_status: status,
                }),
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to end the game');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                console.log(responseData.message);
            }

            if (callback !== null) {
                callback();
            }
        } catch (error) {
            console.error(error);
        }
    }

    const unclockFinalPassword = async () => {
        const url = 'http://127.0.0.1:5000/game/unclock-master-password';
        const headers = {
            'Content-Type': 'application/json',
        };

        let masterPassword = [];
        document.querySelectorAll('.master-password-input-container .master-password-input').forEach((passwordNumber) => {
            masterPassword.push(passwordNumber.value);
        });

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: JSON.stringify({
                    master_password: masterPassword.join(','),
                }),
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to end the game');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                if (responseData.player.game_master_password_retry_times < 5) {
                    alert(responseData.message);
                    return;
                } else {
                    alert(responseData.message);
                    gameEnd('failed', () => {
                        gameResult();
                    });
                    return;
                }
            }

            gameEnd("completed", () => {
                gameResult();
            });

        } catch (error) {
            console.error(error);
        }
    }

    const moveToNextPasswordPiece = (input) => {
        const maxLength = parseInt(input.maxLength, 10);
        const currentLength = input.value.length;

        if (currentLength >= maxLength) {
            const nextInput = input.nextElementSibling;
            if (nextInput && nextInput.tagName === 'INPUT') {
                nextInput.focus();
            }
        }
    }

    const getGameRanking = async () => {
        const url = 'http://127.0.0.1:5000/game/rankings';
        const headers = {
            'Content-Type': 'application/json',
        };

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to get the game ranking');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                console.log(responseData.message);
            }

            const rankingList = responseData.rankings

            let rankingHtml = '';
            rankingList.forEach((ranking, i) => {
                const rankingImage = ` <div class="ranking-item-position">
                                        <img src="static/images/${ranking.player_position === 1 ? 'first' : ''}${ranking.player_position === 2 ? 'second' : ''}${ranking.player_position === 3 ? 'third' : ''}-place.png" class="img-fluid"
                                            alt="${ranking.player_position} Place">
                                    </div>`;
                rankingHtml += `
                    <div class="ranking-item ${ranking.player_position === 1 ? 'first' : ''}${ranking.player_position === 2 ? 'second' : ''}${ranking.player_position === 3 ? 'third' : ''} ${parseInt(player_id) === parseInt(ranking.player_id) ? 'self' : ''}">
                        ${ranking.player_position <= 3 ? rankingImage : ``}
                        <div class="ranking-item-name ${ranking.player_position <= 3 ? '' : 'px-2'}">${ranking.player_position <= 3 ? ranking.player_name : `${ranking.player_position}. ${ranking.player_name}`}</div>
                        <div class="ranking-item-score">
                            <img src="static/images/rating.png" class="img-fluid"
                                alt="Rating">
                            <span class="ranking-value">${ranking.score}</span>
                        </div>
                    </div>`;
            });

            document.querySelector('.game-result-ranking-modal .ranking-list').innerHTML = rankingHtml;
            document.querySelector('.game-result-ranking-modal .your-ranking').innerHTML = '';
            // if player_ranking is undefined, it means that the player is not in the top 5
            if (responseData.player_ranking === undefined) {
                document.querySelector('.game-result-ranking-modal .ranking-list').classList.add('border-0');
                document.querySelector('.game-result-ranking-modal .your-ranking').classList.add('d-none');
            } else {
                document.querySelector('.game-result-ranking-modal .your-ranking').classList.remove('border-0');
                document.querySelector('.game-result-ranking-modal .your-ranking').classList.remove('d-none');
                document.querySelector('.game-result-ranking-modal .your-ranking').innerHTML += `
                    <div class="ranking-item self">
                        <div class="ranking-item-name">${responseData.player_ranking.player_position}. ${responseData.player_ranking.player_name}</div>
                        <div class="ranking-item-score">
                            <img src="static/images/rating.png" class="img-fluid"
                                alt="Rating">
                            <span class="ranking-value">${responseData.player_ranking.score}</span>
                        </div>
                    </div>`;
            }

            $('#gameResultRanking').modal('show');

        } catch (error) {
            console.error(error);
        }
    }

    const retryGame = async () => {
        const url = 'http://127.0.0.1:5000/game/retry';
        const headers = {
            'Content-Type': 'application/json',
        };

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to get the game ranking');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                console.log(responseData.message);
            }

            window.location.reload();

        } catch (error) {
            console.error(error);
        }
    }

    const updatePlayerInfo = async () => {
        const playerName = document.querySelector('.player-name-input').value;
        if (playerName === '') {
            return;
        }

        const url = 'http://127.0.0.1:5000/game/update-player-info';
        const headers = {
            'Content-Type': 'application/json',
        };

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: JSON.stringify({
                    player_name: playerName,
                }),
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to update player info');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                console.log(responseData.message);
            }

            document.querySelector('.player-info .player-name').innerHTML = playerName;
            document.querySelector('.player-info .player-name-container').classList.remove('d-none');
            document.querySelector('.player-info .edit-name-form').classList.add('d-none');

        } catch (error) {
            console.error(error);
        }
    }

    const pauseOrResumeGameTimer = async (status) => {
        const url = 'http://127.0.0.1:5000/game/pause-or-resume-game-timer';
        const headers = {
            'Content-Type': 'application/json',
        };

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: JSON.stringify({
                    pause_or_resume: status,
                }),
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to update player info');
            }

            const responseData = await response.json();

            if (responseData.status !== 1) {
                console.log(responseData.message);
            }

            if (status === 'pause') {
                document.querySelector('.pause-timer-button').classList.add('d-none');
                document.querySelector('.resume-timer-button').classList.remove('d-none');
                clearInterval(gameTimerInterval);
            } else {
                document.querySelector('.pause-timer-button').classList.remove('d-none');
                document.querySelector('.resume-timer-button').classList.add('d-none');
                game_end_at = responseData.player.game_end_at;
                startGameTimer();
            }
        } catch (error) {
            console.error(error);
        }
    }

    const init = () => {
        setUpGame();

        if (game_status === "need_master_password") {
            buildPasswordCollectedList();
            setTimeout(() => {
                $('.final-password-modal').modal('show');
            }, 1000);
        }

        if (game_status === "completed" || game_status === "failed") {
            setTimeout(() => {
                gameResult();
            }, 1000);
        }

        // This is the interval to check if the player has enough energy and weapon in the inventory
        // to continue the game
        checkingInventoryInterval = setInterval(() => {
            if (parseInt(inventory_energy) <= 0 || parseInt(inventory_weapon) <= 0) {
                clearInterval(checkingInventoryInterval);
                gameEnd("failed", () => {
                    gameResult();
                });
            }
        }, 5000);

        document.querySelector('.game-result-modal .exit-button').addEventListener('click', () => {
            $('#loadingModal').modal('show');
            logOut();
        });

        document.querySelector('.game-result-modal .replay-button').addEventListener('click', () => {
            $('.modal:visible').modal('hide');
            retryGame();
        });

        document.querySelector('.game-result-modal .ranking-button').addEventListener('click', () => {
            $('.modal:visible').modal('hide');
            getGameRanking();
        });

        document.querySelector('.game-result-ranking-modal .exit-button').addEventListener('click', () => {
            $('.modal:visible').modal('hide');
            $('#gameResult').modal('show');
        });

        document.querySelector('.log-out-button').addEventListener('click', () => {
            $('#loadingModal').modal('show');
            logOut();
        });

        document.querySelector('.edit-name-button').addEventListener('click', () => {
            document.querySelector('.player-info .player-name-container').classList.add('d-none');
            document.querySelector('.player-info .edit-name-form').classList.remove('d-none');
        });

        document.querySelector('.cancel-edit-name').addEventListener('click', () => {
            document.querySelector('.player-info .player-name-container').classList.remove('d-none');
            document.querySelector('.player-info .edit-name-form').classList.add('d-none');
        });

        document.querySelector('.unclock-password-button').addEventListener('click', () => {
            unclockFinalPassword();
        });

        document.querySelector('.save-edit-name').addEventListener('click', () => {
            updatePlayerInfo();
        });

        document.querySelector('.pause-timer-button').addEventListener('click', () => {
            pauseOrResumeGameTimer('pause');
        });

        document.querySelector('.resume-timer-button').addEventListener('click', () => {
            pauseOrResumeGameTimer('resume');
        });
    }

    init();

    window.checkNeededEnergyAndStartRescue = checkNeededEnergyAndStartRescue; // Expose the checkNeededEnergyAndStartRescue function to the global scope
    window.moveToNextPasswordPiece = moveToNextPasswordPiece; // Expose the moveToNextPasswordPiece function to the global scope

})();
