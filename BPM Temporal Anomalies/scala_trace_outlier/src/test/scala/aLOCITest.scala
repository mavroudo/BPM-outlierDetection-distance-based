import org.apache.spark.sql.SparkSession
import org.scalatest.FunSuite
import oultierDetectionAlgorithms.ALOCIElki

class aLOCITest extends FunSuite{


  test("aLoci test"){
    val filename = "input/financial_log.xes"
    val spark = SparkSession.builder()
      .appName("Temporal trace anomaly detection")
      .master("local[*]")
      .getOrCreate()
    println(s"Starting Spark version ${spark.version}")
    val log = Utils.Utils.read_xes(filename)
    val x=ALOCIElki.assignScore(log)
  }

}
