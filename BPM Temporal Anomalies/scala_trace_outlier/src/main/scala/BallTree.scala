import java.util

import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.execution.datasources.DataSource
import oultierDetectionAlgorithms.Structs
import weka.core.neighboursearch.BallTree
import weka.core.{Attribute, Instance, Instances}





class myBallTree(traces:RDD[Structs.Trace_Vector]) {
//  val spark=SparkSession.builder().getOrCreate()
//  import spark.implicits._
//  traces.toDF()
//  var bs = new DataSource()
//  val source:DataSource =new DataSource(new L)
//
//  val bTree = new BallTree()
}

object Main {


  def main(args: Array[String]): Unit = {
    println("Helloo")
  }
}
