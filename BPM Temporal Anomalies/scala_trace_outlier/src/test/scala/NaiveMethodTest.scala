import Utils.Preprocess
import org.apache.log4j.{Level, Logger}
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import org.scalatest.{BeforeAndAfterAll, FunSuite}
import oultierDetectionAlgorithms.Structs

class NaiveMethodTest extends FunSuite with BeforeAndAfterAll {
  private var preprocessed: RDD[Structs.Trace_Vector] = _
  private var spark: SparkSession = _

  override def beforeAll(): Unit = {
    val filename = "input/financial_log.xes"
    val dims = 10
    Logger.getLogger("org").setLevel(Level.ERROR)
    spark = SparkSession.builder()
      .appName("Temporal trace anomaly detection")
      .master("local[*]")
      .getOrCreate()
    println(s"Starting Spark version ${spark.version}")
    val log = Utils.Utils.read_xes(filename)
    preprocessed = Preprocess.preprocess(log, dims, Utils.Utils.convert_to_vector_both_duration_repetitions)

  }

  test("Naive method") {
    val k = 10
    val zeta = 10
    spark.time({
      val rddDistances = NaiveMethod.initialiazeDistancesRDD(preprocessed, k)
      val sortedByOutlyingFactor = OutlierDetection.assignOutlyingFactor(rddDistances, k)
      //    val outliers:Array[(Long,Double)]=sortedByOutlyingFactor.collect().sortBy(_._2).slice(0,zeta+1)
      val outliers: Array[(Long, Double)] = sortedByOutlyingFactor.sortBy(_._2, ascending = false).collect().slice(0, zeta + 1)
      outliers.foreach(println)
    })
  }

}
