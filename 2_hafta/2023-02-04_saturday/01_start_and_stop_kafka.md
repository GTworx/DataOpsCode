## Start Kafka local

1. Start zookeeper
` [train@localhost play]$ sudo systemctl start zookeeper  `

2. Start kafka server
` [train@localhost play]$ sudo systemctl start kafka  `


3. Stop kafka first then zookeeper

` [train@localhost play]$ sudo systemctl stop kafka  `

` [train@localhost play]$ sudo systemctl stop zookeeper  `
