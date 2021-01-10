import org.apache.spark.sql.SparkSession
import org.scalatest.FunSuite
import oultierDetectionAlgorithms.LofElki

class LOFElkiTest extends FunSuite{

  test("test LoOF from package ELKI"){
    val filename = "input/financial_log.xes"
    val spark = SparkSession.builder()
      .appName("Temporal trace anomaly detection")
      .master("local[*]")
      .getOrCreate()
    println(s"Starting Spark version ${spark.version}")
    val log = Utils.Utils.read_xes(filename)
    val x=LofElki.assignScore(log,10)
    print("hi")
  }

}
