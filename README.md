Run the setup script to drop any existing database and create a fresh one


#Create the Database
This project uses a PostgreSQL database named `nc_plus_one`. 
Run the setup script using the following command:
   ```bash
   sudo -u postgres psql -d postgres -f db/setup.sql
#Use sudo to avoid 'failed: FATAL:  Peer authentication failed for user "postgres"'

