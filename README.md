# Data Engineering Project

This repository documents a comprehensive data engineering project that involves setting up a distributed environment, web scraping data from various anime websites, performing Extract, Transform, Load (ETL) operations, and storing the processed data in a MySQL database. The project is aimed at collecting and structuring information about top-ranked anime.

## Table of Contents
- [Environment Setup](#environment-setup)
- [Scraping](#scraping)
- [ETL](#etl)
- [Database](#database)

## Environment Setup

To create a hadoop cluster with 3 worker nodes and 1 master node, a Tailscale VPN was established, connecting multiple Ubuntu virtual machines. Docker Swarm was initiated on one of the machines, with others joining as worker nodes. Hadoop-Spark cluster was installed on the swarm cluster. The setup ensures seamless communication and resource sharing between various nodes.

### Steps Taken:
1. Connected 4 VMs to Tailscale VPN.
2. Initiated Docker Swarm and joined VMs as worker nodes.
3. Wrote Docker Compose file for persistent storage and suitable container networking.
4. Installed Hadoop-Spark cluster on the swarm cluster using the docker compose file.
5. Set up Python virtual environment with dependencies on the master node for code execution.

## Scraping

Web scraping was performed on multiple anime-related websites to collect valuable information. [Scrapy](https://scrapy.org/) was utilized for efficient extraction, while [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) was employed for additional image scraping.

### Steps Taken:
1. Scraped [MyAnimeList](https://myanimelist.net/topanime.php?limit=0) for 1000 top-ranked anime and extracted around 26 features for each anime.
2. Scraped [Anime News Network](https://www.animenewsnetwork.com/encyclopedia/ratings-anime.php?top50=best_bayesian&n=500) for anime image data.
3. Scraped [AniDB](https://anidb.net/anime/?h=1&noalias=1&orderby.name=1.1&orderby.rating=0.2) for episode, average, reviews, and number of users who like a paticular anime information for top 1000 animes.

## ETL

The Extract, Transform, Load (ETL) process involved transferring scraped data from the master node to Hadoop Distributed File System (HDFS). A Python script was developed to clean and transform the data into the desired format before loading it into a MySQL database.

### Steps Taken:
1. Transferred scraped data from master-node local to HDFS.
2. Wrote a Python script to load from HDFS, clean, and transform data according to database schema.
3. Inserted the processed data into a MySQL database.

## Database

A MySQL database was locally installed on an Ubuntu virtual machine to store the structured anime data. The database system file was configured to allow remote logins, and suitable user accounts were created for different purposes.

### Steps Taken:
1. Installed MySQL database locally on Ubuntu VM.
2. Configured system file for remote logins.
3. Created two user accounts for Docker master-node deployment and local MySQL Workbench access.
4. Implemented a database design suitable for storing scraped anime data.

This repository provides a comprehensive overview of the project, including code, demo video, and configurations used in each phase. Feel free to explore the codebase and documentation for detailed insights into the data engineering process.
