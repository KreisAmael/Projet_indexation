# Projet_indexation

## Pour la partie Collecte des Données via une API Publique

1. Nous avons choisi l'API NosDéputés.fr pour visualiser les données liés à la présence des députés à l'assemblée nationale

##Pour la partie Transmission des Données avec Kafka

1. Pour créer le topic Kafka, il faut : 
  - dans un nouveau terminal, taper la commande : sudo kafka_2.12-3.9.0/bin/zookeeper-server-start.sh kafka_2.12-3.9.0/config/zookeeper.properties
  - dans un nouveau terminal, taper la commande : sudo kafka_2.12-3.9.0/bin/kafka-server-start.sh kafka_2.12-3.9.0/config/server.properties
  - dans un nouveau terminal, taper la commande : sudo kafka_2.12-3.9.0/bin/kafka-topics.sh --create --topic deputes_presence --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

2. Pour configurer le producteur de Kafka, il faut faire python3 data_collect.py


## Pour la partie Transformation et Indexation des Données

1. Pour lire les données depuis Kafka, il faut :
  - kafka-console-producer.sh –brooker-list localhost:9092 --topic deputes_presence< ../access.log (remplacer ../access.log par le path de votre fichier access.log)
  
2. Pour créer le nouveau mapping, il faut :   
  - Supprimer le mapping généré naturellement par Elasticsearch avec : curl -X DELETE "http://localhost:9200/deputes"
  - Créer le nouveau mapping avec : curl -X PUT "http://localhost:9200/deputes" -H "Content-Type: application/json" -d @mapping.json

3. Il faut enfin donner le consumer a logstash avec : sudo /usr/share/logstash/bin/logstash -f ~/Projet_indexation/depute.conf

## Pour la partie Traitement des Données avec Hadoop ou Spark



2. Pour Spark, lancer spark avec : ./spark-3.5.4-bin-hadoop3/bin/spark-shell --packages org.elasticsearch:elasticsearch-spark-30_2.12:8.17.1
  - Rentrer ces lignes spark :
    import org.apache.spark.sql.SparkSession
    import spark.implicits._
    SparkSession.getActiveSession.foreach(_.stop())
    val spark = SparkSession.builder().appName("Read from Elasticsearch").config("spark.es.nodes", "localhost").config("spark.es.port", "9200").master("local[*]")
    val spark2 =spark.getOrCreate()
    val deputesDF = spark2.read.format("org.elasticsearch.spark.sql").option("es.read.field.as.array.include", "emails,anciens_mandats,site_web")
    val dpDF = deputesDF.load("deputes")

  - vous pouvez tester quelques requêtes qui sont dans le rapport.