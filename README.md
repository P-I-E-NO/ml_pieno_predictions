# ml_pieno_predictions
## Overview

This component is part of an IoT project that enables the prediction of growth/decline in gasoline or diesel prices. It includes containers for price prediction, APIs to fetch data, and the creation of a MySQL database. This database stores daily data obtained from government websites and updates prediction data on a daily basis.

## Features

- **Prediction Container:** Utilize this container to obtain predictions regarding the future growth or decline of gasoline and diesel prices.

- **Table Predizioni:** Use this container to create 'predizioni' table on mySQL database.

- **API Prezzi & Predizioni Containers:** These containers facilitate the retrieval of data from external sources, ensuring up-to-date information for accurate predictions.

- **MySQL Database:** A database is set up to store daily data acquired from government websites. This ensures a historical record of fuel prices for analysis and reporting purposes.

- **Table Distributori Modena:** Utilize this container to create 'distributori' table on mySQL database.

- **Push Data Container:** Use this container to populate tabe 'distributori' with daily list of Modena distributor (that contain fuel price in the specific distirbutor).

-- **API Distributori Containers:** These containers facilitate the retrieval of data from external sources, ensuring up-to-date information for all distributors into Modena and province.

## Usage

1. **Prediction Container:**
   - run ./predict.sh in order to create python_predict container (that takes new data, store new data into the db ad compute prediction also saved.)
   - next: 'docker run --network=secondo_docker_ml_pieno_net -e FUEL=Benzina pieno_predict' will produce new data from government website to db, prediction of current day (0 decrease, 1 increase).

2. **Table Predizioni Container:** 
    - run ./table_preds.sh into 'table_predictions' folder to create 'predizioni' table on database.

3. **API Prezzi & Predizioni Containers:**
   - run ./api.sh into flask_mysql_api in order to create docker image for api getting requests.

4. **MySQL Database:**
   - run ./migrate.sh into migrations folder and after that run ./seed.sh into last_seven folder.
   - finally run 'docker compose up'

5. **Table Distributori Container:** 
   - run ./table_dist.sh into 'crate_table_distributor' folder to obtain the table creation. 

6. **Push Data Container:**
   - run ./insert_distributor.sh into 'push_distributors_db' folder in order to push data into mySQL table 'distributori' (created with point 5.); run this insertion every day (because data have daily price for specific distributor). 

7. **API Distributori Modena:**
   - run ./api_distributori.sh into 'api_distributori' folder to create container for distributori API. Next add into the compose.yaml the 'api_distributori' service and go to /api_distributori/get_distributori to obtain all distributors list with relative informations. 
