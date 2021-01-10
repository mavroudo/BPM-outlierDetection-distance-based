package oultierDetectionAlgorithms

import de.lmu.ifi.dbs.elki.database.StaticArrayDatabase
import de.lmu.ifi.dbs.elki.datasource.{ArrayAdapterDatabaseConnection, DatabaseConnection}
import oultierDetectionAlgorithms.Structs.Trace_Vector
import de.lmu.ifi.dbs.elki.algorithm.outlier.lof.LOF
import de.lmu.ifi.dbs.elki.data.NumberVector
import de.lmu.ifi.dbs.elki.database.ids.{DBIDIter, DBIDUtil}
import de.lmu.ifi.dbs.elki.database.relation.DoubleRelation
import de.lmu.ifi.dbs.elki.distance.distancefunction.minkowski.EuclideanDistanceFunction

object LofElki {

  def assignScore(log:Structs.Log,k:Int):Array[(Int,Double)]={
    val data = this.converter(log)
    val dbc: DatabaseConnection = new ArrayAdapterDatabaseConnection(data)
    val db = new StaticArrayDatabase(dbc, null)
    db.initialize()
    val lof = new LOF[NumberVector](k,EuclideanDistanceFunction.STATIC)
    val results = lof.run(db)
    val scores: DoubleRelation = results.getScores
    val iter: DBIDIter = scores.iterDBIDs();
    val scoresArray: Array[(Int, Double)] = new Array(log.traces.count().toInt)
    while (iter.valid()) {
      println(DBIDUtil.toString(iter), scores.doubleValue(iter))
      scoresArray(DBIDUtil.toString(iter).toInt - 1) = (DBIDUtil.toString(iter).toInt, scores.doubleValue(iter))
      iter.advance()
    }
    scoresArray.sortWith((x, y) => x._2 > y._2)


  }

  def converter(log: Structs.Log): Array[Array[Double]] = {
    val traces: Array[Trace_Vector] = Utils.Utils.convert_to_vector_only_durations(log).collect()
    val a = Array.ofDim[Double](traces.length, traces.head.elements.length)
    for (t_index <- traces.indices) {
      val trace = traces(t_index).elements
      for (v_index <- traces.head.elements.indices) {
        a(t_index)(v_index) = trace(v_index)
      }
    }
    a

  }

}
