password="labredesML340"
username="root"
Ip="157.253.205.7"
sshpass -p $password scp -o StrictHostKeyChecking=no logs/UDP.log $username@$Ip:/home/s5g3/logs/