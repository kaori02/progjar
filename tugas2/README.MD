## program dan fungsinya:

### randomloh.py :  
untuk random generate 10000 data yang terdiri dari angkat 1-1000 beserta fungis yang akan digunakan seperti penambahan / pengurangan  

### sequential.py :  
isi dari program server, dimana input diambil dari input.txt, baik server maupun klien bisa lebih dari 1. program berfungsi melakukan penambahan / pengurangan yang diminta.  untuk test pada powershell visual studio code gunakan ``` Get-Content .\tugas2\input.txt | python .\tugas2\sequential.py ```  

### srv_threaded.py :  
- knp tidak seperti klien_paralel.py ada fungsi join(), karna sistemnya yang berjalan while true -> zen_utils.py > accept_connection_forever function