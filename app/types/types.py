clustering_types = """

type Query {
  
  cluster(dataToCluster: DataToClusterAsInput, algorithm: ClusteringAlgorithmAsInput): [ClusterMember]
  makeBlobsForTesting(samples: Int, clusters: Int, randomState: Int, numberOfFeatures: Int, clusterStandardDeviation: Float): DataToClusterOutput
  calculateWCSS(dataToCluster: DataToClusterAsInput, algorithm: ClusteringAlgorithmAsInput): [WCSS]
  computeAverageSilhouetteScore(dataToCluster: DataToClusterAsInput, algorithm: ClusteringAlgorithmAsInput): SilhouetteScore
  CKGErrors: [String]
}

enum AggregateOp {
  MIN
  MAX
  SUM
  COUNT
}

type WCSS {
  id: ID!
  clusterNumber: Int
  value: Float
}

type SilhouetteScore {
  id: ID!
  meanSilhouetteCoefficient: Float
}

type ClusteringAlgorithm {
  id: ID!
  algorithm: String
  numberOfClusters: Int
  initializationMethod: String
  maxNumberOfIterations: Int
  randomSeed: Int
}

input ClusteringAlgorithmAsInput {
  id: ID!
  algorithm: String
  numberOfClusters: Int
  initializationMethod: String
  maxNumberOfIterations: Int
  randomSeed: Int
}

type ClusterMember {
  id: ID!
  segement: Int
}

type DataToCluster {
  id: ID!
  rows: [Row]
}

input DataToClusterAsInput {
  id: ID!
  rows: [RowAsInput]
}

type DataToClusterOutput {
  id: ID!
  rows: [RowOutput]
}

scalar Date

scalar DateTime

type Info {
  id: ID!
  name: String!
  description: String
}

scalar JSON


type Row {
  id: ID!
  values: [Value]
}

type Value {
  id: ID!
  value: Float
}

input ValueAsInput {
  id: ID!
  value: Float
}

input RowAsInput {
  id: ID!
  values: [ValueAsInput]
}

type RowOutput {
  id: ID!
  values: [Float]
}

scalar Time



"""

