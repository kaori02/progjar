## program dan fungsinya:

### randomloh.py :  
untuk random generate 10000 data yang terdiri dari angkat 1-1000 beserta fungis yang akan digunakan seperti penambahan / pengurangan  

### sequential.py :  
isi dari program server, dimana input diambil dari input.txt, baik server maupun klien bisa lebih dari 1. program berfungsi melakukan penambahan / pengurangan yang diminta.  

untuk test dengan powershell visual studio code gunakan ``` Get-Content .\tugas2\input.txt | python .\tugas2\sequential.py ```  

untuk test dengan bash visual studio code gunakan ``` python tugas2/sequential.py < tugas2/input.txt ```  

### srv_threaded.py :  
- knp tidak seperti klien_paralel.py ada fungsi join(), karna sistemnya yang berjalan while true -> zen_utils.py > accept_connection_forever function

## untuk jalanin :  
### test jawaban klien(bash):  
``` python tugas2/klien_paralel.py tugas2/input.txt ```

### akhiri server (bash):  
``` python tugas2/klien_paralel.py tugas2/dummy.txt ```

### server(bash):
``` python tugas2/srv_threaded.py 127.0.0.1 ```

