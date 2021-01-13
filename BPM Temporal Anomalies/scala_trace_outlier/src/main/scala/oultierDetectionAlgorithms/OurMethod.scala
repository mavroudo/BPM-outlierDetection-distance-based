package oultierDetectionAlgorithms

import Indexing.BallTree.BallTree
import Utils.{Preprocess, Utils}
import org.apache.spark.ml.linalg.{DenseVector, Vectors}
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import org.apache.spark.storage.StorageLevel

import scala.collection.mutable.ArrayBuffer



object OurMethod {

  case class DistanceElement(id1: Long, id2: Long, distance: Double)
  case class DistancesFromTrace(id: Long, distances: List[DistanceElement])

  def assignOutlyingFactor(log:Structs.Log,k:Int):Array[(Long,Double)] ={
    val spark = SparkSession.builder().getOrCreate()
    val traces=Utils.convert_to_vector_only_durations(log)
    val preparedForRdd = traces.map(x => Tuple2.apply(x.id, Vectors.dense(x.elements)))
    val df = spark.createDataFrame(preparedForRdd).toDF("id", "features")
    val normalizedDF = Preprocess.normalize(df)
    val preprocessed =normalizedDF.rdd.map(row => {
      Structs.Trace_Vector(row.getAs[Long]("id"), row.getAs[DenseVector]("scaledFeatures").values)
    })
    val rddDistances = this.initializeDistances(preprocessed, k)
    val sortedByOutlyingFactor = this.assignOutlyingFactor(rddDistances, k)
    sortedByOutlyingFactor.sortBy(_._2, ascending = false).collect()
  }

  def assignOutlyingFactorWithPCA(log:Structs.Log,k:Int,dims:Int):Array[(Long,Double)]={
    val spark = SparkSession.builder().getOrCreate()
    val traces=Utils.convert_to_vector_only_durations(log)
    val preparedForRdd = traces.map(x => Tuple2.apply(x.id, Vectors.dense(x.elements)))
    val df = spark.createDataFrame(preparedForRdd).toDF("id", "features")
    val normalizedDF = Preprocess.normalize(df)
    val reduceDimensionalityDF = Preprocess.reduceDimensionalityPCA(normalizedDF, dims) //apply pca
    val preprocessed = reduceDimensionalityDF.rdd.map(row => {
      Structs.Trace_Vector(row.getAs[Long]("id"), row.getAs[DenseVector]("pcaFeatures").values)
    })
    val rddDistances = this.initializeDistances(preprocessed, k)
    val sortedByOutlyingFactor = this.assignOutlyingFactor(rddDistances, k)
    sortedByOutlyingFactor.sortBy(_._2, ascending = false).collect()
  }

  def createBallTree(log:Structs.Log):BallTree={
    val spark = SparkSession.builder().getOrCreate()
    val traces=Utils.convert_to_vector_only_durations(log)
    val preparedForRdd = traces.map(x => Tuple2.apply(x.id, Vectors.dense(x.elements)))
    val df = spark.createDataFrame(preparedForRdd).toDF("id", "features")
    val normalizedDF = Preprocess.normalize(df)
    val preprocessed =normalizedDF.rdd.map(row => {
      Structs.Trace_Vector(row.getAs[Long]("id"), row.getAs[DenseVector]("scaledFeatures").values)
    })
    val ballTree: BallTree = new BallTree(preprocessed)
    ballTree.buildTree()
    ballTree
  }

  def assignOutlyingFactorWithBallTree(log:Structs.Log,ballTree: BallTree,k:Int):Array[(Long,Double)] ={
    val scores=new ArrayBuffer[(Long,Double)]()
    for(i<-0 until log.traces.count().toInt){
      val neighbors=ballTree.kNearestNeighbors(i.toInt,k)
      scores+=((i,neighbors.map(_._2).sum))
    }
    scores.toArray
  }


  private def initializeDistances(traces: RDD[Structs.Trace_Vector], k: Int): RDD[DistancesFromTrace] = {
    val spark = SparkSession.builder().getOrCreate()
    val collected = traces.collect()
    val broadcasted = spark.sparkContext.broadcast(collected)
    val distances = traces.map(v1 => {
      val distanceList = broadcasted.value.map(v2 => {
        DistanceElement(v1.id, v2.id, Utils.distance(v1, v2))
      }).toList
      DistancesFromTrace(v1.id, distanceList.sortBy(_.distance))
    })
      .map(x => {
        DistancesFromTrace(x.id, x.distances.slice(1, k + 1))
      })
      .persist(StorageLevel.MEMORY_AND_DISK)
    distances
  }

  private def assignOutlyingFactor(distances:RDD[DistancesFromTrace],k:Int):RDD[(Long,Double)]={
    var maxSize=k
    if(k>distances.first().distances.length){
      maxSize=distances.first().distances.length
    }
    distances.map(x=>{
      val element:Double=x.distances.slice(0, maxSize + 1).map(_.distance).sum
      (x.id,element)
    })

  }



}
