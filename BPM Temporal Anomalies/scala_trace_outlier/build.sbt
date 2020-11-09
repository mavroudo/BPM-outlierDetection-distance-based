name := "temporal_trace_anomalies"
version := "0.1"
scalaVersion := "2.11.12"
val sparkVersion = "2.4.4"

libraryDependencies += "com.typesafe.scala-logging" % "scala-logging-slf4j_2.10" % "2.1.2"
//libraryDependencies += "org.scalatest" % "scalatest_2.11" % "3.0.4" % "test"
libraryDependencies += "de.uni.freiburg.iig.telematik" % "SEWOL" % "1.0.2"
libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.8" % Test
//to run the sbt assembly the '% "provided",' section must not be in comments
//to debug in IDE the '  "org.apache.spark" % "spark-catalyst_2.11" % sparkVersion , //"2.0.0",' section must be in comments
libraryDependencies ++= Seq(
  "org.apache.spark" % "spark-catalyst_2.11" % sparkVersion , //"2.0.0"
  "org.apache.spark" %% "spark-core" % sparkVersion ,
  "org.apache.spark" %% "spark-mllib" % sparkVersion ,
  "org.apache.spark" %% "spark-sql" % sparkVersion )