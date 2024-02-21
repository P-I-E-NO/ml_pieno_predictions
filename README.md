# ml_pieno_predictions
## Overview

This component is part of an IoT project that enables the prediction of growth/decline in gasoline or diesel prices. It includes containers for price prediction, APIs to fetch data, and the creation of a MySQL database. This database stores daily data obtained from government websites and updates prediction data on a daily basis.

## Features

- **Prediction Container:** Utilize this container to obtain predictions regarding the future growth or decline of gasoline and diesel prices.

- **API Containers:** These containers facilitate the retrieval of data from external sources, ensuring up-to-date information for accurate predictions.

- **MySQL Database:** A database is set up to store daily data acquired from government websites. This ensures a historical record of fuel prices for analysis and reporting purposes.

## Usage

1. **Prediction Container:**
   - run ./predict.sh in order to create python_predict container (that takes new data, store new data into the db ad compute prediction also saved.)
   - next: 'docker run --network=secondo_docker_ml_pieno_net -e FUEL=Benzina pieno_predict' will produce new data from government website to db, prediction of current day (0 decrease, 1 increase).

2. **API Containers:**
   - run ./api.sh into flask_mysql_api in order to create docker image for api getting requests.

3. **MySQL Database:**
   - run ./migrate.sh into migrations folder and after that run ./seed.sh into last_seven folder.
   - finally run 'docker compose up'
