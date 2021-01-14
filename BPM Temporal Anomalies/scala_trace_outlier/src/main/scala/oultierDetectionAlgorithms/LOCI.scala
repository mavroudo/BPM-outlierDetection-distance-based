package oultierDetectionAlgorithms

import Utils.Preprocess
import org.apache.log4j.{Level, Logger}
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import oultierDetectionAlgorithms.Structs.{DistanceElement, DistancesFromTrace}

import scala.collection.mutable.ListBuffer
import scala.util.control.Breaks.{break, breakable}

class LOCI(traces: RDD[Structs.Trace_Vector], alpha: Double, distance: (Structs.Trace_Vector, Structs.Trace_Vector) => Double) {

  private var distance_matrix: RDD[DistancesFromTrace] = _
  private var r_max: Double = _
  private var D: RDD[DistancesFromTrace] = _

  /**
   * Creates the distance matrix, finds the rmax and creates critical values for every trace
   */
  def initialize(): Unit = {
    val spark = SparkSession.builder().getOrCreate()
    val broadcast_distance = spark.sparkContext.broadcast(distance)

    distance_matrix = traces.cartesian(traces)
      .map(v => {
        val v1 = v._1
        val v2 = v._2
        DistanceElement(v1.id, v2.id, broadcast_distance.value(v1, v2))
      })
      .groupBy(_.id1)
      .map(x => DistancesFromTrace(x._1, x._2.toList))

    r_max = distance_matrix.map(x => {
      x.distances.map(_.distance).max
    }).collect().max

    val broadcast_rmax = spark.sparkContext.broadcast(r_max)
    D = distance_matrix.map(d => {
      DistancesFromTrace(d.id, d.distances.filter(_.distance <= broadcast_rmax.value)) //NOT SORTED YET
    })
  }

  def findOutliers():RDD[(DistancesFromTrace,Boolean)] = {
    val spark = SparkSession.builder().getOrCreate()
    val broadAlpha = spark.sparkContext.broadcast(alpha)
    val broadD = spark.sparkContext.broadcast(D.collect())
    val n = D.map(p => { //we will loop for the first on and use the second
      def nn_search(d: DistancesFromTrace, start: Double, end: Double): (Int, List[Long]) = {
        val distances = d.distances.filter(_.distance > start).filter(_.distance <= end)
        (distances.length, distances.map(_.id2))
      }

      var return_val: (DistancesFromTrace, Boolean) = (p, false)
      var points_within_r: ListBuffer[DistancesFromTrace] = new ListBuffer[DistancesFromTrace]
      var n_of_points_in_ar: ListBuffer[Int] = new ListBuffer[Int]
      var r_prev: Double = 0
      breakable {
        for (r <- p.distances.sortBy(_.distance)) {
          val new_points = nn_search(p, r_prev, r.distance)
          for (pp <- points_within_r.indices) {
            val value = nn_search(points_within_r(pp), r_prev * broadAlpha.value, r.distance * broadAlpha.value)
            n_of_points_in_ar(pp) = n_of_points_in_ar(pp) + value._1
          }
          for (np <- new_points._2) {
            val ntrace: DistancesFromTrace = broadD.value.filter(_.id == np)(0)
            val value = nn_search(ntrace, r_prev * broadAlpha.value, r.distance * broadAlpha.value)
            points_within_r += ntrace
            n_of_points_in_ar += value._1
          }
          r_prev = r.distance // change r for the next time
          if (points_within_r.nonEmpty && n_of_points_in_ar.sum > 0) {
            val cur_alpha_n = points_within_r.size
            val n_hat = n_of_points_in_ar.sum / n_of_points_in_ar.size
            val stdev = Math.sqrt((n_of_points_in_ar.map(_ - n_hat)
              .map(t => t * t).sum) / n_of_points_in_ar.length)
            if (n_hat > 20) {
              val mdef = 1 - (cur_alpha_n / n_hat)
              val sigma_mdef = stdev / n_hat
              if (mdef > 3 * sigma_mdef) {
                return_val = (p, true)
                break
              }
            }
          }

        }
      }
      return_val
    }).filter(_._2)
    n.take(2).map(x=>(x._1.id,x._2))foreach(println)
    n
  }

  def nn_search(d: DistancesFromTrace, start: Double, end: Double): (Int, List[Long]) = {
    val distances = d.distances.filter(_.distance > start).filter(_.distance <= end)
    (distances.length, distances.map(_.id2))
  }

}

object LOCI_Main {

  def main(args: Array[String]): Unit = {

    val filename = "input/financial_log.xes"
    val k = 50 //number of nearest neighbors
    val dims = 10
    val zeta = 10
    val n = 4
    Logger.getLogger("org").setLevel(Level.ERROR)
    val spark = SparkSession.builder()
      .appName("Temporal trace anomaly detection")
      .master("local[*]")
      .getOrCreate()
    println(s"Starting Spark version ${spark.version}")
    val log = Utils.Utils.read_xes(filename)
    val rddTransformed_whole = Preprocess.preprocess(log, dims, Utils.Utils.convert_to_vector_both_duration_repetitions)
    val rddTransformed = rddTransformed_whole.sample(withReplacement = false, 0.1)


    val loci: LOCI = new LOCI(rddTransformed, 0.5, Distances.distanceRMSE)
    val d = loci.initialize()
    loci.findOutliers()

  }
}