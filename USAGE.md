
## Features

## cluster
cluster(dataToCluster: DataToClusterAsInput, algorithm: ClusteringAlgorithmAsInput): [ClusterMember]

Takes DataToCluster Kind which is a row / col matrix and Algorithm which defines the parameters by which to genarate the clusters
Returns a list of ClusterMember which provides the segment (custer) that the row in the matrix belongs too.

Within the Alogrithm Kind the property algorithm can take on the following values;

algorithm: "KMeans"
algorithm: "AgglomerativeClustering"
algorithm: "GaussianMixture"


## calculateWCSS
calculateWCSS(dataToCluster: DataToClusterAsInput, algorithm: ClusteringAlgorithmAsInput): [WCSS]

can be used to determine the number of clusters within dataToCluster.  

Within Cluster Some Of Square (WCSS) measures the squared average distance of all the points within a cluster to the cluster centroid.  The goal is to minimise this number.  

Plotting this output will reveal a graph where the "elbow" of the curve reveals the min cluster number within the data. 

Note: this only accepts the property algorithm of Alogrithm to be algorithm: "KMeans"

## makeBlobsForTesting
makeBlobsForTesting(samples: Int, clusters: Int, randomState: Int, numberOfFeatures: Int, clusterStandardDeviation: Float): DataToClusterOutput

This provides a data set to test the above functions.  

Example: 3 features 2 samples
 [ 
   [ f1, f2, f3 ]
   [ f1, f2, f3 ]
]


## Queries

The following queries can be run from the graphQL playground

## create a sample data set
query{
  makeBlobsForTesting(
    samples:10
    clusters:3
    randomState:0
    numberOfFeatures:3
    clusterStandardDeviation:1.0
  ){
    id
    rows {
        id
        values
    }
  }
}

## cluster a sample data set

query{
    cluster(
        algorithm: {
          	id: "algo"
            algorithm: "KMeans"
            numberOfClusters: 3,
            randomSeed: 0,
            initializationMethod: "k-means++",
            maxNumberOfIterations: 300
            
        }
        dataToCluster: {
            id: "blob",
            rows: [
                {
                  id: "row 0",
                  values: [
                      0.3309660395059796,
                      -1.7690535274645085,
                      4.432273545057134
                    ]
                  },
                {
                  id: "row 1",
                  values: [
                      0.5646062584966123,
                      -1.479539195931606,
                      4.3806227087815275
                  ]
                },
                {
                id: "row 2",
                values: [
                    -2.3265337773292405,
                    9.23093228594766,
                    11.06073925558359
                ]
                },
                {
                id: "row 3",
                values: [
                    2.0570819916019403,
                    4.788099481569055,
                    2.634408000139606
                ]
                },
                {
                id: "row 4",
                values: [
                    0.9311025884465655,
                    -0.8463367688667848,
                    1.3543855712331807
                ]
                },
                {
                id: "row 5",
                values: [
                    -1.817773038636893,
                    8.010846548310807,
                    8.810749670584514
                ]
                },
                {
                id: "row 6",
                values: [
                    2.2423886084042737,
                    3.7979107876878784,
                    4.600468299903932
                ]
                },
                {
                id: "row 7",
                values: [
                    1.2514683941228153,
                    3.343032715714602,
                    2.4321944964281608
                ]
                },
                {
                id: "row 8",
                values: [
                    0.7946875058152991,
                    5.713991958579604,
                    1.6807958304526718
                ]
                },
                {
                id: "row 9",
                values: [
                    0.28677335437303264,
                    8.401900053670913,
                    9.42252030173292
                ]
                }
            ]
				}

    ){
      id
      segment
    }
}

## Calculate the WCSS

query{
    calculateWCSS(
        algorithm: {
          	id: "algo"
            algorithm: "KMeans"
            numberOfClusters: 3,
            randomSeed: 0,
            initializationMethod: "k-means++",
            maxNumberOfIterations: 300
            
        },
        dataToCluster: {
            id: "blob",
            rows: [
                {
                  id: "row 0",
                  values: [
                      0.3309660395059796,
                      -1.7690535274645085,
                      4.432273545057134
                    ]
                  },
                {
                  id: "row 1",
                  values: [
                      0.5646062584966123,
                      -1.479539195931606,
                      4.3806227087815275
                  ]
                },
                {
                id: "row 2",
                values: [
                    -2.3265337773292405,
                    9.23093228594766,
                    11.06073925558359
                ]
                },
                {
                id: "row 3",
                values: [
                    2.0570819916019403,
                    4.788099481569055,
                    2.634408000139606
                ]
                },
                {
                id: "row 4",
                values: [
                    0.9311025884465655,
                    -0.8463367688667848,
                    1.3543855712331807
                ]
                },
                {
                id: "row 5",
                values: [
                    -1.817773038636893,
                    8.010846548310807,
                    8.810749670584514
                ]
                },
                {
                id: "row 6",
                values: [
                    2.2423886084042737,
                    3.7979107876878784,
                    4.600468299903932
                ]
                },
                {
                id: "row 7",
                values: [
                    1.2514683941228153,
                    3.343032715714602,
                    2.4321944964281608
                ]
                },
                {
                id: "row 8",
                values: [
                    0.7946875058152991,
                    5.713991958579604,
                    1.6807958304526718
                ]
                },
                {
                id: "row 9",
                values: [
                    0.28677335437303264,
                    8.401900053670913,
                    9.42252030173292
                ]
                }
            ]
				}

    ){
    id
    clusterNumber
    value
  }
}

