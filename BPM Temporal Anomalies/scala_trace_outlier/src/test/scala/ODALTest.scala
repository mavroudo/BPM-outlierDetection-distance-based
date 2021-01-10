import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession
import org.scalatest.{BeforeAndAfterAll, FunSuite}
import oultierDetectionAlgorithms.ODAL

class ODALTest extends FunSuite with BeforeAndAfterAll{
  private var spark: SparkSession = _
  override def beforeAll(): Unit = {
    Logger.getLogger("org").setLevel(Level.ERROR)
    spark = SparkSession.builder()
      .appName("Temporal trace anomaly detection")
      .master("local[*]")
      .getOrCreate()
    println(s"Starting Spark version ${spark.version}")

  }

  test("ODAL Algorithm"){
    val k=10
    val filename="input/financial_log.xes"
    val log = Utils.Utils.read_xes(filename)
    val outliers=ODAL.find_outliers(log,k,3)
    println("Outliers size:",outliers.size)

  }

}
