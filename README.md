# CDC Data Lake Prototype
## Installation
The prototype requires Python3, [Apache Spark 2.4.5](https://www.apache.org/dyn/closer.lua/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz), Bokeh 2.0, PySpark, and Pandas.
### Apache Spark Installation Instructions
Download Spark from any of the mirror links above above. Extract the contents from the .tgz file and move it to a desired location (I used /usr/lib/spark).
```sh
$ tar -zxvf [spark-file-name].tgz
$ cp -r [spark-directory] [your-path]/spark
```
Spark is pre-built with Scala 2.11, so you also need the Java JVM 8. Here's the link to [JDK 8](https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html). You may need to create an Oracle account to download the JDK. Once you have downloaded the JDK unpack it and move it to a desired location (I used /opt/jdk/jdk1.8.0_202).

You will need to create environment variables so that the application knows where to find Spark and Java 8. Open your ~/.bashrc file using the editor of your choice. In the file, scroll all the way to the bottom and add the following lines:
```sh
export JAVA_HOME=[your-jdk1.8-location]
export SPARK_HOME=[your-spark-location]
export PATH=$PATH:$JAVA_HOME/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin
```
For example, the added lines in my ~/.bashrc look like:
```sh
export JAVA_HOME=/opt/jdk/jdk1.8.0_202
export SPARK_HOME=/usr/lib/spark
export PATH=$PATH:$JAVA_HOME/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin
```
Run ```$ spark-submit --version``` to make sure spark has installed properly.
### Bokeh Installation Instructions
Make sure you have Python 3 and pip3 installed (if you have Python 3.4 or later, pip is automatically installed). To install Bokeh via terminal, run:
```sh
$ pip3 install bokeh
```
### PySpark Installation Instructions
In terminal, run:
```sh
$ pip3 install pyspark
```
### Pandas Installation Instructions:
In terminal, run:
```sh
$ pip3 install pandas
```
## Running the Application
To run the application, simply use:
```sh
$ bokeh serve --show app.py
```
