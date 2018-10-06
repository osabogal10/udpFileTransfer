password="labredesML340"
username="root"
Ip="157.253.205.7"
client="$(hostname)"
sshpass -p $password scp -o StrictHostKeyChecking=no udpFileTransfer/cliente/logs/UDP$client.log $username@$Ip:/home/s5g3/logs/