import Utils.Results
import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession
import org.scalatest.{BeforeAndAfterAll, FunSuite}
import oultierDetectionAlgorithms.ODAL

class ODALTest extends FunSuite with BeforeAndAfterAll {
  private var spark: SparkSession = _
  private var results: List[(Int, Int)] = _
  val results_file = "input/results_30_activities_3k_0.1"

  override def beforeAll(): Unit = {
    Logger.getLogger("org").setLevel(Level.ERROR)
    spark = SparkSession.builder()
      .appName("Temporal trace anomaly detection")
      .master("local[*]")
      .getOrCreate()
    println(s"Starting Spark version ${spark.version}")
    results = Results.read(results_file)
  }

  test("ODAL Algorithm") {
    val k = 100
    val filename = "input/outliers_30_activities_3k_0.1.xes"
    val log = Utils.Utils.read_xes(filename)
    spark.time({
      val outliers = ODAL.find_outliers(log, k, 3)
      val found = outliers.count(i => results.map(_._1).contains(i))
      println(found.toDouble / results.size)
    })
  }

}
