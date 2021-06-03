# Tugas 3

### how to run:

- server

  ``` python3 server.py -p 8000 -d data.db ```

- client

  ``` python3 client.py -p 8000 ```


### test pada client:
- test rawquery 

  * **``` rawquery('select count(*) from mockdata') ```**

  * **``` rawquery('select FirstNameLastName, JobTitle from mockdata where ID < 5') ```**


- test tabquery

  * **``` tabquery('select count(*) from mockdata') ```**

  * **``` tabquery('select FirstNameLastName, JobTitle from mockdata where ID < 5') ```**
  
   
### run insert_sql2.py

``` python insert_sql2.py```
