# Family Budget App

This is a REST API application which allows manage expenses and income for several users. Each user can share his wallet with other users, who are able to see his income, expenses and balance, but are not able to modify it or manage. Only the owner of the wallet is able to do this.

## Requirements:

- `docker` and `docker-compose` services  
  **Note:** _For development purposes, there is also required **Python** in >= 3.9 version. Preferable also **virtual environment manager** (eg. miniconda3)_

## Running:

1. Clone repository to your local machine.
1. Open terminal and exec command `make run`.  
   **Note:** _App runs on default port `8000`_

## Usage:

- API documentation in available under `/swagger` endpoint. It is also possible to send example requests via swagger (after earlier authorization)
- App has default Django admin panel under `/admin` endpoint

## Configuration:

- there is required to create superuser **Hint:** Type in your terminal, in the repository directory `make superuser`
- superuser can create users
- users are authenticated by the **Bearer** token

## Development:

- App is covered by unit tests
- To run tests type in the terminal `make test`

### Notes from author:

- soon there will be available data fixtures to load and play with the application
- there are missing views for managing expenses and income -> Work in progress
- there are missing filtering and pagination -> Will be done after the above point
- right now, there is only possible to insert current expenses and income (not planned ones). There was an idea to add Planned Expenses feature, which allows to schedule future operations for certain day, and when this day will come, turn it into an expense. Entire process would be happened automatically with the Celery worker usage. Current setup is ready for this feature, Celery service is already included into the setup, just need to add another application and setup a periodic task
- there are also some others possible future features ideas:
  - architecture is prepared for expanding budgets to different currencies. Right now, there is only supported "Polish złoty"
  - categories might be extracted to a separate model to add the possibility to define own ones
  - with Planned Expenses feature, there might be also added recurring operations feature
