package experiments

import Utils.Results
import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession
import oultierDetectionAlgorithms.{LofElki, ODAL, OurMethod}

import java.io.{BufferedWriter, File, FileWriter}
import scala.collection.mutable.ListBuffer

object Experiments_k {

  def main(args: Array[String]): Unit = {
    Logger.getLogger("org").setLevel(Level.ERROR)
    val spark = SparkSession.builder()
      .appName("Temporal trace anomaly detection")
      .master("local[*]")
      .getOrCreate()
    println(s"Starting Spark version ${spark.version}")

    val ks=List(1,3,10,20,50,100)
    val files=List("30_activities_3k_0.01","30_activities_3k_0.05","30_activities_3k_0.1","financial_log_0.01","financial_log_0.05","financial_log_0.1")

    for (dataset<-files){
      val output="output/"+dataset
      val filename = "input/outliers_"+dataset+".xes"
      val log = Utils.Utils.read_xes(filename)
      val results_file = "input/results_"+dataset
      val results=Results.read(results_file)
      var exp=new ListBuffer[String]()
      for(k<-ks){
        println(dataset,k)
        //Ours
        val t1 = System.nanoTime
        val outliers=OurMethod.assignOutlyingFactor(log,k).slice(0, results.size)
        val found=outliers.count(i => results.map(_._1).contains(i._1)).toDouble/results.size
        val duration = (System.nanoTime - t1) / 1e9d
        exp+="OurMethod,"+dataset+","+k.toString+","+duration.toString+","+found.toString+"\n"
        //LOF
        val t2 = System.nanoTime
        val lof=new LofElki()
        val outliers2=lof.assignScore(log,k).slice(0, results.size)
        val found2=outliers2.count(i => results.map(_._1).contains(i._1)).toDouble/results.size
        val duration2 = (System.nanoTime - t2) / 1e9d
        exp+="LOF,"+dataset+","+k.toString+","+duration2.toString+","+found2.toString+"\n"
        //ODAL
        val t3 = System.nanoTime
        val outliers3 = ODAL.find_outliers(log, k, 3)
        val found3 = outliers3.count(i => results.map(_._1).contains(i)).toDouble/results.size
        val duration3 = (System.nanoTime - t3) / 1e9d
        exp+="ODAL,"+dataset+","+k.toString+","+duration3.toString+","+found3.toString+"\n"
      }
      val file = new File(output)
      val bw = new BufferedWriter(new FileWriter(file))
      exp.toList.foreach(line=>{
        bw.write(line)
      })
      bw.close()
    }
//    val output="output/30_activities_3k_0.01"
//
//    val filename = "input/outliers_30_activities_3k_0.01.xes"
//    val log = Utils.Utils.read_xes(filename)
//    val results_file = "input/results_30_activities_3k_0.01"
//    val results=Results.read(results_file)









  }


}
