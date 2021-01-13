import Utils.Results
import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession
import org.scalatest.FunSuite
import oultierDetectionAlgorithms.LofElki

class LOFElkiTest extends FunSuite {

  test("test LoOF from package ELKI") {
    val filename = "input/outliers_30_activities_3k_0.1.xes"
    val results_file = "input/results_30_activities_3k_0.1"
    val k=100
    val results = Results.read(results_file)
    val spark = SparkSession.builder()
      .appName("Temporal trace anomaly detection")
      .master("local[*]")
      .getOrCreate()
    println(s"Starting Spark version ${spark.version}")
    Logger.getLogger("org").setLevel(Level.ERROR)

    val log = Utils.Utils.read_xes(filename)
    spark.time({
      val lof=new LofElki()
      val outliers = lof.assignScore(log, k).take(results.size)
      val found = outliers.count(i => results.map(_._1).contains(i._1))
      println(found.toDouble / results.size)
    })
  }

}
